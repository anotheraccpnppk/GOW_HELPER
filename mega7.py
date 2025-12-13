import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO

import hashlib
import tempfile

import re
from tkinter import font as tkfont
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import csv
import json
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# ========== СИСТЕМА ПЕРЕВОДОВ ==========
class TranslationManager:
    """Менеджер переводов для поддержки нескольких языков"""
    
    def __init__(self):
        self.current_language = "ru"  # По умолчанию русский
        self.translations = {
            "ru": {
                # Основные элементы интерфейса
                "app_title": "Запрос профилей по UserId",
                "enter_userid": "Введите UserId (каждый с новой строки):",
                "load_userid": "Загрузить UserID",
                "get_userid": "Получить UserID",
                "start": "Начать",
                "show_dophenek": "Показать доп. имя",
                "hide_dophenek": "Скрыть доп. имя",
                "show_guild": "Показать гильдию",
                "hide_guild": "Скрыть гильдию",
                "stats_window": "Окно статов",
                "kingdom_levels": "Уровни королевств",
                "kingdom_power": "Мощь королевств",
                "troop_search": "Поиск Войск",
                "pet_search": "Поиск Питомцев",
                "guild_war": "Война гильдий",
                
                # Колонки таблицы
                "column_number": "#",
                "column_player": "Игрок",
                "column_dophenek": "Доп. Имя",
                "column_guild": "Гильдия",
                "column_delete": "Удалить",
                
                # Сообщения
                "error": "Ошибка",
                "warning": "Предупреждение",
                "success": "Успех",
                "info": "Информация",
                "no_data": "Нет данных",
                "data_loaded": "Данные загружены",
                "enter_userid_error": "Введите хотя бы один UserID",
                "no_data_to_display": "Нет данных для отображения",
                
                # Поиск питомцев
                "pet_search_title": "Поиск питомцев у игроков",
                "search_pet": "Поиск питомца:",
                "add_pet": "Добавить питомца",
                "find_pets": "Найти питомцев",
                "clear_list": "Очистить список",
                "selected_pets": "Выбранные питомцы:",
                "save_csv": "Сохранить как CSV",
                "enter_pet_name": "Введите название питомца",
                "pet_not_found": "Питомец '{pet_name}' не найден.",
                "pet_already_in_list": "Питомец '{pet_name}' уже в списке.",
                "add_at_least_one_pet": "Добавьте хотя бы одного питомца.",
                "no_data_to_export": "Нет данных для экспорта.",
                "data_saved": "Данные сохранены в {file_path}",
                "export_error": "Не удалось экспортировать данные:\n{error}",
                
                # Гильдия
                "get_guild_members": "Получение списка ID участников гильдии",
                "userid_label": "UserID:",
                "get_username": "Получить Username",
                "password_label": "Password:",
                "authorize": "Авторизироваться",
                "username_not_received": "Username: не получен",
                "player": "Игрок: -",
                "guild": "Гильдия: -",
                "status_not_authorized": "Статус: Не авторизован",
                "load_guild_members": "Загрузить участников гильдии",
                "keep_main_guild_only": "Оставить только основную гильдию",
                "transfer_to_main": "Перенести в основное окно",
                "save_userid_list": "Сохранить список UserID",
                "export_csv": "Экспорт в CSV",
                "enter_userid_for_username": "Введите UserID для получения username",
                "getting_username": "Получение username...",
                "username_received": "Username получен! Введите пароль для авторизации",
                "username_error": "Ошибка получения username: {error}",
                "get_username_first": "Сначала получите username",
                "enter_password": "Введите пароль",
                "authorizing": "Авторизация...",
                "status_authorized": "Статус: Авторизован ✅",
                "authorization_success": "Авторизация успешна!",
                "authorization_error": "Ошибка авторизации: {error}",
                "status_error": "Статус: Ошибка ❌",
                "authorize_first": "Сначала авторизуйтесь",
                "getting_members_data": "Получение данных участников...",
                "members_data_error": "Ошибка получения данных: {error}",
                "members_loaded": "Загружено участников: {count} | ID гильдии: {guild_id}",
                "delete_row_confirm": "Удалить эту строку?",
                "no_data_to_transfer": "Нет данных для переноса",
                "ids_transferred": "ID перенесены в основное окно",
                "no_data_to_save": "Нет данных для сохранения",
                "list_saved": "Список сохранён в {file_path}",
                "save_file_error": "Не удалось сохранить файл: {error}",
                "no_data_to_filter": "Нет данных для фильтрации",
                "filter_guilds_error": "Не удалось определить гильдии для фильтрации",
                "only_main_guild": "Оставлены только члены гильдии: {guild}",
                
                # Язык
                "language": "Язык",
                "russian": "Русский",
                "english": "English",
            },
            "en": {
                # Main interface elements
                "app_title": "Profile Request by UserId",
                "enter_userid": "Enter UserId (one per line):",
                "load_userid": "Load UserID",
                "get_userid": "Get UserID",
                "start": "Start",
                "show_dophenek": "Show Alt Name",
                "hide_dophenek": "Hide Alt Name",
                "show_guild": "Show Guild",
                "hide_guild": "Hide Guild",
                "stats_window": "Stats Window",
                "kingdom_levels": "Kingdom Levels",
                "kingdom_power": "Kingdom Power",
                "troop_search": "Troop Search",
                "pet_search": "Pet Search",
                "guild_war": "Guild War",
                
                # Table columns
                "column_number": "#",
                "column_player": "Player",
                "column_dophenek": "Alt Name",
                "column_guild": "Guild",
                "column_delete": "Delete",
                
                # Messages
                "error": "Error",
                "warning": "Warning",
                "success": "Success",
                "info": "Information",
                "no_data": "No data",
                "data_loaded": "Data loaded",
                "enter_userid_error": "Enter at least one UserID",
                "no_data_to_display": "No data to display",
                
                # Pet search
                "pet_search_title": "Search Pets by Players",
                "search_pet": "Search pet:",
                "add_pet": "Add Pet",
                "find_pets": "Find Pets",
                "clear_list": "Clear List",
                "selected_pets": "Selected Pets:",
                "save_csv": "Save as CSV",
                "enter_pet_name": "Enter pet name",
                "pet_not_found": "Pet '{pet_name}' not found.",
                "pet_already_in_list": "Pet '{pet_name}' already in list.",
                "add_at_least_one_pet": "Add at least one pet.",
                "no_data_to_export": "No data to export.",
                "data_saved": "Data saved to {file_path}",
                "export_error": "Failed to export data:\n{error}",
                
                # Guild
                "get_guild_members": "Getting Guild Member IDs",
                "userid_label": "UserID:",
                "get_username": "Get Username",
                "password_label": "Password:",
                "authorize": "Authorize",
                "username_not_received": "Username: not received",
                "player": "Player: -",
                "guild": "Guild: -",
                "status_not_authorized": "Status: Not authorized",
                "load_guild_members": "Load Guild Members",
                "keep_main_guild_only": "Keep Main Guild Only",
                "transfer_to_main": "Transfer to Main Window",
                "save_userid_list": "Save UserID List",
                "export_csv": "Export to CSV",
                "enter_userid_for_username": "Enter UserID to get username",
                "getting_username": "Getting username...",
                "username_received": "Username received! Enter password to authorize",
                "username_error": "Error getting username: {error}",
                "get_username_first": "Get username first",
                "enter_password": "Enter password",
                "authorizing": "Authorizing...",
                "status_authorized": "Status: Authorized ✅",
                "authorization_success": "Authorization successful!",
                "authorization_error": "Authorization error: {error}",
                "status_error": "Status: Error ❌",
                "authorize_first": "Authorize first",
                "getting_members_data": "Getting member data...",
                "members_data_error": "Error getting member data: {error}",
                "members_loaded": "Members loaded: {count} | Guild ID: {guild_id}",
                "delete_row_confirm": "Delete this row?",
                "no_data_to_transfer": "No data to transfer",
                "ids_transferred": "IDs transferred to main window",
                "no_data_to_save": "No data to save",
                "list_saved": "List saved to {file_path}",
                "save_file_error": "Failed to save file: {error}",
                "no_data_to_filter": "No data to filter",
                "filter_guilds_error": "Failed to determine guilds for filtering",
                "only_main_guild": "Only members of guild: {guild}",
                
                # Language
                "language": "Language",
                "russian": "Русский",
                "english": "English",
            }
        }
        self.callbacks = []  # Список функций для обновления при смене языка
    
    def t(self, key, **kwargs):
        """Получить перевод по ключу с возможностью подстановки параметров"""
        translation = self.translations.get(self.current_language, {}).get(key, key)
        if kwargs:
            try:
                return translation.format(**kwargs)
            except:
                return translation
        return translation
    
    def set_language(self, lang):
        """Установить язык и обновить все элементы интерфейса"""
        if lang in self.translations:
            self.current_language = lang
            # Вызываем все зарегистрированные callback'и для обновления интерфейса
            for callback in self.callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"Ошибка обновления интерфейса: {e}")
    
    def register_callback(self, callback):
        """Зарегистрировать функцию для обновления при смене языка"""
        self.callbacks.append(callback)

# Глобальный экземпляр менеджера переводов
translator = TranslationManager()

class ToolTip:
    """Класс для создания всплывающих подсказок"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("Arial", 8), padx=5, pady=5)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

URL = "https://pcmob.parse.gemsofwar.com/call_function"

DOPHENEK_MAP = {
    "W1n1tpfLsE": "Бутчер",
    "1f2Azk4Dcw": "Lina",
    "Zv1wQ5s045": "Zarken11",
    "76bmyuRJSL": "Артист",
    "eCQRFKgEGS": "Velvik",
    "NqfMDuOdD6": "Мини Какуйчик",
    "O9hPzTMr9g": "Мудрый Старец Каку",
    "UUIxpRSAmD": "Здец",
    "Jk9CtQc6Sd": "Фенечка",
    "ApjDU34e3S": "Во мухложуки",
    "p58Icthyl8": "Магутчей воеН",
    "KcjFVyRgRD": "Космос",
    "SZq8iivili": "Кошечка лапой",
    "QVvT3JB9QZ": "Анк",
    "nRkoBA6rVN": "Юра",
}

class BaseWindow(tk.Toplevel):
    """Базовый класс для всех окон с настройкой стиля"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
    def configure_treeview_style(self):
        """Универсальная настройка стиля Treeview для всех окон"""
        try:
            style = ttk.Style(self)
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            style.configure("Treeview", font=('Arial', 9))
            print(f"Стиль Treeview настроен для {self.__class__.__name__}")
        except Exception as e:
            print(f"Ошибка настройки стиля в {self.__class__.__name__}: {e}")


