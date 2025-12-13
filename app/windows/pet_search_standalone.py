"""Окно базы данных питомцев (standalone версия)"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import requests

from windows.base import BaseWindow
from config import DOPHENEK_MAP
from translation import translator

class PetSearchStandaloneWindow(BaseWindow):
    """Окно базы данных питомцев с двумя панелями"""
    
    def __init__(self, parent, player_data, show_guild=False, show_dophenek=False):
        super().__init__(parent)
        self.title(translator.t("pets_database"))
        self.geometry("1600x900")
        
        self.player_data = player_data  # Используем данные из main_window
        self.show_guild = show_guild
        self.show_dophenek = show_dophenek
        
        # Инициализация данных
        self.name_to_id = {}
        self.id_to_name = {}
        self.pet_details = {}
        self.all_pets = []
        
        # Для сортировки
        self.sort_column = "name"
        self.sort_reverse = False
        
        # Загрузка данных о питомцах
        self.load_pets_data()
        
        # Настройка интерфейса
        self.setup_ui()
        self.configure_treeview_style()
        
        # Регистрируем callback для обновления при смене языка
        translator.register_callback(self.update_ui_texts)

    def load_pets_data(self):
        """Загружает данные о питомцах с внешнего ресурса"""
        # Выбираем правильный JSON файл в зависимости от языка
        if translator.current_language == "ru":
            url = "https://garyatrics.com/taran-data/Pets_Russian.json"
        else:
            url = "https://garyatrics.com/taran-data/Pets_English.json"
            
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            pets_data = response.json()
            
            for pet in pets_data.get("pets", []):
                pet_id = pet.get("id")
                name = pet.get("name", "").strip()
                if pet_id and name:
                    self.name_to_id[name.lower()] = pet_id
                    self.id_to_name[str(pet_id)] = name
                    self.pet_details[str(pet_id)] = {
                        'name': name,
                        'kingdom': pet.get("kingdomName", ""),
                        'effect': pet.get("effect", ""),
                        'mana_color': pet.get("manaColor", "")
                    }
                    self.all_pets.append({
                        'id': pet_id,
                        'name': name,
                        'kingdom': pet.get("kingdomName", ""),
                        'effect': pet.get("effect", ""),
                        'mana_color': pet.get("manaColor", "")
                    })
            
            # Сортируем питомцев по имени по умолчанию
            self.all_pets.sort(key=lambda x: x['name'])
            print(f"Загружено {len(self.all_pets)} питомцев")
                    
        except Exception as e:
            messagebox.showerror(translator.t("error"), 
                translator.t("export_error", error=str(e)))

    def update_ui_texts(self):
        """Обновляет тексты интерфейса при смене языка"""
        try:
            self.title(translator.t("pets_database"))
            # Перезагружаем данные питомцев с правильным языком
            self.load_pets_data()
            self.populate_pets_list()
            # Обновляем другие элементы интерфейса
            if hasattr(self, 'left_title'):
                self.update_left_title()
            if hasattr(self, 'pet_info_label'):
                self.pet_info_label.config(text=translator.t("select_pet_to_view"))
        except Exception as e:
            print(f"Ошибка обновления интерфейса: {e}")

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Верхняя панель с кнопками
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=5)
        
        btn_export_csv = tk.Button(
            top_frame, 
            text=translator.t("save_csv"), 
            width=18, 
            command=self.export_to_csv
        )
        btn_export_csv.pack(side="right", padx=5)

        btn_view_player_pets = tk.Button(
            top_frame, 
            text=translator.t("player_pets"), 
            width=18, 
            command=self.show_player_pets_window
        )
        btn_view_player_pets.pack(side="left", padx=5)

        # Основной контейнер с двумя панелями
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        paned_window.pack(fill="both", expand=True, pady=10)

        # Левая панель - список питомцев
        left_frame = tk.Frame(paned_window)
        paned_window.add(left_frame, width=800)

        # Правая панель - игроки с выбранным питомцем
        right_frame = tk.Frame(paned_window)
        paned_window.add(right_frame, width=800)

        # Настройка левой панели
        self.setup_left_panel(left_frame)
        
        # Настройка правой панели
        self.setup_right_panel(right_frame)

    def setup_left_panel(self, parent):
        """Настраивает левую панель со списком питомцев"""
        # Заголовок
        self.left_title = tk.Label(parent, text=translator.t("pets_list") + f" ({translator.t('sorted_by')} {translator.t('pet_name').lower()} ↑)", 
                                 font=('Arial', 12, 'bold'))
        self.left_title.pack(pady=5)
        
        # Поиск
        search_frame = tk.Frame(parent)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(search_frame, text=translator.t("search")).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind('<KeyRelease>', self.filter_pets)
        
        # Таблица питомцев
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Прокрутка
        yscrollbar = ttk.Scrollbar(tree_frame)
        yscrollbar.pack(side="right", fill="y")

        xscrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")

        # Таблица
        self.pets_tree = ttk.Treeview(
            tree_frame,
            columns=("name", "kingdom", "effect", "mana_color"),
            show="headings",
            height=25,
            yscrollcommand=yscrollbar.set,
            xscrollcommand=xscrollbar.set
        )
        
        self.pets_tree.pack(fill="both", expand=True)
        
        # Настройка прокрутки
        yscrollbar.config(command=self.pets_tree.yview)
        xscrollbar.config(command=self.pets_tree.xview)

        # Настройка колонок с сортировкой
        columns_config = {
            "name": {"text": translator.t("pet_name") + " ↑", "anchor": "center", "width": 250},
            "kingdom": {"text": translator.t("kingdom"), "anchor": "center", "width": 150},
            "effect": {"text": translator.t("effect"), "anchor": "center", "width": 200},
            "mana_color": {"text": translator.t("mana_color"), "anchor": "center", "width": 120}
        }
        
        for col, config in columns_config.items():
            self.pets_tree.heading(
                col, 
                text=config["text"],
                command=lambda c=col: self.sort_pets_tree(c)
            )
            self.pets_tree.column(col, anchor=config["anchor"], width=config["width"], stretch=False)
        
        # Заполняем таблицу питомцев
        self.populate_pets_list()
        
        # Обработчик выбора питомца
        self.pets_tree.bind('<<TreeviewSelect>>', self.on_pet_select)

    def setup_right_panel(self, parent):
        """Настраивает правую панель с игроками"""
        # Заголовок с информацией о выбранном питомце
        self.pet_info_label = tk.Label(parent, text=translator.t("select_pet_to_view"), 
                                     font=('Arial', 11, 'bold'), fg='blue')
        self.pet_info_label.pack(pady=5)
        
        # Таблица игроков
        players_frame = tk.LabelFrame(parent, text=translator.t("players_with_pet"), font=('Arial', 10, 'bold'))
        players_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Прокрутка для таблицы игроков
        yscrollbar = ttk.Scrollbar(players_frame)
        yscrollbar.pack(side="right", fill="y")

        xscrollbar = ttk.Scrollbar(players_frame, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        
        # Таблица игроков
        self.players_tree = ttk.Treeview(
            players_frame,
            columns=("#", "player_name", "guild_name", "level", "ascension", "amount"),
            show="headings",
            height=20,
            yscrollcommand=yscrollbar.set,
            xscrollcommand=xscrollbar.set
        )
        
        self.players_tree.pack(fill="both", expand=True)
        
        # Настройка прокрутки
        yscrollbar.config(command=self.players_tree.yview)
        xscrollbar.config(command=self.players_tree.xview)
        
        # Настройка колонок игроков
        players_columns = {
            "#": {"text": "#", "anchor": "center", "width": 50},
            "player_name": {"text": translator.t("column_player"), "anchor": "center", "width": 180},
            "guild_name": {"text": translator.t("column_guild"), "anchor": "center", "width": 150},
            "level": {"text": translator.t("level"), "anchor": "center", "width": 80},
            "ascension": {"text": translator.t("ascension"), "anchor": "center", "width": 100},
            "amount": {"text": translator.t("amount"), "anchor": "center", "width": 100}
        }
        
        for col, config in players_columns.items():
            self.players_tree.heading(col, text=config["text"])
            self.players_tree.column(col, anchor=config["anchor"], width=config["width"], stretch=False)
        
        # Настраиваем цвета строк
        self.players_tree.tag_configure('no_pet', background='#ffcccc')  # Красный - нет питомца
        self.players_tree.tag_configure('low_level', background='#ffffcc')  # Желтый - уровень 1-15
        self.players_tree.tag_configure('max_level', background='#ccffcc')  # Зеленый - уровень 20

    def populate_pets_list(self):
        """Заполняет список питомцев"""
        self.pets_tree.delete(*self.pets_tree.get_children())
        
        for pet in self.all_pets:
            self.pets_tree.insert("", "end", values=(
                pet['name'],
                pet['kingdom'],
                pet['effect'],
                pet['mana_color']
            ))

    def sort_pets_tree(self, col):
        """Сортирует таблицу питомцев по выбранной колонке"""
        if col == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        # Сортируем данные
        if col == "name":
            self.all_pets.sort(key=lambda x: x['name'].lower(), reverse=self.sort_reverse)
        elif col == "kingdom":
            self.all_pets.sort(key=lambda x: x['kingdom'].lower(), reverse=self.sort_reverse)
        elif col == "effect":
            self.all_pets.sort(key=lambda x: x['effect'].lower(), reverse=self.sort_reverse)
        elif col == "mana_color":
            self.all_pets.sort(key=lambda x: x['mana_color'].lower(), reverse=self.sort_reverse)
        
        # Обновляем отображение
        self.populate_pets_list()
        
        # Обновляем заголовки с указанием сортировки
        for column in self.pets_tree["columns"]:
            current_text = self.pets_tree.heading(column)["text"]
            clean_text = current_text.split(" ↑")[0].split(" ↓")[0]
            
            if column == col:
                arrow = " ↓" if self.sort_reverse else " ↑"
                new_text = clean_text + arrow
            else:
                new_text = clean_text
            
            self.pets_tree.heading(column, text=new_text)
        
        # Обновляем заголовок панели
        self.update_left_title()

    def update_left_title(self):
        """Обновляет заголовок левой панели"""
        sort_direction = "↓" if self.sort_reverse else "↑"
        column_names = {
            "name": translator.t("pet_name").lower(),
            "kingdom": translator.t("kingdom").lower(), 
            "effect": translator.t("effect").lower(),
            "mana_color": translator.t("mana_color").lower()
        }
        col_name = column_names.get(self.sort_column, translator.t("pet_name").lower())
        self.left_title.config(
            text=f"{translator.t('pets_list')} ({translator.t('sorted_by')} {col_name} {sort_direction})"
        )

    def filter_pets(self, event=None):
        """Фильтрует список питомцев по поисковому запросу"""
        search_text = self.search_var.get().lower()
        
        self.pets_tree.delete(*self.pets_tree.get_children())
        
        for pet in self.all_pets:
            if (search_text in pet['name'].lower() or 
                search_text in pet['kingdom'].lower() or
                search_text in pet['effect'].lower() or
                search_text in pet['mana_color'].lower()):
                
                self.pets_tree.insert("", "end", values=(
                    pet['name'],
                    pet['kingdom'],
                    pet['effect'],
                    pet['mana_color']
                ))

    def on_pet_select(self, event):
        """Обработчик выбора питомца в списке"""
        selection = self.pets_tree.selection()
        if not selection:
            return
            
        item = self.pets_tree.item(selection[0])
        pet_name = item['values'][0]  # Название питомца
        
        # Находим ID питомца по имени
        pet_id = None
        for pid, name in self.id_to_name.items():
            if name == pet_name:
                pet_id = pid
                break
        
        if pet_id:
            self.show_players_with_pet(pet_id, pet_name)

    def show_players_with_pet(self, pet_id, pet_name):
        """Показывает игроков, у которых есть выбранный питомец"""
        # Обновляем заголовок с информацией о питомце
        pet_data = self.pet_details.get(str(pet_id), {})
        info_text = f"{translator.t('pet_name')}: {pet_name}"
        if pet_data.get('kingdom'):
            info_text += f" | {translator.t('kingdom')}: {pet_data['kingdom']}"
        if pet_data.get('mana_color'):
            info_text += f" | {translator.t('mana_color')}: {pet_data['mana_color']}"
        if pet_data.get('effect'):
            info_text += f" | {translator.t('effect')}: {pet_data['effect']}"
        
        self.pet_info_label.config(text=info_text)
        
        # Очищаем таблицу игроков
        self.players_tree.delete(*self.players_tree.get_children())
        
        if not self.player_data:
            self.players_tree.insert("", "end", values=("", translator.t("no_data"), "", "", "", ""))
            return
            
        pet_id_str = str(pet_id)
        players_data = []
        
        # Собираем данные по всем игрокам из player_data
        for idx, (user_id, data) in enumerate(self.player_data.items(), start=1):
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            player_name = profile.get("Name", translator.t("unknown"))
            # Добавляем доп. имя если нужно
            if self.show_dophenek and user_id in DOPHENEK_MAP:
                player_name += f" ({DOPHENEK_MAP[user_id]})"
            guild_name = profile.get("GuildName", translator.t("no_guild"))
            pets = profile.get("Pets", {})
            
            pet_data = pets.get(pet_id_str, {})
            
            players_data.append({
                'index': idx,
                'name': player_name,
                'guild': guild_name,
                'level': pet_data.get("Level", 0) if pet_data else 0,
                'ascension': pet_data.get("AscensionLevel", 0) if pet_data else 0,
                'amount': pet_data.get("Amount", 0) if pet_data else 0,
                'has_pet': bool(pet_data)
            })
        
        # Сортируем: сначала те, у кого есть питомец (по убыванию уровня), потом те, у кого нет
        players_with_pet = [p for p in players_data if p['has_pet']]
        players_without_pet = [p for p in players_data if not p['has_pet']]
        
        # Сортируем игроков с питомцем по убыванию уровня
        players_with_pet.sort(key=lambda x: (x['level'], x['ascension'], x['amount']), reverse=True)
        
        # Объединяем списки
        all_players = players_with_pet + players_without_pet
        
        # Заполняем таблицу с цветовым кодированием
        for idx, player in enumerate(all_players, start=1):
            values = (
                idx,
                player['name'],
                player['guild'],
                player['level'] if player['has_pet'] else translator.t("no"),
                player['ascension'] if player['has_pet'] else translator.t("no"),
                player['amount'] if player['has_pet'] else translator.t("no")
            )
            
            # Определяем цвет строки
            if not player['has_pet']:
                item = self.players_tree.insert("", "end", values=values, tags=('no_pet',))
            elif player['level'] == 20:
                item = self.players_tree.insert("", "end", values=values, tags=('max_level',))
            elif 1 <= player['level'] <= 15:
                item = self.players_tree.insert("", "end", values=values, tags=('low_level',))
            else:
                item = self.players_tree.insert("", "end", values=values)

    def show_player_pets_window(self):
        """Показывает окно со всеми питомцами конкретного игрока"""
        if not self.player_data:
            messagebox.showwarning(translator.t("warning"), translator.t("no_data"))
            return
        
        # Создаем окно выбора
        select_window = tk.Toplevel(self)
        select_window.title(translator.t("select_player"))
        select_window.geometry("400x300")
        select_window.transient(self)
        select_window.grab_set()
        
        tk.Label(select_window, text=translator.t("select_player_prompt"), font=('Arial', 11, 'bold')).pack(pady=10)
        
        # Комбобокс для выбора игрока
        player_names = []
        player_ids_map = {}
        for user_id, data in self.player_data.items():
            if data:
                profile = data.get("result", {}).get("ProfileData", {})
                name = profile.get("Name", translator.t("unknown"))
                if self.show_dophenek and user_id in DOPHENEK_MAP:
                    name += f" ({DOPHENEK_MAP[user_id]})"
                player_names.append(name)
                player_ids_map[name] = user_id
        
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(select_window, textvariable=player_var, values=player_names, width=30)
        player_combo.pack(pady=10)
        
        if player_names:
            player_combo.set(player_names[0])
        
        def show_selected_player_pets():
            selected_name = player_var.get()
            if not selected_name:
                messagebox.showwarning(translator.t("warning"), translator.t("select_player_prompt"))
                return
            
            user_id = player_ids_map.get(selected_name)
            if user_id:
                # Упрощенная версия - можно расширить позже
                messagebox.showinfo(translator.t("info"), f"Питомцы игрока: {selected_name}\n(Функционал можно расширить)")
            select_window.destroy()
        
        btn_show = tk.Button(select_window, text="OK", command=show_selected_player_pets, width=10)
        btn_show.pack(pady=10)

    def export_to_csv(self):
        """Экспортирует данные текущего питомца в CSV"""
        selection = self.pets_tree.selection()
        if not selection:
            messagebox.showwarning(translator.t("error"), "Выберите питомца для экспорта")
            return
            
        if not self.players_tree.get_children():
            messagebox.showwarning(translator.t("error"), translator.t("no_data_to_export"))
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                
                # Заголовки
                headers = []
                for col in self.players_tree["columns"]:
                    headers.append(self.players_tree.heading(col)["text"])
                writer.writerow(headers)
                
                # Данные
                for item in self.players_tree.get_children():
                    writer.writerow(self.players_tree.item(item)["values"])
                    
            messagebox.showinfo(translator.t("success"), translator.t("data_saved", file_path=file_path))
        except Exception as e:
            messagebox.showerror(translator.t("error"), translator.t("export_error", error=str(e)))

