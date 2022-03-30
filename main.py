
from xml.etree.ElementPath import get_parent_map
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
import datetime
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox



print("CLUE SOLVER")


userCharacterName = ""          #   this will be defined by the checkboxes on the new game screen

numberOfFunctionCalls = 0       # keeping track of how much processing is being done, for the sake of becoming more efficient

initialAnalysisCompletedOfLoadedSavedGame = [False, False]
initialAnalysisCompletedOfLoadedSavedGame[0] = False    # this will toggle to True after the first time processDecline() is run, after a saved game is loaded
initialAnalysisCompletedOfLoadedSavedGame[1] = False    # this will toggle to True after the first time processRespond() is run, after a saved game is loaded

class Card:
    def __init__(self, name, type, place) -> None:
        self.name = name
        self.type = type    # i.e., killer / weapon / room
        self.owner = "unknown"      # might not use this
        self.placeInCardList = place
    def __repr__(self) -> str:
        output = self.name + " (" + self.type + ")"
        return output
    def getType(self):
        return self.type
    def getName(self):
        return self.name
    def getNumberAndName(self):
        tempString = str(self.placeInCardList) + ". " + str(self.name)
        return tempString
    def setOwner(self, player):
        self.owner = player
    def getOwner(self):
        return self.owner
    def getPlaceInCardList(self):
        return self.placeInCardList

greenCard =         Card("Green", "killer", 0)
mustardCard =       Card("Mustard", "killer", 1)
peacockCard =       Card("Peacock", "killer", 2)
plumCard =          Card("Plum", "killer", 3)
scarlettCard =      Card("Scarlett", "killer", 4)
orchidCard =        Card("Orchid", "killer", 5)

candlestickCard =   Card("Candlestick", "weapon", 6)
daggerCard =        Card("Dagger", "weapon", 7)
pipeCard =          Card("Pipe", "weapon", 8)
revolverCard =      Card("Revolver", "weapon", 9)
ropeCard =          Card("Rope", "weapon", 10)
wrenchCard =        Card("Wrench", "weapon", 11)

ballroomCard =      Card("Ballroom", "room", 12)
billiardRoomCard =  Card("Billiard Room", "room", 13)
conservatoryCard =  Card("Conservatory", "room", 14)
diningRoomCard =    Card("Dining Room", "room", 15)
hallCard =          Card("Hall", "room", 16)
kitchenCard =       Card("Kitchen", "room", 17)
libraryCard =       Card("Library", "room", 18)
loungeCard =        Card("Lounge", "room", 19)
studyCard =         Card("Study", "room", 20)

cardList = [greenCard, mustardCard, peacockCard, plumCard, scarlettCard, orchidCard, candlestickCard, daggerCard, pipeCard, revolverCard, ropeCard, wrenchCard, ballroomCard, billiardRoomCard, conservatoryCard, diningRoomCard, hallCard, kitchenCard, libraryCard, loungeCard, studyCard]


class Player:
    def __init__(self, name, turn = -1, column = -1) -> None:
        self.name = name
        self.card1 = Card
        self.card2 = Card
        self.card3 = Card
        self.cardList = []
        self.turnOrder = turn
        self.turnOrderConfirmed = False
        self.columnNumber = column          # this is the column this player will ALWAYS have in the analysisTable
    def __repr__(self) -> str:
        return self.name #+ ", cards: " + self.card1 + ", " + self.card2 + ", " + self.card3
    def getInfoList(self):
        return [self.name, self.turnOrder, self.card1, self.card2, self.card3]
    def getNameOnly(self):
        return self.name
    def getTurnOrder(self):
        return self.turnOrder
    def setTurnOrder(self, newTurn):
        self.turnOrder = newTurn
    def getConfirmedStatus(self):
        return self.turnOrderConfirmed
    def turnOrderConfirmedSetTrue(self):
        self.turnOrderConfirmed = True
    
    def getCardList(self):
        return self.cardList
    def addToCardList(self, card):
        if len(self.cardList) >= 3:
            self.cardList.append(card)
            print("                         !!! WARNING !!! - there are already 3 cards held by the player")
        else:
            self.cardList.append(card)
    def removeFromCardList(self, card):
        self.cardList.remove(card)
    def resetCardList(self):
        self.cardList = []
    
    def addCard1(self, card):
        self.card1 = card
    def addCard2(self, card):
        self.card2 = card
    def addCard3(self, card):
        self.card3 = card
    def getCard1(self):
        return self.card1
    def getCard2(self):
        return self.card2
    def getCard3(self):
        return self.card3

    def getColumnNumber(self):
        return self.columnNumber

scarlettPlayer =  Player("Scarlett", 1, 0)
greenPlayer =     Player("Green", 2, 1)
orchidPlayer =    Player("Orchid", 6, 5)
mustardPlayer =   Player("Mustard", 5, 4)
plumPlayer =      Player("Plum", 4, 3)
peacockPlayer =   Player("Peacock", 3, 2)
playerList = [scarlettPlayer, greenPlayer, orchidPlayer, mustardPlayer, plumPlayer, peacockPlayer]
userCharacter = Player


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
    def setUserCharacter(self, instance, name):
        global userCharacterName
        userCharacterName = name
        print("userCharacterName set to: " + str(userCharacterName))
        # for key, val in self.ids.items():
        #     if val.text == "Next":
        #         val.disabled = False
        self.ids.next_button.disabled = False           # this line, and the for loop above it, will work to enable the NEXT button
        # change text color of selected item
        for key, val in self.ids.items():
            if val.text == instance.text and instance.active == True:
                val.color = 0, 1, 0.2, 1
            if val.text == instance.text and instance.active == False:
                val.color = 1, 1, 1, 1
    def confirmUserCharacter(self):                #   this function is run when the user clicks the "Next" button after selecting their character
        global userCharacter
        for player in playerList:
            if player.getNameOnly() == userCharacterName:
                userCharacter = player
        print("in the startGame function, the userCharacter is: " + str(userCharacter.getNameOnly()))


