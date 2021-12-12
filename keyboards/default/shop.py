from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

from settings.cannot_change import products

shop_menu = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Центр &#127978;", payload={"shop": "indicators"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Одежда &#128088;"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Работа &#128188;"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

shop_products_fruits = (
    Keyboard(one_time=False, inline=False)
    .add(Callback(f"{products['apple']['emoji']} ({products['apple']['fire']}&#128293;"
                  f"{products['apple']['reserve']}&#129377;)",
                  payload={"products": "apple"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{products['kiwi']['emoji']} ({products['kiwi']['fire']}&#128293;"
                  f"{products['kiwi']['reserve']}&#129377;)",
                  payload={"products": "kiwi"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback(f"{products['banana']['emoji']} ({products['banana']['fire']}&#128293;"
                  f"{products['banana']['reserve']}&#129377;)",
                  payload={"products": "banana"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Десерты &#10145;", payload={"shop": "products_gastronomy"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"shop": "back_to_menu"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

shop_products_fastfood = (
    Keyboard(one_time=False, inline=False)
    .add(Callback(f"{products['fries']['emoji']} ({products['fries']['fire']}&#128293;"
                  f"{products['fries']['reserve']}&#129377;)",
                  payload={"products": "fries"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{products['hamburger']['emoji']} ({products['hamburger']['fire']}&#128293;"
                  f"{products['hamburger']['reserve']}&#129377;)",
                  payload={"products": "hamburger"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback(f"{products['pizza']['emoji']} ({products['pizza']['fire']}&#128293;"
                  f"{products['pizza']['reserve']}&#129377;)",
                  payload={"products": "pizza"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Мясо &#10145;", payload={"shop": "products_meat"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"shop": "back_to_menu"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

shop_products_meat = (
    Keyboard(one_time=False, inline=False)
    .add(Callback(f"{products['bacon']['emoji']} ({products['bacon']['fire']}&#128293;"
                  f"{products['bacon']['reserve']}&#129377;)",
                  payload={"products": "bacon"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Callback(f"{products['meat']['emoji']} ({products['meat']['fire']}&#128293;"
                  f"{products['meat']['reserve']}&#129377;)",
                  payload={"products": "meat"}),
         color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Callback(f"{products['poultry_leg']['emoji']} ({products['poultry_leg']['fire']}&#128293;"
                  f"{products['poultry_leg']['reserve']}&#129377;)",
                  payload={"products": "poultry_leg"}),
         color=KeyboardButtonColor.SECONDARY)
    .add(Text("Фрукты &#10145;", payload={"shop": "products_fruits"}), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("&#11013; Назад", payload={"shop": "back_to_menu"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

shop_products_gastronomy = (
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
    .add(Text("&#11013; Назад", payload={"shop": "back_to_menu"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

shop_coffee = (
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
    .add(Text("&#11013; Назад", payload={"shop": "back_to_menu"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)
