# app/windows/stats_window.py
"""StatsWindow - статистика характеристик игроков"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import tkinter.font as tkfont
from PIL import Image, ImageTk
import requests
from io import BytesIO

from app.windows.base import BaseWindow
from app.config import DOPHENEK_MAP
from app.translation import translator

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
        
        self.setup_ui()
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
            justify="left",
            bg="#fff3cd",
            fg="#856404",
            font=("Arial", 10, "bold"),
            bd=1,
            relief="sunken",
            padx=10,
            pady=5
        )
        note_label.pack(pady=(0,10))
        note_label.pack(anchor="center")

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
            FIXED_GUILD_BONUSES["GuildTroopMagicBonus"],
            profile.get("TroopMagicBonus", 0),
            profile.get("RenownTroopMagicBonus", 0)
        ])
        spell_power = profile.get("SpellPower", 0)
        magic_str = f"{magic_base} + {spell_power}" if spell_power else f"{magic_base}"

        # Attack (Атака)
        attack_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopAttackBonus"],
            profile.get("TroopAttackBonus", 0),
            profile.get("RenownTroopAttackBonus", 0)
        ])
        attack_add = profile.get("Attack", 0)
        attack_str = f"{attack_base} + {attack_add}" if attack_add else f"{attack_base}"

        # Health (Жизнь)
        health_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopHealthBonus"],
            profile.get("TroopHealthBonus", 0),
            profile.get("RenownTroopHealthBonus", 0)
        ])
        health_add = profile.get("MaxHealth", 0)
        health_str = f"{health_base} + {health_add}" if health_add else f"{health_base}"

        # Armor (Броня)
        armor_base = sum([
            FIXED_GUILD_BONUSES["GuildTroopArmorBonus"],
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