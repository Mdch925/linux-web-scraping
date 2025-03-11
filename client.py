import socket
import ssl
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

# إعداد SSL مع تعطيل التحقق من الشهادة
context = ssl.create_default_context()
context.check_hostname = False  # تعطيل التحقق من اسم المضيف
context.verify_mode = ssl.CERT_NONE  # تعطيل التحقق من الشهادات

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket, server_hostname="127.0.0.1")
secure_socket.connect(("127.0.0.1", 12345))  # الاتصال بالسيرفر


class ChatApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")

        self.chat_label = Label(text="📩 chating")
        self.layout.add_widget(self.chat_label)

        self.chat_display = TextInput(readonly=True, size_hint_y=4)
        self.layout.add_widget(self.chat_display)

        self.message_input = TextInput(hint_text="📝 Enter your message")
        self.layout.add_widget(self.message_input)

        self.send_button = Button(text="إرسال", on_press=self.send_message)
        self.layout.add_widget(self.send_button)

        threading.Thread(target=self.receive_messages, daemon=True).start()

        return self.layout

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            secure_socket.send(message.encode("utf-8"))
            self.message_input.text = ""

    def receive_messages(self):
        while True:
            try:
                message = secure_socket.recv(1024).decode("utf-8")
                Clock.schedule_once(lambda dt: self.update_chat(message), 0)
            except:
                break

    def update_chat(self, message):
        self.chat_display.text += f"\n{message}"


if __name__ == "__main__":
    ChatApp().run()
