from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.user_states import UserStates
from keyboards.user_kb import get_main_menu_keyboard
from database.models import Cart, Order

router = Router()

@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    cart_items = Cart.get_items(callback.from_user.id)
    
    if cart_items:
        order_id, total_amount, order_date = Order.create(callback.from_user.id, cart_items)
        
        receipt = f"🧾 Chek #{order_id}\n"
        receipt += f"📅 Sana: {order_date}\n\n"
        
        for item in cart_items:
            name, price, quantity = item[1], item[2], item[3]
            receipt += f"{name}\n{quantity} x {price:,} = {price * quantity:,} so'm\n"
        
        receipt += f"\n💰 Jami: {total_amount:,} so'm\n"
        receipt += "\nXaridingiz uchun rahmat! 🙏"
        
        Cart.clear(callback.from_user.id)
        
        await callback.message.edit_text(
            text=receipt,
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await callback.message.edit_text(
            text="Savatingiz bo'sh!",
            reply_markup=get_main_menu_keyboard()
        )
    
    await state.set_state(UserStates.MAIN_MENU)

def setup_checkout_handlers(dp):
    dp.include_router(router)
