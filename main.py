import os.path

from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.card import MDCard


Window.size = (1440, 2960)
Window.set_icon('icon.png')
Window.set_title('Progressbars')
# Window.grab_mouse()


class TimerCard(MDCard):
    # set variables to be used
    event = None
    target_time = NumericProperty(0)
    current_time = NumericProperty(0)
    display_time = NumericProperty(0)
    select_time = NumericProperty(0)
    progressbar_opacity = NumericProperty(0)
    start_button_opacity = NumericProperty(100)
    disabled = False

    # change target_time when buttons are pressed
    def change_target_time(self, time):
        self.target_time += time
        self.display_time += time
        self.select_time += time

    # update the progressbar, reset when finished and add to score
    def update_bar(self, dt):
        if self.current_time < self.target_time - 1:
            self.current_time += 1
            self.display_time -= 0.05
        else:
            # stop the progress bar
            self.event.cancel()
            self.event = None
            # reset target_time to correct value
            self.target_time /= 20
            # reset the opacity for the progress bar and start button
            self.progressbar_opacity = 0
            self.start_button_opacity = 100
            self.current_time = 0
            self.display_time = self.select_time
            # add new value to score
            self.app.score += self.target_time ** 1.2
            # enable buttons
            self.disabled = False
            # debugging info
            print("Progress bar finished! Gained", round(self.target_time ** 1.2, 2),
                  "points. Score is now", round(self.app.score, 4))

    # start updating the progress bar, repeat the update function once every second
    def start_update(self):
        # check if value is valid
        if self.target_time <= 0:
            pass
        elif self.event is None and self.app.score >= self.target_time:
            # start the progress bar
            self.event = Clock.schedule_interval(self.update_bar, 0.05)
            self.start_button_opacity = 0
            self.progressbar_opacity = 100
            self.app.score -= self.target_time
            self.disabled = True
            # multiply target_time to make progress bar smoother
            self.target_time *= 20


class ProgressBarsApp(MDApp):
    # score variable
    score = NumericProperty(0)
    new_slot_price = NumericProperty(1000)

    # load the savefile to resume progress. autosave every second
    def __init__(self, **kwargs):
        self.cards = []
        super().__init__()
        Clock.schedule_once(self.load, 0)
        Clock.schedule_interval(self.save, 1)

    # function for adding another card and check if player has enough points
    def make_card(self):

        def add_card():
            card = TimerCard()
            card.app = self
            self.cards.append(card)
            self.root.ids.box.add_widget(card)
            self.score = self.score - self.new_slot_price
            # make next card more expensive
            self.new_slot_price = 1000 * len(self.cards)

        if self.score > self.new_slot_price:
            add_card()

    def make_card_on_load(self):
        card = TimerCard()
        card.app = self
        self.cards.append(card)
        self.root.ids.box.add_widget(card)

    # save to file function
    def save(self, _):
        with open("savefile.txt", mode="w") as f:
            savetext = str(self.score) + "\n"
            for card in self.cards:
                savetext += str(card.current_time) + "," + str(card.target_time) + "\n"
            f.write(savetext)
            f.close()

    # load savefile function
    def load(self, _):

        def readfile():
            self.score = float(f.readline())
            self.cards = []
            for line in f:
                current, target = line.split(",")
                self.make_card_on_load()

                if float(current) > 0:
                    self.cards[-1].current_time = float(current)
                    self.cards[-1].target_time = float(target) / 20
                    self.cards[-1].display_time = float(current) / 20
                    self.cards[-1].select_time = float(target) / 20

                    self.score += float((target.strip())) / 20
                    self.cards[-1].start_update()
                else:
                    self.cards[-1].current_time = current
                    self.cards[-1].target_time = target
                    self.cards[-1].display_time = target
                    self.cards[-1].select_time = target

            f.close()

        if os.path.exists("savefile.txt"):
            with open("savefile.txt", mode="r") as f:
                readfile()
        else:
            with open("savefile.txt", mode="w") as f:
                f.write("2\n0,0")
                f.close()
            with open("savefile.txt", mode="r") as f:
                readfile()


if __name__ == "__main__":
    ProgressBarsApp().run()
