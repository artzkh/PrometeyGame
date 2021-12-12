from vkbottle import Keyboard, KeyboardButtonColor, Text

menu_positive = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Гостиная &#128682;", payload={"main_menu": "room_hall"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Город &#127890;", payload={"main_menu": "shop_menu"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Инфо &#128293;", payload={"main_menu": "passport"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Игры &#127919;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Сундуки &#127873;", payload={"main_menu": "cases"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

menu_negative = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Гостиная &#128682;", payload={"main_menu": "room_hall"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Город &#127890;", payload={"main_menu": "shop_menu"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Инфо &#128293;", payload={"main_menu": "passport"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Игры &#127919;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Сундуки &#127873;", payload={"main_menu": "cases"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
# &#128104;&#8205;&#128187;
