from vkbottle import Keyboard, OpenLink, Text, KeyboardButtonColor

link_to_chat = (
    Keyboard(one_time=False, inline=True)
    .add(OpenLink(label="Присоединиться к беседе", link='___'))
    .get_json()
)