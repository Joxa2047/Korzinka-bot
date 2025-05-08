from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    START = State()
    MAIN_MENU = State()
    BROWSE_PRODUCTS = State()
    PRODUCT_SELECTED = State()
    VIEW_CART = State()
    CHECKOUT = State()
