"""Версия приложения и информация о сборке"""

from datetime import datetime

# Версия приложения
VERSION = "1.0"

# Дата и время сборки
BUILD_DATE = "04.12.2025"
BUILD_TIME = datetime.now().strftime("%H:%M:%S")

# Полная информация о версии
def get_version_string():
    """Возвращает строку с версией и датой сборки"""
    return f"v{VERSION} ({BUILD_DATE} {BUILD_TIME})"

def get_version_info():
    """Возвращает словарь с информацией о версии"""
    return {
        "version": VERSION,
        "build_date": BUILD_DATE,
        "build_time": BUILD_TIME,
        "full_string": get_version_string()
    }

