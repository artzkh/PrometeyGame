from math import ceil

from vkbottle.bot import Message, Blueprint
from vkbottle.modules import json

from config import db
from keyboards import go_to_kitchen, go_to_bathroom, go_to_hall
from settings.cannot_change import coffee, products, sauna, game, pharmacy
from states import States

import keyboards

bp = Blueprint("shop")


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "shop_menu"})
async def shop_menu(message: Message):
    await message.answer("Куда отправимся?", keyboard=keyboards.shop_menu,
                         attachment="photo318378590_457299623")


@bp.on.private_message(state=States.ACTIVE, payload_map={"back_shop": str})
async def back_shop(message: Message):
    shop = (json.loads(message.payload))['back_shop']
    if shop == 'products':
        await message.answer("Продуктовая лавка", keyboard=keyboards.products_house,
                             attachment='photo318378590_457300110')
    elif shop == 'coffee':
        await message.answer("Кофейня", keyboard=keyboards.coffee_house,
                             attachment='photo318378590_457300108')
    elif shop == 'sauna':
        await message.answer("Сауна", keyboard=keyboards.sauna_house,
                             attachment='photo318378590_457300111')
    elif shop == 'game':
        await message.answer("Геймерская", keyboard=keyboards.game_house,
                             attachment='photo318378590_457300109')
    elif shop == 'pharmacy':
        await message.answer("Аптека", keyboard=keyboards.pharmacy_house,
                             attachment='photo318378590_457300107')


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "indicators"})
async def indicators(message: Message):
    if 'health' in message.state_peer.payload['recommendation']:
        await message.answer("Аптека", keyboard=keyboards.pharmacy_house,
                             attachment='photo318378590_457300107')
    elif 'energy' in message.state_peer.payload['recommendation']:
        await message.answer("Кофейня", keyboard=keyboards.coffee_house,
                             attachment='photo318378590_457300108')
    elif 'hygiene' in message.state_peer.payload['recommendation']:
        await message.answer("Сауна", keyboard=keyboards.sauna_house,
                             attachment='photo318378590_457300111')
    elif 'happiness' in message.state_peer.payload['recommendation']:
        await message.answer("Геймерская", keyboard=keyboards.game_house,
                             attachment='photo318378590_457300109')
    elif 'satiety' in message.state_peer.payload['recommendation']:
        await message.answer("Продуктовая лавка", keyboard=keyboards.products_house,
                             attachment='photo318378590_457300110')
    else:
        await message.answer("Кофейня", keyboard=keyboards.coffee_house,
                             attachment='photo318378590_457300108')


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "back_to_menu"})
async def back_to_indicators(message: Message):
    await message.answer("Зайдём куда-нибудь ещё?", keyboard=keyboards.shop_menu,
                         attachment="photo318378590_457299623")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products"})
async def shop_products(message: Message):
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
async def products_fastfood(message: Message):
    balance, reserve, satiety, max_satiety = await db.get_for_products_shop(peer_id=message.peer_id)
    await message.answer(f"Баланс: {balance}&#128293;{reserve}&#129377;"
                         f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;", keyboard=keyboards.shop_products_fastfood,
                         attachment="photo318378590_457298976")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "products_meat"})
async def products_meat(message: Message):
    balance, reserve, satiety, max_satiety = await db.get_for_products_shop(peer_id=message.peer_id)
    await message.answer(f"Баланс: {balance}&#128293;{reserve}&#129377;"
                         f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;", keyboard=keyboards.shop_products_meat,
                         attachment="photo318378590_457298977")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "coffee"})
async def shop_coffee(message: Message):
    await message.answer("Ты можешь заказать любое блюдо из меню."
                         "\n&#128293; — цена", keyboard=keyboards.shop_coffee,
                         attachment="photo318378590_457298978")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "sauna"})
async def shop_sauna(message: Message):
    await message.answer("Купи веник и мы тебя хорошенько отпарим!"
                         "\n&#128293; — цена", keyboard=keyboards.shop_sauna,
                         attachment="photo318378590_457298979")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "game"})
async def shop_game(message: Message):
    await message.answer("Добро пожаловать в игровой клуб!"
                         "\n&#128293; — цена", keyboard=keyboards.shop_game,
                         attachment="photo318378590_457298981")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "hookah"})
async def shop_hookah(message: Message):
    await message.answer("VIP-комната, здесь всё самое вкусное."
                         "\n&#128293; — цена", keyboard=keyboards.shop_coffee,
                         attachment="photo318378590_457298982")


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "pharmacy"})
async def shop_pharmacy(message: Message):
    await message.answer("В аптеке есть всё для твоего здоровья."
                         "\n&#128293; — цена", keyboard=keyboards.shop_pharmacy,
                         attachment="photo318378590_457299722")


@bp.on.private_message(state=States.ACTIVE, payload_map={"products": str})
async def buy_products(message: Message):
    payload = json.loads(message.payload)
    balance, reserve, satiety, max_satiety = await db.get_balance_and_reserve(message.peer_id)
    if balance < products[payload['products']]['fire']:
        await message.answer(f"Для покупки {products[payload['products']]['emoji']} "
                             f"не хватает "
                             f"{products[payload['products']]['fire'] - balance}&#128293;")
    else:
        balance -= products[payload['products']]['fire']
        new_reserve = reserve + products[payload['products']]['reserve']
        await db.buy_product(message.peer_id, balance, new_reserve)
        if ceil(satiety) == max_satiety:
            await message.answer(
                f"{products[payload['products']]['emoji']} (+{products[payload['products']]['reserve']}&#129377;)"
                f"\nОгонёчков: {balance}&#128293;"
                f"\nСытость: {max_satiety}&#127831;"
                f"\nЗапас: {new_reserve}&#129377;")
        else:
            await message.answer(
                f"{products[payload['products']]['emoji']} (+{products[payload['products']]['reserve']}&#129377;)"
                f"\nОгонёчков: {balance}&#128293;"
                f"\nСытость: {ceil(satiety)}/{max_satiety}&#127831;"
                f"\nЗапас: {new_reserve}&#129377;", keyboard=go_to_kitchen)


