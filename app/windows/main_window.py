# app/windows/main_window.py
"""Главное окно приложения"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import threading
import csv
import requests

from app.config import URL, DOPHENEK_MAP
from app.translation import translator
from app.utils import ToolTip
from app.windows.guild_members import GuildMembersWindow
from app.windows.kingdom_levels import KingdomLevelsWindow
from app.windows.kingdom_power import KingdomPowerWindow
from app.windows.stats_window import StatsWindow
from app.windows.troop_search import TroopSearchWindow

class ColorSettingsWindow(tk.Toplevel):
    """Окно настройки цветов строк с цветовым кругом и ручным вводом"""
    
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.parent_window = parent
        self.callback = callback
        self.title("Настройка цветов строк")
        self.geometry("580x500")
        self.resizable(False, False)
        
        # Центрируем окно
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (580 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.transient(parent)
        self.grab_set()
        
        # Текущие цвета
        self.odd_color = '#e0e0e0'
        self.even_color = '#ffffff'
        
        self.init_ui()
    
    def init_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Секция предустановленных цветов
        preset_frame = tk.LabelFrame(main_frame, text="Быстрые пресеты", padx=10, pady=10)
        preset_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(preset_frame, text="Нажмите чтобы загрузить пресет:", 
                font=("Arial", 9)).pack(anchor="w", pady=(0, 8))
        
        presets = [
            ("⚪ Стандарт", "#e0e0e0", "#ffffff"),
            ("🔵 Голубой", "#e3f2fd", "#ffffff"),
            ("🟢 Зеленый", "#e8f5e9", "#ffffff"),
            ("🟡 Пастель", "#fff3e0", "#ffffff"),
            ("⚫ Темный", "#424242", "#616161")
        ]
        
        preset_buttons_frame = tk.Frame(preset_frame)
        preset_buttons_frame.pack(fill="x")
        
        for text, odd, even in presets:
            btn = tk.Button(
                preset_buttons_frame,
                text=text,
                width=11,
                height=1,
                command=lambda o=odd, e=even: self.load_preset(o, e)
            )
            btn.pack(side="left", padx=2, pady=2)
        
        # Предпросмотр текущих цветов с полями ввода
        preview_frame = tk.LabelFrame(main_frame, text="Текущие цвета", padx=10, pady=10)
        preview_frame.pack(fill="x", pady=(0, 15))
        
        preview_container = tk.Frame(preview_frame)
        preview_container.pack(fill="x", expand=True)
        
        # Нечетные строки (слева)
        left_column = tk.Frame(preview_container)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_column, text="Нечетные строки:", 
                font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.odd_preview_frame = tk.Frame(left_column, relief="solid", borderwidth=2)
        self.odd_preview_frame.pack(fill="x", pady=5)
        
        self.odd_preview = tk.Label(self.odd_preview_frame, text="Пример текста", 
                                   font=("Arial", 9), bg=self.odd_color,
                                   height=2)
        self.odd_preview.pack(fill="both", expand=True, padx=2, pady=2)
        
        odd_btn_frame = tk.Frame(left_column)
        odd_btn_frame.pack(fill="x", pady=(5, 0))
        
        # Поле ввода (шире)
        tk.Label(odd_btn_frame, text="#", font=("Arial", 9)).pack(side="left")
        self.odd_entry = tk.Entry(odd_btn_frame, width=14, font=("Arial", 9))
        self.odd_entry.insert(0, self.odd_color.lstrip('#'))
        self.odd_entry.pack(side="left", padx=(2, 5))
        
        # Зеленая галочка для подтверждения
        tk.Button(odd_btn_frame, text="✓", width=3,
                 command=lambda: self.apply_manual_color('odd'),
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        
        # Кнопка выбора из цветового круга
        tk.Button(odd_btn_frame, text="Выбрать...", width=10,
                 command=self.choose_odd_color).pack(side="left")
        
        # Четные строки (справа)
        right_column = tk.Frame(preview_container)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_column, text="Четные строки:", 
                font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.even_preview_frame = tk.Frame(right_column, relief="solid", borderwidth=2)
        self.even_preview_frame.pack(fill="x", pady=5)
        
        self.even_preview = tk.Label(self.even_preview_frame, text="Пример текста", 
                                    font=("Arial", 9), bg=self.even_color,
                                    height=2)
        self.even_preview.pack(fill="both", expand=True, padx=2, pady=2)
        
        even_btn_frame = tk.Frame(right_column)
        even_btn_frame.pack(fill="x", pady=(5, 0))
        
        # Поле ввода (шире)
        tk.Label(even_btn_frame, text="#", font=("Arial", 9)).pack(side="left")
        self.even_entry = tk.Entry(even_btn_frame, width=14, font=("Arial", 9))
        self.even_entry.insert(0, self.even_color.lstrip('#'))
        self.even_entry.pack(side="left", padx=(2, 5))
        
        # Зеленая галочка для подтверждения
        tk.Button(even_btn_frame, text="✓", width=3,
                 command=lambda: self.apply_manual_color('even'),
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        
        # Кнопка выбора из цветового круга
        tk.Button(even_btn_frame, text="Выбрать...", width=10,
                 command=self.choose_even_color).pack(side="left")
        
        # Кнопка "Поменять местами" - компактная
        swap_frame = tk.Frame(main_frame)
        swap_frame.pack(fill="x", pady=(0, 15))
        
        tk.Button(swap_frame, text="↔ Поменять местами", 
                 width=20, command=self.swap_colors,
                 bg="#2196F3", fg="white", font=("Arial", 9)).pack()
        
        # Информационная панель - компактная
        info_frame = tk.LabelFrame(main_frame, text="Справка", padx=8, pady=6)
        info_frame.pack(fill="x", pady=(0, 15))
        
        info_text = "• Введите HEX код (fff или e0e0e0) и нажмите ✓ или Enter\n• Или нажмите 'Выбрать...' для цветового круга\n• Пресеты - для быстрого выбора"
        
        tk.Label(info_frame, text=info_text, justify="left", 
                font=("Arial", 8), bg="#f5f5f5").pack(anchor="w", padx=5, pady=2)
        
        # Кнопки управления окном
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=(5, 0), fill="x")
        
        # Применить ко всем окнам
        apply_btn = tk.Button(
            btn_frame,
            text="✅ Применить ко всем окнам",
            width=18,
            height=1,
            command=self.apply_colors,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold")
        )
        apply_btn.pack(side="left", padx=2, expand=True, fill="x")
        
        # Сбросить к стандарту
        reset_btn = tk.Button(
            btn_frame,
            text="↺ Сбросить",
            width=10,
            height=1,
            command=self.reset_to_default,
            bg="#FF9800",
            fg="white",
            font=("Arial", 9, "bold")
        )
        reset_btn.pack(side="left", padx=2, expand=True, fill="x")
        
        # Закрыть
        cancel_btn = tk.Button(
            btn_frame,
            text="✖ Закрыть",
            width=10,
            height=1,
            command=self.destroy,
            bg="#f44336",
            fg="white",
            font=("Arial", 9, "bold")
        )
        cancel_btn.pack(side="left", padx=2, expand=True, fill="x")
        
        # Привязываем Enter к полям ввода
        self.odd_entry.bind('<Return>', lambda e: self.apply_manual_color('odd'))
        self.even_entry.bind('<Return>', lambda e: self.apply_manual_color('even'))
        
        # Обновляем предпросмотр
        self.update_preview()
    
    def choose_odd_color(self):
        """Открывает цветовой круг для выбора цвета нечетных строк"""
        color = colorchooser.askcolor(
            title="Выберите цвет нечетных строк",
            initialcolor=self.odd_color,
            parent=self
        )
        if color[1]:
            self.odd_color = color[1]
            self.odd_entry.delete(0, tk.END)
            self.odd_entry.insert(0, self.odd_color.lstrip('#'))
            self.update_preview()
    
    def choose_even_color(self):
        """Открывает цветовой круг для выбора цвета четных строк"""
        color = colorchooser.askcolor(
            title="Выберите цвет четных строк",
            initialcolor=self.even_color,
            parent=self
        )
        if color[1]:
            self.even_color = color[1]
            self.even_entry.delete(0, tk.END)
            self.even_entry.insert(0, self.even_color.lstrip('#'))
            self.update_preview()
    
    def apply_manual_color(self, color_type):
        """Применяет цвет, введенный вручную"""
        try:
            if color_type == 'odd':
                hex_code = self.odd_entry.get().strip()
                if self.validate_hex(hex_code):
                    if not hex_code.startswith('#'):
                        hex_code = '#' + hex_code
                    self.odd_color = hex_code
                    self.odd_entry.delete(0, tk.END)
                    self.odd_entry.insert(0, hex_code.lstrip('#'))
                    self.update_preview()
                else:
                    self.odd_entry.delete(0, tk.END)
                    self.odd_entry.insert(0, self.odd_color.lstrip('#'))
            else:
                hex_code = self.even_entry.get().strip()
                if self.validate_hex(hex_code):
                    if not hex_code.startswith('#'):
                        hex_code = '#' + hex_code
                    self.even_color = hex_code
                    self.even_entry.delete(0, tk.END)
                    self.even_entry.insert(0, hex_code.lstrip('#'))
                    self.update_preview()
                else:
                    self.even_entry.delete(0, tk.END)
                    self.even_entry.insert(0, self.even_color.lstrip('#'))
        except:
            pass
    
    def validate_hex(self, hex_code):
        """Проверяет корректность HEX кода (с # или без)"""
        if hex_code.startswith('#'):
            hex_code = hex_code[1:]
        
        if len(hex_code) not in (3, 6):
            return False
        
        try:
            int(hex_code, 16)
            return True
        except ValueError:
            return False
    
    def update_preview(self):
        """Обновляет предпросмотр цветов"""
        self.odd_preview.config(bg=self.odd_color)
        self.even_preview.config(bg=self.even_color)
        
        def get_text_color(bg_color):
            try:
                hex_color = bg_color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join([c*2 for c in hex_color])
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                return "black" if brightness > 128 else "white"
            except:
                return "black"
        
        self.odd_preview.config(fg=get_text_color(self.odd_color))
        self.even_preview.config(fg=get_text_color(self.even_color))
    
    def load_preset(self, odd_color, even_color):
        """Загружает пресет цветов"""
        self.odd_color = odd_color
        self.even_color = even_color
        
        self.odd_entry.delete(0, tk.END)
        self.odd_entry.insert(0, odd_color.lstrip('#'))
        self.even_entry.delete(0, tk.END)
        self.even_entry.insert(0, even_color.lstrip('#'))
        
        self.update_preview()
    
    def swap_colors(self):
        """Меняет цвета местами"""
        self.odd_color, self.even_color = self.even_color, self.odd_color
        
        self.odd_entry.delete(0, tk.END)
        self.odd_entry.insert(0, self.odd_color.lstrip('#'))
        self.even_entry.delete(0, tk.END)
        self.even_entry.insert(0, self.even_color.lstrip('#'))
        
        self.update_preview()
    
    def reset_to_default(self):
        """Сбрасывает к стандартным цветам"""
        self.load_preset("#e0e0e0", "#ffffff")
    
    def apply_colors(self):
        """Применяет выбранные цвета ко всем окнам"""
        if self.callback:
            self.callback(self.odd_color, self.even_color)
        
        self.destroy()

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
        
        # Цвета по умолчанию (более темный серый)
        self.odd_color = '#e0e0e0'
        self.even_color = '#ffffff'
        
        # Переменная для отслеживания активного виджета прокрутки
        self.active_scroll_widget = None
        
        translator.register_callback(self.update_ui_texts)
        
        self.update_columns()
        self.setup_ui()
        self.configure_treeview_style()
        
        # Инициализируем счетчики
        self.after(200, self.update_counters)
    
    def update_columns(self):
        """Обновляет список колонок в зависимости от языка и настроек"""
        self.base_columns = ["#", "UserId", translator.t("Invite code"), translator.t("column_player")]
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
            
            # Добавляем теги для чередования цветов строк
            style.map('Treeview', background=[('selected', '#347083')])
        except Exception as e:
            print(f"Ошибка настройки стиля главного окна: {e}")
    
    def change_language(self, lang):
        """Переключает язык интерфейса"""
        translator.set_language(lang)
        self.lang_var.set(lang)
    
    def update_ui_texts(self):
        """Обновляет все текстовые элементы интерфейса при смене языка"""
        try:
            self.title(translator.t("app_title"))
            
            # Обновляем кнопки (ТЕПЕРЬ БУДУТ РАБОТАТЬ!)
            if hasattr(self, 'btn_load_userid'):
                self.btn_load_userid.config(text=translator.t("load_list"))
            if hasattr(self, 'btn_get_userid'):
                self.btn_get_userid.config(text=translator.t("get_list"))
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
            
            # Обновляем заголовки полей ввода
            if hasattr(self, 'left_frame'):
                self.left_frame.config(text="Invite Code")
            if hasattr(self, 'right_frame'):
                self.right_frame.config(text="User ID")
            
            self.update_columns()
            if hasattr(self, 'tree'):
                self.setup_columns()
        except Exception as e:
            print(f"Ошибка обновления интерфейса: {e}")
    
    def open_color_settings(self):
        """Открывает окно настройки цветов строк"""
        # Открываем окно настроек с callback для мгновенного обновления
        ColorSettingsWindow(self, callback=self.update_table_colors)
    
    def update_table_colors(self, odd_color, even_color):
        """Обновляет цвета строк в таблице (вызывается из ColorSettingsWindow)"""
        # Сохраняем новые цвета
        self.odd_color = odd_color
        self.even_color = even_color
        
        # Обновляем теги в Treeview
        self.tree.tag_configure('oddrow', background=odd_color)
        self.tree.tag_configure('evenrow', background=even_color)
        
        # Применяем новые теги ко всем строкам
        for index, child in enumerate(self.tree.get_children(), start=1):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            current_tags = list(self.tree.item(child, 'tags') or [])
            
            # Удаляем старые теги чередования
            current_tags = [t for t in current_tags if t not in ('oddrow', 'evenrow')]
            current_tags.append(tag)
            
            self.tree.item(child, tags=current_tags)
    
    def set_active_scroll_widget(self, widget):
        """Устанавливает активный виджет для прокрутки колесиком мыши"""
        self.active_scroll_widget = widget
    
    def on_mousewheel(self, event):
        """Обработчик колесика мыши - прокручивает активный виджет"""
        if self.active_scroll_widget:
            # Определяем направление прокрутки
            if event.delta > 0:
                self.active_scroll_widget.yview_scroll(-1, "units")
            else:
                self.active_scroll_widget.yview_scroll(1, "units")
    
    def update_counters(self, event=None):
        """Обновляет счетчики непустых строк"""
        # Обновляем кнопку "Начать"
        self.check_start_button_state()
        
        # Получаем текст из обоих полей
        userid_text = self.text_userids.get("1.0", "end-1c")
        invitecode_text = self.text_invitecodes.get("1.0", "end-1c")
        
        # Подсчитываем количество непустых строк
        userid_lines = [line for line in userid_text.split('\n') if line.strip()]
        invitecode_lines = [line for line in invitecode_text.split('\n') if line.strip()]
        
        userid_count = len(userid_lines)
        invitecode_count = len(invitecode_lines)
        
        # Обновляем счетчики
        self.userid_counter.config(text=f"User ID: {userid_count}")
        self.invitecode_counter.config(text=f"Invite Code: {invitecode_count}")
        
        # Обновляем кнопку "Начать" - активна если есть хотя бы в одном поле данные
        has_data = (userid_count > 0) or (invitecode_count > 0)
        
        if hasattr(self, 'btn_start'):
            if has_data:
                self.btn_start.config(state="normal")
            else:
                self.btn_start.config(state="disabled")
        
        return "break"
        
    def setup_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Верхняя панель с переключателем языка и кнопкой настроек цветов
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
        lang_menu.pack(side="left", padx=(0, 10))
        
        # Кнопка настроек цветов с красивым оформлением
        color_icon = "🎨"
        self.btn_color_settings = tk.Button(
            top_bar,
            text=f"{color_icon} Цвет строк",
            command=self.open_color_settings,
            width=15,
            height=1,
            bg="#4A90E2",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="raised",
            cursor="hand2",
            bd=2,
            activebackground="#357ABD",
            activeforeground="white"
        )
        self.btn_color_settings.pack(side="right", padx=(0, 10))
        
        # Всплывающая подсказка
        ToolTip(self.btn_color_settings, text="Настройка цветов строк во всех таблицах")

        # Контейнер для двух полей ввода
        input_container = tk.Frame(main_frame)
        input_container.pack(fill="x", padx=10, pady=(10, 0))
        
        # Левая часть - Invite Code
        left_frame = tk.LabelFrame(input_container, text="Invite Code", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Текстовое поле для Invite Code
        invitecode_container = tk.Frame(left_frame)
        invitecode_container.pack(fill="both", expand=True)
        
        self.text_invitecodes = tk.Text(invitecode_container, 
                                        height=10,
                                        font=("Arial", 9),
                                        wrap="none",
                                        bd=1,
                                        relief="solid",
                                        padx=5,
                                        pady=5)
        self.text_invitecodes.pack(side="left", fill="both", expand=True)
        
        # Скроллбар для Invite Code
        invitecode_scrollbar = ttk.Scrollbar(invitecode_container, orient="vertical")
        invitecode_scrollbar.pack(side="right", fill="y")
        
        self.text_invitecodes.config(yscrollcommand=invitecode_scrollbar.set)
        invitecode_scrollbar.config(command=self.text_invitecodes.yview)
        
        # Счетчик для Invite Code
        invitecode_counter_frame = tk.Frame(left_frame)
        invitecode_counter_frame.pack(fill="x", pady=(5, 0))
        
        self.invitecode_counter = tk.Label(invitecode_counter_frame, 
                                          text="Invite Code: 0", 
                                          font=("Arial", 9, "bold"),
                                          fg="#333333")
        self.invitecode_counter.pack(side="left")
        
        # Правая часть - User ID
        right_frame = tk.LabelFrame(input_container, text="User ID", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Текстовое поле для User ID
        userid_container = tk.Frame(right_frame)
        userid_container.pack(fill="both", expand=True)
        
        self.text_userids = tk.Text(userid_container, 
                                    height=10,
                                    font=("Arial", 9),
                                    wrap="none",
                                    bd=1,
                                    relief="solid",
                                    padx=5,
                                    pady=5)
        self.text_userids.pack(side="left", fill="both", expand=True)
        
        # Скроллбар для User ID
        userid_scrollbar = ttk.Scrollbar(userid_container, orient="vertical")
        userid_scrollbar.pack(side="right", fill="y")
        
        self.text_userids.config(yscrollcommand=userid_scrollbar.set)
        userid_scrollbar.config(command=self.text_userids.yview)
        
        # Счетчик для User ID
        userid_counter_frame = tk.Frame(right_frame)
        userid_counter_frame.pack(fill="x", pady=(5, 0))
        
        self.userid_counter = tk.Label(userid_counter_frame, 
                                      text="User ID: 0", 
                                      font=("Arial", 9, "bold"),
                                      fg="#333333")
        self.userid_counter.pack(side="left")
        
        # Привязываем события для обновления счетчиков
        self.text_userids.bind('<KeyRelease>', self.update_counters)
        self.text_invitecodes.bind('<KeyRelease>', self.update_counters)
        
        # Привязываем события входа/выхода курсора для определения активного виджета
        self.text_userids.bind('<Enter>', lambda e: self.set_active_scroll_widget(self.text_userids))
        self.text_userids.bind('<Leave>', lambda e: self.set_active_scroll_widget(None))
        self.text_invitecodes.bind('<Enter>', lambda e: self.set_active_scroll_widget(self.text_invitecodes))
        self.text_invitecodes.bind('<Leave>', lambda e: self.set_active_scroll_widget(None))
        
        # Главный фрейм для кнопок
        main_buttons_frame = tk.Frame(main_frame)
        main_buttons_frame.pack(pady=10, fill="x", padx=10)

        # Утопленный фрейм для кнопок
        sunken_frame = tk.Frame(main_buttons_frame, relief="sunken", bd=1)
        sunken_frame.pack(side="left", padx=(0, 10), pady=5)

        # Левый столбик кнопок внутри утопленного фрейма
        left_column = tk.Frame(sunken_frame)
        left_column.pack(side="left", fill="y", padx=(5, 10), pady=5)

        # Переименованные кнопки
        self.btn_load_userid = ttk.Button(left_column, text=translator.t("load_list"), 
                command=self.load_userids_from_file, width=18)
        self.btn_load_userid.pack(pady=2)
        
        self.btn_get_userid = ttk.Button(left_column, text=translator.t("get_list"), 
                command=self.open_guild_members_window, width=18)
        self.btn_get_userid.pack(pady=2)

        # Кнопка "Начать" справа от столбика
        self.btn_start = ttk.Button(sunken_frame, text=translator.t("start"), 
                                    command=self.start_fetch, width=12, state="disabled")
        self.btn_start.pack(side="left", padx=(10, 5), pady=5)

        # Утопленный фрейм для кнопок "Показать доп. имя" и "Показать гильдию"
        sunken_toggle_frame = tk.Frame(main_buttons_frame, relief="sunken", bd=1)
        sunken_toggle_frame.pack(side="left", padx=(20, 10), pady=5)

        self.btn_toggle_dophenek = ttk.Button(sunken_toggle_frame, 
                                            text=translator.t("show_dophenek"), 
                                            command=self.toggle_dophenek_column, state="disabled", width=18)
        self.btn_toggle_dophenek.pack(pady=2)

        self.btn_toggle_guild = ttk.Button(sunken_toggle_frame, 
                                        text=translator.t("show_guild"), 
                                        command=self.toggle_guild_column, state="disabled", width=18)
        self.btn_toggle_guild.pack(pady=2)

        # Правый блок всех кнопок
        sunken_right_frame = tk.Frame(main_buttons_frame, relief="sunken", bd=1)
        sunken_right_frame.pack(side="left", padx=5, pady=5)

        inner_right = tk.Frame(sunken_right_frame)
        inner_right.pack(padx=5, pady=5)

        # Кнопка "Окно статов"
        col_stats = tk.Frame(inner_right)
        col_stats.pack(side="left", padx=5, fill="y")

        self.btn_show_stats = ttk.Button(col_stats, text=translator.t("stats_window"), 
                                        command=self.open_stats_window, state="disabled", width=18)
        self.btn_show_stats.pack(expand=True)

        # Столбик — уровни королевств / мощь королевств
        col_kingdoms = tk.Frame(inner_right)
        col_kingdoms.pack(side="left", padx=5, fill="y")

        self.btn_kingdom_levels = ttk.Button(col_kingdoms, text=translator.t("kingdom_levels"), 
                                            command=self.open_kingdom_levels_window, state="disabled", width=18)
        self.btn_kingdom_levels.pack(pady=2)

        self.btn_kingdom_power = ttk.Button(col_kingdoms, text=translator.t("kingdom_power"), 
                                            command=self.open_kingdom_power_window, state="disabled", width=18)
        self.btn_kingdom_power.pack(pady=2)

        # Столбик - Поиск
        col_search = tk.Frame(inner_right)
        col_search.pack(side="left", fill="y", padx=5)

        self.btn_troop_search = ttk.Button(col_search, text=translator.t("troop_search"), 
                                        command=self.run_troop_search, state="disabled", width=18)
        self.btn_troop_search.pack(pady=2)

        self.btn_pet_search = ttk.Button(col_search, text=translator.t("pet_search"),
                                        command=self.run_pet_search, state="normal" if self.results else "disabled", width=18)
        self.btn_pet_search.pack(pady=2)

        # Кнопка "Война гильдий"
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

        # Таблица с цветами строк
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
        
        # Добавляем теги для чередования цветов строк
        self.tree.tag_configure('oddrow', background=self.odd_color)
        self.tree.tag_configure('evenrow', background=self.even_color)
        
        self.tree.bind("<Button-1>", self.on_click)
        
        # Привязываем события входа/выхода для таблицы
        self.tree.bind('<Enter>', lambda e: self.set_active_scroll_widget(self.tree))
        self.tree.bind('<Leave>', lambda e: self.set_active_scroll_widget(None))
        
        # Привязываем колесико мыши ко всему окну
        self.bind_all("<MouseWheel>", self.on_mousewheel)
        self.bind_all("<Button-4>", self.on_mousewheel)  # Linux
        self.bind_all("<Button-5>", self.on_mousewheel)  # Linux
        
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
        
        # Изначальная проверка состояния кнопки
        self.after(100, self.update_counters)

    def check_start_button_state(self, event=None):
        """Обновлен для работы с двумя полями"""
        # Теперь логика в update_counters
        pass
    
    def run_pet_search(self):
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        
        # Используйте абсолютный импорт как у вас везде
        from app.windows.pet_search import PetSearchWindow  # <-- вот так
        
        # Открываем основное окно поиска питомцев
        PetSearchWindow(self, self.results, self.show_guild, self.show_dophenek)

    def open_guild_members_window(self):
        """Открывает окно для получения ID гильдии"""
        GuildMembersWindow(self)

  
    def open_stats_window(self):
        """Открывает окно статистики"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        StatsWindow(self, self.results, list(self.results.keys()), 
                   self.show_dophenek, self.show_guild)

    def open_kingdom_levels_window(self):
        """Открывает окно уровней королевств"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        KingdomLevelsWindow(self, self.results, list(self.results.keys()), 
                          self.show_dophenek, self.show_guild)

    def open_kingdom_power_window(self):
        """Открывает окно мощи королевств"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        KingdomPowerWindow(self, self.results, list(self.results.keys()), 
                         self.show_dophenek, self.show_guild)

    def run_troop_search(self):
        """Запускает окно поиска войск"""
        if not self.results:
            messagebox.showwarning("Ошибка", "Сначала загрузите профили игроков!")
            return
        
        TroopSearchWindow(
            self, 
            self.results, 
            show_guild=self.show_guild, 
            show_dophenek=self.show_dophenek
        )

    def open_guild_war_window(self):
        """Открывает окно войны гильдий"""
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
                self.tree.column(col, width=70, minwidth=70, anchor="center", stretch=False)
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
            new_values = [index] + values[1:]
            self.tree.item(k, values=new_values)
            self.tree.move(k, '', index)
            
            # Обновляем тег для чередования цветов
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.item(k, tags=(tag,))

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
        
        if col_index == len(self.tree["columns"]) - 1:
            if messagebox.askyesno("Подтверждение", "Удалить эту строку?"):
                self.deleted_stack.append((row_id, self.results.get(row_id), self.tree.item(row_id)["values"]))
                
                if row_id in self.results:
                    del self.results[row_id]
                self.tree.delete(row_id)
                
                for idx, child in enumerate(self.tree.get_children(), start=1):
                    values = list(self.tree.item(child)["values"])
                    values[0] = idx
                    
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    self.tree.item(child, values=values, tags=(tag,))
                
                self.btn_undo.config(state="normal" if self.deleted_stack else "disabled")

    def update_row_numbers(self):
        """Обновляет номера строк в таблице"""
        for index, iid in enumerate(self.tree.get_children(), start=1):
            vals = list(self.tree.item(iid)["values"])
            vals[0] = index
            self.tree.item(iid, values=vals)

    def start_fetch(self):
        """Начинает загрузку профилей - теперь из двух полей"""
        # Собираем данные из обоих полей
        user_ids = [uid.strip() for uid in self.text_userids.get("1.0", "end").splitlines() if uid.strip()]
        invite_codes = [code.strip() for code in self.text_invitecodes.get("1.0", "end").splitlines() if code.strip()]
        
        if not user_ids and not invite_codes:
            messagebox.showwarning("Ошибка", "Введите хотя бы один UserID или Invite Code")
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

        # Запускаем загрузку для User ID
        if user_ids:
            threading.Thread(target=self.fetch_profiles_by_userid, args=(user_ids,), daemon=True).start()
        
        # TODO: Добавить загрузку по Invite Code когда будет реализовано
        if invite_codes:
            messagebox.showinfo("Информация", f"Загрузка по {len(invite_codes)} Invite Code будет добавлена позже")
        
        # Обновляем счетчики
        self.update_counters()

    def fetch_profiles_by_userid(self, user_ids):
        """Загружает профили по User ID"""
        for index, user_id in enumerate(user_ids):
            if not self._running:
                break
            try:
                response = requests.post(URL, json={"functionName": "get_hero_profile", "Id": user_id}, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.results[user_id] = data
                
                tag = 'evenrow' if (index + 1) % 2 == 0 else 'oddrow'
                self.after(0, lambda uid=user_id, d=data, t=tag: self.update_tree_row(uid, d, t))
            except Exception as e:
                print(f"Ошибка для {user_id}: {e}")

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

    def update_tree_row(self, user_id, data, tag):
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
            
        values.append("❌")
        
        self.tree.insert("", "end", iid=user_id, values=values, tags=(tag,))

    def toggle_dophenek_column(self):
        """Переключает отображение колонки доп. имени"""
        self.show_dophenek = not self.show_dophenek
        self.btn_toggle_dophenek.config(
            text="Скрыть доп. имя" if self.show_dophenek else "Показать доп. имя"
        )
        
        self.update_columns()
        self.setup_columns()
        self.update_table_data()

    def toggle_guild_column(self):
        """Переключает отображение колонки гильдии"""
        self.show_guild = not self.show_guild
        self.btn_toggle_guild.config(
            text="Скрыть гильдию" if self.show_guild else "Показать гильдию"
        )
        
        self.update_columns()
        self.setup_columns()
        self.update_table_data()

    def update_table_data(self):
        """Обновляет данные в таблице"""
        for index, user_id in enumerate(self.tree.get_children(), start=1):
            data = self.results.get(user_id)
            if not data:
                continue
                
            profile = data.get("result", {}).get("ProfileData", {})
            row_num = index
            
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
            
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.item(user_id, values=values, tags=(tag,))

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
            
            # Обновляем счетчики после загрузки файла
            self.update_counters()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

    def undo_last_delete(self):
        """Отменяет последнее удаление"""
        if not self.deleted_stack:
            return
            
        user_id, data, values = self.deleted_stack.pop()
        self.results[user_id] = data
        
        row_num = len(self.tree.get_children()) + 1
        values = [row_num] + values[1:]
        
        tag = 'evenrow' if row_num % 2 == 0 else 'oddrow'
        self.tree.insert("", "end", iid=user_id, values=values, tags=(tag,))
        
        self.update_row_numbers()
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
                
                writer.writerow(selected_columns)
                
                for item in self.tree.get_children():
                    values = self.tree.item(item)["values"]
                    row_dict = dict(zip(self.columns, values))
                    
                    row = [row_dict[col] for col in selected_columns]
                    writer.writerow(row)
                    
            messagebox.showinfo("Успех", f"Данные сохранены в {file_path}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")