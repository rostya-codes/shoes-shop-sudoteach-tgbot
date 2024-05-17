from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app import keyboards as kb
from app.database import requests as rq

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('🙂 Hello! Welcome to Sneakers shop!', reply_markup=kb.main)


@router.message(F.text == 'Catalog 🗂️')
async def catalog_handler(message: Message):
    await message.answer('Select item brand', reply_markup=await kb.catalog())


@router.callback_query(F.data.startswith('category_'))
async def category_items(callback: CallbackQuery):
    await callback.answer('You chose category')
    await callback.message.answer('Choose item', reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item_card(callback: CallbackQuery):
    item = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('You chose category')
    await callback.message.answer(f'Name: {item.name}\n'
                                  f'Description: {item.description}\n'
                                  f'Price: ${item.price}',
                                  reply_markup=await kb.item_buttons(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('basket_'))
async def item_basket(callback: CallbackQuery):
    await rq.set_item_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.answer('Item added to basket!')
    await callback.message.edit_reply_markup(reply_markup=await kb.item_buttons_second(callback.data.split('_')[1]))



