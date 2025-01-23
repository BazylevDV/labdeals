import logging
import os
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramAPIError
from keyboards import main_menu, equipment_menu


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Логи будут записываться в файл
        logging.StreamHandler()  # Логи будут выводиться в консоль
    ]
)

# Создаем диспетчер
dp = Dispatcher()



# Данные для оборудования (остаются жёстко прописанными)
equipment_data = {
    "🟦 Анализатор мочи автоматический H-500, DIRUI, КНР": {
        "photo": r"C:\Users\bdv\PycharmProjects\pythonProject41\fotos\H-500.jpg",
        "description": (
            "**🟦 Анализатор мочи автоматический H-500**\n\n"
            "Современный анализатор для быстрого и точного исследования мочи. "
            "Идеально подходит для лабораторий любого уровня."
        ),
        "conditions": (
            "📜 *Условия предоставления:*\n"
            "1. 🆓 Оборудование предоставляется бесплатно на условиях демонстрационного пользования или аренды.\n"
            "2. 📄 Требуется заключение договора.\n"
            "3. 🚚 Доставка и установка за наш счет."
        ),
        "contact": "📞 *Контактный телефон менеджера:* Екатерина Григорик: +7 (912) 402-31-89"
    },
    "🟩 Анализатор автоматический иммунохемилюминесцентный для диагностики in vitro Maglumi 800, КНР": {
        "photo": r"C:\Users\bdv\PycharmProjects\pythonProject41\fotos\maglumi_800.jpg",
        "description": (
            "**🟩 Анализатор Maglumi 800**\n\n"
            "Иммунохемилюминесцентный анализатор для диагностики in vitro. "
            "Высокая точность и надежность."
        ),
        "conditions": (
            "📜 *Условия предоставления:*\n"
            "1. 🆓 Оборудование предоставляется бесплатно на условиях демонстрационного пользования или аренды.\n"
            "2. 📄 Требуется заключение договора.\n"
            "3. 🚚 Доставка и установка за наш счет."
        ),
        "contact": "📞 *Контактный телефон менеджера:* Екатерина Григорик: +7 (912) 402-31-89"
    },
    "🟨 Анализатор иммунофлуоресцентный Finecare FIA FS-113, Wondfo, КНР": {
        "photo": r"C:\Users\bdv\PycharmProjects\pythonProject41\fotos\Analizator-Finecare.png",
        "description": (
            "**🟨 Анализатор иммунофлуоресцентный Finecare FIA FS-113**\n\n"
            "Иммунофлуоресцентный анализатор для быстрой диагностики. "
            "Компактный и удобный в использовании."
        ),
        "conditions": (
            "📜 *Условия предоставления:*\n"
            "1. 🆓 Оборудование предоставляется бесплатно на условиях демонстрационного пользования или аренды.\n"
            "2. 📄 Требуется заключение договора.\n"
            "3. 🚚 Доставка и установка за наш счет."
        ),
        "contact": "📞 *Контактный телефон менеджера:* Екатерина Григорик: +7 (912) 402-31-89"
    },
}

