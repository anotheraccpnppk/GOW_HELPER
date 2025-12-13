"""Базовый класс для всех окон"""

import tkinter as tk
from tkinter import ttk

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

