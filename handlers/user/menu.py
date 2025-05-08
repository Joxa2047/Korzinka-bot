from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.user_states import UserStates
from keyboards.user_kb import get_main_menu_keyboard, get_categories_keyboard, get_products_keyboard, get_product_detail_keyboard
from database.models import Product, Cart

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user = message.from_user
    await message.answer(
        f"Assalomu alaykum, {user.first_name}! Korzinka.uz botiga xush kelibsiz!",
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(UserStates.MAIN_MENU)

@router.callback_query(F.data == "browse_products")
async def browse_products(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Kategoriyani tanlang:",
        reply_markup=get_categories_keyboard()
    )
    await state.set_state(UserStates.BROWSE_PRODUCTS)

@router.callback_query(F.data.startswith("category_"))
async def select_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    category = callback.data[9:]
    await state.update_data(current_category=category)
    
    await callback.message.edit_text(
        text=f"Kategoriya: {category}\nMahsulotni tanlang:",
        reply_markup=get_products_keyboard(category)
    )
    await state.set_state(UserStates.BROWSE_PRODUCTS)

@router.callback_query(F.data.startswith("product_"))
async def select_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    product_id = int(callback.data[8:])
    product = Product.get_by_id(product_id)
    
    if product:
        product_id, name, price, category = product
        await state.update_data(current_product=product_id)
        
        await callback.message.edit_text(
            text=f"📦 {name}\n💰 Narxi: {price:,} so'm\n🏷 Kategoriya: {category}",
            reply_markup=get_product_detail_keyboard(product_id)
        )
        await state.set_state(UserStates.PRODUCT_SELECTED)

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    product_id = int(callback.data[12:])
    product = Product.get_by_id(product_id)
    
    if product:
        Cart.add_item(callback.from_user.id, product_id)
        
        await callback.message.edit_text(
            text=f"✅ {product[1]} savatga qo'shildi!",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(UserStates.MAIN_MENU)

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Asosiy menyu:",
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(UserStates.MAIN_MENU)

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Kategoriyani tanlang:",
        reply_markup=get_categories_keyboard()
    )
    await state.set_state(UserStates.BROWSE_PRODUCTS)

@router.callback_query(F.data == "back_to_products")
async def back_to_products(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    data = await state.get_data()
    category = data.get('current_category')
    
    if category:
        await callback.message.edit_text(
            text=f"Kategoriya: {category}\nMahsulotni tanlang:",
            reply_markup=get_products_keyboard(category)
        )
        await state.set_state(UserStates.BROWSE_PRODUCTS)

def setup_user_menu(dp):
    dp.include_router(router)