# Обработчик команды /start
async def start(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запустил бота.")
    welcome_text = (
        "👋 *Добро пожаловать в ЛабторгБот!*\n\n"
        "Здесь вы можете:\n"
        "• 🆓 Получить информацию о *бесплатном оборудовании*.\n"
        "• ℹ️ Узнать больше о *нашей компании*.\n"
        "• 🧪 Ознакомиться с *меню тестов к анализаторам Maglumi*.\n"  # Обновленный текст
        "• 🔥 Узнать о *ликвидации склада реагентов и медизделий*.\n\n"
        "👇 *Выберите опцию ниже:*"
    )
    await message.answer(welcome_text, reply_markup=main_menu, parse_mode="Markdown")

# Обработчик кнопки "О нас"
async def about_us(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запросил информацию 'О нас'.")
    try:
        with open("about.txt", "r", encoding="utf-8") as file:
            about_text = file.read()
        await message.answer(f"*О нас:*\n\n{about_text}", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла 'about.txt': {e}")
        await message.answer("Произошла ошибка при получении информации.")

# Обработчик кнопки "Бесплатное оборудование"
async def equipment(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запросил меню оборудования.")
    await message.answer("Выберите оборудование:", reply_markup=equipment_menu)

# Обработчик информации об оборудовании
async def send_equipment_info(message: types.Message):
    logging.info(
        f"Пользователь {message.from_user.id} ({message.from_user.username}) запросил информацию об оборудовании: {message.text}.")
    equipment_name = message.text
    data = equipment_data.get(equipment_name)

    if not data:
        await message.answer("Информация не найдена.")
        return

    # Получаем путь к файлу
    photo_path = data["photo"]

    # Проверяем, существует ли файл
    if not os.path.exists(photo_path):
        await message.answer("Фото оборудования не найдено.")
        return

    try:
        # Отправка фото
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo)

        # Отправка описания
        await message.answer(data["description"], parse_mode="Markdown")

        # Отправка условий
        await message.answer(data["conditions"], parse_mode="Markdown")

        # Отправка контактов
        await message.answer(data["contact"])
    except Exception as e:
        logging.error(f"Ошибка при отправке информации об оборудовании: {e}")
        await message.answer("Произошла ошибка при отправке информации.")


# Обработчик кнопки "Меню тестов к анализаторам Maglumi"
async def send_tests_menu(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запросил меню тестов.")
    file_path = r"C:\Users\bdv\PycharmProjects\pythonProject41\fotos\меню тестов.jpg"

    if not os.path.exists(file_path):
        await message.answer("Файл с меню тестов не найден.")
        return

    try:
        await message.answer("Вот меню тестов для анализаторов Maglumi:")
        await message.answer_document(document=FSInputFile(file_path))
    except TelegramAPIError as e:
        logging.error(f"Ошибка при отправке файла: {e}")
        await message.answer("Произошла ошибка при отправке файла.")

# Обработчик кнопки "Ликвидация склада реагентов"
async def liquidation(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запросил файл ликвидации.")
    try:
        # Указываем путь к файлу
        file_path = r"C:\Users\bdv\PycharmProjects\pythonProject41\data\liquidation_file.xls"
        logging.info(f"Путь к файлу: {file_path}")  # Логируем путь к файлу

        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            await message.answer("Файл ликвидации не найден.")
            return

        # Отправляем файл
        await message.answer("Вот актуальный файл с ликвидацией склада:")
        await message.answer_document(document=FSInputFile(file_path))
    except Exception as e:
        logging.error(f"Ошибка при отправке файла ликвидации: {e}")
        await message.answer("Произошла ошибка при отправке файла.")


# Обработчик кнопки "Назад"
async def back_to_main_menu(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) вернулся в главное меню.")
    await message.answer("Возвращаемся в главное меню:", reply_markup=main_menu)

# Логирование входящих сообщений
@dp.message()
async def log_message(message: types.Message):
    logging.info(f"Получено сообщение: {message.text}")
    await message.answer("Сообщение не обработано.")


# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=['start']))
    dp.message.register(about_us, F.text == "ℹ️ О нас")
    dp.message.register(equipment, F.text == "🆓 Бесплатное оборудование")
    dp.message.register(send_equipment_info, F.text.in_([
        "🟦 Анализатор мочи автоматический H-500, DIRUI, КНР",
        "🟩 Анализатор автоматический иммунохемилюминесцентный для диагностики in vitro Maglumi 800, КНР",
        "🟨 Анализатор иммунофлуоресцентный Finecare FIA FS-113, Wondfo, КНР"
    ]))
    dp.message.register(send_tests_menu, F.text == "🧪 Меню тестов к анализаторам Maglumi")  # Обновленный вызов
    dp.message.register(liquidation, F.text == "🔥 Ликвидация склада реагентов и медизделий")
    dp.message.register(back_to_main_menu, F.text == "🔙 Назад")
    dp.message.register(log_message)