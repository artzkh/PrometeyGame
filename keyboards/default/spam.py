from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

spam = (
    Keyboard(one_time=False, inline=False)
    .add(Callback("Время до разблокировки &#128219;", payload={"main_menu": "spam"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)