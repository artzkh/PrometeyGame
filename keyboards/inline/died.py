from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

died = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Начать сначала", payload={"died": "start_over"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Воскрешение &#128123;", payload={"died": "resurrection"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

start_over = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Да", payload={"died": "start_over_yes"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback("Нет", payload={"died": "start_over_no"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)

resurrection = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Купить", payload={"died": "buy_chung"}), color=KeyboardButtonColor.POSITIVE)
    .add(Callback("Отмена", payload={"died": "start_over_no"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)

have_not_chung = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("Я куплю вип!", payload={"died": "buy_vip"}), color=KeyboardButtonColor.SECONDARY)
    .add(Callback("Начать сначала", payload={"died": "start_over"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
