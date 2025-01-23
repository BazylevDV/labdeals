import requests

# Базовый URL вашего Django-сервера
BASE_URL = 'http://127.0.0.1:8000/api/'

def get_equipment_data():
    """
    Получает данные об оборудовании из API Django.
    """
    response = requests.get(f'{BASE_URL}equipment/')
    if response.status_code == 200:
        return response.json()
    return None

def get_liquidation_file():
    """
    Получает данные о файлах ликвидации из API Django.
    """
    response = requests.get(f'{BASE_URL}liquidation-files/')
    if response.status_code == 200:
        return response.json()
    return None