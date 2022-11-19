from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

chat_menu = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Викторина", payload={"chat_menu": "victorina"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Виселица", payload={"chat_menu": "gallows"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Dice", payload={"chat_menu": "dice"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

chat_victorina_menu = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Соло", payload={"victorina": "solo"}), color=KeyboardButtonColor.PRIMARY)
    .add(Callback("Дуэль", payload={"victorina": "duo"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

chat_victorina_menu2 = (
    Keyboard(one_time=False, inline=True)
    .add(Text("адин", payload={"chat_menu": "victorina1"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Callback("два", payload={"chat_menu": "victorina2"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Callback("сорак шесть", payload={"chat_menu": "victorina3"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)
