from vkbottle import Keyboard, KeyboardButtonColor, Text


menu_positive = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Гостиная &#128682;", payload={"main_menu": "room_hall"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Игры &#127918;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Работа &#128104;&#8205;&#128187;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Магазин &#128717;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Кейсы &#127873;", payload={"main_menu": "cases"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

menu_negative = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Гостиная &#128682;", payload={"main_menu": "room_hall"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Игры &#127918;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Работа &#128104;&#8205;&#128187;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Магазин &#128717;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Кейсы &#127873;", payload={"main_menu": "cases"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