class PetSearchWindow(BaseWindow):
    def __init__(self, parent, player_data, show_guild=False, show_dophenek=False):
        super().__init__(parent)
        self.title("Поиск питомцев у игроков")
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
            messagebox.showerror("Ошибка загрузки", 
                f"Не удалось загрузить список питомцев:\n{str(e)}")

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Верхняя панель с кнопками
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=5)
        
        self.btn_toggle_guild = tk.Button(
            top_frame, 
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию",
            width=18, 
            command=self.toggle_guild_column
        )
        self.btn_toggle_guild.pack(side="left", padx=5)

        self.btn_toggle_dophenek = tk.Button(
            top_frame,
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя",
            width=18,
            command=self.toggle_dophenek_column
        )
        self.btn_toggle_dophenek.pack(side="left", padx=5)

        btn_export_csv = tk.Button(
            top_frame, 
            text="Сохранить как CSV", 
            width=18, 
            command=self.export_to_csv
        )
        btn_export_csv.pack(side="right", padx=5)

        # Панель поиска питомцев
        search_outer_frame = tk.Frame(main_frame)
        search_outer_frame.pack(pady=10, fill="x")

        search_frame = tk.Frame(search_outer_frame)
        search_frame.pack(anchor='center')

        tk.Label(search_frame, text="Поиск питомца:").pack(side="left", padx=5)
        self.entry = tk.Entry(search_frame, width=40)
        self.entry.pack(side="left", padx=5)

        btn_add = tk.Button(search_frame, text="Добавить питомца", width=18, command=self.add_pet)
        btn_add.pack(side="left", padx=5)

        button_frame = tk.Frame(search_outer_frame)
        button_frame.pack(anchor='center', pady=(10, 0))

        btn_search = tk.Button(
            button_frame, 
            text="Найти питомцев", 
            width=20,
            command=self.find_multiple_pets
        )
        btn_search.pack(pady=(0, 5))

        btn_clear = tk.Button(
            button_frame,
            text="Очистить список",
            width=20,
            command=self.clear_pets_list
        )
        btn_clear.pack()

        # Панель выбранных питомцев
        pets_list_frame = tk.Frame(main_frame)
        pets_list_frame.pack(fill="x", pady=(5, 0))
        tk.Label(pets_list_frame, text="Выбранные питомцы:", font=('Arial', 10, 'bold')).pack(anchor="w")
        
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
        
        self.tree.heading("player_name", text="Игрок", command=lambda: self.sort_treeview("player_name", False))
        self.tree.column("player_name", width=180, anchor="center")
        
        if self.show_dophenek:
            self.tree.heading("dophenek_name", text="Доп. имя", command=lambda: self.sort_treeview("dophenek_name", False))
            self.tree.column("dophenek_name", width=150, anchor="center")
        
        if self.show_guild:
            self.tree.heading("guild_name", text="Гильдия", command=lambda: self.sort_treeview("guild_name", False))
            self.tree.column("guild_name", width=150, anchor="center")

    def add_pet(self):
        """Добавляет питомца в список для поиска"""
        pet_name = self.entry.get().strip().lower()
        if not pet_name:
            messagebox.showwarning("Ошибка", "Введите название питомца")
            return

        # Поиск точного совпадения
        exact_matches = [(name, pid) for name, pid in self.name_to_id.items() if name == pet_name]
        
        if exact_matches:
            selected_name, pid = exact_matches[0]
        else:
            # Поиск частичных совпадений
            partial_matches = [(name, pid) for name, pid in self.name_to_id.items() if pet_name in name]
            
            if not partial_matches:
                messagebox.showinfo("Не найдено", f"Питомец '{pet_name}' не найден.")
                return
            elif len(partial_matches) == 1:
                selected_name, pid = partial_matches[0]
            else:
                # Если несколько совпадений - показываем выбор
                selected_name = self.choose_from_list(
                    [self.id_to_name[str(pid)] for _, pid in partial_matches], 
                    title="Выбор питомца",
                    prompt=f"Найдено несколько совпадений для '{pet_name}'"
                )
                if not selected_name:
                    return
                # Находим ID выбранного питомца
                pid = next(pid for name, pid in self.name_to_id.items() 
                          if self.id_to_name[str(pid)] == selected_name)

        # Проверяем, не добавлен ли уже питомец
        if pid in [p[0] for p in self.selected_pets]:
            messagebox.showinfo("Информация", f"Питомец '{self.id_to_name[str(pid)]}' уже в списке.")
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
            messagebox.showwarning("Ошибка", "Добавьте хотя бы одного питомца.")
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
                self.tree.heading(col, text="Игрок", command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=180, anchor="center")
            elif col == "dophenek_name":
                self.tree.heading(col, text="Доп. имя", command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=150, anchor="center")
            elif col == "guild_name":
                self.tree.heading(col, text="Гильдия", command=lambda: self.sort_treeview(col, False))
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
        font = tk.font.Font()
        
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
            messagebox.showwarning("Ошибка", "Нет данных для экспорта.")
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
                    
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные:\n{str(e)}")

    def toggle_guild_column(self):
        """Переключает отображение столбца с гильдией"""
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        if self.selected_pets:
            self.find_multiple_pets()
        else:
            self.show_players_list()

    def toggle_dophenek_column(self):
        """Переключает отображение столбца с доп. именем"""
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
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
                self.tree.heading(col, text="Игрок", command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=180, anchor="center")
            elif col == "dophenek_name":
                self.tree.heading(col, text="Доп. имя", command=lambda: self.sort_treeview(col, False))
                self.tree.column(col, width=150, anchor="center")
            elif col == "guild_name":
                self.tree.heading(col, text="Гильдия", command=lambda: self.sort_treeview(col, False))
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

class GuildMembersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
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
            values[0] = str(idx)  # Обновляем номер
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
            response = requests.post("https://pcmob.parse.gemsofwar.com/call_function", json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "result" not in data or "ProfileData" not in data["result"]:
                raise ValueError("Некорректный ответ сервера")

            profile = data["result"]["ProfileData"]
            username = profile.get("username", "")
            guild_name = profile.get("GuildName", "Без гильдии")  # Получаем название гильдии
            player_name = profile.get("Name", "Неизвестно")
        
            # Создаём кэш, если ещё не создан
            if not hasattr(self, "profiles_cache"):
                self.profiles_cache = {}

            # Сохраняем профиль для UserId
            self.profiles_cache[user_id] = profile

            if not username:
                raise ValueError("Username не найден в ответе")

            self.username_from_profile = username
            
            # Обновляем UI - ДОБАВЛЕНО ОБНОВЛЕНИЕ ГИЛЬДИИ
            self.username_label.config(text=f"Username: {username}", fg="green")
            self.player_label.config(text=f"Игрок: {player_name}", fg="blue")
            self.guild_label.config(text=f"Гильдия: {guild_name}", fg="blue")  # ЭТА СТРОКА БЫЛА ПРОПУЩЕНА
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

            response = requests.post("https://pcmob.parse.gemsofwar.com/call_function", json=auth_payload, timeout=10)
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
                
                profile_response = requests.post("https://pcmob.parse.gemsofwar.com/call_function", json=profile_payload, timeout=10)
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

            # Статус теперь обновляется в display_members

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
        guild_id = "Неизвестно"  # Нужно получить из данных гильдии
        
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
                if not self._running:  # Добавьте флаг _running в __init__
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
            if self.tree.item(item)["values"][4] == user_id:  # UserID в 4-й колонке
                values = list(self.tree.item(item)["values"])
                values[2] = guild_name  # Гильдия в 3-й колонке (индекс 2)
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
            data.append((values[col_idx], child))  # Сохраняем child (идентификатор строки), а не values
        
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
        # Берем UserID из 4-й колонки (индекс 4), а не 3-й
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
        # ВНИМАНИЕ: UserID находится в 5-й колонке (индекс 4) — сохраняем именно его
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
        Оставляет в таблице только участников одной гильдии:
        определяется гильдия, которая встречается чаще всего,
        затем по подтверждению пользователя остальные строки удаляются.
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

class KingdomLevelsWindow(BaseWindow):
    def __init__(self, parent, results, user_ids, show_dophenek=False, show_guild=False):
        super().__init__(parent)
        self.title("Уровни королевств")
        self.geometry("1200x600")
        self.results = results
        self.user_ids = user_ids
        self.show_dophenek = show_dophenek
        self.show_guild = show_guild
        
        # Базовые колонки
        self.base_columns = ["#", "Игрок"]
        self.optional_columns = {
            "dophenek": "Доп. Имя",
            "guild": "Гильдия"
        }
        self.stats_columns = ["Лвл 10", "Лвл 15", "Лвл 20", "Сумма"]
        
        self.setup_ui()

        # Настройка стиля Treeview
        self.configure_treeview_style()

    def get_visible_columns(self):
        """Возвращает список видимых колонок"""
        columns = self.base_columns.copy()
        if self.show_dophenek:
            columns.append(self.optional_columns["dophenek"])
        if self.show_guild:
            columns.append(self.optional_columns["guild"])
        columns.extend(self.stats_columns)
        return columns

    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        container = tk.Frame(main_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar = ttk.Scrollbar(container)
        yscrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            container, 
            columns=self.get_visible_columns(), 
            show="headings",
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        self.tree.pack(fill="both", expand=True)

        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)

        # Кнопки управления
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=5)

        self.btn_toggle_guild = ttk.Button(
            btn_frame,
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию",
            command=self.toggle_guild_column,
        )
        self.btn_toggle_guild.pack(side="left", padx=5)

        self.btn_toggle_dophenek = ttk.Button(
            btn_frame,
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя",
            command=self.toggle_dophenek_column,
        )
        self.btn_toggle_dophenek.pack(side="left", padx=5)

        self.save_btn = ttk.Button(btn_frame, text="Сохранить как .csv", command=self.save_csv)
        self.save_btn.pack(side="left", padx=5)

        self.setup_columns()
        self.load_data()
        self.sort_by_column("Лвл 20", reverse=True)

    def setup_columns(self):
        """Настраивает колонки дерева"""
        columns = self.get_visible_columns()
        self.tree["columns"] = columns
        
        for col in columns:
            if col == "#":
                self.tree.heading(col, text=col)
                self.tree.column(col, width=40, minwidth=40, anchor="center", stretch=False)
            else:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
                if col == self.optional_columns["dophenek"]:
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                elif col == self.optional_columns["guild"]:
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                elif col == "Игрок":
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                else:
                    self.tree.column(col, width=80, minwidth=60, anchor="center")

    def load_data(self):
        """Загружает данные в таблицу"""
        self.tree.delete(*self.tree.get_children())
        player_data = []
        
        for user_id in self.user_ids:
            data = self.results.get(user_id)
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            name = profile.get("Name", "Unknown")
            dophenek_name = DOPHENEK_MAP.get(user_id, "")
            guild_name = profile.get("GuildName", "")

            kingdom_levels = profile.get("KingdomLevels", {})
            considered = [lvl for lvl in kingdom_levels.values() if lvl >= 2]
            
            count_10 = sum(1 for lvl in considered if lvl >= 10)
            count_15 = sum(1 for lvl in considered if lvl >= 15)
            count_20 = sum(1 for lvl in considered if lvl >= 20)
            total_sum = sum(considered)

            player_data.append({
                "name": name,
                "dophenek": dophenek_name,
                "guild": guild_name,
                "count_10": count_10,
                "count_15": count_15,
                "count_20": count_20,
                "total": total_sum,
                "user_id": user_id
            })

        # Сортировка по убыванию Лвл 20
        player_data.sort(key=lambda x: (x["count_20"], x["count_15"], x["count_10"], x["total"]), reverse=True)

        for idx, player in enumerate(player_data, start=1):
            values = [idx, player["name"]]
            if self.show_dophenek:
                values.append(player["dophenek"])
            if self.show_guild:
                values.append(player["guild"])
            values.extend([
                player["count_10"],
                player["count_15"],
                player["count_20"],
                player["total"]
            ])
            self.tree.insert("", "end", iid=player["user_id"], values=values)
        
        self.auto_resize_columns()

    def toggle_guild_column(self):
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        self.rebuild_table()

    def toggle_dophenek_column(self):
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )
        self.rebuild_table()

    def rebuild_table(self):
        current_sort = self.get_current_sort_column()
        self.setup_columns()
        self.load_data()
        if current_sort:
            self.sort_by_column(current_sort["column"], current_sort["reverse"])

    def get_current_sort_column(self):
        for col in self.tree["columns"]:
            heading = self.tree.heading(col)
            if "↓" in heading["text"]:
                return {"column": col, "reverse": False}
            elif "↑" in heading["text"]:
                return {"column": col, "reverse": True}
        return None

    def sort_by_column(self, col, reverse):
        if col == "#":
            return

        data = []
        for k in self.tree.get_children():
            values = self.tree.item(k)['values']
            col_index = self.tree["columns"].index(col)
            v = values[col_index]
            
            if col in self.stats_columns:
                try:
                    sort_key = int(v)
                except:
                    sort_key = 0
            else:
                sort_key = v.lower() if isinstance(v, str) else v
            
            data.append((sort_key, values, k))

        data.sort(reverse=reverse, key=lambda x: x[0])
        
        # Обновляем заголовки с указанием направления сортировки
        for c in self.tree["columns"]:
            text = c
            if "↑" in text or "↓" in text:
                text = text.split()[0]
            if c == col:
                text += " ↓" if reverse else " ↑"
            self.tree.heading(c, text=text, command=lambda c=c: self.sort_by_column(c, not reverse))
        
        # Обновляем данные
        for index, (_, values, k) in enumerate(data, start=1):
            new_values = [index] + values[1:]  # Обновляем нумерацию
            self.tree.item(k, values=new_values)
            self.tree.move(k, '', index)

    def auto_resize_columns(self):
        font = tkfont.Font()
        for col in self.tree["columns"]:
            header_width = font.measure(self.tree.heading(col)["text"].split()[0]) + 20
            self.tree.column(col, width=header_width)
        
        for row in self.tree.get_children():
            for i, value in enumerate(self.tree.item(row)["values"]):
                col_name = self.tree["columns"][i]
                current_width = self.tree.column(col_name, width=None)
                content_width = font.measure(str(value)) + 20
            
                if current_width < content_width:
                    self.tree.column(col_name, width=content_width)

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                headers = []
                for col in self.tree["columns"]:
                    header_text = self.tree.heading(col)["text"]
                    if "↑" in header_text or "↓" in header_text:
                        header_text = header_text.split()[0]
                    headers.append(header_text)
                writer.writerow(headers)
                
                for row_id in self.tree.get_children():
                    writer.writerow(self.tree.item(row_id)["values"])
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")

