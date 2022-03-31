
from dis import dis
from xml.etree.ElementPath import get_parent_map
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
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
            print("                         !!! WARNING !!! - there are more than 3 cards held by the player")
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
playerOrder = ['Scarlett', 'Green', 'Peacock', 'Plum', 'Mustard', 'Orchid']     # this contents is not final... it will be changed by the clickPlayerOrderCheckbox function
analysisTable = [[ ["?"] for i in range(6)] for j in range(21)]
actualKillerWeaponRoom = ["?", "?", "?"]
announcementsHaveBeenMadeForKillerWeaponRoom = [False, False, False]   # this regulates when, in the terminal, the discovery of the killer/weapon/room is announced
fileName = ""





class HomeScreen(Screen):
    pass

class PlayerSelectScreen(Screen):
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
        if instance.active == True:
            self.ids.next_button.disabled = False           # this line, and the for loop above it, will work to enable the NEXT button
        else:
            self.ids.next_button.disabled = True
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
        print("in the startGame function, the userCharacter is set to: " + str(userCharacter.getNameOnly()))

class CardDeclarationScreen(Screen):
    numberOfCardsSelected = NumericProperty(0)
    def clickOnBox(self, instance, value):
        # print(value)
        if value == True:
            self.numberOfCardsSelected += 1
            for card in cardList:
                if card.getName() == instance.text:
                    # put card into user character's cardList
                    userCharacter.addToCardList(card)        
                    print(str(card.getName() + " added to " + str(userCharacter.getNameOnly() + " cardList.")))
        if value == False:
            self.numberOfCardsSelected -= 1
            for card in cardList:
                if card.getName() == instance.text:
                    userCharacter.removeFromCardList(card)
                    print(str(card.getName() + " removed from " + str(userCharacter.getNameOnly() + " cardList.")))                    
        # change the color of the Label & checkbox
        for key, val in self.ids.items():
            if val.text == instance.text and value == True:
                val.color = 0, 1, 0.2, 1
            elif val.text == instance.text and value == False:
                val.color = 1, 1, 1, 1
        print("numberOfCardsSelected: " + str(self.numberOfCardsSelected) + "        " + str(userCharacter.getNameOnly()) + "'s card list: " + str(userCharacter.getCardList()))
        if self.numberOfCardsSelected == 3:
            self.ids.next_button.disabled = False
        else:
            self.ids.next_button.disabled = True
    def uncheckAllCheckboxes(self):
        for key, val in self.ids.items():
            val.active = False      # it seems that setting the checkbox.active to False **counts as a click**    !!!!, so it automatically calls the clickOnBox function!
    def pressNEXTbutton(self):
        if self.numberOfCardsSelected == 3:
            pass
        else:
            pass

class PlayerOrderScreen(Screen):
    playerOrdersSelected = NumericProperty(0)
    def clickPlayerOrderCheckbox(self, instance):
        # CHANGE THE CONTENTS OF THE playerOrder GLOBAL VARIABLE
        turnNumber = instance.vrs['turnNumber']
        player = instance.vrs['player']
        global playerOrder 
        playerOrder[turnNumber - 1] = player
        print("player order: " + str(playerOrder))
        if instance.active == True:
            self.playerOrdersSelected += 1
        else:
            self.playerOrdersSelected -= 1            
        if self.playerOrdersSelected == 6:
            self.ids.next_button.disabled = False
        else:
            self.ids.next_button.disabled = True


        # CHANGE THE APPEARANCE OF THE SCREEN
        # turn EVERY CELL to disabled = False
        for key, val in self.ids.items():
            if val.vrs['type'] != 'next_button':        # gotta make sure we don't enable the next_button until 6 playerOrders are selected
                val.disabled = False

        # change the color of the clicked checkbox & its label, and also change the rowLabel color
        for key, val in self.ids.items():
            #       "if it's the same turnNumber, the same player or if it's a rowLabel, then change the color"
            if val.vrs['turnNumber'] == instance.vrs['turnNumber'] and (val.vrs['player'] == instance.vrs['player'] or val.vrs['player'] == 'rowLabel'):
                if instance.active == True:
                    val.color = 0, 1, 0.2, 1
                if instance.active == False:
                    val.color = 1, 1, 1, 1                        
        
        # for reference:
        # EXAMPLE from .kv file:      vrs: {'turnNumber': 1, 'player': 'Orchid', 'type': 'label', 'shouldBeDisabled': False}

        # now evaluate the entire grid and decide what should or should not be DISABLED
        for key, val in self.ids.items():
            # find a clicked checkbox
            if val.vrs['type'] == 'checkbox' and val.active == True:
                for a, b, in self.ids.items():
                    # the checkboxes and labels in the same column should be DISABLED
                    #  if turnNumber is different...                and player is the same...                and type is checkbox and label, but not the rowLabel
                    if b.vrs['turnNumber'] != val.vrs['turnNumber'] and b.vrs['player'] == val.vrs['player'] and b.vrs['player'] != 'rowLabel':
                        # b.vrs['shouldBeDisabled'] = 'True'
                        b.disabled = True
                    # the other labels in the same row should be DISABLED
                    #  if turnNumber is the same...                 and player is different...               and type is label ONLY,      but not the rowLabel
                    if b.vrs['turnNumber'] == val.vrs['turnNumber'] and b.vrs['player'] != val.vrs['player'] and b.vrs['type'] == 'label' and b.vrs['player'] != 'rowLabel':
                        # b.vrs['shouldBeDisabled']= 'True'
                        b.disabled = True

class ConfirmationScreen(Screen):
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

###########################################################################################################################################################
#       end of kivy stuff








#############################
#   break


