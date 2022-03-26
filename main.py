# # from re import L
# # from tkinter import Grid
# from tkinter import Grid
# import kivy
# from kivy.app import App
# from kivy.uix.label import Label
# # from kivy.uix.gridlayout import GridLayout
# from kivy.uix.floatlayout import FloadLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.widget import Widget
# from kivy.properties import ObjectProperty


# class MyGrid(Widget):
#     name = ObjectProperty(None)
#     email = ObjectProperty(None)
#     pass

#     def btn(self):
#         print("Name: ", self.name.text, " Email: ", self.email.text)

# class MyApp(App):
#     def build(self):
#         return MyGrid()


# if __name__ == "__main__":
#     MyApp().run()

import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen




class HomeScreen(Screen):
    pass
class NewGameScreen(Screen):
    pass
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


# class TestApp(App):
#     def build(self):
#         # create the screen manager
#         sm = ScreenManager()
#         homeScreen = Screen(name='home screen')
#         sm.add_widget(homeScreen)
#         loadGameScreen = Screen(name='load game screen')
#         sm.add_widget(loadGameScreen)
#         newGameScreen = Screen(name='new game screen')
#         sm.add_widget(newGameScreen)
#         return sm


# class MyApp(App):
#     def build(self):
#         return FloatLayout()

