from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

# ----- hall -----
from settings.cannot_change import reserve_button, needs_button

room_hall = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['draw']['name']} {needs_button['draw']['emoji']}",
                  payload={"need_button": "draw"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{needs_button['read']['name']} {needs_button['read']['emoji']}",
                  payload={"need_button": "read"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_hall_true_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['draw']['name']} {needs_button['draw']['emoji']}",
                  payload={"need_button": "draw"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{needs_button['read']['name']} {needs_button['read']['emoji']}",
                  payload={"need_button": "read"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_hall_false_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['draw']['name']} {needs_button['draw']['emoji']}",
                  payload={"need_button": "draw"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{needs_button['read']['name']} {needs_button['read']['emoji']}",
                  payload={"need_button": "read"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_hall_true_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['draw']['name']} {needs_button['draw']['emoji']}",
                  payload={"need_button": "draw"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{needs_button['read']['name']} {needs_button['read']['emoji']}",
                  payload={"need_button": "read"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

# ----- bedroom -----

room_bedroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['sleep']['name']} {needs_button['sleep']['emoji']}",
                  payload={"need_button": "sleep"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{needs_button['rest']['name']} {needs_button['rest']['emoji']}",
                  payload={"need_button": "rest"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bedroom_true_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['sleep']['name']} {needs_button['sleep']['emoji']}",
                  payload={"need_button": "sleep"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{needs_button['rest']['name']} {needs_button['rest']['emoji']}",
                  payload={"need_button": "rest"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bedroom_false_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['sleep']['name']} {needs_button['sleep']['emoji']}",
                  payload={"need_button": "sleep"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{needs_button['rest']['name']} {needs_button['rest']['emoji']}",
                  payload={"need_button": "rest"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bedroom_true_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['sleep']['name']} {needs_button['sleep']['emoji']}",
                  payload={"need_button": "sleep"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{needs_button['rest']['name']} {needs_button['rest']['emoji']}",
                  payload={"need_button": "rest"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

# ----- kitchen -----

room_kitchen_snack = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['ration']['name']} {needs_button['ration']['emoji']}",
                  payload={"need_button": "ration"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{reserve_button['snack']['name']} {reserve_button['snack']['emoji']}",
                  payload={"reserve": "snack"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_kitchen_snack_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['ration']['name']} {needs_button['ration']['emoji']}",
                  payload={"need_button": "ration"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{reserve_button['snack']['name']} {reserve_button['snack']['emoji']}",
                  payload={"reserve": "snack"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_kitchen_eat = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['ration']['name']} {needs_button['ration']['emoji']}",
                  payload={"need_button": "ration"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{reserve_button['eat']['name']} {reserve_button['eat']['emoji']}",
                  payload={"reserve": "eat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_kitchen_eat_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['ration']['name']} {needs_button['ration']['emoji']}",
                  payload={"need_button": "ration"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{reserve_button['eat']['name']} {reserve_button['eat']['emoji']}",
                  payload={"reserve": "eat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "bedroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

# ----- bathroom -----

room_bathroom = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['shower']['name']} {needs_button['shower']['emoji']}",
                  payload={"need_button": "shower"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{needs_button['toilet']['name']} {needs_button['toilet']['emoji']}",
                  payload={"need_button": "toilet"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bathroom_true_false = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['shower']['name']} {needs_button['shower']['emoji']}",
                  payload={"need_button": "shower"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{needs_button['toilet']['name']} {needs_button['toilet']['emoji']}",
                  payload={"need_button": "toilet"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bathroom_false_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['shower']['name']} {needs_button['shower']['emoji']}",
                  payload={"need_button": "shower"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{needs_button['toilet']['name']} {needs_button['toilet']['emoji']}",
                  payload={"need_button": "toilet"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

room_bathroom_true_true = (
    Keyboard(one_time=False, inline=True)
    .add(Callback(f"{needs_button['shower']['name']} {needs_button['shower']['emoji']}",
                  payload={"need_button": "shower"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback(f"{needs_button['toilet']['name']} {needs_button['toilet']['emoji']}",
                  payload={"need_button": "toilet"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Callback("&#11013;", payload={"room_menu": "kitchen"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Мебель", payload={"room_upgrade": "bathroom"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("&#10145;", payload={"room_menu": "hall"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
