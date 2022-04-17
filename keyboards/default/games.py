from vkbottle import Keyboard, KeyboardButtonColor, Text


games_menu = [(
    Keyboard(one_time=False, inline=False)
    .add(Text("Рулетка&#127744;", payload={"games": "roulette"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Слоты &#127920;", payload={"games": "slots"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Яблочко&#127822;", payload={"games": "dice"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Dice &#127922;", payload={"games": "chat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
),
(
    Keyboard(one_time=False, inline=False)
    .add(Text("Рулетка&#127744;", payload={"games": "roulette"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Слоты &#127920;", payload={"games": "slots"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Яблочко&#127822;", payload={"games": "dice"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Викторина&#129300;", payload={"games": "chat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
),
(
    Keyboard(one_time=False, inline=False)
    .add(Text("Рулетка&#127744;", payload={"games": "roulette"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Слоты &#127920;", payload={"games": "slots"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Яблочко&#127822;", payload={"games": "dice"}), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Виселица&#128565;", payload={"games": "chat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)
]


def generate_roulette_menu(bid):
    return (
        Keyboard(one_time=False, inline=False)
        .add(Text(f'&#10084;', payload={"roulette_red": bid}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'&#128154;', payload={"roulette_green": bid}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'&#128420;', payload={"roulette_black": bid}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text(f'Ставка: {"{0:,}".format(bid).replace(",", ".")}&#128293;' if bid < 1000000 else
                  f'{"{0:,}".format(bid).replace(",", ".")}&#128293;',
                  payload={"roulette": "bid"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'Правила&#128211;', payload={"roulette": "rules"}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("&#11013; Назад", payload={"roulette": "games"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Домой&#127968;", payload={"roulette": "home"}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
    )


def generate_roulette_bid_menu(bids, bid):
    colors = [KeyboardButtonColor.SECONDARY]*5
    for i in range(4, -1, -1):
        if bids[i] == bid:
            colors[i] = KeyboardButtonColor.POSITIVE
            break
    return (
        Keyboard(one_time=False, inline=False)
        .add(Text(f'{"{0:,}".format(bids[0]).replace(",", ".")}&#128293;', payload={"roulette_bid": bids[0]}),
             color=colors[0])
        .add(Text(f'{"{0:,}".format(bids[1]).replace(",", ".")}&#128293;', payload={"roulette_bid": bids[1]}),
             color=colors[1])
        .add(Text(f'{"{0:,}".format(bids[2]).replace(",", ".")}&#128293;', payload={"roulette_bid": bids[2]}),
             color=colors[2])
        .row()
        .add(Text(f'{"{0:,}".format(bids[3]).replace(",", ".")}&#128293;', payload={"roulette_bid": bids[3]}),
             color=colors[3])
        .add(Text(f'Ва-банк&#128293;', payload={"roulette_bid": bids[4]}), color=colors[4])
        .row()
        .add(Text("&#11013; Назад", payload={"roulette": "menu"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
    )
