from vkbottle import Keyboard, KeyboardButtonColor, Callback, Text

from settings.cannot_change import needs_button

products_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "game"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop": "products"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "sauna"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

coffee_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "pharmacy"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop": "coffee"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "game"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

sauna_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "products"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop": "sauna"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "hookah"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

game_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "coffee"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop": "game"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "products"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

hookah_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "sauna"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Закрыто", payload={"hookah": "closed"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("&#10145;", payload={"shop_house": "pharmacy"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

pharmacy_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "hookah"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop": "pharmacy"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "coffee"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

shop_clothes = (
    Keyboard(one_time=False, inline=True)
    .add(Text("&#11013;", payload={"clothes_next": "___"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Купить", payload={"clothes": "___"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("&#10145;", payload={"clothes_back": "___"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_clothes_on = (
    Keyboard(one_time=False, inline=True)
    .add(Text("&#11013;", payload={"clothes_next": "___"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Надеть", payload={"clothes": "___"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("&#10145;", payload={"clothes_back": "___"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
# Надето купить надеть