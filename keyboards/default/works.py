from vkbottle import Keyboard, KeyboardButtonColor, Callback, Text


cleaner_menu = (
        Keyboard(one_time=False, inline=True)
        .add(Text("Работать", payload={"work": "cleaner:start"}), color=KeyboardButtonColor.POSITIVE)
        .get_json()
        )

cleaner_work = ((
        Keyboard(one_time=False, inline=True)
        .add(Text("🧹", payload={"work": "cleaner:true"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("🧹", payload={"work": "cleaner:false"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text("🧹", payload={"work": "cleaner:false"}), color=KeyboardButtonColor.SECONDARY)
        .get_json()
        ),
        (
        Keyboard(one_time=False, inline=True)
        .add(Text("🧹", payload={"work": "cleaner:false"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text("🧹", payload={"work": "cleaner:true"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("🧹", payload={"work": "cleaner:false"}), color=KeyboardButtonColor.SECONDARY)
        .get_json()

        ),
        (
        Keyboard(one_time=False, inline=True)
        .add(Text("🧹", payload={"work": "cleaner:false"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text("🧹", payload={"work": "cleaner:false"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text("🧹", payload={"work": "cleaner:true"}), color=KeyboardButtonColor.POSITIVE)
        .get_json()
        )
)

works_list = (
        Keyboard(one_time=False, inline=False)
        .add(Text("Дворник 🧹", payload={"work": "cleaner"}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Город &#127890;", payload={"main_menu": "shop_menu"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Домой&#127968;", payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
        )
