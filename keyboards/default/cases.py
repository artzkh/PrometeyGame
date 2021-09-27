from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

cases_positive = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Бонус &#127873;", payload={"case": "bonus"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Стандарт &#128477;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Вип &#128273;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

cases_negative = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Бонус &#127873;", payload={"case": "bonus"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Text("Стандарт &#128477;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Вип &#128273;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)