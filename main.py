
from xml.etree.ElementPath import get_parent_map
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty


userCharacter = ""

class HomeScreen(Screen):
    pass
class NewGameScreen(Screen):
    userNNNNname = StringProperty("")

    # def update(self):
    #     name = self.ids.enterTextHere_textInput.text
    #     self.ids.textAppearsHere_label.text = name
    #     self.ids.enterTextHere_textInput.text = ""
  
    def checkbox_click(self, instance, value):      # value is boolean, true if clicked
        print(value)
        if value == True:
            pass
        else:
            pass
    def getUserCharacter(self, name):
        global userCharacter
        userCharacter = name
        print("userName: " + str(userCharacter))


        # if self.scarlett.active:
        #     userCharacter = "scarlett"
        # elif self.green.active:
        #     userCharacter = "green"
        # elif self.peacock.active:
        #     userCharacter = "peacock"
        # elif self.plum.active:
        #     userCharacter = "plum"
        # elif self.mustard.active:
        #     userCharacter = "mustard"
        # elif self.orchid.active:
        #     userCharacter = "orchid"
        # else:
        #     print("no character selected")
        # print("userCharacter: " + str(userCharacter))

class LoadGameScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()

