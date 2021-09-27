from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

room_hall = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Письма &#9993;", payload={"room_menu": "letter"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Рисовать &#128210;", payload={"room_menu": "paint"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Апгрейд", payload={"room_upgrade": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bedroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Поспать &#128164;", payload={"room_menu": "letter"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Отдохнуть &#128133;", payload={"room_menu": "paint"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Апгрейд", payload={"room_upgrade": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_kitchen_1 = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Перекусить &#127823;", payload={"room_menu": "letter"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Покушать &#127831;", payload={"room_menu": "paint"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Апгрейд", payload={"room_upgrade": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_kitchen_2 = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Перекусить &#127822;", payload={"room_menu": "letter"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Покушать &#127831;", payload={"room_menu": "paint"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Апгрейд", payload={"room_upgrade": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bathroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Туалет &#128701;", payload={"room_menu": "paint"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Помыться &#128705;", payload={"room_menu": "letter"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Апгрейд", payload={"room_upgrade": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

