from vkbottle.bot import Message, Blueprint

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


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "back_to_indicators"})
async def back_to_indicators(message: Message):
    await message.answer("Зайдём куда-нибудь ещё?", keyboard=keyboards.shop_indicators)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products"})
async def products(message: Message):
    await message.answer("Нажми на продукт, который хочешь приобрести."
                         "\n&#128293; — цена"
                         "\n&#11088; — прибавка к запасу", keyboard=keyboards.shop_products_fruits)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_fruits"})
async def products_fruits(message: Message):
    await message.answer("Фруктовый отдел", keyboard=keyboards.shop_products_fruits)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_gastronomy"})
async def products_gastronomy(message: Message):
    await message.answer("Кондитерский отдел", keyboard=keyboards.shop_products_gastronomy)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_fastfood"})
async def products_gastronomy(message: Message):
    await message.answer("Отдел быстрого питания", keyboard=keyboards.shop_products_fastfood)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_meat"})
async def products_gastronomy(message: Message):
    await message.answer("Мясной отдел", keyboard=keyboards.shop_products_meat)
