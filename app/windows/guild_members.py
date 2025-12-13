# app/windows/guild_members.py
"""GuildMembers window - получение списка участников гильдии"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import threading
import csv

from app.windows.base import BaseWindow
from app.config import URL, DOPHENEK_MAP
from app.translation import translator

class GuildMembersWindow(BaseWindow):  # ИЗМЕНИЛ: было tk.Toplevel, стало BaseWindow
    def __init__(self, parent):
        super().__init__(parent)  # ИЗМЕНИЛ: было tk.Toplevel(parent)
        self.title("Получить список ID гильдии")
        self.geometry("900x800")
        self.parent = parent
        
        # Данные пользователя после авторизации
        self.username_from_profile = None
        self.user_data = None
        self._running = True
        
        self.setup_ui()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Обработчик закрытия окна"""
        self._running = False
        self.destroy()

    def setup_ui(self):
        """Настройка интерфейса окна получения ID гильдии"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Получение списка ID участников гильдии", 
            font=("Arial", 14, "bold"),
            fg="white",
            bg="navy"
        )
        title_label.pack(pady=10, fill="x")
        
        # Основной фрейм для ввода и информации
        main_input_frame = tk.Frame(main_frame)
        main_input_frame.pack(pady=10, fill="x")

        # ======= ЛЕВАЯ ПАНЕЛЬ - ПОЛЯ ВВОДА И КНОПКИ =======
        left_frame = tk.Frame(main_input_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 20))

        # ----------------- UserID -----------------
        userid_label = tk.Label(left_frame, text="UserID:", font=("Arial", 10))
        userid_label.grid(row=0, column=0, padx=(0,10), pady=5, sticky="e")

        self.user_id_entry = tk.Entry(left_frame, width=20, font=("Arial", 10))
        self.user_id_entry.grid(row=0, column=1, padx=(0,5), pady=5, sticky="w")

        self.get_username_btn = tk.Button(
            left_frame,
            text="Получить Username",
            width=18,
            command=self.get_username_from_userid,
            bg="lightblue",
            font=("Arial", 9)
        )
        self.get_username_btn.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # ----------------- Password -----------------
        password_label = tk.Label(left_frame, text="Password:", font=("Arial", 10))
        password_label.grid(row=1, column=0, padx=(0,10), pady=5, sticky="e")

        self.password_entry = tk.Entry(left_frame, width=20, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, padx=(0,5), pady=5, sticky="w")

        self.auth_btn = tk.Button(
            left_frame,
            text="Авторизироваться",
            width=18,
            command=self.authenticate,
            bg="lightgreen",
            font=("Arial", 9),
            state="disabled"
        )
        self.auth_btn.grid(row=1, column=2, padx=5, pady=5, sticky="e")
                
        # ======= ПРАВАЯ ПАНЕЛЬ - ИНФОРМАЦИЯ ОБ АККАУНТЕ =======
        right_frame = tk.Frame(main_input_frame)
        right_frame.pack(side="right", fill="y")

        # Информация об аккаунте в компактном виде с рамкой
        self.info_frame = tk.Frame(right_frame, relief="sunken", bd=1)
        self.info_frame.pack(padx=10, pady=5, fill="both")

        # Внутренний Frame для отступов
        inner_info = tk.Frame(self.info_frame)
        inner_info.pack(padx=10, pady=10)

        # Метки с информацией
        self.username_label = tk.Label(inner_info,
                                    text="Username: не получен",
                                    font=("Arial", 9),
                                    fg="red",
                                    justify="left")
        self.username_label.pack(anchor="w")

        self.player_label = tk.Label(inner_info,
                                    text="Игрок: -",
                                    font=("Arial", 9),
                                    fg="red",
                                    justify="left")
        self.player_label.pack(anchor="w")

        self.guild_label = tk.Label(inner_info,
                                    text="Гильдия: -",
                                    font=("Arial", 9),
                                    fg="red",
                                    justify="left")
        self.guild_label.pack(anchor="w")

        self.auth_status_label = tk.Label(inner_info,
                                        text="Статус: Не авторизован",
                                        font=("Arial", 9, "bold"),
                                        fg="red",
                                        justify="left")
        self.auth_status_label.pack(anchor="w")
        # ======= КОНЕЦ ПРАВОЙ ПАНЕЛИ =======
        
        # Центральный фрейм для кнопки загрузки и фильтра
        center_frame = tk.Frame(main_frame)
        center_frame.pack(pady=0, fill="x")

        # Кнопка загрузки данных участников
        self.get_guild_id_btn = tk.Button(
            center_frame,
            text="Загрузить участников гильдии",
            width=25,
            command=self.get_guild_id,
            bg="orange",
            font=("Arial", 10),
            state="disabled"
        )
        self.get_guild_id_btn.pack(side="left", padx=5, pady=10)

        # Кнопка фильтрации по основной гильдии
        self.filter_main_guild_btn = tk.Button(
            center_frame,
            text="Оставить только основную гильдию",
            width=30,
            command=self.filter_by_main_guild,
            bg="lightyellow",
            font=("Arial", 10),
            state="disabled"
        )
        self.filter_main_guild_btn.pack(side="left", padx=5, pady=10)
        
        # Область для таблицы с участниками
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Создаем Treeview с прокруткой
        self.setup_treeview(table_frame)
        
        # Фрейм для кнопок действий
        action_frame = tk.Frame(main_frame)
        action_frame.pack(pady=(2, 5), fill='x')
        
        # Контейнер для кнопок
        button_container = tk.Frame(action_frame)
        button_container.pack(expand=True)
        
        # Кнопки в одну строку, но с центрированием
        self.transfer_btn = tk.Button(
            button_container,
            text="Перенести в основное окно",
            width=25,
            command=self.transfer_to_main_window,
            bg="lightblue",
            font=("Arial", 9),
            state="disabled"
        )
        self.transfer_btn.grid(row=0, column=0, padx=5, pady=2)
        
        self.save_btn = tk.Button(
            button_container,
            text="Сохранить список UserID",
            width=25,
            command=self.save_userid_list,
            bg="lightgreen",
            font=("Arial", 9),
            state="disabled"
        )
        self.save_btn.grid(row=0, column=1, padx=5, pady=2)
        
        self.export_btn = tk.Button(
            button_container,
            text="Экспорт в CSV",
            width=15,
            command=self.export_to_csv,
            bg="lightyellow",
            font=("Arial", 9),
            state="disabled"
        )
        self.export_btn.grid(row=0, column=2, padx=5, pady=2)
        
        # Центрируем колонки
        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1) 
        button_container.grid_columnconfigure(2, weight=1)
        
        # Статус бар
        self.status_label = tk.Label(
            main_frame,
            text="Введите UserID для получения username",
            font=("Arial", 9),
            fg="gray"
        )
        self.status_label.pack(pady=5)

    def setup_treeview(self, parent_frame):
        """Настройка Treeview для отображения участников"""
        # Фрейм для Treeview и скроллбаров
        tree_container = tk.Frame(parent_frame)
        tree_container.pack(fill="both", expand=True)
        
        # Создаем Treeview
        self.tree = ttk.Treeview(tree_container, columns=("#", "Игрок", "Гильдия", "InviteCode", "UserID", "Удалить"), show="headings")
        
        # Настраиваем колонки С СОРТИРОВКОЙ
        columns_config = {
            "#": {"width": 40, "anchor": "center", "stretch": False},
            "Игрок": {"width": 200, "anchor": "center"},
            "Гильдия": {"width": 150, "anchor": "center"},
            "InviteCode": {"width": 150, "anchor": "center"},
            "UserID": {"width": 150, "anchor": "center"},
            "Удалить": {"width": 80, "anchor": "center", "stretch": False}
        }
        
        for col, config in columns_config.items():
            if col == "#" or col == "Удалить":
                self.tree.heading(col, text=col)  # Без сортировки
            else:
                # Добавляем команду сортировки для остальных колонок
                self.tree.heading(col, text=col, 
                                command=lambda c=col: self.sort_treeview(c, False))
            self.tree.column(col, **config)
        
        # Добавляем скроллбары
        y_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Размещаем элементы
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настройка весов для растягивания
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Привязываем обработчики
        self.tree.bind("<Button-1>", self.on_tree_click)

    def sort_treeview(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#" or col == "Удалить":
            return

        # Получаем все элементы
        items = []
        for k in self.tree.get_children(''):
            value = self.tree.set(k, col)
            items.append((value, k))

        # Специальная обработка для разных типов данных
        if col == "UserID":
            # Числовая сортировка для ID
            items.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        elif col == "Гильдия":
            # Особый порядок для гильдий
            guild_order = {"Загрузка...": 0, "Без гильдии": 1, "Ошибка загрузки": 2}
            items.sort(key=lambda t: (guild_order.get(t[0], 3), t[0].lower()), reverse=reverse)
        else:
            # Текстовая сортировка для остальных колонок
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        
        # Перемещаем элементы
        for index, (_, k) in enumerate(items, start=1):
            self.tree.move(k, '', index)
        
        # Обновляем нумерацию
        for idx, item in enumerate(self.tree.get_children(), start=1):
            values = list(self.tree.item(item)["values"])
            values[0] = str(idx)
            self.tree.item(item, values=values)
        
        # Обновляем заголовки с указанием направления сортировки
        for column in self.tree["columns"]:
            if column == "#" or column == "Удалить":
                continue
                
            heading_text = self.tree.heading(column)["text"]
            # Убираем предыдущие стрелки
            clean_text = heading_text.split(" ↓")[0].split(" ↑")[0]
            
            if column == col:
                # Добавляем стрелку для текущей колонки
                new_text = clean_text + (" ↓" if reverse else " ↑")
            else:
                new_text = clean_text
                
            self.tree.heading(column, text=new_text,
                            command=lambda c=column: self.sort_treeview(c, not reverse))

    def get_username_from_userid(self):
        """Получает username по UserID"""
        user_id = self.user_id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Ошибка", "Введите UserID")
            return
        
        self.status_label.config(text="Получение username...", fg="blue")
        self.update()
        
        try:
            payload = {"functionName": "get_hero_profile", "Id": user_id}
            response = requests.post(URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "result" not in data or "ProfileData" not in data["result"]:
                raise ValueError("Некорректный ответ сервера")

            profile = data["result"]["ProfileData"]
            username = profile.get("username", "")
            guild_name = profile.get("GuildName", "Без гильдии")
            player_name = profile.get("Name", "Неизвестно")
        
            # Создаём кэш, если ещё не создан
            if not hasattr(self, "profiles_cache"):
                self.profiles_cache = {}

            # Сохраняем профиль для UserId
            self.profiles_cache[user_id] = profile

            if not username:
                raise ValueError("Username не найден в ответе")

            self.username_from_profile = username
            
            # Обновляем UI
            self.username_label.config(text=f"Username: {username}", fg="green")
            self.player_label.config(text=f"Игрок: {player_name}", fg="blue")
            self.guild_label.config(text=f"Гильдия: {guild_name}", fg="blue")
            self.auth_btn.config(state="normal")
            
            self.status_label.config(text="Username получен! Введите пароль для авторизации", fg="green")

        except Exception as e:
            self.status_label.config(text=f"Ошибка получения username: {str(e)}", fg="red")
            messagebox.showerror("Ошибка", f"Не удалось получить username:\n{str(e)}")

    def authenticate(self):
        """Проверяет авторизацию"""
        if not hasattr(self, 'username_from_profile') or not self.username_from_profile:
            messagebox.showwarning("Ошибка", "Сначала получите username")
            return
        
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showwarning("Ошибка", "Введите пароль")
            return
        
        self.status_label.config(text="Авторизация...", fg="blue")
        self.update()

        try:
            auth_payload = {
                "functionName": "get_guild_activity",
                "username": self.username_from_profile,
                "password": password
            }

            response = requests.post(URL, json=auth_payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "result" not in data:
                raise ValueError("Некорректный ответ сервера")
            if "error" in data:
                raise ValueError(f"Ошибка авторизации: {data.get('error', 'Неизвестная ошибка')}")

            if "GuildActivityLog" in data["result"]:
                # Получаем дополнительную информацию о профиле
                profile_payload = {
                    "functionName": "get_hero_profile",
                    "username": self.username_from_profile,
                    "password": password,
                    "Id": self.user_id_entry.get().strip()
                }
                
                profile_response = requests.post(URL, json=profile_payload, timeout=10)
                profile_response.raise_for_status()
                profile_data = profile_response.json()
                
                if "result" in profile_data and "ProfileData" in profile_data["result"]:
                    profile = profile_data["result"]["ProfileData"]
                    player_name = profile.get("Name", "Неизвестно")
                    guild_name = profile.get("GuildName", "Без гильдии")
                    
                    self.user_data = {
                        "username": self.username_from_profile,
                        "password": password,
                        "player_name": player_name,
                        "guild_name": guild_name
                    }
                    
                    # Обновляем UI
                    self.auth_status_label.config(text="Статус: Авторизован ✅", fg="green")
                    self.guild_label.config(text=f"Гильдия: {guild_name}", fg="blue")
                    self.get_guild_id_btn.config(state="normal")
                    
                    # Блокируем поля ввода
                    self.user_id_entry.config(state="disabled")
                    self.password_entry.config(state="disabled")
                    self.get_username_btn.config(state="disabled")
                    self.auth_btn.config(state="disabled")
                    
                    self.status_label.config(text="Авторизация успешна!", fg="green")
                else:
                    raise ValueError("Не удалось получить данные профиля")
            else:
                raise ValueError("Некорректный ответ сервера")

        except Exception as e:
            self.status_label.config(text=f"Ошибка авторизации: {str(e)}", fg="red")
            self.auth_status_label.config(text="Статус: Ошибка ❌", fg="red")
            messagebox.showerror("Ошибка", f"Не удалось авторизоваться:\n{str(e)}")

    def get_guild_id(self):
        """Получает данные участников гильдии"""
        if not self.user_data:
            messagebox.showwarning("Ошибка", "Сначала авторизуйтесь")
            return

        username = self.user_data["username"]
        password = self.user_data["password"]

        self.status_label.config(text="Получение данных участников...", fg="blue")
        self.update()

        try:
            payload = {"functionName": "get_guild_activity", "username": username, "password": password}
            response = requests.post(URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # СОХРАНЯЕМ ОТВЕТ ДЛЯ ПОЛУЧЕНИЯ ID ГИЛЬДИИ
            self.last_guild_response = data

            if "result" not in data or "GuildActivityLog" not in data["result"]:
                raise ValueError("Некорректный ответ сервера")

            guild_members = data["result"]["GuildActivityLog"]
            guild_id = data["result"].get("GuildId", "Неизвестно")
            
            # Отображаем участников
            self.display_members(guild_members)

            # Активируем кнопки действий
            self.transfer_btn.config(state="normal")
            self.save_btn.config(state="normal")
            self.export_btn.config(state="normal")
            self.filter_main_guild_btn.config(state="normal")

        except Exception as e:
            self.status_label.config(text=f"Ошибка получения данных: {str(e)}", fg="red")
            messagebox.showerror("Ошибка", f"Не удалось получить данные участников:\n{str(e)}")

    def display_members(self, guild_members):
        """Отображает участников в таблице"""
        self.tree.delete(*self.tree.get_children())
        
        members = {}
        for entry in guild_members:
            if "UserId" in entry and "Data" in entry and len(entry["Data"]) > 0:
                user_id = entry["UserId"]
                if user_id not in members:
                    name = entry["Data"][0]
                    members[user_id] = {
                        "name": name,
                        "guild": "Загрузка...",  # Временное значение
                        "invite_code": entry.get("NameCode", "")
                    }

        # ОБНОВЛЯЕМ СТАТУС СРАЗУ
        member_count = len(members)
        guild_id = "Неизвестно"
        
        # Если есть доступ к ID гильдии из response данных, используем его
        if hasattr(self, 'last_guild_response'):
            guild_id = self.last_guild_response.get("result", {}).get("GuildId", "Неизвестно")
        
        self.status_label.config(
            text=f"Загружено участников: {member_count} | ID гильдии: {guild_id}", 
            fg="green"
        )

        for idx, (user_id, data) in enumerate(members.items(), start=1):
            self.tree.insert("", "end", values=(
                idx,
                data["name"],
                data["guild"],
                data["invite_code"],
                user_id,
                "❌"
            ))
        
        # Запускаем асинхронную загрузку гильдий
        self.load_guilds_for_members(members)

    def load_guilds_for_members(self, members):
        """Асинхронно загружает данные гильдий для всех участников"""
        def fetch_guild_data():
            for user_id in members.keys():
                if not self._running:
                    break
                    
                try:
                    # Делаем запрос для каждого участника
                    payload = {"functionName": "get_hero_profile", "Id": user_id}
                    response = requests.post(URL, json=payload, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    if "result" in data and "ProfileData" in data["result"]:
                        profile = data["result"]["ProfileData"]
                        guild_name = profile.get("GuildName", "Без гильдии")
                        
                        # Обновляем значение в основном потоке
                        self.after(0, lambda uid=user_id, gn=guild_name: 
                                self.update_member_guild(uid, gn))
                    
                except Exception as e:
                    print(f"Ошибка загрузки гильдии для {user_id}: {e}")
                    self.after(0, lambda uid=user_id: 
                            self.update_member_guild(uid, "Ошибка загрузки"))
        
        # Запускаем в отдельном потоке
        threading.Thread(target=fetch_guild_data, daemon=True).start()

    def update_member_guild(self, user_id, guild_name):
        """Обновляет название гильдии для конкретного участника"""
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][4] == user_id:
                values = list(self.tree.item(item)["values"])
                values[2] = guild_name
                self.tree.item(item, values=values)
                break
     
    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        col = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        
        if not row_id:
            return

        col_index = int(col.replace("#", "")) - 1
        
        if col_index == 5:  # Колонка "Удалить"
            if messagebox.askyesno("Подтверждение", "Удалить эту строку?"):
                self.tree.delete(row_id)
                self.renumber_rows()
    
    def renumber_rows(self):
        for index, item in enumerate(self.tree.get_children(), start=1):
            values = list(self.tree.item(item, "values"))
            values[0] = index
            self.tree.item(item, values=values)
    
    def sort_by_column(self, col, reverse):
        if col == "#" or col == "Удалить":
            return

        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)["values"]
            col_idx = self.tree["columns"].index(col)
            data.append((values[col_idx], child))
        
        data.sort(reverse=reverse, key=lambda x: x[0])
        
        # Обновляем заголовки
        for c in self.tree["columns"]:
            heading = self.tree.heading(c)
            if c == col:
                heading["text"] = f"{c} {'↓' if reverse else '↑'}"
            else:
                heading["text"] = c
                
        # Перемещаем строки
        for index, (_, child) in enumerate(data, start=1):
            self.tree.move(child, "", index)
        
        # Перенумеровываем строки
        self.renumber_rows()
        
        self.tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))
            
    def transfer_to_main_window(self):
        # Берем UserID из 4-й колонки (индекс 4)
        user_ids = [self.tree.item(child)["values"][4] for child in self.tree.get_children()]
        if not user_ids:
            messagebox.showwarning("Предупреждение", "Нет данных для переноса")
            return
            
        self.parent.text_userids.delete("1.0", "end")
        self.parent.text_userids.insert("1.0", "\n".join(user_ids))
        # Вызываем проверку состояния кнопки после переноса
        self.parent.check_start_button_state()
        self.status_label.config(text="ID перенесены в основное окно", fg="green")
        
    def save_userid_list(self):
        # UserID находится в 5-й колонке (индекс 4) — сохраняем именно его
        user_ids = [self.tree.item(child)["values"][4] for child in self.tree.get_children()]
        if not user_ids:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(user_ids))
            messagebox.showinfo("Успех", f"Список сохранён в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def filter_by_main_guild(self):
        """
        Оставляет в таблице только участников одной гильдии
        """
        items = list(self.tree.get_children())
        if not items:
            messagebox.showwarning("Предупреждение", "Нет данных для фильтрации")
            return

        # Собираем частоты гильдий (колонка 'Гильдия' — индекс 2)
        guild_counts = {}
        for item in items:
            values = self.tree.item(item)["values"]
            guild_name = values[2]
            guild_counts[guild_name] = guild_counts.get(guild_name, 0) + 1

        if not guild_counts:
            messagebox.showwarning("Предупреждение", "Не удалось определить гильдии для фильтрации")
            return

        # Находим гильдию с максимальным количеством вхождений
        main_guild = max(guild_counts.items(), key=lambda kv: kv[1])[0]

        # Спрашиваем подтверждение у пользователя
        if not messagebox.askyesno(
            "Фильтрация по гильдии",
            f"Оставить только членов гильдии \"{main_guild}\"?"
        ):
            return

        # Удаляем всех, кто не из основной гильдии
        for item in items:
            values = self.tree.item(item)["values"]
            if values[2] != main_guild:
                self.tree.delete(item)

        # Перенумеровываем строки
        self.renumber_rows()

        # Обновляем статус
        self.status_label.config(
            text=f"Оставлены только члены гильдии: {main_guild}",
            fg="green"
        )
    
    def export_to_csv(self):
        columns = [col for col in self.tree["columns"] if col not in ("#", "Удалить")]
        selected_columns = self.select_columns(columns)
        
        if not selected_columns:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                headers = ["#"] + selected_columns
                writer.writerow(headers)
                
                for child in self.tree.get_children():
                    values = self.tree.item(child)["values"]
                    row = [values[0]]  # Номер
                    for col in selected_columns:
                        col_idx = self.tree["columns"].index(col)
                        row.append(values[col_idx])
                    writer.writerow(row)
                    
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
            
    def select_columns(self, columns):
        dlg = tk.Toplevel(self)
        dlg.title("Выберите столбцы для экспорта")
        dlg.resizable(False, False)
        
        selected = {col: tk.BooleanVar(value=True) for col in columns}
        
        for idx, col in enumerate(columns):
            cb = tk.Checkbutton(dlg, text=col, variable=selected[col])
            cb.grid(row=idx, column=0, sticky="w", padx=10, pady=2)
            
        def on_ok():
            dlg.selected = [col for col, var in selected.items() if var.get()]
            dlg.destroy()
            
        btn_ok = tk.Button(dlg, text="OK", command=on_ok)
        btn_ok.grid(row=len(columns), column=0, pady=10)
        
        self.wait_window(dlg)
        return getattr(dlg, "selected", [])