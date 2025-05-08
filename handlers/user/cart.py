from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.user_states import UserStates
from keyboards.user_kb import get_main_menu_keyboard, get_cart_keyboard
from database.models import Cart

router = Router()

@router.callback_query(F.data == "view_cart")
async def view_cart(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    cart_items = Cart.get_items(callback.from_user.id)
    
    if not cart_items:
        await callback.message.edit_text(
            text="Savatingiz bo'sh!",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(UserStates.MAIN_MENU)
        return
    
    total = sum(item[2] * item[3] for item in cart_items)
    cart_text = "🧺 Savatingiz:\n\n"
    
    for item in cart_items:
        name, price, quantity = item[1], item[2], item[3]
        cart_text += f"{name} - {quantity} x {price:,} = {price * quantity:,} so'm\n"
    
    cart_text += f"\nJami: {total:,} so'm"
    
    await callback.message.edit_text(
        text=cart_text,
        reply_markup=get_cart_keyboard(cart_items)
    )
    await state.set_state(UserStates.VIEW_CART)

@router.callback_query(F.data.startswith("remove_"))
async def remove_from_cart(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    cart_id = int(callback.data[7:])
    Cart.remove_item(cart_id)
    
    cart_items = Cart.get_items(callback.from_user.id)
    
    if not cart_items:
        await callback.message.edit_text(
            text="Savatingiz bo'sh!",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(UserStates.MAIN_MENU)
        return
    
    total = sum(item[2] * item[3] for item in cart_items)
    cart_text = "🧺 Savatingiz:\n\n"
    
    for item in cart_items:
        name, price, quantity = item[1], item[2], item[3]
        cart_text += f"{name} - {quantity} x {price:,} = {price * quantity:,} so'm\n"
    
    cart_text += f"\nJami: {total:,} so'm"
    
    await callback.message.edit_text(
        text=cart_text,
        reply_markup=get_cart_keyboard(cart_items)
    )
    await state.set_state(UserStates.VIEW_CART)

def setup_cart_handlers(dp):
    dp.include_router(router)
