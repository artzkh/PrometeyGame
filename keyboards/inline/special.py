from vkbottle import Keyboard, KeyboardButtonColor, Callback

go_to_kitchen = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("На кухню", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

go_to_bathroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("В ванную", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

go_to_hall = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("В гостинную", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
