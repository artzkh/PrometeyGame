from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

from settings.cannot_change import products, coffee, sauna, game, pharmacy

shop_products_fruits = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{products['apple']['emoji']} ({products['apple']['fire']}&#128293;"
              f"{products['apple']['reserve']}&#129377;)",
              payload={"products": "apple"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{products['kiwi']['emoji']} ({products['kiwi']['fire']}&#128293;"
              f"{products['kiwi']['reserve']}&#129377;)",
              payload={"products": "kiwi"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{products['banana']['emoji']} ({products['banana']['fire']}&#128293;"
              f"{products['banana']['reserve']}&#129377;)",
              payload={"products": "banana"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Десерты &#10145;", payload={"shop": "products_gastronomy"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "products"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_products_fastfood = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{products['fries']['emoji']} ({products['fries']['fire']}&#128293;"
              f"{products['fries']['reserve']}&#129377;)",
              payload={"products": "fries"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{products['hamburger']['emoji']} ({products['hamburger']['fire']}&#128293;"
              f"{products['hamburger']['reserve']}&#129377;)",
              payload={"products": "hamburger"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{products['pizza']['emoji']} ({products['pizza']['fire']}&#128293;"
              f"{products['pizza']['reserve']}&#129377;)",
              payload={"products": "pizza"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Мясо &#10145;", payload={"shop": "products_meat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "products"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_products_meat = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{products['bacon']['emoji']} ({products['bacon']['fire']}&#128293;"
              f"{products['bacon']['reserve']}&#129377;)",
              payload={"products": "bacon"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{products['meat']['emoji']} ({products['meat']['fire']}&#128293;"
              f"{products['meat']['reserve']}&#129377;)",
              payload={"products": "meat"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{products['poultry_leg']['emoji']} ({products['poultry_leg']['fire']}&#128293;"
              f"{products['poultry_leg']['reserve']}&#129377;)",
              payload={"products": "poultry_leg"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Фрукты &#10145;", payload={"shop": "products_fruits"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "products"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_products_gastronomy = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{products['croissant']['emoji']} ({products['croissant']['fire']}&#128293;"
              f"{products['croissant']['reserve']}&#129377;)",
              payload={"products": "croissant"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{products['doughnut']['emoji']} ({products['doughnut']['fire']}&#128293;"
              f"{products['doughnut']['reserve']}&#129377;)",
              payload={"products": "doughnut"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{products['cake']['emoji']} ({products['cake']['fire']}&#128293;"
              f"{products['cake']['reserve']}&#129377;)",
              payload={"products": "cake"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Фастфуд &#10145;", payload={"shop": "products_fastfood"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "products"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_coffee = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{coffee['cookie']['emoji']} ({coffee['cookie']['fire']}&#128293;"
              f"{coffee['cookie']['energy']}&#9889;)",
              payload={"coffee": "cookie"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{coffee['cake']['emoji']} ({coffee['cake']['fire']}&#128293;"
              f"{coffee['cake']['energy']}&#9889;)",
              payload={"coffee": "cake"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{coffee['coffee']['emoji']} ({coffee['coffee']['fire']}&#128293;"
              f"{coffee['coffee']['energy']}&#9889;)",
              payload={"coffee": "coffee"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{coffee['cocktail']['emoji']} ({coffee['cocktail']['fire']}&#128293;"
              f"{coffee['cocktail']['energy']}&#9889;)",
              payload={"coffee": "cocktail"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "coffee"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_sauna = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{sauna['sponge']['emoji']} ({sauna['sponge']['fire']}&#128293;"
              f"{sauna['sponge']['hygiene']}&#129531;)",
              payload={"sauna": "sponge"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{sauna['soap']['emoji']} ({sauna['soap']['fire']}&#128293;"
              f"{sauna['soap']['hygiene']}&#129531;)",
              payload={"sauna": "soap"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{sauna['lotion']['emoji']} ({sauna['lotion']['fire']}&#128293;"
              f"{sauna['lotion']['hygiene']}&#129531;)",
              payload={"sauna": "lotion"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{sauna['broom']['emoji']} ({sauna['broom']['fire']}&#128293;"
              f"{sauna['broom']['hygiene']}&#129531;)",
              payload={"sauna": "broom"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "sauna"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_game = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{game['joystick']['emoji']} ({game['joystick']['fire']}&#128293;"
              f"{game['joystick']['happiness']}&#127881;)",
              payload={"game": "joystick"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{game['karaoke']['emoji']} ({game['karaoke']['fire']}&#128293;"
              f"{game['karaoke']['happiness']}&#127881;)",
              payload={"game": "karaoke"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{game['film']['emoji']} ({game['film']['fire']}&#128293;"
              f"{game['film']['happiness']}&#127881;)",
              payload={"game": "film"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{game['gamepad']['emoji']} ({game['gamepad']['fire']}&#128293;"
              f"{game['gamepad']['happiness']}&#127881;)",
              payload={"game": "gamepad"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "game"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_pharmacy = (
    Keyboard(one_time=False, inline=False)
    .add(Text(f"{pharmacy['mandarin']['emoji']} ({pharmacy['mandarin']['fire']}&#128293;"
              f"{pharmacy['mandarin']['health']}&#129505;)",
              payload={"pharmacy": "mandarin"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{pharmacy['honey']['emoji']} ({pharmacy['honey']['fire']}&#128293;"
              f"{pharmacy['honey']['health']}&#129505;)",
              payload={"pharmacy": "honey"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{pharmacy['syringe']['emoji']} ({pharmacy['syringe']['fire']}&#128293;"
              f"{pharmacy['syringe']['health']}&#129505;)",
              payload={"pharmacy": "pill"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text(f"{pharmacy['pill']['emoji']} ({pharmacy['pill']['fire']}&#128293;"
              f"{pharmacy['pill']['health']}&#129505;)",
              payload={"pharmacy": "pill"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "pharmacy"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)

shop_hookah = (
    Keyboard(one_time=False, inline=False)
    .add(Callback(f"{products['croissant']['emoji']} ({products['croissant']['fire']}&#128293;"
                  f"{products['croissant']['reserve']}&#129377;)",
                  payload={"products": "croissant"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{products['doughnut']['emoji']} ({products['doughnut']['fire']}&#128293;"
                  f"{products['doughnut']['reserve']}&#129377;)",
                  payload={"products": "doughnut"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback(f"{products['cake']['emoji']} ({products['cake']['fire']}&#128293;"
                  f"{products['cake']['reserve']}&#129377;)",
                  payload={"products": "cake"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Фастфуд &#10145;", payload={"shop": "products_fastfood"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Центр&#127978;", payload={"back_shop": "hookah"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)
