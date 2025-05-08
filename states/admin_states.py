from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    ADMIN_MENU = State()
    ADMIN_ADD_PRODUCT = State()
    ADMIN_EDIT_PRODUCT = State()
    ADMIN_DELETE_PRODUCT = State()
    WAITING_PRODUCT_NAME = State()
    WAITING_PRODUCT_PRICE = State()
    WAITING_CATEGORY_SELECTION = State()
    WAITING_EDIT_FIELD = State()
    WAITING_NEW_VALUE = State()
    WAITING_CATEGORY_NAME = State()
