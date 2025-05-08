from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.user_states import UserStates
from keyboards.user_kb import get_main_menu_keyboard

router = Router()

@router.callback_query(F.data == "back_to_main_from_admin")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Asosiy menyu:",
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(UserStates.MAIN_MENU)

def setup_settings_handlers(dp):
    dp.include_router(router)
