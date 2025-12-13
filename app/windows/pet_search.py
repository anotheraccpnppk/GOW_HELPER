"""Окно поиска питомцев"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import requests
from tkinter import font as tkfont

from windows.base import BaseWindow
from config import DOPHENEK_MAP
from translation import translator

class PetSearchWindow(BaseWindow):
    def __init__(self, parent, player_data, show_guild=False, show_dophenek=False):
        super().__init__(parent)
        self.title(translator.t("pet_search_title"))
        self.geometry("1400x750")
        self.player_data = player_data
        self.show_guild = show_guild
        self.show_dophenek = show_dophenek
        
        # Инициализация данных
        self.name_to_id = {}
        self.id_to_name = {}
        self.pet_details = {}
        self.selected_pets = []
        self.pet_ui_refs = []
        
        # Загрузка данных о питомцах
        self.load_pets_data()
        
        # Настройка интерфейса
        self.setup_ui()
        self.show_players_list()
        self.configure_treeview_style()

    def load_pets_data(self):
        """Загружает данные о питомцах с внешнего ресурса"""
        url = "https://garyatrics.com/taran-data/Pets_Russian.json"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            pets_data = response.json()
            
            for pet in pets_data.get("pets", []):
                pet_id = pet.get("id")
                name = pet.get("name", "").strip().lower()
                if pet_id and name:
                    self.name_to_id[name] = pet_id
                    self.id_to_name[str(pet_id)] = pet.get("name", "").strip()
                    self.pet_details[str(pet_id)] = {
                        'name': pet.get("name", ""),
                        'kingdom': pet.get("kingdomName", ""),
                        'effect': pet.get("effect", ""),
                        'mana_color': pet.get("manaColor", "")
                    }
                    
        except Exception as e:
            messagebox.showerror(translator.t("error"), 
                translator.t("export_error", error=str(e)))

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Верхняя панель с кнопками
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=5)
        
        self.btn_toggle_guild = tk.Button(
            top_frame, 
            text=translator.t("hide_guild") if self.show_guild else translator.t("show_guild"),
            width=18, 
            command=self.toggle_guild_column
        )
        self.btn_toggle_guild.pack(side="left", padx=5)

        self.btn_toggle_dophenek = tk.Button(
            top_frame,
            text=translator.t("hide_dophenek") if self.show_dophenek else translator.t("show_dophenek"),
            width=18,
            command=self.toggle_dophenek_column
        )
        self.btn_toggle_dophenek.pack(side="left", padx=5)

        btn_export_csv = tk.Button(
            top_frame, 
            text=translator.t("save_csv"), 
            width=18, 
            command=self.export_to_csv
        )
        btn_export_csv.pack(side="right", padx=5)

        # Панель поиска питомцев
        search_outer_frame = tk.Frame(main_frame)
        search_outer_frame.pack(pady=10, fill="x")

        search_frame = tk.Frame(search_outer_frame)
        search_frame.pack(anchor='center')

        tk.Label(search_frame, text=translator.t("search_pet")).pack(side="left", padx=5)
        self.entry = tk.Entry(search_frame, width=40)
        self.entry.pack(side="left", padx=5)

        btn_add = tk.Button(search_frame, text=translator.t("add_pet"), width=18, command=self.add_pet)
        btn_add.pack(side="left", padx=5)

        button_frame = tk.Frame(search_outer_frame)
        button_frame.pack(anchor='center', pady=(10, 0))

        btn_search = tk.Button(
            button_frame, 
            text=translator.t("find_pets"), 
            width=20,
            command=self.find_multiple_pets
        )
        btn_search.pack(pady=(0, 5))

        btn_clear = tk.Button(
            button_frame,
            text=translator.t("clear_list"),
            width=20,
            command=self.clear_pets_list
        )
        btn_clear.pack()

        # Панель выбранных питомцев
        pets_list_frame = tk.Frame(main_frame)
        pets_list_frame.pack(fill="x", pady=(5, 0))
        tk.Label(pets_list_frame, text=translator.t("selected_pets"), font=('Arial', 10, 'bold')).pack(anchor="w")
        
        self.pets_listbox = tk.Listbox(
            pets_list_frame, 
            height=4, 
            selectmode=tk.SINGLE,
            exportselection=0
        )
        self.pets_listbox.pack(fill="x", pady=5)
        self.pets_listbox.bind('<<ListboxSelect>>', self.on_pet_select)

        # Фрейм для деталей питомца
        self.pet_details_frame = tk.Frame(pets_list_frame)
        self.pet_details_frame.pack(fill="x", pady=5)
        
        # Таблица с результатами
        self.setup_results_tree(main_frame)

    def setup_results_tree(self, parent):
        """Настраивает Treeview для отображения результатов"""
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Создаем горизонтальную и вертикальную прокрутку
        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar = ttk.Scrollbar(container)
        yscrollbar.pack(side="right", fill="y")

        # Создаем Treeview с базовыми колонками
        base_columns = ["#", "player_name"]
        if self.show_dophenek:
            base_columns.append("dophenek_name")
        if self.show_guild:
            base_columns.append("guild_name")
            
        self.tree = ttk.Treeview(
            container, 
            columns=base_columns, 
            show="headings", 
            height=15,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set,
            selectmode="browse"
        )
        
        self.tree.pack(fill="both", expand=True)
        
        # Настраиваем прокрутку
        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)

        # Настройка базовых колонок
        self.tree.heading("#", text="#")
        self.tree.column("#", width=40, anchor="center", stretch=False)
        
        self.tree.heading("player_name", text=translator.t("column_player"), command=lambda: self.sort_treeview("player_name", False))
        self.tree.column("player_name", width=180, anchor="center")
        
        if self.show_dophenek:
            self.tree.heading("dophenek_name", text=translator.t("column_dophenek"), command=lambda: self.sort_treeview("dophenek_name", False))
            self.tree.column("dophenek_name", width=150, anchor="center")
        
        if self.show_guild:
            self.tree.heading("guild_name", text=translator.t("column_guild"), command=lambda: self.sort_treeview("guild_name", False))
            self.tree.column("guild_name", width=150, anchor="center")

    def add_pet(self):
        """Добавляет питомца в список для поиска"""
        pet_name = self.entry.get().strip().lower()
        if not pet_name:
            messagebox.showwarning(translator.t("error"), translator.t("enter_pet_name"))
            return

        # Поиск точного совпадения
        exact_matches = [(name, pid) for name, pid in self.name_to_id.items() if name == pet_name]
        
        if exact_matches:
            selected_name, pid = exact_matches[0]
        else:
            # Поиск частичных совпадений
            partial_matches = [(name, pid) for name, pid in self.name_to_id.items() if pet_name in name]
            
            if not partial_matches:
                messagebox.showinfo(translator.t("info"), translator.t("pet_not_found", pet_name=pet_name))
                return
            elif len(partial_matches) == 1:
                selected_name, pid = partial_matches[0]
            else:
                # Если несколько совпадений - показываем выбор
                selected_name = self.choose_from_list(
                    [self.id_to_name[str(pid)] for _, pid in partial_matches], 
                    title=translator.t("info"),
                    prompt=translator.t("pet_not_found", pet_name=pet_name)
                )
                if not selected_name:
                    return
                # Находим ID выбранного питомца
                pid = next(pid for name, pid in self.name_to_id.items() 
                          if self.id_to_name[str(pid)] == selected_name)

        # Проверяем, не добавлен ли уже питомец
        if pid in [p[0] for p in self.selected_pets]:
            messagebox.showinfo(translator.t("info"), translator.t("pet_already_in_list", pet_name=self.id_to_name[str(pid)]))
            return

        # Добавляем питомца в список
        self.selected_pets.append((pid, self.id_to_name[str(pid)]))
        self.update_pets_listbox()
        self.entry.delete(0, tk.END)
        self.show_pet_details(pid)

    def update_pets_listbox(self):
        """Обновляет список выбранных питомцев"""
        self.pets_listbox.delete(0, tk.END)
        for pid, name in self.selected_pets:
            self.pets_listbox.insert(tk.END, name)

    def on_pet_select(self, event):
        """Обработчик выбора питомца в списке"""
        selection = self.pets_listbox.curselection()
        if selection:
            pid = self.selected_pets[selection[0]][0]
            self.show_pet_details(pid)

    def show_pet_details(self, pet_id):
        """Показывает детальную информацию о выбранном питомце"""
        # Очищаем фрейм с деталями
        for widget in self.pet_details_frame.winfo_children():
            widget.destroy()

        pet_data = self.pet_details.get(str(pet_id), {})
        if not pet_data:
            return

        # Создаем элементы для отображения информации
        details = [
            ("Название:", pet_data.get('name', 'Н/Д')),
            ("Королевство:", pet_data.get('kingdom', 'Н/Д')),
            ("Эффект:", pet_data.get('effect', 'Н/Д')),
            ("Цвет маны:", pet_data.get('mana_color', 'Н/Д'))
        ]

        for i, (label, value) in enumerate(details):
            tk.Label(self.pet_details_frame, text=label, font=('Arial', 9, 'bold')).grid(row=i, column=0, sticky="e", padx=5)
            tk.Label(self.pet_details_frame, text=value).grid(row=i, column=1, sticky="w", padx=5)

    def find_multiple_pets(self):
        """Поиск выбранных питомцев у всех игроков"""
        if not self.selected_pets:
            messagebox.showwarning(translator.t("error"), translator.t("add_at_least_one_pet"))
            return

        self.tree.delete(*self.tree.get_children())
        
        # Определяем колонки
        columns = ["#", "player_name"]
        if self.show_dophenek:
            columns.append("dophenek_name")
        if self.show_guild:
            columns.append("guild_name")
            
        # Добавляем колонки для каждого питомца
        for pid, name in self.selected_pets:
            columns.extend([
                f"{pid}_owned",      # Наличие
                f"{pid}_level",      # Уровень
                f"{pid}_ascension",  # Уровень возвышения
                f"{pid}_amount",     # Количество
            ])

        self.tree["columns"] = columns
        
        # Настраиваем все колонки
        for col in columns:
            if col == "#":
                self.tree.heading(col, text="#")
                self.tree.column(col, width=40, anchor="center", stretch=False)
            elif col == "player_name":
                self.tree.heading(col, text=translator.t("column_player"), command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=180, anchor="center")
            elif col == "dophenek_name":
                self.tree.heading(col, text=translator.t("column_dophenek"), command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=150, anchor="center")
            elif col == "guild_name":
                self.tree.heading(col, text=translator.t("column_guild"), command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=150, anchor="center")
            elif col.endswith("_owned"):
                pet_id = col.split("_")[0]
                pet_name = self.id_to_name.get(pet_id, "Питомец")
                self.tree.heading(col, text=f"{pet_name}\nНаличие", command=lambda c=col: self.sort_treeview(c, False))
                self.tree.column(col, width=80, anchor="center")
            elif col.endswith("_level"):
                pet_id = col.split("_")[0]
                pet_name = self.id_to_name.get(pet_id, "Питомец")
                self.tree.heading(col, text=f"{pet_name}\nУровень", command=lambda c=col: self.sort_treeview(c, False))
                self.tree.column(col, width=80, anchor="center")
            elif col.endswith("_ascension"):
                pet_id = col.split("_")[0]
                pet_name = self.id_to_name.get(pet_id, "Питомец")
                self.tree.heading(col, text=f"{pet_name}\nВозвышение", command=lambda c=col: self.sort_treeview(c, False))
                self.tree.column(col, width=80, anchor="center")
            elif col.endswith("_amount"):
                pet_id = col.split("_")[0]
                pet_name = self.id_to_name.get(pet_id, "Питомец")
                self.tree.heading(col, text=f"{pet_name}\nКол-во", command=lambda c=col: self.sort_treeview(c, False))
                self.tree.column(col, width=80, anchor="center")
           
        # Заполняем таблицу данными
        for idx, (user_id, data) in enumerate(self.player_data.items(), start=1):
            profile = data.get("result", {}).get("ProfileData", {})
            player_name = profile.get("Name", "Неизвестно")
            dophenek_name = DOPHENEK_MAP.get(user_id, "")
            guild_name = profile.get("GuildName", "")
            pets = profile.get("Pets", {})

            row = [str(idx), player_name]
            if self.show_dophenek:
                row.append(dophenek_name)
            if self.show_guild:
                row.append(guild_name)
                
            for pid, _ in self.selected_pets:
                pet_data = pets.get(str(pid), {})
                
                # Наличие питомца
                row.append("✓" if pet_data else "✗")
                
                # Уровень питомца
                row.append(str(pet_data.get("Level", 0)) if pet_data else "0")
                
                # Уровень возвышения
                row.append(str(pet_data.get("AscensionLevel", 0)) if pet_data else "0")
                
                # Количество питомцев
                row.append(str(pet_data.get("Amount", 0)) if pet_data else "0")
                      
            self.tree.insert("", tk.END, values=row)

        # Автоматически подгоняем ширину колонок
        self.auto_resize_columns()

    def auto_resize_columns(self):
        """Автоматически подгоняет ширину колонок"""
        font = tkfont.Font()
        
        # Подгонка по заголовкам
        for col in self.tree["columns"]:
            header_text = self.tree.heading(col)["text"]
            header_width = font.measure(header_text) + 20
            self.tree.column(col, width=header_width)

        # Подгонка по содержимому
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            for i, col in enumerate(self.tree["columns"]):
                if i < len(values):
                    value = str(values[i])
                    width = font.measure(value) + 20
                    if self.tree.column(col, width=None) < width:
                        self.tree.column(col, width=width)

    def clear_pets_list(self):
        """Очищает список выбранных питомцев"""
        self.selected_pets = []
        self.update_pets_listbox()
        for widget in self.pet_details_frame.winfo_children():
            widget.destroy()

    def export_to_csv(self):
        """Экспортирует данные в CSV файл"""
        if not self.tree.get_children():
            messagebox.showwarning(translator.t("error"), translator.t("no_data_to_export"))
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                
                # Заголовки
                headers = []
                for col in self.tree["columns"]:
                    headers.append(self.tree.heading(col)["text"].replace("\n", " "))
                writer.writerow(headers)
                
                # Данные
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)["values"])
                    
            messagebox.showinfo(translator.t("success"), translator.t("data_saved", file_path=file_path))
        except Exception as e:
            messagebox.showerror(translator.t("error"), translator.t("export_error", error=str(e)))

    def toggle_guild_column(self):
        """Переключает отображение столбца с гильдией"""
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text=translator.t("hide_guild") if self.show_guild else translator.t("show_guild")
        )
        if self.selected_pets:
            self.find_multiple_pets()
        else:
            self.show_players_list()

    def toggle_dophenek_column(self):
        """Переключает отображение столбца с доп. именем"""
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text=translator.t("hide_dophenek") if self.show_dophenek else translator.t("show_dophenek")
        )
        if self.selected_pets:
            self.find_multiple_pets()
        else:
            self.show_players_list()

    def show_players_list(self):
        """Показывает список игроков без фильтрации по питомцам"""
        self.tree.delete(*self.tree.get_children())
        columns = ["#", "player_name"]
        if self.show_dophenek:
            columns.append("dophenek_name")
        if self.show_guild:
            columns.append("guild_name")
        
        self.tree["columns"] = columns
        
        # Настройка колонок
        for col in columns:
            if col == "#":
                self.tree.heading(col, text="#")
                self.tree.column(col, width=40, anchor="center", stretch=False)
            elif col == "player_name":
                self.tree.heading(col, text=translator.t("column_player"), command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=180, anchor="center")
            elif col == "dophenek_name":
                self.tree.heading(col, text=translator.t("column_dophenek"), command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=150, anchor="center")
            elif col == "guild_name":
                self.tree.heading(col, text=translator.t("column_guild"), command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=150, anchor="center")

        # Заполнение данными
        for idx, user_id in enumerate(self.player_data.keys(), start=1):
            data = self.player_data.get(user_id, {})
            profile = data.get("result", {}).get("ProfileData", {})
            player_name = profile.get("Name", "Неизвестно")
            dophenek_name = DOPHENEK_MAP.get(user_id, "")
            guild_name = profile.get("GuildName", "")

            row = [str(idx), player_name]
            if self.show_dophenek:
                row.append(dophenek_name)
            if self.show_guild:
                row.append(guild_name)
                
            self.tree.insert("", tk.END, values=row)
        
        self.auto_resize_columns()

    def sort_treeview(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#":
            return

        # Получаем все элементы
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Определяем тип сортировки
        if col.endswith("_level") or col.endswith("_ascension") or col.endswith("_amount"):
            # Числовая сортировка для уровней, возвышения и количества
            items.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        elif col.endswith("_owned"):
            # Специальная сортировка для наличия (✓ выше)
            items.sort(key=lambda t: (t[0] != "✓", t[0]), reverse=reverse)
        else:
            # Текстовая сортировка
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        
        # Перемещаем элементы
        for index, (_, k) in enumerate(items, start=1):
            self.tree.move(k, '', index)
        
        # Обновляем нумерацию
        for idx, item in enumerate(self.tree.get_children(), start=1):
            self.tree.set(item, "#", str(idx))
        
        # Обновляем заголовки с указанием направления сортировки
        for column in self.tree["columns"]:
            heading = self.tree.heading(column)
            if column == col:
                heading["text"] = heading["text"].split(" ↓")[0].split(" ↑")[0] + (" ↓" if reverse else " ↑")
            else:
                heading["text"] = heading["text"].split(" ↓")[0].split(" ↑")[0]
            self.tree.heading(column, 
                            text=heading["text"],
                            command=lambda c=column: self.sort_treeview(c, not reverse))

    def choose_from_list(self, options, title="Выбор", prompt="Выберите вариант"):
        """Показывает диалог выбора из списка"""
        selected = []
        top = tk.Toplevel(self)
        top.title(title)
        top.grab_set()
        
        tk.Label(top, text=prompt).pack(pady=10)
        
        listbox = tk.Listbox(top, selectmode=tk.SINGLE, height=10, width=40)
        scrollbar = tk.Scrollbar(top, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.pack(padx=10, pady=5)
        
        for item in sorted(options):
            listbox.insert(tk.END, item)
        
        def on_ok():
            selection = listbox.curselection()
            if selection:
                selected.append(listbox.get(selection[0]))
            top.destroy()
        
        btn_ok = tk.Button(top, text="OK", width=10, command=on_ok)
        btn_ok.pack(pady=10)
        
        self.wait_window(top)
        return selected[0] if selected else None