@bp.on.private_message(state=States.ACTIVE, payload_map={"coffee": str})
async def buy_coffee(message: Message):
    payload = json.loads(message.payload)
    balance, energy, max_energy = await db.get_balance_and_energy(message.peer_id)
    if balance < coffee[payload['coffee']]['fire']:
        await message.answer(f"Для покупки {coffee[payload['coffee']]['emoji']} "
                             f"не хватает "
                             f"{coffee[payload['coffee']]['fire'] - balance}&#128293;")
    else:
        if ceil(energy) == max_energy:
            await message.answer(f"&#9889;Ты полон энергии!&#9889;")
            return
        elif energy + coffee[payload['coffee']]['energy'] > max_energy:
            new_energy = max_energy
        else:
            new_energy = energy + coffee[payload['coffee']]['energy']
        balance -= coffee[payload['coffee']]['fire']
        await db.buy_coffee(message.peer_id, balance, new_energy)
        await message.answer(f"{coffee[payload['coffee']]['emoji']} ( +{coffee[payload['coffee']]['energy']}&#9889;)"
                             f"\nОгонёчков: {balance}&#128293;"
                             f"\nЭнергии: {ceil(new_energy)}/{max_energy}&#9889;")


@bp.on.private_message(state=States.ACTIVE, payload_map={"sauna": str})
async def buy_sauna(message: Message):
    payload = json.loads(message.payload)
    balance, hygiene, max_hygiene = await db.get_balance_and_hygiene(message.peer_id)
    if balance < sauna[payload['sauna']]['fire']:
        await message.answer(f"Для покупки {sauna[payload['sauna']]['emoji']} "
                             f"не хватает "
                             f"{sauna[payload['sauna']]['fire'] - balance}&#128293;")
    else:
        if ceil(hygiene) == max_hygiene:
            await message.answer(f"&#129531;Ты полносью чист!&#129531;", keyboard=go_to_bathroom)
            return
        elif hygiene + sauna[payload['sauna']]['hygiene'] > max_hygiene:
            new_hygiene = max_hygiene
        else:
            new_hygiene = hygiene + sauna[payload['sauna']]['hygiene']
        balance -= sauna[payload['sauna']]['fire']
        await db.buy_sauna(message.peer_id, balance, new_hygiene)
        await message.answer(f"{sauna[payload['sauna']]['emoji']} ( +{sauna[payload['sauna']]['hygiene']}&#129531;)"
                             f"\nОгонёчков: {balance}&#128293;"
                             f"\nГигиена: {ceil(new_hygiene)}/{max_hygiene}&#129531;")


@bp.on.private_message(state=States.ACTIVE, payload_map={"game": str})
async def buy_game(message: Message):
    payload = json.loads(message.payload)
    balance, happiness, max_happiness = await db.get_balance_and_happiness(message.peer_id)
    if balance < game[payload['game']]['fire']:
        await message.answer(f"Для покупки {game[payload['game']]['emoji']} "
                             f"не хватает "
                             f"{game[payload['game']]['fire'] - balance}&#128293;")
    else:
        if ceil(happiness) == max_happiness:
            await message.answer(f"&#127881;Ты счастлив!&#127881;", keyboard=go_to_hall)
            return
        elif happiness + game[payload['game']]['happiness'] > max_happiness:
            new_happiness = max_happiness
        else:
            new_happiness = happiness + game[payload['game']]['happiness']
        balance -= game[payload['game']]['fire']
        await db.buy_game(message.peer_id, balance, new_happiness)
        await message.answer(f"{game[payload['game']]['emoji']} (+{game[payload['game']]['happiness']}&#127881;)"
                             f"\nОгонёчков: {balance}&#128293;"
                             f"\nСчастье: {ceil(new_happiness)}/{max_happiness}&#127881;")


@bp.on.private_message(state=States.ACTIVE, payload_map={"pharmacy": str})
async def buy_pharmacy(message: Message):
    payload = json.loads(message.payload)
    balance, health, max_health = await db.get_balance_and_health(message.peer_id)
    if balance < pharmacy[payload['pharmacy']]['fire']:
        await message.answer(f"Для покупки {pharmacy[payload['pharmacy']]['emoji']} "
                             f"не хватает "
                             f"{pharmacy[payload['pharmacy']]['fire'] - balance}&#128293;")
    else:
        if ceil(health) == max_health:
            await message.answer(f"&#129505;Ты полностью здоров!&#129505;", keyboard=go_to_hall)
            return
        elif health + pharmacy[payload['pharmacy']]['health'] > max_health:
            new_health = max_health
        else:
            new_health = health + pharmacy[payload['pharmacy']]['health']

        balance -= pharmacy[payload['pharmacy']]['fire']
        await db.buy_pharmacy(message.peer_id, balance, new_health)
        await message.answer(f"{pharmacy[payload['pharmacy']]['emoji']} (+{pharmacy[payload['pharmacy']]['health']}&#129505;)"
                             f"\nОгонёчков: {balance}&#128293;"
                             f"\nЗдоровье: {ceil(new_health)}/{max_health}&#129505;")
