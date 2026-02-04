from aiogram.fsm.state import State, StatesGroup

class RegistrationSG(StatesGroup):
    name = State()
    phone = State()
