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


def shop_clothes_buy(num):
    return (
        Keyboard(one_time=False, inline=True)
        .add(Callback("Купить", payload={"clothes": str(num)}), color=KeyboardButtonColor.NEGATIVE)
        .row()
        .add(Callback("&#11013;", payload={"clothes_page": str(num-1 if num-1 > 0 else 7)}), color=KeyboardButtonColor.SECONDARY)
        .add(Callback("&#10145;", payload={"clothes_page": str(num+1 if num+1 < 8 else 1)}), color=KeyboardButtonColor.SECONDARY)
        .get_json()
    )


def shop_clothes_off(num):
    return (
        Keyboard(one_time=False, inline=True)
        .add(Callback("Надеть", payload={"clothes": str(num)}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Callback("&#11013;", payload={"clothes_page": str(num-1 if num-1 > 0 else 7)}), color=KeyboardButtonColor.SECONDARY)
        .add(Callback("&#10145;", payload={"clothes_page": str(num+1 if num+1 < 8 else 1)}), color=KeyboardButtonColor.SECONDARY)
        .get_json()
    )


def shop_clothes_back(num):
    return (
        Keyboard(one_time=False, inline=True)
        .add(Callback("Гостиная 🚪", payload={"room_menu": "clothes"}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Callback("&#11013;", payload={"clothes_page": str(num-1 if num-1 > 0 else 7)}), color=KeyboardButtonColor.SECONDARY)
        .add(Callback("&#10145;", payload={"clothes_page": str(num+1 if num+1 < 8 else 1)}), color=KeyboardButtonColor.SECONDARY)
        .get_json()
    )