from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Функция для создания клавиатуры
def create_keyboard(buttons):
    # Создаем список списков для клавиатуры
    keyboard = [[button] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Главное меню с эмодзи
main_menu_buttons = [
    KeyboardButton(text="🆓 Бесплатное оборудование"),
    KeyboardButton(text="ℹ️ О нас"),
    KeyboardButton(text="🧪 Меню тестов к анализаторам Maglumi"),  # Измененное название
    KeyboardButton(text="🔥 Ликвидация склада реагентов и медизделий")
]
main_menu = create_keyboard(main_menu_buttons)

# Меню "Бесплатное оборудование" с эмодзи и кнопкой "Назад"
equipment_menu_buttons = [
    KeyboardButton(text="🟦 Анализатор мочи автоматический H-500, DIRUI, КНР"),
    KeyboardButton(text="🟩 Анализатор автоматический иммунохемилюминесцентный для диагностики in vitro Maglumi 800, КНР"),
    KeyboardButton(text="🟨 Анализатор иммунофлуоресцентный Finecare FIA FS-113, Wondfo, КНР"),
    KeyboardButton(text="🔙 Назад")
]
equipment_menu = create_keyboard(equipment_menu_buttons)

# Меню "Меню тестов Maglumi" больше не нужно, так как файл отправляется сразу