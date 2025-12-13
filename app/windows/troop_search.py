import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import tkinter.font as tkfont
import requests
from app.windows.base import BaseWindow
from app.config import DOPHENEK_MAP
from app.translation import translator
class TroopSearchWindow(BaseWindow):
    def __init__(self, parent, player_data, show_guild=False, show_dophenek=False):
        super().__init__(parent)
        self.title("Поиск войск у игроков")
        self.geometry("1100x650")
        self.player_data = player_data
        self.show_guild = show_guild
        self.show_dophenek = show_dophenek

        self.column_display_names = {
        "#": "#",
        "player_name": "Игрок", 
        "dophenek_name": "Доп. имя",
        "guild_name": "Гильдия"
    }
        
        # Инициализация словарей для войск
        self.name_to_id = {}  # Соответствие имени войска его ID
        self.id_to_name = {}  # Соответствие ID войска его имени
        self.selected_troops = []  # Выбранные войска для отображения
        self.troop_ui_refs = []    # Ссылки на UI элементы
        self.troop_columns_display = {}

        # Загрузка данных о войсках
        self.load_troops_data()
        
        self.setup_ui()
        self.show_players_list()

        # Настройка стиля Treeview
        self.configure_treeview_style()

    def load_troops_data(self):
        """Загружает данные о войсках с внешнего сервера"""
        url = "https://garyatrics.com/taran-data/Troops_Russian.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            troops = response.json().get("troops", [])
            
            for troop in troops:
                if "id" in troop and "name" in troop:
                    troop_id = troop["id"]
                    name = troop["name"].strip().lower()
                    self.name_to_id[name] = troop_id
                    self.id_to_name[str(troop_id)] = troop["name"].strip()
                    
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", 
                f"Не удалось загрузить список войск:\n{e}\n"
                "Проверьте интернет-соединение")

    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=5)

        self.btn_toggle_guild = tk.Button(
            top_frame, 
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию",
            width=15, 
            command=self.toggle_guild_column
        )
        self.btn_toggle_guild.pack(side="left", padx=5)

        self.btn_toggle_dophenek = tk.Button(
            top_frame,
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя",
            width=15,
            command=self.toggle_dophenek_column
        )
        self.btn_toggle_dophenek.pack(side="left", padx=5)

        btn_export = tk.Button(
            top_frame, 
            text="Сохранить как .csv", 
            width=15, 
            command=self.export_to_csv
        )
        btn_export.pack(side="right", padx=5)

        center_frame = tk.Frame(main_frame)
        center_frame.pack(fill="x", pady=10)

        search_frame = tk.Frame(center_frame)
        search_frame.pack(expand=True, fill="x")

        search_container = tk.Frame(search_frame)
        search_container.pack(pady=5)

        tk.Label(search_container, text="Название войска:").pack(side="left", padx=5)
        self.entry = tk.Entry(search_container, width=30)
        self.entry.pack(side="left", padx=5)
        
        btn_add = tk.Button(
            search_container, 
            text="Добавить войско", 
            width=15, 
            command=self.add_troop
        )
        btn_add.pack(side="left", padx=5)

        btn_run = tk.Button(
            center_frame, 
            text="Показать войска", 
            width=15, 
            command=self.find_multiple_troops
        )
        btn_run.pack(pady=(10, 0))

        troop_list_frame = tk.Frame(main_frame)
        troop_list_frame.pack(fill="x", pady=(5,0))
        tk.Label(troop_list_frame, text="Выбранные войска:").pack(anchor="w")
        self.troop_entries_frame = tk.Frame(troop_list_frame)
        self.troop_entries_frame.pack(anchor="w", fill="x")

        self.setup_results_tree(main_frame)
        
    def setup_results_tree(self, parent):
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        
        yscrollbar = ttk.Scrollbar(container)
        yscrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            container, 
            columns=["#", "player_name"] + 
                (["dophenek_name"] if self.show_dophenek else []) + 
                (["guild_name"] if self.show_guild else []), 
            show="headings", 
            height=20,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        
        self.tree.pack(fill="both", expand=True)
        
        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)

        # Настройка колонок с обработчиками сортировки
        self.tree.heading("#", text="#")
        self.tree.column("#", width=40, minwidth=40, anchor="center", stretch=False)
        
        self.tree.heading("player_name", text="Игрок", command=lambda: self.sort_treeview("player_name", False))
        self.tree.column("player_name", width=150, minwidth=100, anchor="w")
        
        if self.show_dophenek:
            self.tree.heading("dophenek_name", text="Доп. имя", command=lambda: self.sort_treeview("dophenek_name", False))
            self.tree.column("dophenek_name", width=150, minwidth=100, anchor="center")
        
        if self.show_guild:
            self.tree.heading("guild_name", text="Гильдия", command=lambda: self.sort_treeview("guild_name", False))
            self.tree.column("guild_name", width=150, minwidth=100, anchor="center")    

    def sort_treeview(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#":
            return  # Не сортируем по номеру строки

        # Получаем все элементы
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Определяем тип сортировки
        if col.endswith("_level") or col.endswith("_amount"):
            # Числовая сортировка для уровней и количества
            items.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        elif col.endswith("_elite"):
            # Специальная сортировка для медалей (текстовая, но с особым порядком)
            medal_order = {"нет": 0, "бронза": 1, "серебро": 2, "золото": 3}
            items.sort(key=lambda t: medal_order.get(t[0].lower(), 0), reverse=reverse)
        elif col.endswith("_traits"):
            # Числовая сортировка для навыков
            items.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        else:
            # Текстовая сортировка для имен и гильдий
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

    def show_players_list(self):
        self.tree.delete(*self.tree.get_children())
        columns = ["#", "player_name"]
        
        if self.show_dophenek:
            columns.append("dophenek_name")
        if self.show_guild:
            columns.append("guild_name")
        
        self.tree["columns"] = columns
        
        # Настройка заголовков с использованием отображаемых имен
        for col in columns:
            display_name = self.column_display_names.get(col, col)
            self.tree.heading(col, text=display_name, 
                            command=lambda c=col: self.sort_treeview(c, False))
            
            if col == "#":
                self.tree.column(col, width=40, anchor="center", stretch=False)
            elif col == "player_name":
                self.tree.column(col, width=150, anchor="center")
            else:
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

    def toggle_guild_column(self):
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        if self.selected_troops:
            self.find_multiple_troops()
        else:
            self.show_players_list()

    def toggle_dophenek_column(self):
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )
        if self.selected_troops:
            self.find_multiple_troops()
        else:
            self.show_players_list()

    def add_troop(self):

        """Добавляет войско в список для поиска"""
        troop_name = self.entry.get().strip().lower()
        if not troop_name:
            messagebox.showwarning("Ошибка", "Введите название войска")
            return

        # Поиск точного совпадения
        exact_matches = [(name, tid) for name, tid in self.name_to_id.items() if name == troop_name]
        
        if exact_matches:
            selected_name, tid = exact_matches[0]
        else:
            # Поиск частичных совпадений
            partial_matches = [(name, tid) for name, tid in self.name_to_id.items() if troop_name in name]
            
            if not partial_matches:
                messagebox.showinfo("Не найдено", f"Войско '{troop_name}' не найдено.")
                return
            elif len(partial_matches) == 1:
                selected_name, tid = partial_matches[0]
            else:
                # Если несколько совпадений - показываем выбор
                selected_name = self.choose_from_list(
                    [self.id_to_name[str(tid)] for _, tid in partial_matches], 
                    title="Выбор войска",
                    prompt=f"Найдено несколько совпадений для '{troop_name}'"
                )
                if not selected_name:
                    return
                # Находим ID выбранного войска
                tid = next(tid for name, tid in self.name_to_id.items() 
                        if self.id_to_name[str(tid)] == selected_name)

        # Проверяем, не добавлено ли уже войско
        if tid in [t[0] for t in self.selected_troops]:
            messagebox.showinfo("Информация", f"Войско '{self.id_to_name[str(tid)]}' уже в списке.")
            return

        # Добавляем войско в список
        self.selected_troops.append((tid, self.id_to_name[str(tid)], tk.BooleanVar(value=False)))
        self.render_selected_troops()
        self.entry.delete(0, tk.END)

    def render_selected_troops(self):
        """Отрисовывает список выбранных войск с элементами управления"""
        # Полностью очищаем фрейм
        for widget in self.troop_entries_frame.winfo_children():
            widget.destroy()
        
        # Сохраняем состояния чекбоксов
        old_states = {tid: (level_var.get(), elite_var.get(), traits_var.get()) 
                    for tid, _, level_var, elite_var, traits_var, _ in self.troop_ui_refs}
        self.troop_ui_refs = []
        
        # Создаем элементы управления для каждого войска
        for tid, name, level_var in self.selected_troops:
            frame = tk.Frame(self.troop_entries_frame)
            frame.pack(anchor="w", fill="x", pady=5)

            # Название войска
            label = tk.Label(frame, text=name, width=25, anchor="w")
            label.pack(side="left", padx=5)

            # Чекбокс уровня
            level_cb = tk.Checkbutton(
                frame, 
                text="Уровень", 
                variable=level_var,
                command=self.update_troop_columns
            )
            level_cb.pack(side="left", padx=5)

            # Чекбокс медалей (бывший elite)
            elite_var = tk.BooleanVar(value=old_states.get(tid, (False, False, False))[1])
            elite_cb = tk.Checkbutton(
                frame,
                text="Медали",  # Изменили текст
                variable=elite_var,
                command=self.update_troop_columns
            )
            elite_cb.pack(side="left", padx=5)

            # Чекбокс навыков
            traits_var = tk.BooleanVar(value=old_states.get(tid, (False, False, False))[2])
            traits_cb = tk.Checkbutton(
                frame,
                text="Навыки",
                variable=traits_var,
                command=self.update_troop_columns
            )
            traits_cb.pack(side="left", padx=5)

            # Кнопка удаления
            btn = tk.Button(
                frame,
                text="Удалить",
                command=lambda t=tid, f=frame: self.remove_troop(t, f),
                width=8,
                padx=5,
                pady=2
            )
            btn.pack(side="left", padx=10)

            self.troop_ui_refs.append((tid, frame, level_var, elite_var, traits_var, btn))

    def update_troop_columns(self):
        """Обновляет отображение колонок при изменении чекбоксов"""
        # Просто перезагружаем таблицу с обновленными настройками колонок
        if hasattr(self, 'tree') and self.selected_troops:
            self.find_multiple_troops()

    def remove_troop(self, troop_id, frame):
        # Удаляем из списка выбранных
        self.selected_troops = [t for t in self.selected_troops if t[0] != troop_id]
        
        # Удаляем UI элементы
        frame.destroy()
        self.troop_ui_refs = [t for t in self.troop_ui_refs if t[0] != troop_id]
        
        # Немедленно обновляем таблицу
        if hasattr(self, 'tree') and self.tree.get_children():
           self.find_multiple_troops()

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

    def find_multiple_troops(self):
    
        if not self.selected_troops:
            self.tree.delete(*self.tree.get_children())
            return

        self.tree.delete(*self.tree.get_children())
        
        # Базовые колонки
        columns = ["#", "player_name"]
        
        if self.show_dophenek:
            columns.append("dophenek_name")
        if self.show_guild:
            columns.append("guild_name")
            
        self.troop_columns_display = {}
        
        # Добавляем колонки для каждого войска
        for troop_info in self.troop_ui_refs:
            tid, _, show_level_var, show_elite_var, show_traits_var, *_ = troop_info
            
            # Создаем имена колонки для каждого атрибута войска
            amount_col = f"{tid}_amount"  # Колонка количества
            level_col = f"{tid}_level"    # Колонка уровня
            elite_col = f"{tid}_elite"    # Колонка медалей
            traits_col = f"{tid}_traits"  # Колонка навыков
            
            # Получаем имя войска для отображения в заголовке
            name = next((name for tid2, name, _ in self.selected_troops if tid2 == tid), "Unknown")
            
            # Сохраняем отображаемые имена для каждой колонки
            self.troop_columns_display[amount_col] = f"{name} (кол-во)"
            if show_level_var.get():
                self.troop_columns_display[level_col] = f"{name} (уровень)"
            if show_elite_var.get():
                self.troop_columns_display[elite_col] = f"{name} (медали)"
            if show_traits_var.get():
                self.troop_columns_display[traits_col] = f"{name} (навыки)"
            
            # Добавляем колонки в список
            columns.append(amount_col)
            if show_level_var.get():
                columns.append(level_col)
            if show_elite_var.get():
                columns.append(elite_col)
            if show_traits_var.get():
                columns.append(traits_col)

        # Устанавливаем колонки в Treeview
        self.tree["columns"] = columns
        
        # Настраиваем заголовки и колонки
        for col in columns:
            if col == "#":
                # Колонка с номерами - статичная, без сортировки
                self.tree.heading(col, text="#")
                self.tree.column(col, width=40, anchor="center", stretch=False)
            else:
                # Для всех остальных колонок
                display_name = self.troop_columns_display.get(col, 
                                self.column_display_names.get(col, col))
                
                # Устанавливаем заголовок с обработчиком сортировки
                self.tree.heading(col, 
                                text=display_name,
                                command=lambda c=col: self.sort_treeview(c, False))
                
                # Настраиваем ширину колонок
                if col in ["player_name", "dophenek_name", "guild_name"]:
                    self.tree.column(col, width=150, anchor="center")
                else:
                    self.tree.column(col, width=100, anchor="center")

        # Заполняем таблицу данными
        for idx, (user_id, data) in enumerate(self.player_data.items(), start=1):
            profile = data.get("result", {}).get("ProfileData", {})
            player_name = profile.get("Name", "Неизвестно")
            dophenek_name = DOPHENEK_MAP.get(user_id, "")
            guild_name = profile.get("GuildName", "")
            troops = profile.get("Troops", {})

            # Начинаем формировать строку
            row = [str(idx), player_name]
            
            if self.show_dophenek:
                row.append(dophenek_name)
            if self.show_guild:
                row.append(guild_name)
                
            # Добавляем данные по каждому войску
            for troop_info in self.troop_ui_refs:
                tid, _, show_level_var, show_elite_var, show_traits_var, *_ = troop_info
                troop = troops.get(str(tid), {})
                
                # Количество
                row.append(str(troop.get("Amount", 0)))
                
                # Уровень (если включено)
                if show_level_var.get():
                    row.append(str(troop.get("Level", 0)))
                
                # Медали (если включено)
                if show_elite_var.get():
                    elite_level = troop.get("EliteLevel", 0)
                    medal_text = self.get_medal_text(elite_level)
                    row.append(medal_text)
                
                # Навыки (если включено)
                if show_traits_var.get():
                    row.append(str(troop.get("TraitsOwned", 0)))
                    
            # Вставляем строку в таблицу
            self.tree.insert("", tk.END, values=row)
        
        # Автоматически подгоняем ширину колонок
        self.auto_resize_columns()

    def get_medal_text(self, elite_level):
        """Преобразует числовое значение медалей в текст"""
        medal_mapping = {
            0: "нет",
            1: "бронза",
            2: "серебро",
            3: "золото"
        }
        return medal_mapping.get(elite_level, str(elite_level))

    def auto_resize_columns(self):
        font = tkfont.Font()
        for col in self.tree["columns"]:
            header_width = font.measure(self.tree.heading(col)["text"]) + 20
            self.tree.column(col, width=header_width)
        
        for row in self.tree.get_children():
            for i, value in enumerate(self.tree.item(row)["values"]):
                col_name = self.tree["columns"][i]
                current_width = self.tree.column(col_name, width=None)
                content_width = font.measure(str(value)) + 20
            
                if current_width < content_width:
                    self.tree.column(col_name, width=content_width)

    def export_to_csv(self):
        if not self.tree.get_children():
            messagebox.showwarning("Ошибка", "Нет данных для экспорта.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                headers = [self.tree.heading(col)["text"] for col in self.tree["columns"]]
                writer.writerow(headers)
                for row_id in self.tree.get_children():
                    writer.writerow(self.tree.item(row_id)["values"])
            messagebox.showinfo("Успех", f"Файл сохранён:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать:\n{e}")
