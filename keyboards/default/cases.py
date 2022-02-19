from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

cases_positive = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Бонус &#127873;", payload={"case": "bonus"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("100&#128293;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("500&#128293;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("100&#126980;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

cases_negative = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Бонус &#127873;", payload={"case": "bonus"}), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("100&#128293;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("500&#128293;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("100&#126980;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)