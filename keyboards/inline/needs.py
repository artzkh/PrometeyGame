from vkbottle import Keyboard, KeyboardButtonColor, Callback, Text

from settings.cannot_change import needs_button

products_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "hookah"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop": "products"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "coffee"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

coffee_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "products"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop_house": "in_coffee"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "sauna"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

sauna_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "coffee"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop_house": "in_sauna"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "game"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

game_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "sauna"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop_house": "in_game"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "hookah"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

hookah_house = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("&#11013;", payload={"shop_house": "game"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Зайти", payload={"shop_house": "in_hookah"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"shop_house": "products"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
