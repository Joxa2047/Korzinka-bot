from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Product

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="🛍 Mahsulotlarni ko'rish", callback_data='browse_products')],
        [InlineKeyboardButton(text="🧺 Savatni ko'rish", callback_data='view_cart')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_categories_keyboard():
    categories = Product.get_categories()
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(text=category, callback_data=f'category_{category}')])
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_main')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_products_keyboard(category):
    products = Product.get_by_category(category)
    keyboard = []
    for product in products:
        product_id, name, price = product
        keyboard.append([InlineKeyboardButton(text=f"{name} - {price:,} so'm", callback_data=f'product_{product_id}')])
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_categories')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_product_detail_keyboard(product_id):
    keyboard = [
        [InlineKeyboardButton(text="➕ Savatga qo'shish", callback_data=f'add_to_cart_{product_id}')],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_products')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cart_keyboard(cart_items):
    keyboard = []
    for item in cart_items:
        cart_id = item[0]
        keyboard.append([InlineKeyboardButton(text=f"❌ {item[1]}", callback_data=f'remove_{cart_id}')])
    
    if cart_items:
        keyboard.append([InlineKeyboardButton(text="✅ Buyurtma berish", callback_data='checkout')])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_main')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
