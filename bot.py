from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from db import kurs_qoshish_func



TOKEN = "6858399276:AAF3PaCiVmqnOcZjLfRqdfGsMsB7MM87wFo"

bot = Bot(TOKEN)

dp = Dispatcher()

class Kurs_qoshish(StatesGroup):
    kurs_nomi = State()
    kurs_narxi = State()
    toliq_malumot = State()
    oqituvchi_haqida = State()
    


@dp.message(CommandStart())
async def start_button(message: Message):
    print(message.chat.id)
    await message.answer("Assalom Aleykum, botimizga xush kelibsiz!!!", reply_markup=start_buttons())

def start_buttons() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text="O'quv kurslar")
    button_2 = KeyboardButton(text="Bizning afzalliklarimiz")
    button_3 = KeyboardButton(text="Kurs qo'shish")

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [button_1, button_2, button_3]          
        ], resize_keyboard=True
    )
    return reply_buttons

def oquv_kurs_inline_button(): 
    buttons = InlineKeyboardBuilder()
    button1 = InlineKeyboardButton(text="Backend", callback_data='backend')
    button2 = InlineKeyboardButton(text="Frontend", callback_data='frontend')
    button3 = InlineKeyboardButton(text="...", callback_data='boshqalar')
    buttons.add(button1, button2, button3)
    return buttons.as_markup()


@dp.message(lambda message: message.text == "O'quv kurslar")
async def  oquv_kurslar_button(message: types.Message):
    await message.answer("Bizning o'quv kurslarimiz", reply_markup=oquv_kurs_inline_button())

@dp.message(lambda message: message.text == "Bizning afzalliklarimiz")
async def  bizning_afzalliklar(message: types.Message):
    await message.answer("Biz haqimizda ma'lumot, afzalliklar va etc")



@dp.message(F.text == "Kurs qo'shish")
async def ish_joyi_kerak(message: types.Message, state:FSMContext):
    text = '''Kurs qo'shish:

    Kurs nomini kiriting:
'''
    await message.answer(text=text)
    await state.set_state(Kurs_qoshish.kurs_nomi)

@dp.message(Kurs_qoshish.kurs_nomi)
async def set_user_name(message: types.Message, state: FSMContext):
    await state.update_data(kurs_nomi=message.text)
    text = '''Kurs narxini kiriting:
'''
    await message.answer(text)
    await state.set_state(Kurs_qoshish.kurs_narxi)

@dp.message(Kurs_qoshish.kurs_narxi)
async def set_yosh(message: types.Message, state: FSMContext):
    await state.update_data(kurs_narxi=message.text)
    text = '''To'liq ma'lumot'''
    await message.answer(text)
    await state.set_state(Kurs_qoshish.toliq_malumot)

@dp.message(Kurs_qoshish.toliq_malumot)
async def set_yosh(message: types.Message, state: FSMContext):
    await state.update_data(toliq_malumot=message.text)
    text = '''kurs o'qituvchisi
    haqida ma'lumot'''
    await message.answer(text)
    await state.set_state(Kurs_qoshish.oqituvchi_haqida)
@dp.message(Kurs_qoshish.oqituvchi_haqida, F.text == "Xa" or "Yo'q")
async def jonatish(message: types.Message, state:FSMContext):
    if message.text == "Yo'q":
        return await message.answer("Bazaga qo'shish yuborilmadi")
    
    data = await state.get_data()
    text = f"""
    Kurs nomi:{data['kurs_nomi']}
    Kurs narxi: {data['kurs_narxi']}
    To'liq ma'lumot: {data['toliq_malumot']}
    O'qituvchi haqida: {data['oqituvchi_haqida']}"""
    kurs_qoshish_func(data['kurs_nomi'],data['kurs_nomi'],data['toliq_malumot'],data['oqituvchi_haqida'])
    state.clear()
    await bot.send_message(chat_id=1978574076,text=text)   #chat_id meni chat idim
    await message.answer("Bazaga qo'shildi!!!")

@dp.message(Kurs_qoshish.oqituvchi_haqida)
async def set_nm(message: types.Message,state:FSMContext):

    reply_button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Xa"),
             KeyboardButton(text="Yo'q")]
        ],resize_keyboard=True
    )
    await state.update_data(oqituvchi_haqida=message.text)
    data = await state.get_data()
    print(data)
    text = f"""
    Kurs nomi:{data['kurs_nomi']}
    Kurs narxi: {data['kurs_narxi']}
    To'liq ma'lumot: {data['toliq_malumot']}
    O'qituvchi haqida: {data['oqituvchi_haqida']}"""
    await message.answer(text=text,reply_markup=reply_button)





async def main():
    print("Bot muvaffaqiyatli ishga tushdi !!!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())