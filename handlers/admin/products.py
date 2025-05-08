from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.admin_states import AdminStates
from keyboards.admin_kb import get_admin_keyboard, get_all_products_keyboard, get_edit_field_keyboard, get_categories_selection_keyboard
from database.models import Product
from config import ADMIN_IDS

router = Router()

@router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    
    await message.answer(
        "Admin panelga xush kelibsiz!",
        reply_markup=get_admin_keyboard()
    )
    await state.set_state(AdminStates.ADMIN_MENU)

@router.callback_query(F.data == "admin_add")
async def admin_add(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Yangi mahsulot nomini kiriting:"
    )
    await state.set_state(AdminStates.WAITING_PRODUCT_NAME)

@router.callback_query(F.data == "admin_edit")
async def admin_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Tahrirlash uchun mahsulotni tanlang:",
        reply_markup=get_all_products_keyboard('edit')
    )
    await state.set_state(AdminStates.ADMIN_EDIT_PRODUCT)

@router.callback_query(F.data == "admin_delete")
async def admin_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="O'chirish uchun mahsulotni tanlang:",
        reply_markup=get_all_products_keyboard('delete')
    )
    await state.set_state(AdminStates.ADMIN_DELETE_PRODUCT)

@router.message(AdminStates.WAITING_PRODUCT_NAME)
async def product_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(new_product_name=name)
    
    await message.answer("Mahsulot narxini kiriting (faqat raqam):")
    await state.set_state(AdminStates.WAITING_PRODUCT_PRICE)

@router.message(AdminStates.WAITING_PRODUCT_PRICE)
async def product_price_handler(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(new_product_price=price)
        
        # Show category selection keyboard instead of asking to type
        await message.answer(
            "Mahsulot kategoriyasini tanlang:",
            reply_markup=get_categories_selection_keyboard()
        )
        await state.set_state(AdminStates.WAITING_CATEGORY_SELECTION)
    except ValueError:
        await message.answer("Iltimos, faqat raqam kiriting:")

@router.callback_query(AdminStates.WAITING_CATEGORY_SELECTION, F.data.startswith("select_category_"))
async def category_selection_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    category = callback.data[16:]  # bu to‘g‘ri: 'select_category_' qirqilyapti
    data = await state.get_data()
    name = data.get('new_product_name')
    price = data.get('new_product_price')
    
    Product.add(name, price, category)
    
    await callback.message.edit_text(
        f"✅ Yangi mahsulot qo'shildi!\nNomi: {name}\nNarxi: {price:,} so'm\nKategoriya: {category}",
        reply_markup=get_admin_keyboard()
    )
    await state.set_state(AdminStates.ADMIN_MENU)

@router.callback_query(F.data == "admin_add_category")
async def admin_add_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Yangi kategoriya nomini kiriting:"
    )
    await state.set_state(AdminStates.WAITING_CATEGORY_NAME)

@router.message(AdminStates.WAITING_CATEGORY_NAME)
async def category_name_handler(message: Message, state: FSMContext):
    category_name = message.text
    
    success = Product.add_category(category_name)
    
    if success:
        await message.answer(
            f"✅ Yangi kategoriya '{category_name}' qo'shildi!",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            f"❌ Kategoriya '{category_name}' allaqachon mavjud!",
            reply_markup=get_admin_keyboard()
        )
    
    await state.set_state(AdminStates.ADMIN_MENU)

@router.callback_query(AdminStates.ADMIN_EDIT_PRODUCT, F.data.startswith("edit_"))
async def select_product_to_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    product_id = int(callback.data[5:])  # Remove 'edit_' prefix
    await state.update_data(edit_product_id=product_id)
    product = Product.get_by_id(product_id)
    
    await callback.message.edit_text(
        text=f"Mahsulot: {product[1]}\nNarxi: {product[2]:,} so'm\nKategoriya: {product[3]}\n\nQaysi maydonni tahrirlash kerak?",
        reply_markup=get_edit_field_keyboard()
    )
    await state.set_state(AdminStates.WAITING_EDIT_FIELD)

@router.callback_query(AdminStates.WAITING_EDIT_FIELD, F.data.startswith("edit_field_"))
async def select_edit_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    field = callback.data[11:]  # Remove 'edit_field_' prefix
    await state.update_data(edit_field=field)
    
    if field == 'category':
        await callback.message.edit_text(
            text="Yangi kategoriyani tanlang:",
            reply_markup=get_categories_selection_keyboard()
        )
        await state.set_state(AdminStates.WAITING_NEW_VALUE)
        return
    
    field_name = {
        'name': 'nomini',
        'price': 'narxini',
        'category': 'kategoriyasini'
    }.get(field)
    
    await callback.message.edit_text(
        text=f"Yangi {field_name} kiriting:"
    )
    await state.set_state(AdminStates.WAITING_NEW_VALUE)

@router.callback_query(AdminStates.WAITING_NEW_VALUE, F.data.startswith("select_category_"))
async def edit_category_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    new_value = callback.data[15:]  # Remove 'select_category_' prefix
    data = await state.get_data()
    product_id = data.get('edit_product_id')
    field = data.get('edit_field')

    Product.update(product_id, field, new_value)
    product = Product.get_by_id(product_id)

    await callback.message.edit_text(
        f"✅ Mahsulot kategoriyasi yangilandi!\n\nMahsulot: {product[1]}\nNarxi: {product[2]:,} so'm\nKategoriya: {product[3]}",
        reply_markup=get_admin_keyboard()
    )
    await state.set_state(AdminStates.ADMIN_MENU)

@router.message(AdminStates.WAITING_NEW_VALUE)
async def edit_value_handler(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    product_id = data.get('edit_product_id')
    field = data.get('edit_field')
    
    if product_id and field:
        try:
            if field == 'price':
                new_value = float(new_value)
            
            Product.update(product_id, field, new_value)
            product = Product.get_by_id(product_id)
            
            field_name = {
                'name': 'nomi',
                'price': 'narxi',
                'category': 'kategoriyasi'
            }.get(field)
            
            await message.answer(
                f"✅ Mahsulot {field_name} yangilandi!\n\nMahsulot: {product[1]}\nNarxi: {product[2]:,} so'm\nKategoriya: {product[3]}",
                reply_markup=get_admin_keyboard()
            )
            await state.set_state(AdminStates.ADMIN_MENU)
        except ValueError:
            if field == 'price':
                await message.answer("Iltimos, faqat raqam kiriting:")
    else:
        await message.answer(
            "Xatolik yuz berdi. Qaytadan urinib ko'ring.",
            reply_markup=get_admin_keyboard()
        )
        await state.set_state(AdminStates.ADMIN_MENU)

@router.callback_query(AdminStates.ADMIN_DELETE_PRODUCT, F.data.startswith("delete_"))
async def delete_product_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    product_id = int(callback.data[7:])  # Remove 'delete_' prefix
    product = Product.get_by_id(product_id)
    
    if product:
        Product.delete(product_id)
        
        await callback.message.edit_text(
            text=f"✅ {product[1]} o'chirildi!",
            reply_markup=get_admin_keyboard()
        )
    else:
        await callback.message.edit_text(
            text="Mahsulot topilmadi.",
            reply_markup=get_admin_keyboard()
        )
    
    await state.set_state(AdminStates.ADMIN_MENU)

@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Admin paneli:",
        reply_markup=get_admin_keyboard()
    )
    await state.set_state(AdminStates.ADMIN_MENU)

def setup_product_handlers(dp):
    dp.include_router(router)
