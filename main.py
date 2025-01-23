import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers import register_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем диспетчер
dp = Dispatcher()

# Обработчик команды /equipment
@dp.message(Command("equipment"))
async def send_equipment_info(message: types.Message):
    """
    Отправляет пользователю данные об оборудовании.
    """
    await message.answer("Данные об оборудовании не найдены.")

# Обработчик команды /liquidation
@dp.message(Command("liquidation"))
async def send_liquidation_file(message: types.Message):
    """
    Отправляет пользователю файл ликвидации.
    """
    await message.answer("Файлы ликвидации не найдены.")

async def main():
    bot = Bot(token=BOT_TOKEN)

    # Регистрируем обработчики из handlers.py
    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        await bot.session.close()  # Закрываем сессию бота

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен вручную.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        sys.exit(1)

# Экспортируем dp и send_liquidation_file для использования в других модулях
__all__ = ["dp", "send_liquidation_file"]