import os.path

from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.card import MDCard


Window.size = (428, 926)
print("window")

class TimerCard(MDCard):
    # set variables to be used
    event = None
    targettime = NumericProperty(0)
    currenttime = NumericProperty(0)
    displaytime = NumericProperty(0)
    selecttime = NumericProperty(0)
    progressbaropacity = NumericProperty(0)
    startbuttonopacity = NumericProperty(100)
    disabled = False
    print("variables")
    # change targettime when buttons are pressed
    def change_targettime(self, time):
        print("change targettime")
        self.targettime += time
        self.displaytime += time
        self.selecttime += time

    # update the progressbar, reset when finished and add to score
    def update_bar(self, dt):
        print("update bar")
        if self.currenttime < self.targettime - 1:
            self.currenttime += 1
            self.displaytime -= 0.01
        else:
            # stop the progress bar
            self.event.cancel()
            self.event = None
            # reset targettime to correct value
            self.targettime /= 100
            # reset the opacity for the progress bar and start button
            self.progressbaropacity = 0
            self.startbuttonopacity = 100
            self.currenttime = 0
            # add new value to score
            self.app.score += self.targettime ** 1.2
            # enable buttons
            self.disabled = False
            # debugging info
            print("Progress bar finished! Gained", self.targettime ** 1.2,
                  "points! Score is now", self.app.score)

    # start updating the progress bar, repeat the update function once every second
    def start_update(self):
        print("start update")
        # check if value is valid
        if self.targettime <= 0:
            pass
        elif self.event is None and self.app.score >= self.targettime:
            # start the progress bar
            self.event = Clock.schedule_interval(self.update_bar, 0.01)
            self.startbuttonopacity = 0
            self.progressbaropacity = 100
            self.app.score -= self.targettime
            self.disabled = True
            # multiply targettime to make progress bar smoother
            self.targettime *= 100


class ProgressBarsApp(MDApp):
    # score variable
    score = NumericProperty(0)
    newslotprice = NumericProperty(1000)
    print("score variables")
    # load the savefile to resume progress. autosave every second
    def __init__(self, **kwargs):
        self.cards = []
        super().__init__()
        Clock.schedule_once(self.load, 0)
        Clock.schedule_interval(self.save, 1)
        print("init")

    # function for adding another card and check if player has enough points
    def make_card(self):
        print("make card")
        def add_card():
            print("add card")
            card = TimerCard()
            card.app = self
            self.cards.append(card)
            self.root.ids.box.add_widget(card)
            self.score = self.score - self.newslotprice
            # make next card more expensive
            self.newslotprice = 1000 * len(self.cards) * 1.18
            print("add card end")

        if self.score > self.newslotprice:
            add_card()

    def make_card_on_load(self):
        print("card on load start")
        card = TimerCard()
        card.app = self
        self.cards.append(card)
        self.root.ids.box.add_widget(card)
        print("card on load end")

    # save to file function
    def save(self, _):
        print("save start")
        with open("savefile.txt", mode="w") as f:
            savetext = str(self.score) + "\n"
            for card in self.cards:
                savetext += str(card.currenttime) + "," + str(card.targettime) + "\n"
            f.write(savetext)
            f.close()
        print("save end")

    # load savefile function
    def load(self, _):

        def readfile():
            print("readfile start")
            self.score = float(f.readline())
            self.cards = []
            for line in f:
                print("readfile loop")
                current, target = line.split(",")
                self.make_card_on_load()
                self.cards[-1].currenttime = current
                self.cards[-1].targettime = target
                self.cards[-1].displaytime = target
                self.cards[-1].selecttime = target
                if float(current) > 0:
                    self.score += float((target.strip()))
                    self.cards[-1].start_update()
            f.close()
            print("readfile end")

        if os.path.exists("savefile.txt"):
            print("true")
            with open("savefile.txt", mode="r") as f:
                readfile()
        else:
            print("false")
            with open("savefile.txt", mode="w") as f:
                f.write("2\n0,0")
                f.close()
            with open("savefile.txt", mode="r") as f:
                readfile()


if __name__ == "__main__":
    ProgressBarsApp().run()
