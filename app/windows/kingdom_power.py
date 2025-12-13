# app/windows/kingdom_power.py
"""KingdomPower window - мощь королевств"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import tkinter.font as tkfont

from app.windows.base import BaseWindow
from app.config import DOPHENEK_MAP
from app.translation import translator

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