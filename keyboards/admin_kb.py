from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Product


def get_admin_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="➕ Mahsulot qo'shish", callback_data='admin_add')],
        [InlineKeyboardButton(text="➕ Kategoriya qo'shish", callback_data='admin_add_category')],
        [InlineKeyboardButton(text="✏️ Mahsulotni tahrirlash", callback_data='admin_edit')],
        [InlineKeyboardButton(text="❌ Mahsulotni o'chirish", callback_data='admin_delete')],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data='back_to_main_from_admin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_all_products_keyboard(action: str):
    products = Product.get_all()
    keyboard = []

    for product in products:
        product_id, name, price, _ = product
        keyboard.append([
            InlineKeyboardButton(
                text=f"{name} - {price:,} so'm",
                callback_data=f'{action}_{product_id}'
            )
        ])

    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_admin')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_edit_field_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="📝 Nomi", callback_data='edit_field_name')],
        [InlineKeyboardButton(text="💰 Narxi", callback_data='edit_field_price')],
        [InlineKeyboardButton(text="📂 Kategoriyasi", callback_data='edit_field_category')],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_admin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_categories_selection_keyboard():
    categories = Product.get_categories()
    keyboard = []

    for category in categories:
        # Faqat aniq kategoriya nomini callback_data ga qo‘shamiz
        keyboard.append([
            InlineKeyboardButton(
                text=category,
                callback_data=f'select_category_{category}'
            )
        ])

    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_admin')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
