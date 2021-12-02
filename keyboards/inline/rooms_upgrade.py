from vkbottle import Keyboard, KeyboardButtonColor, Callback

upgrade_room_lvl_hall = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отмена", payload={"room_menu": "hall"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"room_upgrade": "lvl"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

upgrade_room_lvl_kitchen = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отмена", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"room_upgrade": "lvl"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

upgrade_room_lvl_bedroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отмена", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"room_upgrade": "lvl"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

upgrade_room_lvl_bathroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отмена", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"room_upgrade": "lvl"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

upgrade_hall = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отменить", payload={"room_menu": "hall"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"buy_upgrade": "hall"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

upgrade_bedroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отменить", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"buy_upgrade": "bedroom"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

upgrade_kitchen = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отменить", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"buy_upgrade": "kitchen"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

upgrade_bathroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Отменить", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Купить", payload={"buy_upgrade": "bathroom"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

buy_upgrade_hall_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Домой &#128682;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

buy_upgrade_bedroom_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Домой &#128682;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

buy_upgrade_kitchen_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Домой &#128682;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

buy_upgrade_bathroom_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Домой &#128682;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)

buy_upgrade_hall_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Уйти", payload={"room_menu": "hall"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Работать", payload={"main_menu": "work"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

buy_upgrade_bedroom_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Уйти", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Работать", payload={"main_menu": "work"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

buy_upgrade_kitchen_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Уйти", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Работать", payload={"main_menu": "work"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

buy_upgrade_bathroom_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Уйти", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.NEGATIVE)
    .add(Callback("Работать", payload={"main_menu": "work"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
