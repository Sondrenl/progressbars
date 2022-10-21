
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


class DebuggingApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 10
        Clock.schedule_once(self.test)

    def test(self, _):
        self.value = 20
        print(self.value)


if __name__ == "__main__":
    DebuggingApp().run()