class KingdomPowerWindow(BaseWindow):
    def __init__(self, parent, results, user_ids, show_dophenek=False, show_guild=False):
        super().__init__(parent)
        self.title("Мощь королевств")
        self.geometry("1200x600")
        self.results = results
        self.user_ids = user_ids
        self.show_dophenek = show_dophenek
        self.show_guild = show_guild
        
        # Базовые колонки
        self.base_columns = ["#", "Игрок"]
        self.optional_columns = {
            "dophenek": "Доп. Имя",
            "guild": "Гильдия"
        }
        self.stats_columns = ["5★", "10★", "20★", "30★", "Сумма"]
        
        self.setup_ui()

        # Настройка стиля Treeview
        self.configure_treeview_style()

    def setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        container = tk.Frame(main_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Создаем scrollbars
        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        yscrollbar = ttk.Scrollbar(container)
        yscrollbar.pack(side="right", fill="y")

        # Создаем treeview
        self.tree = ttk.Treeview(
            container, 
            columns=self.get_visible_columns(), 
            show="headings",
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        self.tree.pack(fill="both", expand=True)

        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)

        # Кнопки управления
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=5)

        self.btn_toggle_guild = ttk.Button(
            btn_frame,
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию",
            command=self.toggle_guild_column,
        )
        self.btn_toggle_guild.pack(side="left", padx=5)

        self.btn_toggle_dophenek = ttk.Button(
            btn_frame,
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя",
            command=self.toggle_dophenek_column,
        )
        self.btn_toggle_dophenek.pack(side="left", padx=5)

        self.save_btn = ttk.Button(btn_frame, text="Сохранить как .csv", command=self.save_csv)
        self.save_btn.pack(side="left", padx=5)

        # Настраиваем колонки и загружаем данные
        self.setup_columns()
        self.load_data()
        self.sort_by_column("Сумма", reverse=True)

    def get_visible_columns(self):
        """Возвращает список видимых колонок"""
        columns = self.base_columns.copy()
        if self.show_dophenek:
            columns.append(self.optional_columns["dophenek"])
        if self.show_guild:
            columns.append(self.optional_columns["guild"])
        columns.extend(self.stats_columns)
        return columns

    def setup_columns(self):
        """Настраивает колонки дерева"""
        columns = self.get_visible_columns()
        
        # Удаляем все существующие колонки
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        
        # Устанавливаем новые колонки
        self.tree["columns"] = columns
        
        for col in columns:
            if col == "#":
                self.tree.heading(col, text=col)
                self.tree.column(col, width=40, minwidth=40, anchor="center", stretch=False)
            else:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
                if col == self.optional_columns["dophenek"]:
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                elif col == self.optional_columns["guild"]:
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                elif col == "Игрок":
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                else:
                    self.tree.column(col, width=80, minwidth=60, anchor="center")

    def load_data(self):
        """Загружает данные в таблицу"""
        self.tree.delete(*self.tree.get_children())
        player_data = []
        
        for user_id in self.user_ids:
            data = self.results.get(user_id)
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            name = profile.get("Name", "Unknown")
            dophenek_name = DOPHENEK_MAP.get(user_id, "")
            guild_name = profile.get("GuildName", "")

            total_power = 0
            count_5 = 0
            count_10 = 0
            count_20 = 0
            count_30 = 0

            progress = profile.get("Progress", {})
            for key, kingdom in progress.items():
                if key.isdigit() and isinstance(kingdom, dict):
                    power = kingdom.get("PowerRank", 0)
                    if power >= 1:
                        total_power += power
                    if power >= 5:
                        count_5 += 1
                    if power >= 10:
                        count_10 += 1
                    if power >= 20:
                        count_20 += 1
                    if power >= 30:
                        count_30 += 1

            player_data.append({
                "name": name,
                "dophenek": dophenek_name,
                "guild": guild_name,
                "count_5": count_5,
                "count_10": count_10,
                "count_20": count_20,
                "count_30": count_30,
                "total": total_power,
                "user_id": user_id
            })

        # Сортировка по убыванию
        player_data.sort(key=lambda x: (x["count_30"], x["count_20"], x["count_10"], x["count_5"], x["total"]), reverse=True)

        for idx, player in enumerate(player_data, start=1):
            values = [idx, player["name"]]
            if self.show_dophenek:
                values.append(player["dophenek"])
            if self.show_guild:
                values.append(player["guild"])
            values.extend([
                player["count_5"],
                player["count_10"],
                player["count_20"],
                player["count_30"],
                player["total"]
            ])
            self.tree.insert("", "end", iid=player["user_id"], values=values)
        
        self.auto_resize_columns()

    def auto_resize_columns(self):
        """Автоматически подбирает ширину колонок"""
        font = tkfont.Font()
        for col in self.tree["columns"]:
            header_width = font.measure(self.tree.heading(col)["text"].split()[0]) + 20
            self.tree.column(col, width=header_width)
        
        for row in self.tree.get_children():
            for i, value in enumerate(self.tree.item(row)["values"]):
                col_name = self.tree["columns"][i]
                current_width = self.tree.column(col_name, width=None)
                content_width = font.measure(str(value)) + 20
            
                if current_width < content_width:
                    self.tree.column(col_name, width=content_width)

    def toggle_guild_column(self):
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        self.rebuild_table()

    def toggle_dophenek_column(self):
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )
        self.rebuild_table()

    def rebuild_table(self):
        """Полностью перестраивает таблицу с новыми колонками"""
        current_sort = self.get_current_sort_column()
        self.setup_columns()
        self.load_data()
        if current_sort:
            self.sort_by_column(current_sort["column"], current_sort["reverse"])

    def get_current_sort_column(self):
        """Возвращает информацию о текущей сортировке"""
        for col in self.tree["columns"]:
            heading = self.tree.heading(col)
            if "↓" in heading["text"]:
                return {"column": col, "reverse": False}
            elif "↑" in heading["text"]:
                return {"column": col, "reverse": True}
        return None

    def sort_by_column(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#":
            return

        data = []
        for k in self.tree.get_children():
            values = self.tree.item(k)['values']
            col_index = self.tree["columns"].index(col)
            v = values[col_index]
            
            # Для числовых колонок
            if col in self.stats_columns:
                try:
                    sort_key = int(v)
                except:
                    sort_key = 0
            else:
                sort_key = v.lower() if isinstance(v, str) else v
            
            data.append((sort_key, values, k))

        data.sort(reverse=reverse, key=lambda x: x[0])
        
        # Обновляем текст заголовка с указанием направления сортировки
        for c in self.tree["columns"]:
            text = c
            if "↑" in text or "↓" in text:
                text = text.split()[0]
            if c == col:
                text += " ↓" if reverse else " ↑"
            self.tree.heading(c, text=text, command=lambda c=c: self.sort_by_column(c, not reverse))
        
        # Обновляем данные
        for index, (_, values, k) in enumerate(data, start=1):
            new_values = [index] + values[1:]  # Обновляем нумерацию
            self.tree.item(k, values=new_values)
            self.tree.move(k, '', index)

    def save_csv(self):
        """Сохраняет данные в CSV файл"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Заголовки (без указания направления сортировки)
                headers = []
                for col in self.tree["columns"]:
                    header_text = self.tree.heading(col)["text"]
                    if "↑" in header_text or "↓" in header_text:
                        header_text = header_text.split()[0]
                    headers.append(header_text)
                writer.writerow(headers)
                
                # Данные
                for row_id in self.tree.get_children():
                    writer.writerow(self.tree.item(row_id)["values"])
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")

class StatsWindow(BaseWindow):
    def __init__(self, parent, results, user_ids, show_dophenek=False, show_guild=False):
        super().__init__(parent)
        self.title("Статы выбранных пользователей")
        self.geometry("1200x400")
        self.results = results
        self.user_ids = user_ids
        self.show_dophenek = show_dophenek
        self.show_guild = show_guild

        self.icon_urls = {
            "Магия": "https://garyatrics.com/gow_assets/Atlas/magic.png",
            "Атака": "https://garyatrics.com/gow_assets/Atlas/attack.png",
            "Жизнь": "https://garyatrics.com/gow_assets/Atlas/health.png",
            "Броня": "https://garyatrics.com/gow_assets/Atlas/armor.png"
        }
        self.icons = {}  # сюда будем складывать загруженные иконки
        
        self.column_display_names = {
            "#": "#",
            "Name": "Игрок", 
            "Доп. Имя": "Доп. Имя",
            "Гильдия": "Гильдия",
            "Total": "Всего"
        }

        # Инициализация колонок
        self.cols_base = ["#", "Игрок"]
        self.col_dophenek = ["Доп. Имя"] if show_dophenek else []
        self.col_guild = ["Гильдия"] if show_guild else []
        self.cols_stats = ["Магия", "Атака", "Жизнь", "Броня"]
        self.col_total = ["Всего"]
        self.columns = self.cols_base + self.col_dophenek + self.col_guild + self.col_total + self.cols_stats
        
        self.setup_ui()  # ИСПРАВЛЕНО: правильное имя метода

        # Настройка стиля Treeview
        self.configure_treeview_style()

    def load_icon(self, key, size=(16, 16)):
        url = self.icon_urls.get(key)
        if not url:
            return None
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).resize(size, Image.LANCZOS)
            icon = ImageTk.PhotoImage(img)
            self.icons[key] = icon  # сохраняем, чтобы не удалялось GC
            return icon
        except:
            return None

    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        container = tk.Frame(main_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar = ttk.Scrollbar(container)
        yscrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            container, 
            columns=self.columns, 
            show="headings",
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        self.tree.pack(fill="both", expand=True)

        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)

        self.btn_toggle_guild = ttk.Button(
            btn_frame,
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию",
            command=self.toggle_guild_column,
        )
        self.btn_toggle_guild.pack(side="left", padx=5)

        self.btn_toggle_dophenek = ttk.Button(
            btn_frame,
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя",
            command=self.toggle_dophenek_column,
        )
        self.btn_toggle_dophenek.pack(side="left", padx=5)

        self.save_btn = ttk.Button(btn_frame, text="Сохранить как .csv", command=self.save_csv)
        self.save_btn.pack(side="left", padx=5)

        self.setup_columns()
        self.load_stats()
        self.sort_by_column("Всего", reverse=True)

        # ===== Примечание в рамке над кнопками =====
        note_text = (
            "Примечание:\n"
            "Числа в столбиках имеют вид X+Y:\n"
            "X — прибавка ко всем войскам, Y — прибавка только герою (зависит от уровня)."
        )

        note_label = tk.Label(
            main_frame,
            text=note_text,
            justify="left",   # строки внутри label слева
            bg="#fff3cd",
            fg="#856404",
            font=("Arial", 10, "bold"),
            bd=1,
            relief="sunken",
            padx=10,
            pady=5
        )
        note_label.pack(pady=(0,10))       # вертикальный отступ
        note_label.pack(anchor="center")    # сам блок по центру окна

    def toggle_guild_column(self):
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        self.rebuild_table()

    def toggle_dophenek_column(self):
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )
        self.rebuild_table()

    def rebuild_table(self):
        """Полностью перестраивает таблицу с новыми колонками"""
        # Обновляем список колонки
        self.col_dophenek = ["Доп. Имя"] if self.show_dophenek else []
        self.col_guild = ["Гильдия"] if self.show_guild else []
        self.columns = self.cols_base + self.col_dophenek + self.col_guild + self.col_total + self.cols_stats
        
        # Сохраняем текущую сортировку
        current_sort = self.get_current_sort_column()
        
        # Удаляем все текущие колонки
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        
        # Устанавливаем новые колонки
        self.tree["columns"] = self.columns
        
        # Настраиваем колонки
        self.setup_columns()
        
        # Перезагружаем данные
        self.load_stats()
        
        # Восстанавливаем сортировку
        if current_sort:
            self.sort_by_column(current_sort["column"], current_sort["reverse"])

    def get_current_sort_column(self):
        """Возвращает информацию о текущей сортировке"""
        for col in self.tree["columns"]:
            heading = self.tree.heading(col)
            if "↓" in heading["text"]:
                return {"column": col, "reverse": False}
            elif "↑" in heading["text"]:
                return {"column": col, "reverse": True}
        return None

    def setup_columns(self):
        """Настраивает колонки дерева"""
        for col in self.columns:
            if col == "#":
                self.tree.heading(col, text=col)
                self.tree.column(col, width=40, minwidth=40, anchor="center", stretch=False)
            else:
                # ВАШ КОД ДЛЯ ОТОБРАЖЕНИЯ ИКОНОК
                if col in self.icon_urls:
                    icon = self.load_icon(col)
                    self.tree.heading(col, text=f" {col}", image=icon,
                                    command=lambda c=col: self.sort_by_column(c, False),
                                    anchor="center")
                    self.tree.column(col, width=80, minwidth=60, anchor="center")
                else:
                    display_name = self.column_display_names.get(col, col)
                    self.tree.heading(col, text=display_name,
                                    command=lambda c=col: self.sort_by_column(c, False))
                    
                # Дополнительные настройки ширины для специфических колонок
                if col == "Доп. Имя":
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                elif col == "Гильдия":
                    self.tree.column(col, width=150, minwidth=100, anchor="center")
                elif col == "Total":
                    self.tree.column(col, width=100, minwidth=80, anchor="center")
                elif col in self.icon_urls:  # Для колонок с иконками
                    self.tree.column(col, width=80, minwidth=60, anchor="center")
                else:
                    self.tree.column(col, width=100, minwidth=80, anchor="center")

    def load_stats(self):
        """Загружает статистику в таблицу"""
        self.tree.delete(*self.tree.get_children())
        for idx, user_id in enumerate(self.user_ids, start=1):
            data = self.results.get(user_id)
            if not data:
                continue
                
            values = self.calculate_stats(idx, user_id, data.get("result", {}).get("ProfileData", {}))
            self.tree.insert("", "end", values=values)
        
        self.auto_resize_columns()

    def calculate_stats(self, idx, user_id, profile):
        """Вычисляет статистику для одного игрока с фиксированными гильдейскими бонусами"""
        name = profile.get("Name", "")
        dophenek_name = DOPHENEK_MAP.get(user_id, "") if self.show_dophenek else ""
        guild_name = profile.get("GuildName", "") if self.show_guild else ""

        # Фиксированные гильдейские бонусы (вместо реальных)
        FIXED_GUILD_BONUSES = {
            "GuildTroopMagicBonus": 4,
            "GuildTroopAttackBonus": 6,
            "GuildTroopHealthBonus": 16,
            "GuildTroopArmorBonus": 16
        }

        # Magic (Магия)
        magic_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopMagicBonus"],  # Фиксированный вместо profile.get("GuildTroopMagicBonus", 0)
            profile.get("TroopMagicBonus", 0),
            profile.get("RenownTroopMagicBonus", 0)
        ])
        spell_power = profile.get("SpellPower", 0)
        magic_str = f"{magic_base} + {spell_power}" if spell_power else f"{magic_base}"

        # Attack (Атака)
        attack_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopAttackBonus"],  # Фиксированный
            profile.get("TroopAttackBonus", 0),
            profile.get("RenownTroopAttackBonus", 0)
        ])
        attack_add = profile.get("Attack", 0)
        attack_str = f"{attack_base} + {attack_add}" if attack_add else f"{attack_base}"

        # Health (Жизнь)
        health_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopHealthBonus"],  # Фиксированный
            profile.get("TroopHealthBonus", 0),
            profile.get("RenownTroopHealthBonus", 0)
        ])
        health_add = profile.get("MaxHealth", 0)
        health_str = f"{health_base} + {health_add}" if health_add else f"{health_base}"

        # Armor (Броня)
        armor_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopArmorBonus"],  # Фиксированный
            profile.get("TroopArmorBonus", 0),
            profile.get("RenownTroopArmorBonus", 0)
        ])
        armor_add = profile.get("Armor", 0)
        armor_str = f"{armor_base} + {armor_add}" if armor_add else f"{armor_base}"

        total_base = magic_base + attack_base + health_base + armor_base
        total_add = spell_power + attack_add + health_add + armor_add
        total_str = f"{total_base} + {total_add}"

        values = [idx, name]
        if self.show_dophenek:
            values.append(dophenek_name)
        if self.show_guild:
            values.append(guild_name)
        values.extend([total_str, magic_str, attack_str, health_str, armor_str])
        
        return values

    def sort_by_column(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#":
            return

        data = []
        for k in self.tree.get_children():
            values = self.tree.item(k)['values']
            col_index = self.columns.index(col)
            v = values[col_index]
            
            if col == "Всего":
                try:
                    base, add = map(int, v.split("+"))
                    sort_key = base + add
                except:
                    sort_key = 0
            else:
                try:
                    sort_key = float(v.split("+")[0]) if "+" in v else float(v)
                except:
                    sort_key = v.lower()
            
            data.append((sort_key, values, k))

        data.sort(reverse=reverse, key=lambda x: x[0])
        
        # Обновляем заголовки с указанием направления сортировки
        for c in self.tree["columns"]:
            text = c
            if "↑" in text or "↓" in text:
                text = text.split()[0]
            if c == col:
                text += " ↓" if reverse else " ↑"
            self.tree.heading(c, text=text, command=lambda c=c: self.sort_by_column(c, not reverse))
        
        # Обновляем данные
        for index, (_, values, k) in enumerate(data, start=1):
            new_values = [index] + values[1:]  # Обновляем нумерацию
            self.tree.item(k, values=new_values)
            self.tree.move(k, '', index)

    def auto_resize_columns(self):
        """Автоматически подбирает ширину колонок"""
        font = tkfont.Font()
        for col in self.columns:
            header_width = font.measure(col) + 20
            self.tree.column(col, width=header_width)
        
        for row in self.tree.get_children():
            for i, value in enumerate(self.tree.item(row)["values"]):
                col_width = font.measure(str(value)) + 20
                if self.tree.column(self.columns[i], width=None) < col_width:
                    self.tree.column(self.columns[i], width=col_width)

    def save_csv(self):
        """Сохраняет данные в CSV файл"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Записываем заголовки (без указания направления сортировки)
                headers = []
                for col in self.columns:
                    header_text = col
                    if "↑" in header_text or "↓" in header_text:
                        header_text = header_text.split()[0]
                    headers.append(header_text)
                writer.writerow(headers)
                
                # Записываем данные
                for row_id in self.tree.get_children():
                    writer.writerow(self.tree.item(row_id)["values"])
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")

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

class DefenseMapWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Карта защиты - Война гильдий")
        self.geometry("1100x800")
        
        # Для хранения загруженного изображения
        self.defense_map_image = None
        self.cached_map_path = None
        self.troop_data = {
            "Святилище": {"troops": [6175, 7177, 1220, 6779], "x1": 100, "y1": 50, "x2": 250, "y2": 150},
            "Оборотни": {"troops": [1234, 5678, 9012, 3456], "x1": 300, "y1": 80, "x2": 450, "y2": 180},
            # Добавьте другие области с координатами
        }
        
        self.setup_ui()
        self.load_defense_map()

        # Настройка стиля Treeview
        self.configure_treeview_style()
        
    def setup_ui(self):
        """Настройка интерфейса окна карты"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Верхняя панель для кнопок
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Кнопка "обновить карту"
        btn_refresh = tk.Button(
            top_frame,
            text="обновить карту",
            width=15,
            command=self.load_defense_map,
            bg="lightgreen",
            font=("Arial", 10)
        )
        btn_refresh.pack(side="left", padx=5)
        
        # Кнопка "очистить кэш"
        btn_clear_cache = tk.Button(
            top_frame,
            text="очистить кэш",
            width=15,
            command=self.clear_cache,
            bg="lightcoral",
            font=("Arial", 10)
        )
        btn_clear_cache.pack(side="left", padx=5)
        
        # Label для статуса загрузки
        self.status_label = tk.Label(top_frame, text="", fg="blue")
        self.status_label.pack(side="left", padx=10)
        
        # Canvas для карты
        self.map_canvas = tk.Canvas(main_frame, bg="white", cursor="hand2")
        self.map_canvas.pack(fill="both", expand=True, pady=5)
        self.map_canvas.bind("<Button-1>", self.on_map_click)
        
    def on_map_click(self, event):
        """Обработчик клика по карте"""
        # Проверяем, попал ли клик в какую-либо область
        for area_name, area_data in self.troop_data.items():
            x1, y1, x2, y2 = area_data["x1"], area_data["y1"], area_data["x2"], area_data["y2"]
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.show_troops_popup(area_name, area_data["troops"])
                return
    
    def show_troops_popup(self, area_name, troop_ids):
        """Показывает всплывающее окно с войсками"""
        popup = tk.Toplevel(self)
        popup.title(f"Войска - {area_name}")
        popup.geometry("300x400")
        popup.transient(self)
        popup.grab_set()
        
        # Заголовок
        tk.Label(popup, text=f"Войска области:\n{area_name}", 
                font=("Arial", 12, "bold"), fg="blue").pack(pady=10)
        
        # Фрейм для войск
        troops_frame = tk.Frame(popup)
        troops_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Отображаем войска в столбик
        for i, troop_id in enumerate(troop_ids, 1):
            troop_frame = tk.Frame(troops_frame, relief="raised", bd=1)
            troop_frame.pack(fill="x", pady=2)
            
            tk.Label(troop_frame, text=f"Войско {i}:", width=10, 
                    font=("Arial", 9, "bold")).pack(side="left", padx=5)
            tk.Label(troop_frame, text=str(troop_id), 
                    font=("Arial", 10)).pack(side="left", padx=5)
        
        # Кнопка закрытия
        tk.Button(popup, text="Закрыть", command=popup.destroy,
                 bg="lightcoral", width=15).pack(pady=10)
    
    def get_cache_path(self):
        """Возвращает путь к кэшированному файлу карты"""
        map_url = "https://i.imgur.com/D0Ay1uI.png"
        url_hash = hashlib.md5(map_url.encode()).hexdigest()
        cache_dir = tempfile.gettempdir()
        return os.path.join(cache_dir, f"gow_defense_map_{url_hash}.png")
    
    def download_map(self):
        """Скачивает карту и сохраняет в кэш"""
        map_url = "https://i.imgur.com/D0Ay1uI.png"
        self.cached_map_path = self.get_cache_path()
        
        try:
            self.status_label.config(text="Загрузка карты...", fg="blue")
            self.update()
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(map_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(self.cached_map_path, 'wb') as f:
                f.write(response.content)
                
            self.status_label.config(text="Карта загружена", fg="green")
            return True
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка загрузки: {str(e)}", fg="red")
            return False
    
    def load_defense_map(self):
        """Загружает и отображает карту защиты"""
        try:
            cache_path = self.get_cache_path()
            
            if not os.path.exists(cache_path):
                if not self.download_map():
                    return
            else:
                self.cached_map_path = cache_path
                self.status_label.config(text="Кэшированная карта", fg="green")
            
            # Загружаем изображение из кэша
            image_data = Image.open(self.cached_map_path)
            
            # Масштабируем изображение
            max_width = 1000
            if image_data.width > max_width:
                ratio = max_width / image_data.width
                new_height = int(image_data.height * ratio)
                image_data = image_data.resize((max_width, new_height), Image.LANCZOS)
            else:
                new_height = image_data.height
            
            # Конвертируем для Tkinter
            self.defense_map_image = ImageTk.PhotoImage(image_data)
            
            # Очищаем canvas и рисуем карту
            self.map_canvas.delete("all")
            self.map_canvas.config(width=max_width, height=new_height)
            self.map_canvas.create_image(0, 0, anchor="nw", image=self.defense_map_image)
            
            # Рисуем кликабельные области
            self.draw_clickable_areas()
            
            # Добавляем информационный текст
            self.map_canvas.create_text(
                max_width // 2, 
                new_height - 20, 
                text="Карта защиты - Война гильдий", 
                fill="blue",
                font=("Arial", 12, "bold")
            )
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка загрузки карты: {str(e)}", fg="red")
    
    def draw_clickable_areas(self):
        """Рисует кликабельные области на карте"""
        for area_name, area_data in self.troop_data.items():
            x1, y1, x2, y2 = area_data["x1"], area_data["y1"], area_data["x2"], area_data["y2"]
            
            # Рисуем прямоугольник области
            self.map_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="red", width=2, fill="lightblue", stipple="gray50",
                tags=("clickable_area", area_name)
            )
            
            # Добавляем текст названия области
            self.map_canvas.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=area_name, fill="darkred", font=("Arial", 10, "bold"),
                tags=("area_text", area_name)
            )
    
    def clear_cache(self):
        """Очищает кэш карты"""
        cache_path = self.get_cache_path()
        if os.path.exists(cache_path):
            os.remove(cache_path)
            self.status_label.config(text="Кэш очищен", fg="green")
            self.load_defense_map()  # Перезагружаем карту
        else:
            self.status_label.config(text="Кэш уже пуст", fg="blue")

class GuildWarWindow(BaseWindow):
    def __init__(self, parent, player_data, show_guild=False, show_dophenek=False):
        super().__init__(parent)
        self.title("Война гильдий")
        self.geometry("1800x700")
        self.player_data = player_data
        self.show_guild = show_guild
        self.show_dophenek = show_dophenek

        # Таблица соответствия Restriction -> Русское название
        self.location_mapping = {
            "Wargare": "Оборотни",
            "Wildfolk": "Дикий народец",
            "Elemental": "Элементали",
            "Elf": "Эльфы",
            "Goblin": "Гоблины",
            "Divine": "Божества",
            "Naga": "Наги",
            "Tauros": "Быки",
            "Green": "Зеленые",
            "Beast": "Звери",
            "Sanctuary": "Святилище"
        }

        # Для хранения данных о войсках и оружии (ID -> название)
        self.troop_id_to_name = {}
        self.weapon_id_to_name = {}
        
        # Для хранения данных о классах (classCode -> русское название)
        self.class_code_to_name = {}
        
        # Для хранения данных о знаменах (id -> bannerMana)
        self.banner_id_to_mana = {}

        # Для хранения полных данных защиты
        self.defense_data_full = {}
        self.opponent_data_full = {}

        # Инициализируем defense_data как None - данных еще нет
        self.defense_data = None

        # Для хранения направления сортировки
        self.sort_column = None
        self.sort_reverse = False
        
        # Загружаем данные о войсках, оружии, классах и знаменах
        self.load_troops_data()
        self.load_weapons_data()
        self.load_classes_data()
        self.load_banners_data()
        
        # Настройка интерфейса
        self.setup_ui()

        # Настройка стиля Treeview
        self.configure_treeview_style()

    def load_banners_data(self):
        """Загружает данные о знаменах с внешнего сервера"""
        url = "https://garyatrics.com/taran-data/Kingdoms_Russian.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            kingdoms_data = data.get("kingdoms", [])
            
            for kingdom in kingdoms_data:
                if "id" in kingdom and "bannerMana" in kingdom:
                    banner_id = kingdom["id"]
                    banner_mana = kingdom["bannerMana"].strip()
                    banner_mana = re.sub(r'пурпурный', 'фиолетовый', banner_mana, flags=re.IGNORECASE)
                    self.banner_id_to_mana[banner_id] = banner_mana
                    
        except Exception as e:
            messagebox.showerror("Ошибка загрузки знамен", 
                f"Не удалось загрузить данные о знаменах:\n{e}")

    def get_banner_mana(self, banner_id):
        """Получает информацию о мане знамени по ID"""
        return self.banner_id_to_mana.get(banner_id, f"ID:{banner_id}")

    def load_classes_data(self):
        """Загружает данные о классах с внешнего сервера"""
        url = "https://garyatrics.com/taran-data/ClassesDetails_Russian.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            classes_data = response.json().get("classes", [])
            
            for class_data in classes_data:
                if "classCode" in class_data and "name" in class_data:
                    class_code = class_data["classCode"]
                    name = class_data["name"].strip()
                    self.class_code_to_name[class_code] = name
                    
        except Exception as e:
            messagebox.showerror("Ошибка загрузки классов", 
                f"Не удалось загрузить список классов:\n{e}")

    def get_class_name(self, class_code):
        """Получает русское название класса по classCode"""
        return self.class_code_to_name.get(class_code, class_code)

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
                    name = troop["name"].strip()
                    self.troop_id_to_name[str(troop_id)] = name
                    
        except Exception as e:
            messagebox.showerror("Ошибка загрузки войск", 
                f"Не удалось загрузить список войск:\n{e}")

    def load_weapons_data(self):
        """Загружает данные об оружии с внешнего сервера"""
        url = "https://garyatrics.com/taran-data/Weapons_Russian.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            weapons = response.json().get("weapons", [])
            
            for weapon in weapons:
                if "id" in weapon and "name" in weapon:
                    weapon_id = weapon["id"]
                    name = weapon["name"].strip()
                    self.weapon_id_to_name[str(weapon_id)] = name
                    
        except Exception as e:
            messagebox.showerror("Ошибка загрузки оружия", 
                f"Не удалось загрузить список оружия:\n{e}")
            
    def get_item_name(self, item_id):
        """Получает название предмета (войска или оружия) по ID"""
        troop_name = self.troop_id_to_name.get(str(item_id))
        if troop_name:
            return troop_name
            
        weapon_name = self.weapon_id_to_name.get(str(item_id))
        if weapon_name:
            return weapon_name
            
        return f"ID:{item_id}"
    
    def get_item_names(self, item_ids):
        """Преобразует список ID в список названий"""
        item_names = []
        for item_id in item_ids:
            item_name = self.get_item_name(item_id)
            item_names.append(item_name)
        return item_names
    
    def format_items_display(self, item_ids):
        """Форматирует список предметов с выделением 'Жезл звезд'"""
        if not item_ids:
            return "—"
        
        item_names = []
        for item_id in item_ids:
            item_name = self.get_item_name(item_id)
            if item_name == "Жезл звезд":
                item_names.append(f"🔥{item_name.upper()}🔥")
            else:
                item_names.append(item_name)
        
        formatted_text = ""
        for i in range(0, len(item_names), 4):
            line_items = item_names[i:i+4]
            formatted_text += ", ".join(line_items) + "\n"
        
        return formatted_text.strip()

    def get_location_name(self, location_key, location_data):
        """Получает читаемое название локации из данных"""
        # Сначала проверяем Restriction в данных локации
        restriction = location_data.get("Restriction")
        print(f"DEBUG: location_key={location_key}, restriction={restriction}")
        
        if restriction and restriction in self.location_mapping:
            result = self.location_mapping[restriction]
            print(f"DEBUG: found restriction mapping: {result}")
            return result
        
        # Если Restriction не найден, проверяем сам ключ локации
        if location_key in self.location_mapping:
            result = self.location_mapping[location_key]
            print(f"DEBUG: found key mapping: {result}")
            return result
        
        # Для стандартных локаций
        location_translation = {
            "Gate": "Ворота",
            "Palace": "Дворец",
            "Keep": "Крепость",
            "Sanctuary": "Святилище"
        }
        
        # Для Rank локаций
        if location_key.startswith("Rank"):
            parts = location_key.replace("Rank", "").replace("Loc", " ")
            result = f"Ранг {parts.strip()}"
            print(f"DEBUG: rank location: {result}")
            return result
        
        result = location_translation.get(location_key, location_key)
        print(f"DEBUG: final result: {result}")
        return result
        
    def load_defense_data(self):
        """Загружает данные о защите из файла - возвращает None если файл не выбран"""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл tstsir.txt с данными защиты",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not file_path:
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                return None
                
            if not content.endswith('}}'):
                last_brace = content.rfind('}')
                if last_brace != -1:
                    content = content[:last_brace + 1]
            
            data = json.loads(content)
            
            guild_keep_data = data.get("result", {}).get("GuildKeepData", {})
            self.defense_data_full = guild_keep_data.get("MyKeepData", {}).get("DefenceData", {})
            self.opponent_data_full = guild_keep_data
            
            defenders = self.extract_defenders(self.defense_data_full, "наша")
            
            return defenders
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные защиты:\n{str(e)}")
            return None

    def extract_defenders(self, defense_data, defense_type="наша"):
        """Извлекает защитников из данных защиты"""
        defenders = []
        
        for location_key, location_data in defense_data.items():
            if isinstance(location_data, dict) and "Defenders" in location_data:
                defenders_list = location_data["Defenders"]
                
                if isinstance(defenders_list, list):
                    for defender in defenders_list:
                        if isinstance(defender, dict):
                            defense_team = defender.get("DefenceTeam", {})
                            troops = defense_team.get("Troops", [])
                            weapon = None
                            class_code = defense_team.get("Class", "")
                            banner_id = defense_team.get("Banner", None)
                            
                            class_name = self.get_class_name(class_code)
                            banner_mana = self.get_banner_mana(banner_id) if banner_id else "—"
                            
                            full_team = troops.copy()
                            if weapon:
                                full_team.append(weapon)
                            
                            location_name = self.get_location_name(location_key, location_data)
                            
                            # Убедимся, что UserID - строка и без пробелов
                            user_id = str(defender.get("UserId", "")).strip()
                            
                            defender_data = {
                                "Name": defender.get("Name", ""),
                                "UserId": user_id,  # Используем очищенный UserID
                                "Team": full_team,
                                "Class": class_name,
                                "Banner": banner_mana,
                                "Location": location_name,
                                "DefenseType": defense_type
                            }
                            
                            print(f"DEBUG: Защитник {defender_data['Name']}, UserID: '{user_id}', Локация: {defender_data['Location']}")
                            
                            defenders.append(defender_data)
        return defenders

    def open_defense_map(self):
        """Открывает отдельное окно с картой защиты"""
        DefenseMapWindow(self)

    def open_opponent_defense(self):
        """Открывает окно с защитой противника"""
        if not self.opponent_data_full:
            messagebox.showinfo("Информация", "Данные защиты противника не загружены")
            return
            
        opponent_keep_data = self.opponent_data_full.get("OpponentKeepData", {})
        
        OpponentDefenseWindow(
            self, 
            opponent_keep_data,
            self.troop_id_to_name, 
            self.weapon_id_to_name, 
            self.location_mapping,
            self.class_code_to_name, 
            self.banner_id_to_mana
        )
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Верхняя панель
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))

        btn_refresh = tk.Button(
            top_frame,
            text="Загрузить данные\nзащиты из файла",
            width=20,
            command=self.refresh_defense_data,
            bg="lightgreen",
            font=("Arial", 10)
        )
        btn_refresh.pack(side="left", padx=5)

        # НОВАЯ КНОПКА - добавляем справа от существующей
        btn_create_defense = tk.Button(
            top_frame,
            text="Сформировать файл\nс данными защиты",
            width=20,
            command=self.open_create_defense_window,  # Этот метод создадим позже
            bg="lightblue",
            font=("Arial", 10)
        )
        btn_create_defense.pack(side="left", padx=5)
        
        btn_view_defense = tk.Button(
            top_frame,
            text="защита на карте",
            width=15,
            command=self.open_defense_map,
            bg="lightblue",
            font=("Arial", 10, "bold")
        )
        btn_view_defense.pack(side="left", padx=5)
        
        btn_view_opponent = tk.Button(
            top_frame,
            text="защита противника",
            width=20,
            command=self.open_opponent_defense,
            bg="lightcoral",
            font=("Arial", 10, "bold")
        )
        btn_view_opponent.pack(side="right", padx=5)
        
        self.status_label = tk.Label(top_frame, text="Данные защиты не загружены", fg="red")
        self.status_label.pack(side="left", padx=10)
        
        # Таблица
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True)
        
        self.setup_war_tree(table_frame)
        
        # ПЕРЕМЕСТИТЕ НАСТРОЙКУ СТИЛЕЙ СЮДА - ДО ВЫЗОВА load_players_list()
        self.war_tree.tag_configure('has_staff', background='#ffcccc')
        self.war_tree.tag_configure('not_in_guild', background='#ffffcc')
        
        # Теперь загружаем список игроков
        self.load_players_list()
        
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=(10, 0))

        btn_save_csv = tk.Button(
            bottom_frame,
            text="Сохранить как .csv",
            width=20,
            command=self.save_war_data_csv,
            bg="lightyellow",
            font=("Arial", 10, "bold")
        )
        btn_save_csv.pack(pady=5)

    def open_create_defense_window(self):
        """Открывает окно для формирования файла защиты"""
        CreateDefenseWindow(self)
    
    def refresh_defense_data(self):
        """Обновляет данные о защите"""
        defense_data = self.load_defense_data()
        if defense_data is not None:
            self.defense_data = defense_data
            print(f"DEBUG: Загружено {len(defense_data)} защитников")
            self.load_players_data()
        else:
            self.status_label.config(text="Файл не выбран", fg="red")
            print("DEBUG: Файл не выбран или ошибка загрузки")

    def load_players_list(self):
        """Загружает только список игроков без данных о защите"""
        self.war_tree.delete(*self.war_tree.get_children())
        
        total_players = len(self.player_data) if self.player_data else 0
        status_text = f"Защита: ?/{total_players}"
        self.status_label.config(text=status_text, fg="blue")
        
        if not self.player_data:
            return
            
        for idx, (user_id, data) in enumerate(self.player_data.items(), start=1):
            profile = data.get("result", {}).get("ProfileData", {})
            player_name = profile.get("Name", "Неизвестно")
            
            row = [
                str(idx),
                player_name,
                "❓ Неизвестно",
                "—",
                "",
                "",
                ""
            ]
            
            self.war_tree.insert("", "end", values=row)
        
        self.auto_resize_columns()

    def has_defense(self, user_id):
        """Проверяет, установлена ли защита у игрока"""
        if self.defense_data is None:
            return False, [], "", "", ""
            
        for defender in self.defense_data:
            if defender.get("UserId") == user_id:
                return True, defender.get("Team", []), defender.get("Location", ""), defender.get("Class", ""), defender.get("Banner", "")
        return False, [], "", "", ""
        
    def setup_war_tree(self, parent):
        """Настраивает таблицу для войны гильдий"""
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True)
        
        xscrollbar = ttk.Scrollbar(container, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        
        yscrollbar = ttk.Scrollbar(container)
        yscrollbar.pack(side="right", fill="y")
        
        columns = ["#", "Игрок", "Защита", "Команда защиты", "Класс", "Знамя", "Локация"]
        
        self.war_tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            height=20,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        
        self.war_tree.pack(fill="both", expand=True)
        
        xscrollbar.config(command=self.war_tree.xview)
        yscrollbar.config(command=self.war_tree.yview)
        
        column_config = {
            "#": {"width": 40, "anchor": "center", "minwidth": 40},
            "Игрок": {"width": 150, "anchor": "center", "minwidth": 100},
            "Защита": {"width": 100, "anchor": "center", "minwidth": 100},
            "Команда защиты": {"width": 250, "anchor": "center", "minwidth": 150},
            "Класс": {"width": 120, "anchor": "center", "minwidth": 80},
            "Знамя": {"width": 200, "anchor": "center", "minwidth": 120},
            "Локация": {"width": 100, "anchor": "center", "minwidth": 80}
        }
        
        for col in columns:
            if col == "#":
                self.war_tree.heading(col, text=col)
            else:
                self.war_tree.heading(col, text=col, 
                                    command=lambda c=col: self.sort_by_column(c, False))
            
            config = column_config.get(col, {})
            self.war_tree.column(col, **config)
    
    def sort_by_column(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#":
            return

        items = []
        for k in self.war_tree.get_children(''):
            value = self.war_tree.set(k, col)
            items.append((value, k))

        if col == "Защита":
            items.sort(key=lambda t: (t[0] != "✅ Да", t[0]), reverse=reverse)
        elif col == "Команда защиты":
            items.sort(key=lambda t: t[0].count('\n') if t[0] != "—" else -1, reverse=reverse)
        else:
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        
        for index, (_, k) in enumerate(items, start=1):
            self.war_tree.move(k, '', index)
        
        for idx, item in enumerate(self.war_tree.get_children(), start=1):
            values = list(self.war_tree.item(item)["values"])
            values[0] = str(idx)
            self.war_tree.item(item, values=values)
        
        for column in self.war_tree["columns"]:
            heading = self.war_tree.heading(column)
            if column == col:
                heading["text"] = heading["text"].split(" ↓")[0].split(" ↑")[0] + (" ↓" if reverse else " ↑")
            else:
                heading["text"] = heading["text"].split(" ↓")[0].split(" ↑")[0]
            if column != "#":
                self.war_tree.heading(column, 
                                    text=heading["text"],
                                    command=lambda c=column: self.sort_by_column(c, not reverse))
    
    def load_players_data(self):
        """Загружает данные игроков в таблицу"""
        print("DEBUG: Начинаем load_players_data()")
        print(f"DEBUG: player_data count: {len(self.player_data)}")
        print(f"DEBUG: defense_data count: {len(self.defense_data) if self.defense_data else 0}")
        
        self.war_tree.delete(*self.war_tree.get_children())
        
        # Если нет данных игроков, но есть данные защиты - показываем только защиту
        if not self.player_data and self.defense_data:
            print("DEBUG: Нет player_data, но есть defense_data - показываем только защиту")
            self.load_defense_only()
            return
            
        if not self.player_data:
            print("DEBUG: Нет никаких данных")
            return
            
        # ДЕБАГ: выводим все UserID из списка игроков
        print("DEBUG: UserID из списка игроков:")
        for user_id in self.player_data.keys():
            print(f"  '{user_id}'")
        
        self.war_tree.tag_configure('has_staff', background='#ffcccc')
        
        defense_count = 0
        total_players = len(self.player_data)
        
        # Создаем словарь для быстрого поиска защитников по UserId
        defenders_by_user_id = {}
        if self.defense_data:
            for defender in self.defense_data:
                user_id = defender.get("UserId")
                if user_id:
                    defenders_by_user_id[str(user_id)] = defender
                    # ДЕБАГ: выводим UserID из защиты
                    print(f"DEBUG: UserID из защиты: {user_id}")
        
        for idx, (user_id, data) in enumerate(self.player_data.items(), start=1):
            profile = data.get("result", {}).get("ProfileData", {})
            player_name = profile.get("Name", "Неизвестно")
            
            # Проверяем есть ли защита у этого игрока
            defender = defenders_by_user_id.get(user_id)
            
            if defender:
                defense_count += 1
                team = defender.get("Team", [])
                defense_location = defender.get("Location", "Неизвестно")
                defense_class = defender.get("Class", "")
                defense_banner = defender.get("Banner", "")
                
                # ДЕБАГ: выводим информацию о совпадении
                print(f"DEBUG: СОВПАДЕНИЕ! Игрок {player_name}, UserID: {user_id}, Локация: '{defense_location}'")
                
            else:
                team = []
                defense_location = "Нет защиты"
                defense_class = ""
                defense_banner = ""
                print(f"DEBUG: НЕТ защиты для {player_name}, UserID: {user_id}")
            
            team_display = self.format_items_display(team)
            
            has_staff = any(self.get_item_name(item_id) == "Жезл звезд" for item_id in team)
            
            row = [
                str(idx),
                player_name,
                "✅ Да" if defender else "❌ Нет",
                team_display,
                defense_class,
                defense_banner,
                defense_location
            ]
            
            tags = ('has_staff',) if has_staff else ()
            self.war_tree.insert("", "end", values=row, tags=tags)
        
        status_text = f"Защита: {defense_count}/{total_players}"
        
        if defense_count == 0:
            color = "red"
        elif defense_count == total_players:
            color = "green"
        elif defense_count >= total_players * 0.7:
            color = "green"
        elif defense_count >= total_players * 0.5:
            color = "orange"
        else:
            color = "red"
        
        self.status_label.config(text=status_text, fg=color)
        
        self.auto_resize_columns()

    def auto_resize_columns(self):
        """Автоматически подгоняет ширину колонок"""
        if not hasattr(self, 'war_tree') or not self.war_tree.get_children():
            return
        
        font = tk.font.Font()
        
        min_widths = {
            "#": 40,
            "Игрок": 150, 
            "Защита": 100,
            "Команда защиты": 250,
            "Класс": 120,
            "Знамя": 200,
            "Локация": 100
        }
        
        for col in self.war_tree["columns"]:
            if col == "Защита":
                self.war_tree.column(col, width=min_widths["Защита"])
            else:
                header_text = self.war_tree.heading(col)["text"].split(" ↓")[0].split(" ↑")[0]
                max_width = font.measure(header_text) + 30
                
                for row in self.war_tree.get_children():
                    value = self.war_tree.set(row, col)
                    if value:
                        width = font.measure(str(value)) + 20
                        
                        if col == "Команда защиты" and value != "—":
                            max_line_width = 0
                            for line in value.split('\n'):
                                line_width = font.measure(line) + 20
                                if line_width > max_line_width:
                                    max_line_width = line_width
                            width = max_line_width
                        
                        if width > max_width:
                            max_width = width
                
                if col in min_widths and max_width < min_widths[col]:
                    max_width = min_widths[col]
                
                if max_width > 400:
                    max_width = 400
                    
                self.war_tree.column(col, width=max_width)

    def load_defense_only(self):
        """Загружает только данные защиты без привязки к основным игрокам"""
        if not self.defense_data:
            return
            
        # Настраиваем стили для строк
        self.war_tree.tag_configure('has_staff', background='#ffcccc')
        
        defense_count = 0
        
        for defender in self.defense_data:
            defense_count += 1
            
            team = defender.get("Team", [])
            team_display = self.format_items_display(team)
            
            # Проверяем наличие "Жезл звезд"
            has_staff = any(self.get_item_name(item_id) == "Жезл звезд" for item_id in team)
            
            row = [
                str(defense_count),
                defender.get("Name", "Неизвестный игрок"),
                "✅ Да",  # Все из файла защиты имеют защиту
                team_display,
                defender.get("Class", ""),
                defender.get("Banner", ""),
                defender.get("Location", "Неизвестно")
            ]
            
            tags = ('has_staff',) if has_staff else ()
            self.war_tree.insert("", "end", values=row, tags=tags)
        
        status_text = f"Защита: {defense_count} игроков (только из файла)"
        self.status_label.config(text=status_text, fg="purple")
        
        # Автоматически подгоняем ширину колонок
        self.auto_resize_columns()

    def save_war_data_csv(self):
        """Сохраняет данные войны гильдий в CSV файл"""
        if not hasattr(self, 'war_tree') or not self.war_tree.get_children():
            messagebox.showwarning("Ошибка", "Нет данных для сохранения")
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
                
                headers = []
                for col in self.war_tree["columns"]:
                    header_text = self.war_tree.heading(col)["text"]
                    if "↑" in header_text or "↓" in header_text:
                        header_text = header_text.split()[0]
                    headers.append(header_text)
                writer.writerow(headers)
                
                for row_id in self.war_tree.get_children():
                    writer.writerow(self.war_tree.item(row_id)["values"])
                    
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

class CreateDefenseWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Формирование файла защиты")
        self.geometry("900x800")
        
        # Данные пользователя после авторизации
        self.user_data = None
        self.available_events = [5337, 5340, 5342, 5343, 5354]
        
        self.setup_ui()
        self.configure_treeview_style()

    def setup_ui(self):
        """Настройка интерфейса окна формирования защиты"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Формирование файла с данными защиты", 
            font=("Arial", 14, "bold"),
            fg="white",
            bg="navy"   # тёмный фон
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

        self.userid_entry = tk.Entry(left_frame, width=20, font=("Arial", 10))
        self.userid_entry.grid(row=0, column=1, padx=(0,5), pady=5, sticky="w")

        self.btn_get_username = tk.Button(
            left_frame,
            text="Получить Username",
            width=18,
            command=self.get_username_from_userid,
            bg="lightblue",
            font=("Arial", 9)
        )
        self.btn_get_username.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        ToolTip(userid_label, 
            "UserID игрока:\n"
            "1. Можно получить из основного окна программы\n"
            "2. Или через Charles Proxy в запросах\n"
            "3. Уникальный идентификатор игрока")

        # ----------------- Password -----------------
        password_label = tk.Label(left_frame, text="Password:", font=("Arial", 10))
        password_label.grid(row=1, column=0, padx=(0,10), pady=5, sticky="e")

        self.password_entry = tk.Entry(left_frame, width=20, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, padx=(0,5), pady=5, sticky="w")

        self.btn_auth = tk.Button(
            left_frame,
            text="Авторизироваться",
            width=18,
            command=self.authenticate,
            bg="lightgreen",
            font=("Arial", 9),
            state="disabled"
        )
        self.btn_auth.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        ToolTip(password_label,
            "Пароль аккаунта:\n"
            "1. В настройках игры (Settings)\n" 
            "2. Через Charles Proxy - смотреть в запросах\n"
            "3. Пароль от вашего аккаунта в игре")
                
       # ======= ПРАВАЯ ПАНЕЛЬ - ИНФОРМАЦИЯ ОБ АККАУНТЕ =======
        right_frame = tk.Frame(main_input_frame)
        right_frame.pack(side="right", fill="y")

        # Информация об аккаунте в компактном виде с рамкой и внешним отступом
        self.info_frame = tk.Frame(right_frame, relief="sunken", bd=1)
        self.info_frame.pack(padx=10, pady=5, fill="both")

        # Внутренний Frame для равномерного внутреннего отступа со всех сторон
        inner_info = tk.Frame(self.info_frame)
        inner_info.pack(padx=10, pady=10)  # <-- общий отступ сверху, снизу, слева, справа

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
        
        # Центральный фрейм для параметров войны (посередине)
        center_frame = tk.Frame(main_frame)
        center_frame.pack(pady=15, fill="x")

        # Фрейм для выбора параметров войны вместе с надписью
        self.war_params_frame = tk.Frame(center_frame)
        self.war_params_frame.pack()  # сверху в center_frame

        # Кнопка загрузки данных (под параметрами войны)
        self.btn_load_data = tk.Button(
            center_frame,
            text="Загрузить данные защиты",
            width=20,
            command=self.load_defense_data,
            bg="orange",
            font=("Arial", 10),
            state="disabled"
        )
              
        ToolTip(self.btn_load_data,
            "Загружает данные защиты для выбранного события и дня войны\n"
            "Данные будут включать расстановку войск и информацию о защите")
        
        # Область для результатов
        self.results_frame = tk.Frame(main_frame)
        self.results_frame.pack(fill="both", expand=True, pady=10)
        
        # Статус бар (в самом низу)
        self.status_label = tk.Label(
            main_frame,
            text="Введите UserID (ID)",
            font=("Arial", 9),
            fg="gray"
        )
        self.status_label.pack(pady=5)

    def get_username_from_userid(self):
        """Получает username по UserID"""
        user_id = self.userid_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Ошибка", "Введите UserID")
            return
        
        self.status_label.config(text="Получение username...", fg="blue")
        self.update()
        
        try:
            # Запрос для получения профиля по UserID
            payload = {
                "functionName": "get_hero_profile",
                "Id": user_id
            }
            
            response = requests.post(URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "result" not in data or "ProfileData" not in data["result"]:
                raise ValueError("Некорректный ответ сервера")
            
            profile = data["result"]["ProfileData"]
            username = profile.get("username", "")
            player_name = profile.get("Name", "Неизвестно")
            guild_name = profile.get("GuildName", "Без гильдии")
            
            if not username:
                raise ValueError("Username не найден в ответе")
            
            # Сохраняем username для дальнейшего использования
            self.username_from_profile = username
            
            # Обновляем UI в компактном виде
            self.username_label.config(text=f"Username: {username}", fg="green")
            self.player_label.config(text=f"Игрок: {player_name}", fg="blue")
            self.guild_label.config(text=f"Гильдия: {guild_name}", fg="blue")
            
            # Активируем кнопку проверки авторизации
            self.btn_auth.config(state="normal")
            
            self.status_label.config(text="Username получен! Теперь введи пароль для авторизации", fg="green")
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка получения username: {str(e)}", fg="red")
            messagebox.showerror("Ошибка", f"Не удалось получить username:\n{str(e)}")

    def authenticate(self):
        """Проверяет авторизацию с полученным username и введенным паролем"""
        if not hasattr(self, 'username_from_profile') or not self.username_from_profile:
            messagebox.showwarning("Ошибка", "Сначала получите username")
            return
        
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showwarning("Ошибка", "Введите пароль")
            return
        
        self.status_label.config(text="Авторизация...", fg="blue")  # Обновили текст
        self.update()
            
        try:
            # Проверяем авторизацию через get_guild_activity
            auth_payload = {
                "functionName": "get_guild_activity",
                "username": self.username_from_profile,
                "password": password
            }
            
            response = requests.post(URL, json=auth_payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Проверяем успешность авторизации
            if "result" not in data:
                raise ValueError("Некорректный ответ сервера")
            
            # Если есть ошибка в ответе
            if "error" in data:
                error_msg = data.get("error", "Неизвестная ошибка")
                raise ValueError(f"Ошибка авторизации: {error_msg}")
            
            # Если есть GuildActivityLog - авторизация успешна
            if "GuildActivityLog" in data["result"]:
                # Получаем полную информацию о профиле для отображения
                profile_payload = {
                    "functionName": "get_hero_profile",
                    "username": self.username_from_profile,
                    "password": password,
                    "Id": self.userid_entry.get().strip()
                }
                
                profile_response = requests.post(URL, json=profile_payload, timeout=10)
                profile_response.raise_for_status()
                profile_data = profile_response.json()
                
                if "result" in profile_data and "ProfileData" in profile_data["result"]:
                    profile = profile_data["result"]["ProfileData"]
                    player_name = profile.get("Name", "Неизвестно")
                    guild_name = profile.get("GuildName", "Без гильдии")
                    
                    # Сохраняем данные пользователя
                    self.user_data = {
                        "username": self.username_from_profile,
                        "password": password,
                        "player_name": player_name,
                        "guild_name": guild_name
                    }
                    
                    # Обновляем UI в компактном виде
                    self.auth_status_label.config(text="Статус: Авторизован ✅", fg="green")
                    
                    # Показываем параметры войны
                    self.setup_war_params_ui()
                    
                    # Показываем надпись и кнопку после успешной авторизации
                    self.btn_load_data.pack(pady=15)
                    self.btn_load_data.config(state="normal")  # активируем кнопку
                    
                    # Блокируем поля ввода
                    self.userid_entry.config(state="disabled")
                    self.password_entry.config(state="disabled")
                    self.btn_get_username.config(state="disabled")
                    self.btn_auth.config(state="disabled")
                    
                    self.status_label.config(text="Авторизация успешна!", fg="green")
                else:
                    raise ValueError("Не удалось получить данные профиля после авторизации")
            else:
                raise ValueError("Некорректный ответ сервера - нет GuildActivityLog")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                self.status_label.config(text="Ошибка авторизации: Неверный пароль", fg="red")
                self.auth_status_label.config(text="Статус: Ошибка авторизации ❌", fg="red")
            else:
                self.status_label.config(text=f"HTTP ошибка: {e.response.status_code}", fg="red")
            messagebox.showerror("Ошибка", f"Ошибка авторизации:\n{str(e)}")
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка авторизации: {str(e)}", fg="red")
            self.auth_status_label.config(text="Статус: Ошибка ❌", fg="red")
            messagebox.showerror("Ошибка", f"Не удалось авторизоваться:\n{str(e)}")

    def setup_war_params_ui(self):
        """Настраивает UI для выбора параметров войны после авторизации"""
        # Очищаем фрейм
        for widget in self.war_params_frame.winfo_children():
            widget.destroy()
        
        # ======== Надпись сверху ========
        war_label = tk.Label(
            self.war_params_frame,
            text="Выберите параметры войны гильдий:",
            font=("Arial", 10, "bold"),
            fg="darkblue",
            justify="center"
        )
        war_label.pack(pady=(0, 10))  # надпись выше параметров

        # Создаем контейнер для параметров войны (Event ID / War Day)
        params_container = tk.Frame(self.war_params_frame)
        params_container.pack()  # контейнер с параметрами

        # Выбор EventId
        event_label = tk.Label(params_container, text="Дата Войны гильдий:", font=("Arial", 10))
        event_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.event_var = tk.StringVar(value=str(self.available_events[-1]))
        event_combo = ttk.Combobox(params_container, textvariable=self.event_var, 
                                values=[str(e) for e in self.available_events],
                                state="readonly", width=12, font=("Arial", 10))
        event_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        ToolTip(event_label,
            "ID события войны гильдий:\n"
            "Доступные события: 5337, 5340, 5342, 5343, 5354\n"
            "Обычно выбирается последнее активное событие")
        
        # Выбор WarDay
        war_day_label = tk.Label(params_container, text="День войны:", font=("Arial", 10))
        war_day_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        self.war_day_var = tk.StringVar(value="1")
        war_day_combo = ttk.Combobox(params_container, textvariable=self.war_day_var,
                                values=["1", "2", "3", "4"],
                                state="readonly", width=8, font=("Arial", 10))
        war_day_combo.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        ToolTip(war_day_label,
            "День войны:\n"
            "1 - Первый день войны\n"
            "2 - Второй день войны\n" 
            "3 - Третий день войны\n"
            "4 - Четвертый день войны")

    def load_defense_data(self):
        """Загружает данные защиты"""
        if not self.user_data:
            messagebox.showwarning("Ошибка", "Сначала авторизуйтесь")
            return
        
        try:
            event_id = int(self.event_var.get())
            war_day = int(self.war_day_var.get()) - 1
            
            self.status_label.config(text="Загрузка данных защиты...", fg="blue")
            self.update()
            
            payload = {
                "functionName": "guild_wars_get_guild_keep_data",
                "username": self.user_data["username"],
                "password": self.user_data["password"],
                "EventId": event_id,
                "WarDay": war_day,
                "NumWars": 4
            }
            
            response = requests.post(URL, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Обрабатываем полученные данные
            self.process_defense_data(data, event_id, war_day)
            
            self.status_label.config(text="Данные загружены успешно!", fg="green")
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка загрузки: {str(e)}", fg="red")
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные защиты:\n{str(e)}")

    def process_defense_data(self, data, event_id, war_day):
        """Обрабатывает полученные данные защиты"""
        # Очищаем область результатов
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Создаем текстовое поле для отображения данных
        text_widget = tk.Text(self.results_frame, wrap="word", height=15)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Форматируем и выводим данные
        text_widget.insert("1.0", f"Данные защиты (Event: {event_id}, Day: {war_day}):\n")
        text_widget.insert("2.0", "=" * 50 + "\n")
        text_widget.insert("3.0", json.dumps(data, ensure_ascii=False, indent=2))
        
        # Делаем текстовое поле только для чтения
        text_widget.config(state="disabled")
        
        # Кнопка сохранения в файл
        btn_frame = tk.Frame(self.results_frame)
        btn_frame.pack(pady=5)
        
        btn_save = tk.Button(
            btn_frame,
            text="Сохранить в файл",
            command=lambda: self.save_to_file(data, event_id, war_day),
            bg="lightyellow",
            font=("Arial", 10)
        )
        btn_save.pack(pady=5, fill="x")
        
        # Кнопка копирования в буфер
        btn_copy = tk.Button(
            btn_frame,
            text="Копировать данные",
            command=lambda: self.copy_to_clipboard(data),
            bg="lightgreen",
            font=("Arial", 10)
        )
        btn_copy.pack(pady=5, fill="x")

    def save_to_file(self, data, event_id, war_day):
        """Сохраняет данные в файл"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"defense_data_event{event_id}_day{war_day}.txt"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"Данные сохранены в:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def copy_to_clipboard(self, data):
        """Копирует данные в буфер обмена"""
        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            self.clipboard_clear()
            self.clipboard_append(json_str)
            self.status_label.config(text="Данные скопированы в буфер обмена!", fg="green")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать данные:\n{str(e)}")

class OpponentDefenseWindow(BaseWindow):
    def __init__(self, parent, opponent_data, troop_id_to_name, weapon_id_to_name, location_mapping, class_code_to_name, banner_id_to_mana):
        super().__init__(parent)
        
        # Извлекаем название гильдии противника
        self.opponent_guild_name = self.extract_guild_name(opponent_data)
        self.title(f"Защита противника - {self.opponent_guild_name}")
        self.geometry("1600x700")

        self.opponent_data = opponent_data
        self.troop_id_to_name = troop_id_to_name
        self.weapon_id_to_name = weapon_id_to_name
        self.location_mapping = location_mapping
        self.class_code_to_name = class_code_to_name
        self.banner_id_to_mana = banner_id_to_mana
        
        # Для хранения направления сортировки
        self.sort_column = None
        self.sort_reverse = False
        
        # Извлекаем защитников противника
        self.defenders = self.extract_defenders()
        
        # Настройка интерфейса
        self.setup_ui()
        self.load_opponent_data()

        # Настройка стиля Treeview
        self.configure_treeview_style()

    def extract_guild_name(self, opponent_data):
        """Извлекает название гильдии противника из данных"""
        try:
            guild_data = opponent_data.get("GuildData", {})
            guild_name = guild_data.get("Name")
            
            if guild_name:
                return guild_name
                
            return "Неизвестная гильдия"
                    
        except Exception as e:
            print(f"Ошибка при извлечении названия гильдии: {e}")
            return "Неизвестная гильдия"
    
    def extract_defenders(self):
        """Извлекает защитников противника из данных"""
        defenders = []
        
        try:
            defense_data = self.opponent_data.get("DefenceData", {})
            
            print(f"Найдено {len(defense_data)} локаций в защите противника")
            
            for location, location_data in defense_data.items():
                if isinstance(location_data, dict) and "Defenders" in location_data:
                    defenders_list = location_data["Defenders"]
                    
                    if isinstance(defenders_list, list):
                        for defender in defenders_list:
                            if isinstance(defender, dict):
                                defense_team = defender.get("DefenceTeam", {})
                                troops = defense_team.get("Troops", [])
                                weapon = defense_team.get("Weapon", None)
                                class_code = defense_team.get("Class", "")
                                banner_id = defense_team.get("Banner", None)
                                
                                class_name = self.get_class_name(class_code)
                                banner_mana = self.get_banner_mana(banner_id) if banner_id else "—"
                                
                                full_team = troops.copy()
                                if weapon:
                                    full_team.append(weapon)
                                
                                location_name = self.get_location_name(location)
                                
                                defenders.append({
                                    "Name": defender.get("Name", ""),
                                    "NameCode": defender.get("NameCode", ""),
                                    "UserId": defender.get("UserId", ""),
                                    "Level": defender.get("Level", 0),
                                    "Team": full_team,
                                    "Class": class_name,
                                    "Banner": banner_mana,
                                    "Location": location_name,
                                    "IsGuardian": location_data.get("IsGuardian", False),
                                    "Restriction": location_data.get("Restriction", "")
                                })
            
        except Exception as e:
            print(f"Ошибка при извлечении защитников противника: {e}")
        
        return defenders
      
    def get_location_name(self, location_key):
        """Преобразует ключ локации в читаемое русское название на основе restriction"""
        defense_data = self.opponent_data.get("DefenceData", {})
        
        # Получаем данные локации
        location_data = defense_data.get(location_key, {})
        if isinstance(location_data, dict) and "Restriction" in location_data:
            restriction = location_data["Restriction"]
            return self.location_mapping.get(restriction, restriction)
        
        # Если restriction не найден, используем запасной вариант
        location_translation = {
            "Gate": "Ворота",
            "Palace": "Дворец"
        }
        
        # Для Rank локаций добавляем номер
        if location_key.startswith("Rank"):
            parts = location_key.replace("Rank", "").replace("Loc", " ")
            return f"Ранг {parts}"
        
        return location_translation.get(location_key, location_key)

    def get_class_name(self, class_code):
        """Получает русское название класса по classCode"""
        return self.class_code_to_name.get(class_code, class_code)
    
    def get_banner_mana(self, banner_id):
        """Получает информацию о мане знамени по ID"""
        return self.banner_id_to_mana.get(banner_id, f"ID:{banner_id}")
        
    def get_item_name(self, item_id):
        """Получает название предмета (войска или оружия) по ID"""
        troop_name = self.troop_id_to_name.get(str(item_id))
        if troop_name:
            return troop_name
            
        weapon_name = self.weapon_id_to_name.get(str(item_id))
        if weapon_name:
            return weapon_name
            
        return f"ID:{item_id}"
    
    def format_items_display(self, item_ids):
        """Форматирует список предметов с выделением 'Жезл звезд'"""
        if not item_ids:
            return "—"
        
        item_names = []
        for item_id in item_ids:
            item_name = self.get_item_name(item_id)
            if item_name == "Жезл звезд":
                item_names.append(f"🔥{item_name.upper()}🔥")
            else:
                item_names.append(item_name)
        
        formatted_text = ""
        for i in range(0, len(item_names), 4):
            line_items = item_names[i:i+4]
            formatted_text += ", ".join(line_items) + "\n"
        
        return formatted_text.strip()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок с названием гильдии противника
        title_label = tk.Label(
            main_frame, 
            text=f"Защита противника - {self.opponent_guild_name}", 
            font=("Arial", 16, "bold"), 
            fg="red"
        )
        title_label.pack(pady=10)
        
        # Таблица
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Прокрутка
        xscrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        
        yscrollbar = ttk.Scrollbar(table_frame)
        yscrollbar.pack(side="right", fill="y")
        
        # Колонки
        columns = ["#", "Игрок", "Команда защиты", "Класс", "Знамя", "Локация"]
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )
        
        self.tree.pack(fill="both", expand=True)
        
        # Настройка прокрутки
        xscrollbar.config(command=self.tree.xview)
        yscrollbar.config(command=self.tree.yview)
        
        # Настройка колонки с обработчиками сортировки
        column_config = {
            "#": {"width": 40, "anchor": "center", "minwidth": 40},
            "Игрок": {"width": 150, "anchor": "center", "minwidth": 100},
            "Команда защиты": {"width": 300, "anchor": "center", "minwidth": 150},
            "Класс": {"width": 120, "anchor": "center", "minwidth": 80},
            "Знамя": {"width": 200, "anchor": "center", "minwidth": 120},
            "Локация": {"width": 120, "anchor": "center", "minwidth": 80}
        }
        
        for col in columns:
            if col == "#":
                self.tree.heading(col, text=col)
            else:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
            
            config = column_config.get(col, {})
            self.tree.column(col, **config)
    
    def sort_by_column(self, col, reverse):
        """Сортирует таблицу по указанной колонке"""
        if col == "#":
            return

        items = []
        for k in self.tree.get_children(''):
            value = self.tree.set(k, col)
            items.append((value, k))

        if col == "Команда защиты":
            items.sort(key=lambda t: t[0].count('\n') if t[0] != "—" else -1, reverse=reverse)
        else:
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        
        for index, (_, k) in enumerate(items, start=1):
            self.tree.move(k, '', index)
        
        for idx, item in enumerate(self.tree.get_children(), start=1):
            values = list(self.tree.item(item)["values"])
            values[0] = str(idx)
            self.tree.item(item, values=values)
        
        for column in self.tree["columns"]:
            heading = self.tree.heading(column)
            if column == col:
                heading["text"] = heading["text"].split(" ↓")[0].split(" ↑")[0] + (" ↓" if reverse else " ↑")
            else:
                heading["text"] = heading["text"].split(" ↓")[0].split(" ↑")[0]
            if column != "#":
                self.tree.heading(column, 
                                text=heading["text"],
                                command=lambda c=column: self.sort_by_column(c, not reverse))
    
    def load_opponent_data(self):
        """Загружает данные противника в таблицу"""
        self.tree.delete(*self.tree.get_children())
        
        for idx, defender in enumerate(self.defenders, start=1):
            team_display = self.format_items_display(defender["Team"])
            
            row = [
                str(idx),
                defender["Name"],
                team_display,
                defender["Class"],
                defender["Banner"],
                defender["Location"]
            ]
            
            self.tree.insert("", "end", values=row)
        
        self.auto_resize_columns()

    def auto_resize_columns(self):
        """Автоматически подгоняет ширину колонок на основе содержимого"""
        if not hasattr(self, 'tree') or self.tree is None:
            return
        
        if not self.tree.get_children():
            return
        
        font = tk.font.Font()
        
        max_widths = {
            "#": 60,
            "Игрок": 200,
            "Команда защиты": 400,
            "Класс": 150,
            "Знамя": 300,
            "Локация": 150
        }
        
        for col in self.tree["columns"]:
            header_text = self.tree.heading(col)["text"].split(" ↓")[0].split(" ↑")[0]
            max_width = font.measure(header_text) + 30
            
            for row in self.tree.get_children():
                value = self.tree.set(row, col)
                if value:
                    width = font.measure(str(value)) + 20
                    
                    if col == "Команда защиты" and value != "—":
                        max_line_width = 0
                        for line in value.split('\n'):
                            line_width = font.measure(line) + 20
                            if line_width > max_line_width:
                                max_line_width = line_width
                        width = max_line_width
                    
                    if width > max_width:
                        max_width = width
            
            if col in max_widths and max_width > max_widths[col]:
                max_width = max_widths[col]
            
            self.tree.column(col, width=max_width)
        
        self.update()

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

        # НАСТРОЙКА СТИЛЯ ДО ВСЕХ ЭЛЕМЕНТОВ
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
        
            # Добавляем метод для запуска поиска питомцев
    def run_pet_search(self):
            if not self.results:
                messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
                return
            PetSearchWindow(self, self.results, self.show_guild, self.show_dophenek)

    def open_guild_members_window(self):
        """Открывает окно для получения ID гильдии"""
        GuildMembersWindow(self)

    def open_guild_war_window(self):
        """Открывает окно войны гильдий"""
        # Передаем пустой словарь, если results пуст
        player_data = self.results if self.results else {}
        GuildWarWindow(self, player_data, self.show_guild, self.show_dophenek)   

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

        self.tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))

    def toggle_guild_column(self):
        self.show_guild = not self.show_guild
        self.setup_columns()
        
        for user_id in self.tree.get_children():
            data = self.results.get(user_id)
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            values = [
                self.tree.item(user_id)["values"][0],
                user_id,
                profile.get("NameCode", ""),
                profile.get("Name", "")
            ]
            
            if self.show_dophenek:
                values.append(DOPHENEK_MAP.get(user_id, ""))
            if self.show_guild:
                values.append(profile.get("GuildName", ""))

            # В последней колонке всегда показываем крестик удаления
            values.append("❌")
            
            self.tree.item(user_id, values=values)
        
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )

    def toggle_dophenek_column(self):
        self.show_dophenek = not self.show_dophenek
        self.setup_columns()
        
        for user_id in self.tree.get_children():
            data = self.results.get(user_id)
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            values = [
                self.tree.item(user_id)["values"][0],
                user_id,
                profile.get("NameCode", ""),
                profile.get("Name", "")
            ]
            
            if self.show_dophenek:
                values.append(DOPHENEK_MAP.get(user_id, ""))
            if self.show_guild:
                values.append(profile.get("GuildName", ""))
                
            values.append("❌")  # Вместо "Удалить" ставим "❌"
            
            self.tree.item(user_id, values=values)
        
        # ИСПРАВЛЕНО: btn_toggle_dophenek вместо btn_show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )

    def update_tree_row(self, user_id, data):
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

    def start_fetch(self):
        user_ids = [uid.strip() for uid in self.text_userids.get("1.0", "end").splitlines() if uid.strip()]
        if not user_ids:
            messagebox.showwarning(translator.t("error"), translator.t("enter_userid_error"))
            return

        self.results.clear()
        self.tree.delete(*self.tree.get_children())
        self.deleted_stack.clear()
        self.btn_undo.config(state="disabled")

        threading.Thread(target=self.fetch_profiles, args=(user_ids,), daemon=True).start()

    def fetch_profiles(self, user_ids):
        for user_id in user_ids:
            if not self._running:
                break

            try:
                response = requests.post(URL, json={"functionName": "get_hero_profile", "Id": user_id})
                data = response.json()
                self.results[user_id] = data
                self.after(0, lambda uid=user_id, d=data: self.update_tree_row(uid, d))
            except Exception as e:
                print(f"Ошибка для {user_id}: {e}")

        self.after(0, lambda: [
            # ИСПРАВЛЕНО: активируем правильные кнопки
            self.btn_toggle_dophenek.config(state="normal"),
            self.btn_toggle_guild.config(state="normal"),
            self.btn_show_stats.config(state="normal"),
            self.btn_kingdom_power.config(state="normal"),
            self.btn_kingdom_levels.config(state="normal"),
            self.btn_troop_search.config(state="normal"),
            self.btn_pet_search.config(state="normal"),
            self.btn_guild_war.config(state="normal"),
            messagebox.showinfo(translator.t("success"), translator.t("data_loaded"))
        ])

    def open_stats_window(self):
        if not self.results:
            messagebox.showwarning("Ошибка", "Нет данных для отображения")
            return
        StatsWindow(self, self.results, list(self.results.keys()), 
                  self.show_dophenek, self.show_guild)

    def open_kingdom_power_window(self):
        if not self.results:
            messagebox.showwarning("Ошибка", "Нет данных для отображения")
            return
        KingdomPowerWindow(self, self.results, list(self.results.keys()), 
                      self.show_dophenek, self.show_guild)
        
    def open_kingdom_levels_window(self):
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили!")
            return
        KingdomLevelsWindow(self, self.results, list(self.results.keys()), 
                         self.show_dophenek, self.show_guild)    

    def run_troop_search(self):
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили!")
            return
        TroopSearchWindow(self, self.results, self.show_guild, self.show_dophenek)

    def on_click(self, event):
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
                
                self.update_row_numbers()
                
                self.btn_undo.config(state="normal")

    def undo_last_delete(self):
    
        if not self.deleted_stack:
            return
            
        user_id, data, values = self.deleted_stack.pop()
        self.results[user_id] = data
        
        # Восстанавливаем строку с "❌" в последней колонке
        new_values = values[:-1] + ["❌"]  # Заменяем последнее значение на "❌"
        self.tree.insert("", "end", iid=user_id, values=new_values)
        
        self.update_row_numbers()
        
        self.btn_undo.config(state="normal" if self.deleted_stack else "disabled")

    def update_row_numbers(self):
        for index, iid in enumerate(self.tree.get_children(), start=1):
            vals = list(self.tree.item(iid)["values"])
            vals[0] = index
            self.tree.item(iid, values=vals)

    def load_userids_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            self.text_userids.delete("1.0", "end")
            self.text_userids.insert("1.0", data)
            # Вызываем проверку состояния кнопки после загрузки
            self.check_start_button_state()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def save_current_userid_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for item in self.tree.get_children():
                    f.write(self.tree.item(item)["values"][1] + "\n")
            messagebox.showinfo("Успех", f"Список сохранён в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}")

    def save_table_columns_dialog(self):
        cols_to_choose = [col for col in self.columns if col != "Удалить"]
        dlg = ColumnsSelectDialog(self, cols_to_choose)
        self.wait_window(dlg)
        if dlg.result:
            self.save_table_as_csv(dlg.result)

    def save_table_as_csv(self, selected_columns):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(selected_columns)
                for row_id in self.tree.get_children():
                    row = self.tree.item(row_id)["values"]
                    row_dict = dict(zip(self.columns, row))
                    writer.writerow([row_dict[col] for col in selected_columns])
            messagebox.showinfo("Успех", f"Таблица сохранена в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_close(self):
        self._running = False
        self.destroy()

class ColumnsSelectDialog(BaseWindow):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Выберите столбцы для сохранения")
        self.columns = columns
        self.result = None

        self.vars = {}
        for col in columns:
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(self, text=col, variable=var)
            chk.pack(anchor="w", padx=10, pady=2)
            self.vars[col] = var

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        btn_ok = ttk.Button(btn_frame, text="OK", command=self.on_ok)
        btn_ok.pack(side="left", padx=5)
        btn_cancel = ttk.Button(btn_frame, text="Отмена", command=self.destroy)
        btn_cancel.pack(side="left", padx=5)

    def on_ok(self):
        self.result = [col for col, var in self.vars.items() if var.get()]
        self.destroy()

if __name__ == "__main__":
    app = ProfileFetcherApp()
    app.mainloop()