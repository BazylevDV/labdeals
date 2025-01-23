import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
from aiogram import types
from aiogram.types import FSInputFile
from handlers import (
    start,
    about_us,
    equipment,
    send_equipment_info,
    send_tests_menu,  # Обновленный импорт
    liquidation,
    back_to_main_menu,
    register_handlers,
)
from main import dp, send_liquidation_file
import logging



# Настройка логирования для тестов
logging.basicConfig(level=logging.INFO)

# Мокируем объект бота
@pytest.fixture
def mock_bot():
    return AsyncMock()

# Мокируем объект сообщения
@pytest.fixture
def mock_message():
    message = AsyncMock()
    message.from_user.id = 123
    message.from_user.username = "test_user"
    message.text = "test"
    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()
    message.answer_document = AsyncMock()
    return message

# Тест для команды /start
@pytest.mark.asyncio
async def test_start(mock_message):
    await start(mock_message)
    mock_message.answer.assert_called_once()
    assert "Добро пожаловать в ЛабторгБот!" in mock_message.answer.call_args[0][0]

# Тест для кнопки "О нас"
@pytest.mark.asyncio
async def test_about_us(mock_message):
    with patch("builtins.open", MagicMock()) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "Тестовая информация о нас."
        await about_us(mock_message)
        mock_message.answer.assert_called_once()
        assert "О нас:" in mock_message.answer.call_args[0][0]

# Тест для кнопки "Бесплатное оборудование"
@pytest.mark.asyncio
async def test_equipment(mock_message):
    await equipment(mock_message)
    mock_message.answer.assert_called_once()
    assert "Выберите оборудование:" in mock_message.answer.call_args[0][0]

# Тест для отправки информации об оборудовании
@pytest.mark.asyncio
async def test_send_equipment_info(mock_message):
    equipment_name = "🟦 Анализатор мочи автоматический H-500, DIRUI, КНР"
    mock_message.text = equipment_name

    with patch("os.path.exists", return_value=True):
        await send_equipment_info(mock_message)
        mock_message.answer_photo.assert_called_once()
        mock_message.answer.assert_called()
        assert "Анализатор мочи автоматический H-500" in mock_message.answer.call_args_list[0][0][0]


# Тест для кнопки "Меню тестов к анализаторам Maglumi"
@pytest.mark.asyncio
async def test_send_tests_menu(mock_message):
    file_path = r"C:\Users\bdv\PycharmProjects\pythonProject41\fotos\меню тестов.jpg"

    with patch("os.path.exists", return_value=True):
        await send_tests_menu(mock_message)  # Используем новое имя функции
        mock_message.answer_document.assert_called_once()
        assert "меню тестов" in mock_message.answer.call_args[0][0]


# Тест для кнопки "Ликвидация склада реагентов"
@pytest.mark.asyncio
async def test_liquidation(mock_message):
    file_path = r"C:\Users\bdv\PycharmProjects\pythonProject41\data\liquidation_file.xls"

    with patch("os.path.exists", return_value=True):
        await liquidation(mock_message)
        mock_message.answer_document.assert_called_once()
        assert "Вот актуальный файл с ликвидацией склада:" in mock_message.answer.call_args[0][0]

# Тест для случая, когда файл ликвидации не найден
@pytest.mark.asyncio
async def test_liquidation_file_not_found(mock_message):
    with patch("os.path.exists", return_value=False):
        await liquidation(mock_message)
        mock_message.answer.assert_called_once()
        assert "Файл ликвидации не найден." in mock_message.answer.call_args[0][0]

# Тест для кнопки "Назад"
@pytest.mark.asyncio
async def test_back_to_main_menu(mock_message):
    await back_to_main_menu(mock_message)
    mock_message.answer.assert_called_once()
    assert "Возвращаемся в главное меню:" in mock_message.answer.call_args[0][0]

# Тест для регистрации обработчиков
def test_register_handlers():
    mock_dp = MagicMock()
    register_handlers(mock_dp)
    assert mock_dp.message.register.called

# Тест для команды /liquidation (из main.py)
@pytest.mark.asyncio
async def test_send_liquidation_file_command(mock_message):
    await send_liquidation_file(mock_message)
    mock_message.answer.assert_called_once()
    assert "Файлы ликвидации не найдены." in mock_message.answer.call_args[0][0]