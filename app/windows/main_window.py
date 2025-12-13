# app/windows/main_window.py
"""Главное окно приложения"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import csv
import requests

from app.config import URL, DOPHENEK_MAP
from app.translation import translator
from app.utils import ToolTip
from app.windows.guild_members import GuildMembersWindow
from app.windows.kingdom_levels import KingdomLevelsWindow

# Временные импорты для окон, которые будут созданы позже
# TODO: Перенести эти окна в отдельные модули

class ProfileFetcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(translator.t("app_title"))
        self.geometry("1300x600")
        self.results = {}
        self._running = True
        self.show_dophenek = False
        self.show_guild = False
        self.deleted_stack = []
        
        # Регистрируем callback для обновления интерфейса при смене языка
        translator.register_callback(self.update_ui_texts)
        
        self.update_columns()
        self.setup_ui()
        self.configure_treeview_style()
    
    def update_columns(self):
        """Обновляет список колонок в зависимости от языка и настроек"""
        self.base_columns = ["#", "UserId", "InviteCode", translator.t("column_player")]
        self.dophenek_col = [translator.t("column_dophenek")] if self.show_dophenek else []
        self.guild_col = [translator.t("column_guild")] if self.show_guild else []
        self.delete_col = [translator.t("column_delete")]
        self.columns = self.base_columns + self.dophenek_col + self.guild_col + self.delete_col

    def configure_treeview_style(self):
        """Настраивает стиль Treeview для главного окна"""
        try:
            style = ttk.Style()
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            style.configure("Treeview", font=('Arial', 9))
            print("Стиль Treeview настроен для главного окна")
        except Exception as e:
            print(f"Ошибка настройки стиля главного окна: {e}")
    
    def change_language(self, lang):
        """Переключает язык интерфейса"""
        translator.set_language(lang)
        self.lang_var.set(lang)
    
    def update_ui_texts(self):
        """Обновляет все текстовые элементы интерфейса при смене языка"""
        try:
            # Обновляем заголовок окна
            self.title(translator.t("app_title"))
            
            # Обновляем метки и кнопки
            if hasattr(self, 'label_userid'):
                self.label_userid.config(text=translator.t("enter_userid"))
            if hasattr(self, 'btn_load_userid'):
                self.btn_load_userid.config(text=translator.t("load_userid"))
            if hasattr(self, 'btn_get_userid'):
                self.btn_get_userid.config(text=translator.t("get_userid"))
            if hasattr(self, 'btn_start'):
                self.btn_start.config(text=translator.t("start"))
            if hasattr(self, 'btn_toggle_dophenek'):
                text = translator.t("hide_dophenek") if self.show_dophenek else translator.t("show_dophenek")
                self.btn_toggle_dophenek.config(text=text)
            if hasattr(self, 'btn_toggle_guild'):
                text = translator.t("hide_guild") if self.show_guild else translator.t("show_guild")
                self.btn_toggle_guild.config(text=text)
            if hasattr(self, 'btn_show_stats'):
                self.btn_show_stats.config(text=translator.t("stats_window"))
            if hasattr(self, 'btn_kingdom_levels'):
                self.btn_kingdom_levels.config(text=translator.t("kingdom_levels"))
            if hasattr(self, 'btn_kingdom_power'):
                self.btn_kingdom_power.config(text=translator.t("kingdom_power"))
            if hasattr(self, 'btn_troop_search'):
                self.btn_troop_search.config(text=translator.t("troop_search"))
            if hasattr(self, 'btn_pet_search'):
                self.btn_pet_search.config(text=translator.t("pet_search"))
            if hasattr(self, 'btn_guild_war'):
                self.btn_guild_war.config(text=translator.t("guild_war"))
            
            # Обновляем колонки таблицы
            self.update_columns()
            if hasattr(self, 'tree'):
                self.setup_columns()
        except Exception as e:
            print(f"Ошибка обновления интерфейса: {e}")
        
    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Верхняя панель с переключателем языка
        top_bar = tk.Frame(main_frame)
        top_bar.pack(fill="x", padx=10, pady=5)
        
        # Переключатель языка справа
        lang_frame = tk.Frame(top_bar)
        lang_frame.pack(side="right")
        ttk.Label(lang_frame, text=translator.t("language") + ":").pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value=translator.current_language)
        lang_menu = ttk.OptionMenu(lang_frame, self.lang_var, 
                                  translator.current_language,
                                  "ru", "en",
                                  command=self.change_language)
        lang_menu.pack(side="left")

        self.label_userid = ttk.Label(main_frame, text=translator.t("enter_userid"))
        self.label_userid.pack(anchor="w", padx=10, pady=(10,0))
        self.text_userids = tk.Text(main_frame, height=10)
        self.text_userids.pack(fill="x", padx=10)

        # Главный фрейм для кнопок
        main_buttons_frame = tk.Frame(main_frame)
        main_buttons_frame.pack(pady=10, fill="x", padx=10)

        # Утопленный фрейм для кнопок
        sunken_frame = tk.Frame(main_buttons_frame, relief="sunken", bd=1)
        sunken_frame.pack(side="left", padx=(0, 10), pady=5)

        # Левый столбик кнопок внутри утопленного фрейма
        left_column = tk.Frame(sunken_frame)
        left_column.pack(side="left", fill="y", padx=(5, 10), pady=5)

        self.btn_load_userid = ttk.Button(left_column, text=translator.t("load_userid"), 
                command=self.load_userids_from_file, width=18)
        self.btn_load_userid.pack(pady=2)
        self.btn_get_userid = ttk.Button(left_column, text=translator.t("get_userid"), 
                command=self.open_guild_members_window, width=18)
        self.btn_get_userid.pack(pady=2)

        # Кнопка "Начать" справа от столбика, на этом же уровне
        self.btn_start = ttk.Button(sunken_frame, text=translator.t("start"), 
                                    command=self.start_fetch, width=12, state="disabled")
        self.btn_start.pack(side="left", padx=(10, 5), pady=5)

        # Утопленный фрейм для кнопок "Показать доп. имя" и "Показать гильдию"
        sunken_toggle_frame = tk.Frame(main_buttons_frame, relief="sunken", bd=1)
        sunken_toggle_frame.pack(side="left", padx=(20, 10), pady=5)

        # Кнопки в столбик внутри утопленного фрейма
        self.btn_toggle_dophenek = ttk.Button(sunken_toggle_frame, 
                                            text=translator.t("show_dophenek"), 
                                            command=self.toggle_dophenek_column, state="disabled", width=18)
        self.btn_toggle_dophenek.pack(pady=2)

        self.btn_toggle_guild = ttk.Button(sunken_toggle_frame, 
                                        text=translator.t("show_guild"), 
                                        command=self.toggle_guild_column, state="disabled", width=18)
        self.btn_toggle_guild.pack(pady=2)

        # Правый блок всех кнопок
        right_columns = tk.Frame(main_buttons_frame)
        right_columns.pack(side="left", fill="y")

        # ===== Правый блок всех кнопок в утопленной рамке =====
        sunken_right_frame = tk.Frame(main_buttons_frame, relief="sunken", bd=1)
        sunken_right_frame.pack(side="left", padx=5, pady=5)

        # Внутренний frame для отступа внутри рамки
        inner_right = tk.Frame(sunken_right_frame)
        inner_right.pack(padx=5, pady=5)

        # 2) Кнопка "Окно статов" в отдельном фрейме, выровнена по вертикали
        col_stats = tk.Frame(inner_right)
        col_stats.pack(side="left", padx=5, fill="y")

        self.btn_show_stats = ttk.Button(col_stats, text=translator.t("stats_window"), 
                                        command=self.open_stats_window, state="disabled", width=18)
        self.btn_show_stats.pack(expand=True)

        # 3) Столбик — уровни королевств / мощь королевств
        col_kingdoms = tk.Frame(inner_right)
        col_kingdoms.pack(side="left", padx=5, fill="y")

        self.btn_kingdom_levels = ttk.Button(col_kingdoms, text=translator.t("kingdom_levels"), 
                                            command=self.open_kingdom_levels_window, state="disabled", width=18)
        self.btn_kingdom_levels.pack(pady=2)

        self.btn_kingdom_power = ttk.Button(col_kingdoms, text=translator.t("kingdom_power"), 
                                            command=self.open_kingdom_power_window, state="disabled", width=18)
        self.btn_kingdom_power.pack(pady=2)

        # 7) Столбик - Поиск
        col_search = tk.Frame(inner_right)
        col_search.pack(side="left", fill="y", padx=5)

        self.btn_troop_search = ttk.Button(col_search, text=translator.t("troop_search"), 
                                        command=self.run_troop_search, state="disabled", width=18)
        self.btn_troop_search.pack(pady=2)

        self.btn_pet_search = ttk.Button(col_search, text=translator.t("pet_search"),
                                        command=self.run_pet_search, state="normal" if self.results else "disabled", width=18)
        self.btn_pet_search.pack(pady=2)

        # 8) Кнопка "Война гильдий" по центру
        self.btn_guild_war = tk.Button(
            main_buttons_frame,
            text=translator.t("guild_war"),
            command=self.open_guild_war_window,
            state="normal",
            width=18,
            bg="lightcoral",
            font=("Arial", 10, "bold")
        )
        self.btn_guild_war.pack(side="left", padx=(50, 25))

        # Таблица и остальной код без изменений...
        tree_container = tk.Frame(main_frame)
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        xscrollbar = ttk.Scrollbar(tree_container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar = ttk.Scrollbar(tree_container)
        yscrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_container, columns=self.columns, show="headings",
                            xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.tree.pack(fill="both", expand=True)
        
        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)
        
        self.tree.bind("<Button-1>", self.on_click)
        
        self.setup_columns()

        # Нижняя панель для дополнительных кнопок
        frame_bottom = ttk.Frame(main_frame)
        frame_bottom.pack(pady=5)
        self.btn_undo = ttk.Button(frame_bottom, text="Отменить последнее удаление", 
                                command=self.undo_last_delete, state="disabled")
        self.btn_undo.pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="Сохранить список UserID", 
                command=self.save_current_userid_list).pack(side="left", padx=5)
        ttk.Button(frame_bottom, text="Сохранить как .csv", 
                command=self.save_table_columns_dialog).pack(side="left", padx=5)
        
        # Привязываем событие изменения текста для активации кнопки "Начать"
        self.text_userids.bind("<KeyRelease>", self.check_start_button_state)
        
        # Изначально проверяем состояние
        self.check_start_button_state()

    def check_start_button_state(self, event=None):
        """Проверяет, можно ли активировать кнопку Начать"""
        text = self.text_userids.get("1.0", "end").strip()
        has_userids = any(line.strip() for line in text.splitlines() if line.strip())
        
        if has_userids:
            self.btn_start.config(state="normal")
        else:
            self.btn_start.config(state="disabled")
    
    def run_pet_search(self):
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        # TODO: Заменить на реальный импорт
        messagebox.showinfo("Информация", "Окно поиска питомцев будет добавлено позже")

    def open_guild_members_window(self):
        """Открывает окно для получения ID гильдии"""
        GuildMembersWindow(self)

    def open_stats_window(self):
        """Открывает окно статистики"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        # TODO: Заменить на реальный импорт
        messagebox.showinfo("Информация", "Окно статистики будет добавлено позже")

    def open_kingdom_levels_window(self):
        """Открывает окно уровней королевств"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        from app.windows.kingdom_levels import KingdomLevelsWindow
        KingdomLevelsWindow(self, self.results, list(self.results.keys()), 
                          self.show_dophenek, self.show_guild)

    def open_kingdom_power_window(self):
        """Открывает окно мощи королевств"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        # TODO: Заменить на реальный импорт
        messagebox.showinfo("Информация", "Окно мощи королевств будет добавлено позже")

    def run_troop_search(self):
        """Запускает окно поиска войск"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        # TODO: Заменить на реальный импорт
        messagebox.showinfo("Информация", "Окно поиска войск будет добавлено позже")

    def open_guild_war_window(self):
        """Открывает окно войны гильдий"""
        # TODO: Заменить на реальный импорт
        messagebox.showinfo("Информация", "Окно войны гильдий будет добавлено позже")

    def setup_columns(self):
        self.dophenek_col = ["Доп. Имя"] if self.show_dophenek else []
        self.guild_col = ["Гильдия"] if self.show_guild else []
        self.delete_col = ["Удалить"]
        self.columns = self.base_columns + self.dophenek_col + self.guild_col + self.delete_col

        self.tree["columns"] = self.columns
        
        for col in self.columns:
            if col != "#" and col != "Удалить":
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
            else:
                self.tree.heading(col, text=col)
            
        for col in self.columns:
            if col == "#":
                self.tree.column(col, width=40, minwidth=40, anchor="center", stretch=False)
            elif col == "Удалить":
                self.tree.column(col, width=70, minwidth=70, anchor="center", stretch=False)  # Уменьшили ширину
            elif col == "Доп. Имя":
                self.tree.column(col, width=150, minwidth=100, anchor="center")
            elif col == "Гильдия":
                self.tree.column(col, width=150, minwidth=100, anchor="center")
            else:
                self.tree.column(col, width=120, minwidth=80, anchor="center")

    def sort_by_column(self, col, reverse):
        if col == "#" or col == "Удалить":
            return

        data = []
        for k in self.tree.get_children():
            values = self.tree.item(k)['values']
            col_index = self.columns.index(col)
            v = values[col_index]
            data.append((v.lower() if isinstance(v, str) else v, values, k))

        data.sort(reverse=reverse, key=lambda x: x[0])
        
        for index, (_, values, k) in enumerate(data, start=1):
            new_values = [index] + values[1:]  # Обновляем нумерацию
            self.tree.item(k, values=new_values)
            self.tree.move(k, '', index)

    def on_click(self, event):
        """Обработчик клика по таблице"""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        col = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        
        if not row_id:
            return

        col_index = int(col.replace("#", "")) - 1
        
        # Проверяем, что кликнули на колонку "Удалить" (последняя колонка)
        if col_index == len(self.tree["columns"]) - 1:
            if messagebox.askyesno("Подтверждение", "Удалить эту строку?"):
                self.deleted_stack.append((row_id, self.results.get(row_id), self.tree.item(row_id)["values"]))
                
                if row_id in self.results:
                    del self.results[row_id]
                self.tree.delete(row_id)
                
                # Обновляем номера строк
                for idx, child in enumerate(self.tree.get_children(), start=1):
                    values = list(self.tree.item(child)["values"])
                    values[0] = idx
                    self.tree.item(child, values=values)
                
                self.btn_undo.config(state="normal" if self.deleted_stack else "disabled")

    def update_row_numbers(self):
        """Обновляет номера строк в таблице"""
        for index, iid in enumerate(self.tree.get_children(), start=1):
            vals = list(self.tree.item(iid)["values"])
            vals[0] = index
            self.tree.item(iid, values=vals)

    def start_fetch(self):
        """Начинает загрузку профилей"""
        user_ids = [uid.strip() for uid in self.text_userids.get("1.0", "end").splitlines() if uid.strip()]
        if not user_ids:
            messagebox.showwarning("Ошибка", "Введите хотя бы один UserID")
            return

        self.results.clear()
        self.tree.delete(*self.tree.get_children())
        self.deleted_stack.clear()
        self.btn_undo.config(state="disabled")

        # Сбросить кнопки перед загрузкой
        self.btn_toggle_dophenek.config(state="disabled")
        self.btn_toggle_guild.config(state="disabled")
        self.btn_show_stats.config(state="disabled")
        self.btn_kingdom_power.config(state="disabled")
        self.btn_kingdom_levels.config(state="disabled")
        self.btn_troop_search.config(state="disabled")
        self.btn_pet_search.config(state="disabled")
        self.btn_guild_war.config(state="disabled")

        threading.Thread(target=self.fetch_profiles, args=(user_ids,), daemon=True).start()

    def fetch_profiles(self, user_ids):
        """Загружает профили пользователей"""
        for user_id in user_ids:
            if not self._running:
                break
            try:
                response = requests.post(URL, json={"functionName": "get_hero_profile", "Id": user_id}, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.results[user_id] = data
                self.after(0, lambda uid=user_id, d=data: self.update_tree_row(uid, d))
            except Exception as e:
                print(f"Ошибка для {user_id}: {e}")
                # Можно добавить запись ошибки в интерфейс

        self.after(0, lambda: [
            self.btn_toggle_dophenek.config(state="normal"),
            self.btn_toggle_guild.config(state="normal"),
            self.btn_show_stats.config(state="normal"),
            self.btn_kingdom_power.config(state="normal"),
            self.btn_kingdom_levels.config(state="normal"),
            self.btn_troop_search.config(state="normal"),
            self.btn_pet_search.config(state="normal"),
            self.btn_guild_war.config(state="normal"),
            messagebox.showinfo("Успех", "Данные загружены")
        ])

    def update_tree_row(self, user_id, data):
        """Обновляет строку в таблице"""
        profile = data.get("result", {}).get("ProfileData", {})
        row_num = len(self.tree.get_children()) + 1
        
        values = [
            row_num,
            user_id,
            profile.get("NameCode", ""),
            profile.get("Name", "")
        ]
        
        if self.show_dophenek:
            values.append(DOPHENEK_MAP.get(user_id, ""))
        if self.show_guild:
            values.append(profile.get("GuildName", ""))
            
        values.append("❌")  # Вместо "Удалить" ставим "❌"
        
        self.tree.insert("", "end", iid=user_id, values=values)

    def toggle_dophenek_column(self):
        """Переключает отображение колонки доп. имени"""
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )
        
        # Перестраиваем таблицу с новыми колонками
        self.update_columns()
        self.setup_columns()
        
        # Обновляем данные в таблице
        self.update_table_data()

    def toggle_guild_column(self):
        """Переключает отображение колонки гильдии"""
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        
        # Перестраиваем таблицу с новыми колонками
        self.update_columns()
        self.setup_columns()
        
        # Обновляем данные в таблице
        self.update_table_data()

    def update_table_data(self):
        """Обновляет данные в таблице"""
        for user_id in self.tree.get_children():
            data = self.results.get(user_id)
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            row_num = self.tree.item(user_id)["values"][0]
            
            values = [
                row_num,
                user_id,
                profile.get("NameCode", ""),
                profile.get("Name", "")
            ]
            
            if self.show_dophenek:
                values.append(DOPHENEK_MAP.get(user_id, ""))
            if self.show_guild:
                values.append(profile.get("GuildName", ""))

            values.append("❌")
            
            self.tree.item(user_id, values=values)

    def load_userids_from_file(self):
        """Загружает UserID из файла"""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            self.text_userids.delete("1.0", "end")
            self.text_userids.insert("1.0", content)
            
            # Проверяем состояние кнопки
            self.check_start_button_state()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

    def undo_last_delete(self):
        """Отменяет последнее удаление"""
        if not self.deleted_stack:
            return
            
        user_id, data, values = self.deleted_stack.pop()
        self.results[user_id] = data
        
        # Восстанавливаем строку с правильным номером
        row_num = len(self.tree.get_children()) + 1
        values = [row_num] + values[1:]
        self.tree.insert("", "end", iid=user_id, values=values)
        
        # Обновляем все номера строк
        self.update_row_numbers()
        
        # Обновляем состояние кнопки отмены
        self.btn_undo.config(state="normal" if self.deleted_stack else "disabled")

    def save_current_userid_list(self):
        """Сохраняет текущий список UserID"""
        user_ids = [self.tree.item(child)["values"][1] for child in self.tree.get_children()]
        
        if not user_ids:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(user_ids))
                
            messagebox.showinfo("Успех", f"Список сохранён в {file_path}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def save_table_columns_dialog(self):
        """Диалог сохранения таблицы в CSV"""
        columns_to_select = [col for col in self.columns if col != "Удалить"]
        
        dialog = tk.Toplevel(self)
        dialog.title("Выберите столбцы для экспорта")
        dialog.geometry("300x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        selected_vars = {}
        
        # Чекбоксы для выбора колонок
        for col in columns_to_select:
            var = tk.BooleanVar(value=True)
            selected_vars[col] = var
            
            cb = tk.Checkbutton(dialog, text=col, variable=var, anchor="w")
            cb.pack(fill="x", padx=10, pady=2)
        
        def on_ok():
            selected = [col for col, var in selected_vars.items() if var.get()]
            if selected:
                dialog.selected_columns = selected
                dialog.destroy()
                self.save_table_as_csv(selected)
        
        def on_cancel():
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отмена", width=10, command=on_cancel).pack(side="left", padx=5)

    def save_table_as_csv(self, selected_columns):
        """Сохраняет таблицу в CSV файл"""
        if not selected_columns:
            messagebox.showwarning("Предупреждение", "Не выбраны колонки для экспорта")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Заголовки
                writer.writerow(selected_columns)
                
                # Данные
                for item in self.tree.get_children():
                    values = self.tree.item(item)["values"]
                    row_dict = dict(zip(self.columns, values))
                    
                    # Собираем строку только из выбранных колонок
                    row = [row_dict[col] for col in selected_columns]
                    writer.writerow(row)
                    
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")