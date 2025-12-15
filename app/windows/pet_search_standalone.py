"""Standalone версия окна базы данных питомцев"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
from datetime import datetime

from .base import BaseWindow
from app.config import DOPHENEK_MAP, URL
from app.translation import translator

class PetSearchStandaloneWindow(BaseWindow):
    """Окно базы данных питомцев (standalone версия)"""
    
    def __init__(self, parent, player_data, show_guild=False, show_dophenek=False):
        super().__init__(parent)
        self.title(translator.t("pets_database"))
        self.geometry("1600x900")
        
        self.player_data = player_data
        self.show_guild = show_guild
        self.show_dophenek = show_dophenek
        
        # Данные будут переданы из основного окна
        self.name_to_id = {}
        self.id_to_name = {}
        self.pet_details = {}
        self.all_pets = []
        
        # Время последнего обновления
        self.last_update_time = datetime.now()
        self.update_in_progress = False
        
        # Для сортировки
        self.sort_column = "name"
        self.sort_reverse = False
        
        # Настройка интерфейса
        self.setup_ui()
        self.configure_treeview_style()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ВЕРХНЯЯ ПАНЕЛЬ с кнопками
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=5)
        
        # ЛЕВАЯ ЧАСТЬ - кнопки управления
        left_buttons_frame = tk.Frame(top_frame)
        left_buttons_frame.pack(side="left", fill="y")
        
        # Кнопка возврата
        btn_back = tk.Button(
            left_buttons_frame,
            text="← Вернуться к поиску питомцев",
            width=25,
            command=self.return_to_search_window,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold")
        )
        btn_back.pack(side="left", padx=5)
        
        # Кнопка обновления данных
        self.btn_refresh = tk.Button(
            left_buttons_frame,
            text="🔄 Обновить данные игроков",
            width=25,
            command=self.refresh_player_data,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_refresh.pack(side="left", padx=5)
        
        # ПРАВАЯ ЧАСТЬ - информация о времени
        right_info_frame = tk.Frame(top_frame)
        right_info_frame.pack(side="right", fill="y")
        
        # Метка времени обновления
        self.time_label = tk.Label(
            right_info_frame,
            text=f"Последнее обновление: {self.last_update_time.strftime('%H:%M:%S')}",
            font=("Arial", 9, "italic"),
            fg="gray"
        )
        self.time_label.pack(side="right", padx=10)
        
        # Статус обновления
        self.status_label = tk.Label(
            right_info_frame,
            text="Готов",
            font=("Arial", 9),
            fg="green"
        )
        self.status_label.pack(side="right", padx=5)
        
        # Основной контейнер с двумя панелями
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        paned_window.pack(fill="both", expand=True, pady=10)

        # Левая панель - список питомцев
        left_frame = tk.Frame(paned_window)
        paned_window.add(left_frame, width=800)
        self.setup_left_panel(left_frame)
        
        # Правая панель - игроки с выбранным питомцем
        right_frame = tk.Frame(paned_window)
        paned_window.add(right_frame, width=800)
        self.setup_right_panel(right_frame)
        
        # Привязка события выбора питомца
        self.pets_tree.bind('<<TreeviewSelect>>', self.on_pet_select)
    
    def return_to_search_window(self):
        """Возвращается к основному окну поиска"""
        from .pet_search import PetSearchWindow
        
        # Закрываем текущее окно
        self.destroy()
        
        # Открываем основное окно с теми же данными
        search_window = PetSearchWindow(
            self.master,  # parent
            self.player_data,
            self.show_guild,
            self.show_dophenek
        )
        
        # Передаем уже загруженные данные
        search_window.name_to_id = self.name_to_id
        search_window.id_to_name = self.id_to_name
        search_window.pet_details = self.pet_details
    
    def refresh_player_data(self):
        """Обновляет данные игроков"""
        if self.update_in_progress:
            messagebox.showinfo("Информация", "Обновление уже выполняется...")
            return
        
        # Проверяем, есть ли UserID для обновления
        if not self.player_data:
            messagebox.showwarning("Ошибка", "Нет данных игроков для обновления")
            return
        
        # Получаем список UserID из данных игроков
        user_ids = list(self.player_data.keys())
        if not user_ids:
            messagebox.showwarning("Ошибка", "Нет UserID для обновления")
            return
        
        # Меняем статус
        self.update_in_progress = True
        self.btn_refresh.config(state="disabled", text="🔄 Обновление...")
        self.status_label.config(text="Обновление...", fg="blue")
        self.time_label.config(text="Обновление...")
        
        # Запускаем обновление в отдельном потоке
        threading.Thread(target=self._fetch_updated_data, args=(user_ids,), daemon=True).start()
    
    def _fetch_updated_data(self, user_ids):
        """Загружает обновленные данные в отдельном потоке"""
        updated_data = {}
        errors = []
        
        try:
            for idx, user_id in enumerate(user_ids):
                try:
                    response = requests.post(
                        URL, 
                        json={"functionName": "get_hero_profile", "Id": user_id},
                        timeout=10
                    )
                    response.raise_for_status()
                    data = response.json()
                    updated_data[user_id] = data
                    
                    # Обновляем прогресс
                    progress = (idx + 1) / len(user_ids) * 100
                    self.after(0, lambda p=progress: self._update_progress(p))
                    
                except Exception as e:
                    errors.append(f"{user_id}: {str(e)}")
            
            # Обновляем данные в основном потоке
            self.after(0, lambda: self._apply_updated_data(updated_data, errors))
            
        except Exception as e:
            self.after(0, lambda: self._update_failed(f"Ошибка обновления: {str(e)}"))
    
    def _update_progress(self, progress):
        """Обновляет индикатор прогресса"""
        self.time_label.config(text=f"Загрузка: {progress:.0f}%")
    
    def _apply_updated_data(self, updated_data, errors):
        """Применяет обновленные данные"""
        # Обновляем данные
        self.player_data = updated_data
        
        # Обновляем время
        self.last_update_time = datetime.now()
        
        # Обновляем UI
        self.time_label.config(
            text=f"Последнее обновление: {self.last_update_time.strftime('%H:%M:%S')}",
            fg="gray"
        )
        
        # Сбрасываем статус
        self.update_in_progress = False
        self.btn_refresh.config(state="normal", text="🔄 Обновить данные игроков")
        
        # Показываем результаты
        if errors:
            self.status_label.config(text=f"Ошибок: {len(errors)}", fg="orange")
            if len(errors) <= 5:  # Показываем только первые 5 ошибок
                error_msg = "\n".join(errors[:5])
                if len(errors) > 5:
                    error_msg += f"\n... и ещё {len(errors) - 5} ошибок"
                messagebox.showwarning("Ошибки обновления", 
                    f"Обновлено {len(self.player_data)} из {len(self.player_data) + len(errors)} игроков\n\nОшибки:\n{error_msg}")
        else:
            self.status_label.config(text="✓ Успешно", fg="green")
            messagebox.showinfo("Успех", f"Данные {len(self.player_data)} игроков успешно обновлены")
        
        # Если есть выбранный питомец - обновляем таблицу
        selection = self.pets_tree.selection()
        if selection:
            item = self.pets_tree.item(selection[0])
            pet_name = item['values'][0]
            
            # Находим ID питомца по имени
            pet_id = None
            for pid, name in self.id_to_name.items():
                if name == pet_name:
                    pet_id = pid
                    break
            
            if pet_id:
                self.show_players_with_pet(pet_id, pet_name)
    
    def _update_failed(self, error_msg):
        """Обрабатывает ошибку обновления"""
        self.update_in_progress = False
        self.btn_refresh.config(state="normal", text="🔄 Обновить данные игроков")
        self.status_label.config(text="❌ Ошибка", fg="red")
        self.time_label.config(text=f"Ошибка: {datetime.now().strftime('%H:%M:%S')}")
        messagebox.showerror("Ошибка", error_msg)
    
    def setup_left_panel(self, parent):
        """Настраивает левую панель со списком питомцев"""
        # Заголовок
        self.left_title = tk.Label(parent, text="Список питомцев", 
                                 font=('Arial', 12, 'bold'))
        self.left_title.pack(pady=5)
        
        # Поиск
        search_frame = tk.Frame(parent)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(search_frame, text="Поиск:").pack(side="left")
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

        # Настройка колонок
        columns_config = {
            "name": {"text": "Название", "anchor": "center", "width": 250},
            "kingdom": {"text": "Королевство", "anchor": "center", "width": 150},
            "effect": {"text": "Эффект", "anchor": "center", "width": 200},
            "mana_color": {"text": "Цвет маны", "anchor": "center", "width": 120}
        }
        
        for col, config in columns_config.items():
            self.pets_tree.heading(col, text=config["text"])
            self.pets_tree.column(col, anchor=config["anchor"], width=config["width"], stretch=False)
    
    def setup_right_panel(self, parent):
        """Настраивает правую панель с игроками"""
        self.pet_info_label = tk.Label(parent, text="Выберите питомца для просмотра", 
                                     font=('Arial', 11, 'bold'), fg='blue')
        self.pet_info_label.pack(pady=5)
        
        # Таблица игроков
        players_frame = tk.LabelFrame(parent, text="Игроки с питомцем")
        players_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Прокрутка
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
            "player_name": {"text": "Игрок", "anchor": "center", "width": 180},
            "guild_name": {"text": "Гильдия", "anchor": "center", "width": 150},
            "level": {"text": "Уровень", "anchor": "center", "width": 80},
            "ascension": {"text": "Возвышение", "anchor": "center", "width": 100},
            "amount": {"text": "Кол-во", "anchor": "center", "width": 100}
        }
        
        for col, config in players_columns.items():
            self.players_tree.heading(col, text=config["text"])
            self.players_tree.column(col, anchor=config["anchor"], width=config["width"], stretch=False)
        
        # Настройка цветов строк
        self.players_tree.tag_configure('no_pet', background='#ffcccc')  # Красный - нет питомца
        self.players_tree.tag_configure('low_level', background='#ffffcc')  # Желтый - уровень 1-15
        self.players_tree.tag_configure('max_level', background='#ccffcc')  # Зеленый - уровень 20
    
    def populate_pets_list(self):
        """Заполняет список питомцев (вызывается после передачи данных)"""
        if not self.all_pets:
            # Создаем список из pet_details
            self.all_pets = []
            for pet_id, details in self.pet_details.items():
                self.all_pets.append({
                    'id': int(pet_id),
                    'name': details['name'],
                    'kingdom': details['kingdom'],
                    'effect': details['effect'],
                    'mana_color': details['mana_color']
                })
            
            # Сортируем по имени
            self.all_pets.sort(key=lambda x: x['name'])
        
        # Заполняем таблицу
        self.pets_tree.delete(*self.pets_tree.get_children())
        for pet in self.all_pets:
            self.pets_tree.insert("", "end", values=(
                pet['name'],
                pet['kingdom'],
                pet['effect'],
                pet['mana_color']
            ))
    
    def on_pet_select(self, event):
        """Обработчик выбора питомца"""
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
        
        info_text = f"Питомец: {pet_name}"
        if pet_data.get('kingdom'):
            info_text += f" | Королевство: {pet_data['kingdom']}"
        if pet_data.get('mana_color'):
            info_text += f" | Цвет маны: {pet_data['mana_color']}"
        
        self.pet_info_label.config(text=info_text)
        
        # Очищаем таблицу игроков
        self.players_tree.delete(*self.players_tree.get_children())
        
        if not self.player_data:
            self.players_tree.insert("", "end", values=("", "Нет данных", "", "", "", ""))
            return
        
        pet_id_str = str(pet_id)
        players_data = []
        
        # Собираем данные по всем игрокам
        for idx, (user_id, data) in enumerate(self.player_data.items(), start=1):
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            if not profile:
                continue
                
            player_name = profile.get("Name", "Неизвестно")
            guild_name = profile.get("GuildName", "Нет гильдии")
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
        
        # Сортируем: сначала те, у кого есть питомец, потом те, у кого нет
        players_with_pet = [p for p in players_data if p['has_pet']]
        players_without_pet = [p for p in players_data if not p['has_pet']]
        
        # Сортируем игроков с питомцем по убыванию уровня
        players_with_pet.sort(key=lambda x: (x['level'], x['ascension'], x['amount']), reverse=True)
        
        # Объединяем списки
        all_players = players_with_pet + players_without_pet
        
        # Заполняем таблицу
        for idx, player in enumerate(all_players, start=1):
            values = (
                idx,
                player['name'],
                player['guild'],
                player['level'] if player['has_pet'] else "Нет",
                player['ascension'] if player['has_pet'] else "Нет",
                player['amount'] if player['has_pet'] else "Нет"
            )
            
            # Определяем цвет строки
            if not player['has_pet']:
                self.players_tree.insert("", "end", values=values, tags=('no_pet',))
            elif player['level'] == 20:
                self.players_tree.insert("", "end", values=values, tags=('max_level',))
            elif 1 <= player['level'] <= 15:
                self.players_tree.insert("", "end", values=values, tags=('low_level',))
            else:
                self.players_tree.insert("", "end", values=values)
    
    def filter_pets(self, event=None):
        """Фильтрует список питомцев"""
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