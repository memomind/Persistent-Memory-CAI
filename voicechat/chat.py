import flet as ft
from ._msg import Message,ChatMessage
from ._response import reply


def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "广东话聊天机器人"

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )


    def join_chat_click(e):
        if join_user_name.value is None or join_user_name=='':
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            on_message(Message('ChatBot', '你好，我係廣東話傾偈機械人。 有咩可以幫到你？', message_type='chat_message'))
            page.update()

    def send_message_click(e):
        new_msg = new_message.value
        if new_msg != "":
            on_message(Message(page.session.get("user_name"), new_msg, message_type="chat_message"))
            response = reply(new_msg)
            on_message(Message('ChatBot', response, message_type='chat_message'))
            new_message.value = ""
            new_message.focus()
            page.update()


    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()


    # A dialog asking for a user display name
    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )



    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
            # width=1300

        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

def run():
    ft.app(port=8550, target=main)