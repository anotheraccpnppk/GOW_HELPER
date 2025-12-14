"""Система переводов для поддержки нескольких языков"""

class TranslationManager:
    """Менеджер переводов для поддержки нескольких языков"""
    
    def __init__(self):
        self.current_language = "ru"  # По умолчанию русский
        self.translations = {
            "ru": {
                # Основные элементы интерфейса
                "app_title": "Запрос профилей по UserId",
                "enter_userid": "Введите UserId (каждый с новой строки):",
                "load_list": "Загрузить список",
                "get_list": "Получить список",
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
                
                # Поиск питомцев (standalone)
                "pets_database": "База данных питомцев",
                "update_players_data": "Обновить данные игроков",
                "player_pets": "Питомцы игрока",
                "pets_list": "Список питомцев",
                "sorted_by": "отсортировано по",
                "search": "Поиск:",
                "pet_name": "Название питомца",
                "kingdom": "Королевство",
                "effect": "Эффект",
                "mana_color": "Цвет маны",
                "select_pet_to_view": "Выберите питомца для просмотра игроков",
                "players_with_pet": "Игроки с этим питомцем",
                "level": "Уровень",
                "ascension": "Возвышение",
                "amount": "Количество",
                "no": "Нет",
                "no_guild": "Без гильдии",
                "unknown": "Неизвестно",
                "select_player": "Выбор игрока",
                "select_player_prompt": "Выберите игрока:",
                "all_pets": "Все питомцы",
                "owned_only": "Только имеющиеся",
                "missing_only": "Только отсутствующие",
                "total_pets": "Всего питомцев",
                "max_level": "Макс. уровень",
                "missing": "Отсутствуют",
                "status": "Статус",
                "has": "Есть",
                "missing_status": "Отсутствует",
            },
            "en": {
                # Main interface elements
                "app_title": "Profile Request by UserId",
                "enter_userid": "Enter UserId (one per line):",
                "load_list": "Load list",
                "get_list": "Get list",
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
                
                # Pet search (standalone)
                "pets_database": "Pets Database",
                "update_players_data": "Update Players Data",
                "player_pets": "Player's Pets",
                "pets_list": "Pets List",
                "sorted_by": "sorted by",
                "search": "Search:",
                "pet_name": "Pet Name",
                "kingdom": "Kingdom",
                "effect": "Effect",
                "mana_color": "Mana Color",
                "select_pet_to_view": "Select a pet to view players",
                "players_with_pet": "Players with this pet",
                "level": "Level",
                "ascension": "Ascension",
                "amount": "Amount",
                "no": "No",
                "no_guild": "No Guild",
                "unknown": "Unknown",
                "select_player": "Select Player",
                "select_player_prompt": "Select Player:",
                "all_pets": "All Pets",
                "owned_only": "Owned Only",
                "missing_only": "Missing Only",
                "total_pets": "Total Pets",
                "max_level": "Max Level",
                "missing": "Missing",
                "status": "Status",
                "has": "Has",
                "missing_status": "Missing",
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

