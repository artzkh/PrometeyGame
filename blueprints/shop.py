from vkbottle.bot import Message, Blueprint

from functions import generate_attachment
from functions.cases import is_bonus
from json_data import pictures
from states import States

import keyboards

bp = Blueprint("shop")


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "shop_menu"})
async def shop_menu(message: Message):
    await message.answer("Выбери подходящую категорию", keyboard=keyboards.shop_menu)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "indicators"})
async def indicators(message: Message):
    await message.answer("Куда пойдем?", keyboard=keyboards.shop_indicators)


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
