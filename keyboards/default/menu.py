from vkbottle import Keyboard, KeyboardButtonColor, Text

menu_positive = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Гостиная &#128682;", payload={"main_menu": "room_hall"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Город &#127890;", payload={"main_menu": "shop_menu"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Инфо &#128293;", payload={"main_menu": "passport"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Игры &#127919;", payload={"main_menu": "games"}), color=KeyboardButtonColor.SECONDARY)
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
    .add(Text("Игры &#127919;", payload={"main_menu": "games"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Сундуки &#127873;", payload={"main_menu": "cases"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

city_menu = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Центр &#127978;", payload={"shop": "indicators"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Одежда &#128088;", payload={"shop": "clothes"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Работа &#128188;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)