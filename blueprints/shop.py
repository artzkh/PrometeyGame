from math import ceil

from vkbottle.bot import Message, Blueprint

from config import db
from functions import generate_attachment
from functions.cases import is_bonus
from json_data import pictures
from states import States

import keyboards

bp = Blueprint("shop")


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "shop_menu"})
async def shop_menu(message: Message):
    await message.answer("Куда отправимся?", keyboard=keyboards.shop_menu,
                         attachment="photo318378590_457298968")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "indicators"})
async def indicators(message: Message):
    if 'satiety' in message.state_peer.payload['recommendation']:
        await message.answer("Продуктовая лавка", keyboard=keyboards.products_house,
                             attachment='photo318378590_457298973')
    elif 'energy' in message.state_peer.payload['recommendation']:
        await message.answer("Кофейня", keyboard=keyboards.coffee_house,
                             attachment='photo318378590_457298978')
    elif 'hygiene' in message.state_peer.payload['recommendation']:
        await message.answer("Сауна", keyboard=keyboards.sauna_house,
                             attachment='photo318378590_457298980')
    elif 'happiness' in message.state_peer.payload['recommendation']:
        await message.answer("Геймерская", keyboard=keyboards.game_house,
                             attachment='photo318378590_457298981')
    else:
        await message.answer("Продуктовая лавка", keyboard=keyboards.products_house,
                             attachment='photo318378590_457298973')


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "back_to_menu"})
async def back_to_indicators(message: Message):
    await message.answer("Зайдём куда-нибудь ещё?", keyboard=keyboards.shop_menu,
                         attachment="photo318378590_457298968")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products"})
async def products(message: Message):
    await message.answer("Нажми на продукт, который хочешь приобрести."
                         "\n&#128293; — цена"
                         "\n&#11088; — прибавка к запасу", keyboard=keyboards.shop_products_fruits,
                         attachment="photo318378590_457298974")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_fruits"})
async def products_fruits(message: Message):
    balance, reserve, satiety, max_satiety = await db.get_for_products_shop(peer_id=message.peer_id)
    await message.answer(f"Баланс: {balance}&#128293;{reserve}&#129377;"
                         f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;", keyboard=keyboards.shop_products_fruits,
                         attachment="photo318378590_457298974")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_gastronomy"})
async def products_gastronomy(message: Message):
    balance, reserve, satiety, max_satiety = await db.get_for_products_shop(peer_id=message.peer_id)
    await message.answer(f"Баланс: {balance}&#128293;{reserve}&#129377;"
                         f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;", keyboard=keyboards.shop_products_gastronomy,
                         attachment="photo318378590_457298975")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_fastfood"})
async def products_gastronomy(message: Message):
    balance, reserve, satiety, max_satiety = await db.get_for_products_shop(peer_id=message.peer_id)
    await message.answer(f"Баланс: {balance}&#128293;{reserve}&#129377;"
                         f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;", keyboard=keyboards.shop_products_fastfood,
                         attachment="photo318378590_457298976")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_meat"})
async def products_gastronomy(message: Message):
    balance, reserve, satiety, max_satiety = await db.get_for_products_shop(peer_id=message.peer_id)
    await message.answer(f"Баланс: {balance}&#128293;{reserve}&#129377;"
                         f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;", keyboard=keyboards.shop_products_meat,
                         attachment="photo318378590_457298977")