numberOfCardsSelected = 0
class CardDeclarationScreen(Screen):
    def clickOnBox(self, instance, value):
        global numberOfCardsSelected            # this line allows us to write to the global variable
        # print(value)
        if value == True:
            numberOfCardsSelected += 1
            for card in cardList:
                if card.getName() == instance.text:
                    # put card into user character's cardList
                    userCharacter.addToCardList(card)        
        if value == False:
            numberOfCardsSelected -= 1
            for card in cardList:
                if card.getName() == instance.text:
                    userCharacter.removeFromCardList(card)
        # change the color of the Label & checkbox
        for key, val in self.ids.items():
            if val.text == instance.text and value == True:
                val.color = 0, 1, 0.2, 1
            elif val.text == instance.text and value == False:
                val.color = 1, 1, 1, 1
        print("numberOfCardsSelected: " + str(numberOfCardsSelected) + ". User's card list: " + str(userCharacter.getCardList()))
        if numberOfCardsSelected == 3:
            self.ids.next_button.disabled = False
        if numberOfCardsSelected != 3:
            self.ids.next_button.disabled = True
    def uncheckAllCheckboxes(self):
        for key, val in self.ids.items():
            val.active = False      # it seems that setting the checkbox.active to False **counts as a click**    !!!!, so it automatically calls the clickOnBox function!
    def pressNEXTbutton(self):
        if numberOfCardsSelected == 3:
            pass
        else:
            pass

class PlayerOrderScreen(Screen):
    def clickOnPlayerOrderBox(self, instance):  
        # disable this character name from being able to be selected for another turn
        if instance.active == True:
            for key, val in self.ids.items():
                print("key={0}, val={1}".format(key, val))          # so the id is the key, and the memory address is the value

            print("test begins here:")

            for key, val in self.ids.items():
                if "green" in key:
                    print("key: " + str(key))                   #### i think we're on to something here



            for key, val in self.ids.items():
                # print("val.text:      " + str(val.text))
                # print("val:           " + str(val))
                # print("val.ids:       " + str(val.ids))
                if val.text == instance.text and val != instance:
                    # print("val.text:      " + str(val.text))
                    # print("val:           " + str(val))
                    # print("instance.text: " + str(instance.text))
                    # print("instance:      " + str(instance))
                    # print("")
                    val.disabled = True
        if instance.active == False:
            for key, val in self.ids.items():
                if val.text == instance.text and val != instance:
                    val.disabled = False
    def testFunctionBaby(self, instance):
        # print(str(theVeryID))

        if instance in self.ids.values():
            print(list(self.ids.keys())[list(self.ids.values()).index(instance)])

        whatTurnIsIt = instance.memberOfTurn
        print("whatTurnIsIt: " + str(whatTurnIsIt))
###BINGO BINGO
        whatPlayerIsIt = instance.player
        print("whatPlayerIsIt: " + str(whatPlayerIsIt))


#   so we'll do something like:
#           if instance.whatTurnIsIt == 1 and instance.whatPlayerIsIt == "green":
#               for key, val in self.ids.items():
#                   if val.whatTurnIsIt != 1 and val.whatPlayerIsIt == "green":
#                       val.disabled = True
#                       






        if instance.active == True:
            # self.ids.green_checkbox_turn_1.color = 1, 0, 0, 1
            # self.ids.tempIDthing.color = 1, 0, 0, 1
            self.ids.green_label_turn_1.color = 1, 0, 0, 1
            self.ids.green_label_turn_2.disabled = True
            self.ids.green_checkbox_turn_2.disabled = True
            self.ids.green_label_turn_3.disabled = True
            self.ids.green_checkbox_turn_3.disabled = True
            self.ids.first_turn_label.color = 1, 0, 0, 1
        if instance.active == False:
            self.ids.green_checkbox_turn_1.color = 1, 1, 1, 1            
            self.ids.green_label_turn_1.color = 1, 1, 1, 1
            self.ids.green_label_turn_2.disabled = False
            self.ids.green_checkbox_turn_2.disabled = False
            self.ids.green_label_turn_3.disabled = False
            self.ids.green_checkbox_turn_3.disabled = False
            self.ids.first_turn_label.color = 1, 1, 1, 1













        # change the color of the label immediately above the clicked box, and of the clicked box itself
        # for key, val in self.ids.items():
        # # for key, val in instance.root.ids.items():
        #     if val.text == instance.text and instance.active == True:
        #         val.color = 0, 1, 0.2, 1
        #     elif val.text == instance.text and instance.active == False:
        #         val.color = 1, 1, 1, 1

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

###########################################################################################################################################################
#       end of kivy stuff








#############################
#   break


