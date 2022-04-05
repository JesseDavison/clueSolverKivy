import datetime
from dis import dis
from fileinput import filename
import os
import ast
from os import stat
from tkinter import BooleanVar
from xml.etree.ElementPath import get_parent_map
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
import datetime
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView


print("CLUE SOLVER")


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
    # @staticmethod
    def getCardFromCardList(self, integer):
        return self.cardList[integer]
    
    def getColumnNumber(self):
        return self.columnNumber

# tempPlayer = Player("temp", -1, -1)
scarlettPlayer =  Player("Scarlett", 1, 0)
greenPlayer =     Player("Green", 2, 1)
orchidPlayer =    Player("Orchid", 6, 5)
mustardPlayer =   Player("Mustard", 5, 4)
plumPlayer =      Player("Plum", 4, 3)
peacockPlayer =   Player("Peacock", 3, 2)
playerList = [scarlettPlayer, greenPlayer, orchidPlayer, mustardPlayer, plumPlayer, peacockPlayer]

userCharacterName = ""          #   this will be defined by the checkboxes on the new game screen
userCharacter = Player
playerOrder = ['', '', '', '', '', '']     # to be changed by the clickPlayerOrderCheckbox function
analysisTable = [[ ["?"] for i in range(6)] for j in range(21)]
actualKillerWeaponRoom = ["?", "?", "?"]
announcementsHaveBeenMadeForKillerWeaponRoom = [False, False, False]   # this regulates when, in the terminal, the discovery of the killer/weapon/room is announced
fileName = ""
currentTurnNumber = -1
turnLog = {}


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
        
        if instance.active == True:
            playerOrder[turnNumber - 1] = player
            self.playerOrdersSelected += 1
            print("active")
        else:
            playerOrder[turnNumber - 1] = ''
            self.playerOrdersSelected -= 1            
            print("not active")
        if self.playerOrdersSelected == 6:
            self.ids.next_button.disabled = False
        else:
            self.ids.next_button.disabled = True
        print("player order: " + str(playerOrder))

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
        print("Just to confirm, the user's character is: " + str(userCharacter.getNameOnly()))
    
    @staticmethod
    def confirmPlayerOrder():
        # SET THE .turnOrder PROPERTY OF EACH PLAYER OBJECT
        x = 1
        for name in playerOrder:
            for player in playerList:
                if name == player.getNameOnly():
                    player.setTurnOrder(x)
            x += 1

class ConfirmationScreen(Screen):
    def on_enter(self, *args):
        self.ids.you_are_playing_as.text = "You are playing as " + userCharacter.getNameOnly()   
        self.ids.your_cards.text = "Your cards are " + str(userCharacter.getCardList())
        self.ids.your_player_order.text = "The player turn order is: " + str(playerOrder)     
        return super().on_enter(*args)
    def createGameSaveFile(self):
        x = datetime.datetime.now()     # create a timestamp, for the purpose of making a unique filename
        timeStamp = str(x.year) + "-" + str(x.month) + "-" + str(x.day) + " " + str(x.hour) + "h-" + str(x.minute) + "m-" + str(x.second) + "s"
        global fileName
        fileName = "ClueSolverGameSave " + str(timeStamp) + ".txt"        
        fileObject = open(fileName, 'w')        # use 'w' because we're creating a new file
        fileObject.write(str(userCharacter.getNameOnly()) + "\n")       # line 0
        fileObject.close()
        # add in the player's 3 cards
        fileObject = open(fileName, 'a')      # 'a' for append
        for x in range(len(userCharacter.getCardList())):
            fileObject.write(str(userCharacter.getCardFromCardList(x).getPlaceInCardList()) + "\n")     # lines 1, 2, 3
        # include the playerOrder
        fileObject.write(str(playerOrder) + "\n")       # line 4
        fileObject.write("{}\n")
        fileObject.write("0")
        fileObject.close()

        global currentTurnNumber
        currentTurnNumber = 1

class ExecuteTurnScreen(Screen):
    @staticmethod
    def convertTurnToPlayerTurn(turnNum):
        return ((turnNum - 1) % 6) + 1

    respondentList = ['', '', '', '', '', '']

    def on_enter(self, *args):
        global currentTurnNumber
        activePlayer = Player
        for player in playerList:
            if player.getTurnOrder() == self.convertTurnToPlayerTurn(int(currentTurnNumber)):
                activePlayer = player
        activePlayerName = activePlayer.getNameOnly()      
        self.respondentList[0] = str(activePlayerName) 

        # now identify who 'player1 response' is, who 'player2 response' is, etc
        incrementalVariable = 1
        while incrementalVariable < 6:
            respondentTurnOrder = self.convertTurnToPlayerTurn(currentTurnNumber + incrementalVariable)
            for player in playerList:
                if player.getTurnOrder() == respondentTurnOrder:
                    self.respondentList[incrementalVariable] = str(player.getNameOnly())
            incrementalVariable += 1
        # now put those players' names onto the screen
        self.ids.player1_response_label.text = str(self.respondentList[1])
        self.ids.player2_response_label.text = str(self.respondentList[2])
        self.ids.player3_response_label.text = str(self.respondentList[3])
        self.ids.player4_response_label.text = str(self.respondentList[4])
        self.ids.player5_response_label.text = str(self.respondentList[5])
        # prepare the spinners so they can easily tell us which player they represent
        self.ids.player1_response_spinner.playerName = str(self.respondentList[1])
        self.ids.player2_response_spinner.playerName = str(self.respondentList[2])
        self.ids.player3_response_spinner.playerName = str(self.respondentList[3])
        self.ids.player4_response_spinner.playerName = str(self.respondentList[4])
        self.ids.player5_response_spinner.playerName = str(self.respondentList[5])

        print("active player is: " + str(activePlayerName)) 
        self.ids.title_label.text = "Turn " + str(currentTurnNumber) + ", " + str(activePlayerName) + " suggests:"
        self.ids.title_label.defaultText = "Turn " + str(currentTurnNumber) + ", " + str(activePlayerName) + " suggests:"

        # initialize this turn's entry in turnLog
        global turnLog
        turnLog[currentTurnNumber] = {}
        turnLog[currentTurnNumber]['guesser'] = activePlayerName
        turnLog[currentTurnNumber]['killerGuessed'] = -1
        turnLog[currentTurnNumber]['weaponGuessed'] = -1
        turnLog[currentTurnNumber]['roomGuessed'] = -1
        for x in range(6):
            for player in playerList:               
                if x+1 == player.getTurnOrder():
                    turnLog[currentTurnNumber][str(player.getNameOnly()).lower() + "Response"] = "n"        
        turnLog[currentTurnNumber]['card'] = -1

        # set the spinners & checkboxes to default
        self.ids.able_to_guess.text = self.ids.able_to_guess.defaultText            # these .text changes WILL TRIGGER the functions attached to the spinners
        self.ids.killer_spinner.text = self.ids.killer_spinner.defaultText
        self.ids.weapon_spinner.text = self.ids.weapon_spinner.defaultText
        self.ids.room_spinner.text = self.ids.room_spinner.defaultText
        self.ids.player1_response_spinner.text = self.ids.player1_response_spinner.defaultText
        self.ids.player2_response_spinner.text = self.ids.player2_response_spinner.defaultText
        self.ids.player3_response_spinner.text = self.ids.player3_response_spinner.defaultText
        self.ids.player4_response_spinner.text = self.ids.player4_response_spinner.defaultText
        self.ids.player5_response_spinner.text = self.ids.player5_response_spinner.defaultText                                
        self.ids.card_known_checkbox_NO.active = True

        return super().on_enter(*args)



    def cardKnown(self, instance):
        if instance.active == True:
            self.ids.card_known_spinner.disabled = False
        else: 
            self.ids.card_known_spinner.disabled = True            


    def reset_sectionAbleToGuess(self):
        for key, val in self.ids.items():
            if val.section == 'ableToGuess':
                val.disabled = False
                val.color = 1, 1, 1, 1
                val.text = val.defaultText            
    def reset_sectionA(self):
        for key, val in self.ids.items():
            if val.section == 'A':
                val.disabled = False
                val.color = 1, 1, 1, 1
                val.text = val.defaultText
    def reset_sectionB(self):
        for key, val in self.ids.items():
            if val.section == 'B':
                val.disabled = True
                val.color = 1, 1, 1, 1
                val.text = val.defaultText
    def reset_sectionC(self):
        for key, val in self.ids.items():
            if val.section == 'C':
                val.disabled = True
                val.color = 1, 1, 1, 1
                val.text = val.defaultText
                if val.type == 'checkboxNO':
                    val.active = True
    def reset_sectionCompleteTurnButton(self):
        for key, val in self.ids.items():
            if val.section == "completeTurnButton":
                val.disabled = True
    def disable_sectionA(self):
        for key, val in self.ids.items():
            if val.section == 'A':
                val.disabled = True
    def disable_sectionB(self):
        for key, val in self.ids.items():
            if val.section == 'B':
                val.disabled = True
    def enable_sectionB(self):
        for key, val in self.ids.items():
            if val.section == 'B':
                val.disabled = False
    def disable_sectionC(self):
        for key, val in self.ids.items():
            if val.section == 'C':
                val.disabled = True
    def enable_sectionC(self):
        for key, val in self.ids.items():
            if val.section == 'C':
                val.disabled = False                
    def disable_completeTurnButton(self):
        self.ids.complete_turn_button.disabled = True
    def enable_completeTurnButton(self):
        self.ids.complete_turn_button.disabled = False                     
    def greenText_sectionA(self):
        for key, val in self.ids.items():
            if val.section == 'A':
                val.color = 0, 1, 0.2, 1
    def greenText_sectionB(self):
        for key, val in self.ids.items():
            if val.section == 'B':
                val.color = 0, 1, 0.2, 1                


    suggestedKiller = StringProperty('')
    suggestedKillerCardNum = NumericProperty(-1)
    suggestedWeapon = StringProperty('')
    suggestedWeaponCardNum = NumericProperty(-1)
    suggestedRoom = StringProperty('')
    suggestedRoomCardNum = NumericProperty(-1)
    killerSuggested = BooleanProperty(False)
    weaponSuggested = BooleanProperty(False)
    roomSuggested = BooleanProperty(False)        
    playerResponses = ListProperty(['null', 'null', 'null', 'null', 'null'])
    cardShown = NumericProperty(-1)
    textOfCardShown = StringProperty('')


    def spinnerClicked(self, spinner):
        spinner.text = spinner.text                 # this function can handle all the spinners
        global turnLog
        # Set the killer / weapon / room
        if spinner.type == "killer":
            if 'suggested' in spinner.text:
                self.suggestedKiller = ''
                self.killerSuggested = False
            else:
                self.suggestedKiller = spinner.text
                self.killerSuggested = True
            self.ids.card_known_spinner.values[0] = self.suggestedKiller
            # get the cardNum
            inCardList = False
            for card in cardList:
                if self.suggestedKiller == card.getName():
                    self.suggestedKillerCardNum = card.getPlaceInCardList()
                    inCardList = True
            if inCardList == False:
                self.suggestedKillerCardNum = -1
            turnLog[currentTurnNumber]['killerGuessed'] = self.suggestedKillerCardNum
        if spinner.type == "weapon":
            if 'suggested' in spinner.text:
                self.suggestedWeapon = ''
                self.weaponSuggested = False
            else:
                self.suggestedWeapon = spinner.text
                self.weaponSuggested = True
            self.ids.card_known_spinner.values[1] = self.suggestedWeapon
            inCardList = False
            for card in cardList:
                if self.suggestedWeapon == card.getName():
                    self.suggestedWeaponCardNum = card.getPlaceInCardList()  
                    inCardList = True
            if inCardList == False:
                self.suggestedWeaponCardNum = -1    
            turnLog[currentTurnNumber]['weaponGuessed'] = self.suggestedWeaponCardNum     
        if spinner.type == "room":
            if 'suggested' in spinner.text:
                self.suggestedRoom = ''
                self.roomSuggested = False
            else:
                self.suggestedRoom = spinner.text
                self.roomSuggested = True
            self.ids.card_known_spinner.values[2] = self.suggestedRoom            
            inCardList = False
            for card in cardList:
                if self.suggestedRoom == card.getName():
                    self.suggestedRoomCardNum = card.getPlaceInCardList()            
                    inCardList = True
            if inCardList == False:
                self.suggestedRoomCardNum = -1
            turnLog[currentTurnNumber]['roomGuessed'] = self.suggestedRoomCardNum


        # record players who declined to show a card
        if spinner.type == 'playerResponseSpinner':
            playerName = str(spinner.playerName)
            tempString = str(playerName).lower() + "Response"
            response = ''
            if spinner.text == 'declined':
                self.playerResponses[spinner.player - 1] = 'declined'           # might not need this
                response = 'd'
            elif spinner.text == 'null':
                self.playerResponses[spinner.player - 1] = 'null'
                response = 'n'
            elif spinner.text == 'showed card':
                self.playerResponses[spinner.player - 1] = 'showed card'
                response = 'r'  # 'r' means responded, as in, they showed a card
            turnLog[currentTurnNumber][tempString] = response


        if spinner.type == 'cardKnownSpinner':
            if spinner.text != '':
                self.textOfCardShown = spinner.text
                # now find the cardNum of that card
                for card in cardList:
                    if self.textOfCardShown == card.getName():
                        self.cardShown = card.getPlaceInCardList()
                        turnLog[currentTurnNumber]['card'] = card.getPlaceInCardList()
            elif spinner.text == '':
                turnLog[currentTurnNumber]['card'] = -1


        print("***")
        print("killer/weapon/room: " + str(self.suggestedKillerCardNum) + "/" + str(self.suggestedWeaponCardNum) + "/" + str(self.suggestedRoomCardNum))
        print("killer/weapon/room: " + str(self.suggestedKiller) + " / " + str(self.suggestedWeapon) + " / " + str(self.suggestedRoom))            
        print("playerResponses: " + str(self.playerResponses))
        print("shown card: " + str(turnLog[currentTurnNumber]['card']))
        print("turnLog: " + str(turnLog[currentTurnNumber]))
        print("*** end")
        print("")

    def checkboxNOclicked(self, checkbox):
        self.ids.card_known_spinner.text = ""
        self.ids.card_known_spinner.disabled = True
        self.cardShown = -1
        self.textOfCardShown = ''
    def checkboxYESclicked(self, checkbox):
        self.ids.card_known_spinner.disabled = False

    @staticmethod
    def printTurnsPretty(turnNumber, turnDataDictionary):
        print("")
        print("TURN SUMMARY:")
        print("                      -------GUESSED------       ------------------RESPONSES-----------------             ")
        print("turnNum  Guesser      killer   wep    room       scar    green   orchid  must    plum    peac    cardShown")

        for x in range(turnNumber):
            turnNum = x + 1
            print(str(turnNum).ljust(2, " ") + "".center(7, " ") + str(turnDataDictionary[turnNum]['guesser']).ljust(13, " "), end="")
            print(str(turnDataDictionary[turnNum]['killerGuessed']).ljust(9, " "), end="")
            print(str(turnDataDictionary[turnNum]['weaponGuessed']).ljust(7, " ") + str(turnDataDictionary[turnNum]['roomGuessed']).ljust(11, " "), end="")
            print(str(turnDataDictionary[turnNum]['scarlettResponse']).ljust(8, " ") + str(turnDataDictionary[turnNum]['greenResponse']).ljust(8, " "), end="")
            print(str(turnDataDictionary[turnNum]['orchidResponse']).ljust(8, " ") + str(turnDataDictionary[turnNum]['mustardResponse']).ljust(8, " "), end="")
            print(str(turnDataDictionary[turnNum]['plumResponse']).ljust(8, " ") + str(turnDataDictionary[turnNum]['peacockResponse']).ljust(8, " "), end="")
            print(str(turnDataDictionary[turnNum]['card']).ljust(8, " "))
        print("")

    def completeTurn(self, button):
        # print out the turns to the terminal
        self.printTurnsPretty(currentTurnNumber, turnLog)

        # copy the current contents of the turnInfo file, and then replace the turnLog line with the newest turnLog
        with open(fileName, 'r') as fileObject:
            currentContents = fileObject.readlines()
        
        currentContents[5] = str(turnLog) + "\n"         # replace turnDataDictionary with the newest version
        currentContents[6] = str(currentTurnNumber)                        # records the most recent completed turn (for the purpose of loading an old game)

        with open(fileName, 'w') as fileObject:
            fileObject.writelines(currentContents)

    @staticmethod
    def analyzeData(turnNumber, turnData, analyTable, user, killerWeaponRoom, announces):

        # if turnNumber == 1:
        #       turning this off so we can paste in old games and start at turnNumber > 1
        print("ffs user is: " + str(user.getNameOnly()))
        card1 = user.getCardFromCardList(0)
        card2 = user.getCardFromCardList(1)
        card3 = user.getCardFromCardList(2)

        column = user.getColumnNumber()     # identify the user's player's column number
        #   the row number is simply the card's id #
        row1 = card1.getPlaceInCardList()
        row2 = card2.getPlaceInCardList()
        row3 = card3.getPlaceInCardList()

        #   now, we change the analysis table to reflect the fact that these cards' owner is known
        analyTable[row1][column] = ["Y"]
        analyTable[row2][column] = ["Y"]
        analyTable[row3][column] = ["Y"]


        def howManyYsInColumn(columnNum):
            numberOfYs = 0
            for row in range(21):
                if "Y" in analyTable[row][columnNum]:
                    numberOfYs += 1
            return numberOfYs

        def processYsHorizontal():      # if a row contains a 'Y', then mark all other cells in that row with '-' because it's impossible that another player also has that cardu
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1
            for row in range(21):
                for column in range(6):
                    if "Y" in analyTable[row][column]:
                        for x in range(6):
                            if x != column:
                                analyTable[row][x] = ["-"]
                                ################## CALL FUNCTION(S) HERE 
                                functionsToCallIfNegativeAdded()
                                # allFunctions()


    #   if a player has three Ys in their column, then we know they do NOT have any other cards
    #   if a player has two Ys in their column and one ?, then we know that "?" is actually a "Y"
    #   if a player has two Ys in their column and 1 to 3 other cells with a turnNumber, then we know that all '?'-only cells in the column should be changed to '-'
    #   if a player has one Y  in their column and two distinct "groups" of turnNumbers, then we know that all '?'-only cells in the column should be changed to '-'
        def processYsVertical():        
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1
            #   look down each column and count up how many Ys we see
            for column in range(6):
                numberOfYs = 0
                locationOfYs = []
                numberOfQuestionMarks = 0            
                locationOfQuestionMarks = []
                doAtLeastTwoCellsShareATurnNumber = False
                # tally up the Ys and ?s
                for row in range(21):
                    # tally up the Ys
                    if "Y" in analyTable[row][column]:
                        numberOfYs += 1
                        locationOfYs.append(row)
                    if numberOfYs > 3:
                        print("THERE ARE TOO MANY Ys IN COLUMN " + str(column))
                    # tally up the ?s
                    if "?" in analyTable[row][column]:
                        numberOfQuestionMarks += 1
                        locationOfQuestionMarks.append(row)

                if numberOfYs == 3:     #   if a player has three Ys in their column, then we know they do NOT have any other cards
                    for y in range(21):
                        if y not in locationOfYs and "-" not in analyTable[y][column]:
                            analyTable[y][column] = ["-"]
                            print("THREE Ys WERE FOUND IN COLUMN " + str(column) + ", SO THE CELL AT ROW " + str(y) + " WAS MARKED WITH '-'")
                            ############## CALL FUNCTION(S) HERE
                            functionsToCallIfNegativeAdded()
                            # allFunctions()
                if numberOfYs == 2 and numberOfQuestionMarks == 1:      #   if a player has two Ys in their column and one ?, then we know that the "?" should be changed to "Y"
                    analyTable[locationOfQuestionMarks[0]][column] = ["Y"]  
                    print("COLUMN " + str(column) + " WAS FOUND TO HAVE TWO Ys AND ONE ?, SO WE TURNED THE ? AT ROW " + str(locationOfQuestionMarks[0]) + " INTO A Y.")
                    #### CALL FUNCTION(S) HERE
                    functionsToCallIfYAdded()
                    functionsToCallIfQuestionMarkRemoved()
                    functionsToCallIfTurnNumberRemoved()
                    # allFunctions()

                # if a player has two Ys in their column and 1 to 3 other cells with a turnNumber, then we know that all '?'-only cells in the column should be changed to '-'                
                # check whether there are at least 2 cells that share a turnNumber
                for x in range(turnNumber):
                    for row in range(21):               # this chunk of code was backed up by one shift-tab
                        if (x+1) in analyTable[row][column]:
                            for rrow in range(21):
                                if (x+1) in analyTable[rrow][column] and row != rrow:        
                                    doAtLeastTwoCellsShareATurnNumber = True
                if numberOfYs == 2 and doAtLeastTwoCellsShareATurnNumber:
                    for row in range(21):
                        if analyTable[row][column] == ["?"]:
                            analyTable[row][column] = ["-"]
                            print("(vertical function) COLUMN " + str(column) + " HAD TWO Ys AND AT LEAST ONE OTHER SET OF turnNUMBERS, SO AT ROW " + str(row) + " WE REPLACED THE LONE ? WITH '-'")
                            ########### CALL FUNCTION HERE    
                            functionsToCallIfQuestionMarkRemoved()
                            functionsToCallIfTurnNumberRemoved()
                            functionsToCallIfNegativeAdded()                    
                            # allFunctions()

                #   if a player has one Y  in their column and two distinct "groups" of turnNumbers, then we know that all '?'-only cells in the column should be changed to '-'
                if numberOfYs == 1:       # don't bother will all this crap if numberOfYs isn't 1
    #######################################################################################################################################################
    #######################################################################################################################################################
    ##########################       START      #############################################################################################################################
    #######################################################################################################################################################
    #######################################################################################################################################################
                    groupXCells = [ [] for i in range(10)]          # for example, groupXCells[1] = []          is a list of the cells in group 1
                    groupXTurnNumbers = [ [] for i in range(10)]	# for example, groupXTurnNumbers[1] = []    is a list of the turnNumbers in group 1
                    # we're assuming that there will never be more than 10 groups... doesn't feel like a dangerous assumption in a six player game.....

                    # save all non-Y, non-'-', non-?-only cells to a list
                    listOfCellsInColumnWithTurnNumbers = []
                    for row in range(21):
                        if 'Y' not in analyTable[row][column] and '-' not in analyTable[row][column] and analyTable[row][column] != ['?']:
                            listOfCellsInColumnWithTurnNumbers.append(row)         

                    # if column == 1:
                    #     print("listOfCells: " + str(listOfCellsInColumnWithTurnNumbers))
                    #     for element in listOfCellsInColumnWithTurnNumbers:
                    #         print(analyTable[element][column])
                    #         print("done")

                    def putCellsIntoGroupsCorrectlyForGodsSake(listOfCells, groupNum):
                        # pick one of the biggest cells to start with
                        biggestCellSize = -1
                        for cell in listOfCells:            # 'cell' is a row number
                            if len(analyTable[cell][column]) > biggestCellSize:
                                biggestCellSize = len(analyTable[cell][column])
                        indexOfOneOfBiggestCells = -1
                        for cell in listOfCells:
                            if len(analyTable[cell][column]) == biggestCellSize:
                                indexOfOneOfBiggestCells = cell
                                # break                   # as of right now this line makes or break it... and that should not be the case#################################################

                        # identify the turnNumbers contained in that "biggest" cell and consider them the founding members of our first "group"
                        turnNumbersInBiggestGroup = []
                        for element in analyTable[indexOfOneOfBiggestCells][column]:
                            if element != '?' and element != '-' and element not in turnNumbersInBiggestGroup:
                                turnNumbersInBiggestGroup.append(element)
                                # now that we've added a turnNumber into the group, let's hunt down every single row that might also have that turnNumber
                                for y in range(len(listOfCells)):     # not sure how many times, at minimum, the following loop needs to repeat..... but i know that stuff gets missed if only once
                                    for cell in listOfCells:    # if anything in this cell is already in turnNumbersInBiggestGroup, then add EVERYTHING in that cell to turnNumbersInBiggestGroup
                                        isAnythingAlreadyInGroup = False
                                        for thingInCell in analyTable[cell][column]:
                                            if thingInCell in turnNumbersInBiggestGroup:
                                                isAnythingAlreadyInGroup = True
                                        if isAnythingAlreadyInGroup:        # add the entire contents of the cell to the group
                                            for thingInCell in analyTable[cell][column]:
                                                if thingInCell not in turnNumbersInBiggestGroup and thingInCell != '?':
                                                    turnNumbersInBiggestGroup.append(thingInCell)       

                        # identify any cells that DO NOT SHARE any turnNumbers with our "biggest" cell, so we can try to put these in ANOTHER group
                        cellsThatDidntFitInThisGroup = []     # again, remember that "cell" = row number in the analyTable
                        for cell in listOfCells:
                            cellDoesShareTurnNumbersWithBiggestCell = False
                            for turnNum in turnNumbersInBiggestGroup:
                                if turnNum in analyTable[cell][column] and turnNum != '?':
                                    cellDoesShareTurnNumbersWithBiggestCell = True
                            if cellDoesShareTurnNumbersWithBiggestCell == False:
                                cellsThatDidntFitInThisGroup.append(cell)
                        cellsThatDoFITINTHEGROUP = []                # we'll make a parallel list, so we can process these cells first
                        for cell in listOfCells:
                            if cell not in cellsThatDidntFitInThisGroup:
                                cellsThatDoFITINTHEGROUP.append(cell)            #boom, this is group1... don't need to use that other function

                        groupXCells[groupNum] = cellsThatDoFITINTHEGROUP
                        groupXTurnNumbers[groupNum] = turnNumbersInBiggestGroup
                        
                        # now that that is done, we start again, this time defining our "biggest" cell again from the cellsThatDoNotShareTurnNumbers
                        if len(cellsThatDidntFitInThisGroup) > 0:
                            putCellsIntoGroupsCorrectlyForGodsSake(cellsThatDidntFitInThisGroup, groupNum + 1)


                    putCellsIntoGroupsCorrectlyForGodsSake(listOfCellsInColumnWithTurnNumbers, 0) 

                    # if len(groupXCells[0]) > 0:
                    #     print("groupXCells:       " + str(groupXCells))
                    #     print("groupXTurnNumbers: " + str(groupXTurnNumbers))

                    numberOfGroups = 0
                    for x in range(len(groupXCells)):
                        if len(groupXCells[x]) > 0:
                            numberOfGroups += 1

                    # all of this was so we can execute the following:
                    if numberOfYs == 1 and numberOfGroups > 1:      # yes, we already know that numberOfYs is 1, because we indented above... but we repeat here for the coder's benefit
                        # if there is one Y and at least 2 distinct groups of turnNumbers, then we know that all cells in that column that only have '?' can be changed to '-'
                        # so, go thru this __column and change the ? to -
                        for row in range(21):
                            if analyTable[row][column] == ['?']:
                                analyTable[row][column] = ['-']
                                print("OMG IT ACTUALLY WORKED?? in column " + str(column) + " we found one Y and two or more groups of turnNumbers, so we changed row " + str(row) + "'s '?' to '-'")
                                ############# CALL FUNCTION HERE
                                functionsToCallIfQuestionMarkRemoved()
                                functionsToCallIfNegativeAdded()
                                functionsToCallIfTurnNumberRemoved()
                                # allFunctions()
                    # look at .txt file titled 'clueSolver - one Y and groups.txt' for a breakdown (or muddy history?) of how we got this to work


        def checkForAllNegativesInRow(namesOfKillerWeaponRoom, announcements):
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1
            #   if a row has all "-", we know that that card is in the envelope, so announce that fact by printing it at top of analysis table printout
            for row in range(21):       # look at row 0 of the analysis table. If there is a "-" in every column then we're golden
                numberOfNegatives = 0
                for column in range(6):                
                    if "-" in analyTable[row][column]:
                        numberOfNegatives += 1
                if numberOfNegatives == 6:
                    if row < 6:
                        namesOfKillerWeaponRoom[0] = cardList[row].getName()
                        if announcements[0] == False:
                            print("KILLER DISCOVERED, BECAUSE SIX '-' WERE FOUND IN ROW " + str(row) + ".")
                            announcements[0] = True
                    if row > 5 and row < 12:
                        namesOfKillerWeaponRoom[1] = cardList[row].getName()
                        if announcements[1] == False:
                            print("WEAPON DISCOVERED, BECAUSE SIX '-' WERE FOUND IN ROW " + str(row) + ".")
                            announcements[1] = True
                    if row > 11:
                        namesOfKillerWeaponRoom[2] = cardList[row].getName()
                        if announcements[2] == False:
                            print("ROOM DISCOVERED, BECAUSE SIX '-' WERE FOUND IN ROW " + str(row) + ".")
                            announcements[2] = True


        def checkForLastRemainingQuestionMarksInCategory():             
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1        
            # this function checks whether the last few (or single) ? in a section can be changed into a Y or Ys, or possibly a '-'
            # basically, if Y + ? = 5, and the killer is known, then the ? can safely be turned into Y
            #####################################################################################
            # scan the killers & tally up
            tallyKillerSection = [0, 0]       # tallyKillerSection[0] = number of Y     ...         tallyKillerSection[1] = number of ?
            for row in range(6):
                for column in range(6):
                    if "Y" in analyTable[row][column]:
                        tallyKillerSection[0] += 1
                    if "?" in analyTable[row][column]:
                        tallyKillerSection[1] += 1
            if tallyKillerSection[0] < 5 and tallyKillerSection[0] + tallyKillerSection[1] == 5:
                for row in range(6):
                    for column in range(6):
                        if "?" in analyTable[row][column]:
                            whatWasRemoved = []
                            whatWasRemoved = analyTable[row][column]
                            analyTable[row][column] = ["Y"]
                            print("IN THE KILLER SECTION THERE WERE " + str(tallyKillerSection[0]) + " Ys AND " + str(tallyKillerSection[1]) + " ?s, SO WE TURNED THE ? AT ROW " + str(row) + ", COLUMN " + str(column) + " INTO Y.")
                            for rrow in range(21):
                                for element in whatWasRemoved:
                                    if element in analyTable[rrow][column] and element != "?" and element != "Y" and element != "-":   # include "Y" bc we don't want to undo what we just did
                                        analyTable[rrow][column].remove(element)
                            ############ CALL FUNCTION HERE
                            functionsToCallIfYAdded()
                            functionsToCallIfQuestionMarkRemoved()
                            # allFunctions()

            elif tallyKillerSection[0] == 5:    # if there are n-1 Ys in the section, then the last row, no matter what, is the card in the envelope
                for row in range(6):
                    for column in range(6):
                        if "?" in analyTable[row][column]:
                            analyTable[row][column] = ["-"]
                            print("FIVE Ys WERE FOUND IN THE KILLER SECTION, MEANING THAT THE REMAINING ROW MUST REPRESENT THE CARD IN THE ENVELOPE")
                            ########### CALL FUNCTION HERE
                            functionsToCallIfNegativeAdded()
                            # allFunctions()
            
            #####################################################################################
            tallyWeaponSection = [0, 0]       
            for row in range(6, 12):
                for column in range(6):
                    if "Y" in analyTable[row][column]:
                        tallyWeaponSection[0] += 1
                    if "?" in analyTable[row][column]:
                        tallyWeaponSection[1] += 1
            if tallyWeaponSection[0] < 5 and tallyWeaponSection[0] + tallyWeaponSection[1] == 5:
                for row in range(6, 12):
                    for column in range(6):
                        if "?" in analyTable[row][column]:
                            whatWasRemoved = []
                            whatWasRemoved = analyTable[row][column]
                            analyTable[row][column] = ["Y"]
                            print("IN THE WEAPON SECTION THERE WERE " + str(tallyWeaponSection[0]) + " Ys AND " + str(tallyWeaponSection[1]) + " ?s, SO WE TURNED THE ? AT ROW " + str(row) + ", COLUMN " + str(column) + " INTO Y.")
                            for rrow in range(21):
                                for element in whatWasRemoved:
                                    if element in analyTable[rrow][column] and element != "?" and element != "Y" and element != "-":
                                        analyTable[rrow][column].remove(element)
                            ######## CALL FUNCTION HERE
                            functionsToCallIfYAdded()
                            functionsToCallIfQuestionMarkRemoved()
                            # allFunctions()
            elif tallyWeaponSection[0] == 5:    # if there are n-1 Ys in the section, then the last row, no matter what, is the card in the envelope
                for row in range(6, 12):
                    for column in range(6):
                        if "?" in analyTable[row][column]:
                            analyTable[row][column] = ["-"]
                            print("FIVE Ys WERE FOUND IN THE WEAPON SECTION, MEANING THAT THE REMAINING ROW MUST REPRESENT THE CARD IN THE ENVELOPE")
                            ######## CALL FUNCTION HERE
                            functionsToCallIfNegativeAdded()
                            # allFunctions()
            #####################################################################################
            tallyRoomSection = [0, 0]       
            for row in range(12, 21):
                for column in range(6):
                    if "Y" in analyTable[row][column]:
                        tallyRoomSection[0] += 1
                    if "?" in analyTable[row][column]:
                        tallyRoomSection[1] += 1
            if tallyRoomSection[0] < 5 and tallyRoomSection[0] + tallyRoomSection[1] == 5:
                for row in range(12, 21):
                    for column in range(6):
                        if "?" in analyTable[row][column]:
                            whatWasRemoved = []
                            whatWasRemoved = analyTable[row][column]
                            analyTable[row][column] = ["Y"]
                            print("IN THE ROOM SECTION THERE WERE " + str(tallyRoomSection[0]) + " Ys AND " + str(tallyRoomSection[1]) + " ?s, SO WE TURNED THE ? AT ROW " + str(row) + ", COLUMN " + str(column) + " INTO Y.")
                            for rrow in range(21):
                                for element in whatWasRemoved:
                                    if element in analyTable[rrow][column] and element != "?" and element != "Y" and element != "-":
                                        analyTable[rrow][column].remove(element)
                            ########### CALL FUNCTION HERE
                            functionsToCallIfYAdded()
                            functionsToCallIfQuestionMarkRemoved()
                            # allFunctions()
            elif tallyRoomSection[0] == 8:    # if there are n-1 Ys in the section, then the last row, no matter what, is the card in the envelope
                for row in range(12, 21):
                    for column in range(6):
                        if "?" in analyTable[row][column]:
                            analyTable[row][column] = ["-"]
                            print("EIGHT Ys WERE FOUND IN THE ROOM SECTION, MEANING THAT THE REMAINING ROW MUST REPRESENT THE CARD IN THE ENVELOPE")    
                            ######### CALL FUNCTION HERE
                            functionsToCallIfNegativeAdded()
                            # allFunctions()

        def checkForSingleTurnNumbersInColumn():    #   if a turnNumber appears only once in a column, we know that that player has that card
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1        
            for column in range(6):   #   loop thru each column, one at a time:
                # initialize a tally list for that column, to keep track of how many times we see each turn number appear
                #   the tally list answers the question, "How many times does turn 1 appear in the entire analysis table column? 0, 1, 2 or 3 times?"
                tally = {}
                for turn in range(turnNumber):
                    tally[turn + 1] = 0         # initialize the tallies at zero
                # if we look at a cell, and see for example [?, 4, 5], then we do: tally[4] += 1, and tally[5] += 1
                for row in range(21):
                    for turnMinusOne in range(turnNumber):
                        if turnMinusOne+1 in analyTable[row][column]:
                            tally[turnMinusOne+1] += 1
                # now we've got our tally list... and we check to see if any turn# appears ONLY ONCE in the tally dictionary
                for turn in range(turnNumber):
                    if tally[turn + 1] == 1:
                        print("WE IDENTIFIED A LONE TURN " + str(turn + 1) + " IN COLUMN " + str(column))
                        # because we know that the turn number exists only once, we know that the player has that card... so we need to change that turn number into a "Y"
                        # but we don't know the exact location within the analysisTable ... all we know is that for example there is "one 6 in Orchid's column"
                        #   so because we know the column, we can cycle thru the rows and replace (turn + 1) with "Y"
                        for row in range(21):
                            if (turn + 1) in analyTable[row][column]:
                                # WE NEED TO ACT IMMEDIATELY to prevent a logic error!!!!!!! Keep track of whatWasThere and remove those turn numbers from the rest of the column
                                # for example if a cell has [17, 18, 19] and the 19 is the only 19 in the column, then when we change the cell to ["Y"] it will look like the 
                                # 17 and 18 that are in other cells in that column are indicative of a card being held... and that should not happen
                                whatWasThere = []
                                whatWasThere = analyTable[row][column]
                                analyTable[row][column] = ["Y"]
                                print("...AND REPLACED IT WITH A 'Y' AT ROW " + str(row))
                                # IMMEDIATELY we need to go up & down that column and remove the turn numbers that USED TO BE in the cell where we're putting the "Y"
                                if "Y" not in whatWasThere and "-" not in whatWasThere:
                                    for row in range(21):
                                        for element in whatWasThere:
                                            if element in analyTable[row][column] and element != "?":
                                                analyTable[row][column].remove(element)
                                ######### CALL FUNCTION(S) HERE
                                functionsToCallIfYAdded()
                                functionsToCallIfTurnNumberRemoved()
                                # allFunctions()



        def processDecline():       # mark a "-" for each player who declines, for those three cards
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1        
            #   identify all players who declined ... i.e., scarlettResponse == 'd', mustardResponse == 'd', etc, and mark all three card in that guess as "-" for that respondent

            listOfIterations = []
            if initialAnalysisCompletedOfLoadedSavedGame[0] == False:           # when loading a saved game we want to process each turn in the turnData dictionary
                listOfIterations = [x for x in range(turnNumber)]
                initialAnalysisCompletedOfLoadedSavedGame[0] = True
            elif initialAnalysisCompletedOfLoadedSavedGame[0] == True:
                listOfIterations = [turnNumber-1]

            for turnMinusOne in listOfIterations:

                killerRowNum = turnData[turnMinusOne+1]['killerGuessed']
                weaponRowNum = turnData[turnMinusOne+1]['weaponGuessed']
                roomRowNum = turnData[turnMinusOne+1]['roomGuessed']

                for player in playerList:
                    nameString = player.getNameOnly().lower() + "Response"
                    if turnData[turnMinusOne+1][nameString] == 'd':
                        analyTable[killerRowNum][player.getColumnNumber()] = ["-"]
                        analyTable[weaponRowNum][player.getColumnNumber()] = ["-"]
                        analyTable[roomRowNum][player.getColumnNumber()] = ["-"]  
                    ####### CALL FUNCTION(S) HERE
                    functionsToCallIfNegativeAdded()
                    # allFunctions()


            
        #       respond by showing a card (r)
        #           if we don't know what card was shown, then we replace the "?" with the turn number, indicating that on that turn one of those 3 cards is held by the player
        #           if the card is known, then the ONLY THING we put into the analyTable is the "Y" for the owner of the card, and we remove everything else
        #           every time a new Y appears in the table, we need to run horizontal & vertical processing
        def processRespond():
            global numberOfFunctionCalls
            numberOfFunctionCalls += 1

            listOfIterations = []         
            if initialAnalysisCompletedOfLoadedSavedGame[1] == False:           # when loading a saved game we want to process each turn in the turnData dictionary
                listOfIterations = [x for x in range(turnNumber)]
                initialAnalysisCompletedOfLoadedSavedGame[1] = True
            elif initialAnalysisCompletedOfLoadedSavedGame[1] == True:
                listOfIterations = [turnNumber-1]

            for turnMinusOne in listOfIterations:
                killerRowNum = turnData[turnMinusOne+1]['killerGuessed']
                weaponRowNum = turnData[turnMinusOne+1]['weaponGuessed']
                roomRowNum = turnData[turnMinusOne+1]['roomGuessed']

                isTheShownCardKnown = False
                if turnData[turnMinusOne+1]['card'] != -1:
                    isTheShownCardKnown = True

                #   going to append the turnNumber into the cell's list
                for player in playerList:
                    nameString = player.getNameOnly().lower() + "Response"
                    if turnData[turnMinusOne+1][nameString] == 'r':
                        if isTheShownCardKnown:     #   if the card is known then don't enter turnNumbers... only enter "Y"
                            cardNumber = turnData[turnMinusOne+1]['card']
                            whatWasRemoved = []
                            whatWasRemoved = analyTable[cardNumber][player.getColumnNumber()]
                            analyTable[cardNumber][player.getColumnNumber()] = ["Y"]
                            for row in range(21):
                                for element in whatWasRemoved:
                                    if element in analyTable[row][player.getColumnNumber()] and element in [x+1 for x in range(turnNumber)]: # i.e. we don't want to remove "Y" or "?"
                                        analyTable[row][player.getColumnNumber()].remove(element)
                            ######### CALL FUNCTION(S) HERE
                            functionsToCallIfYAdded()
                            functionsToCallIfQuestionMarkRemoved()
                            functionsToCallIfTurnNumberRemoved()
                            functionsToCallIfNegativeRemoved()
                            # allFunctions()


                        #   if there is a "Y" in any of the three cards that were just guessed, then don't bother recording the turnNumbers bc for all we know they showed that "Y" card
                        elif "Y" in analyTable[killerRowNum][player.getColumnNumber()] or "Y" in analyTable[weaponRowNum][player.getColumnNumber()] or "Y" in analyTable[roomRowNum][player.getColumnNumber()]:
                            continue
                        else:    #  if there's no '-' already, and we don't already know that player's 3 cards, then add the turn number
                            if "-" not in analyTable[killerRowNum][player.getColumnNumber()] and howManyYsInColumn(player.getColumnNumber()) < 3:
                                if (turnMinusOne + 1) not in analyTable[killerRowNum][player.getColumnNumber()]:  # don't add more than one instance of that turnNumber
                                    analyTable[killerRowNum][player.getColumnNumber()].append(turnMinusOne + 1)
                            if "-" not in analyTable[weaponRowNum][player.getColumnNumber()] and howManyYsInColumn(player.getColumnNumber()) < 3:
                                if (turnMinusOne + 1) not in analyTable[weaponRowNum][player.getColumnNumber()]:
                                    analyTable[weaponRowNum][player.getColumnNumber()].append(turnMinusOne + 1)
                            if "-" not in analyTable[roomRowNum][player.getColumnNumber()] and howManyYsInColumn(player.getColumnNumber()) < 3:
                                if (turnMinusOne + 1) not in analyTable[roomRowNum][player.getColumnNumber()]:
                                    analyTable[roomRowNum][player.getColumnNumber()].append(turnMinusOne + 1)
                            ##### CALL FUNCTION(S) HERE
                            functionsToCallIfTurnNumberAdded()
                            # allFunctions()

        # Dealing with changes to -
        def functionsToCallIfNegativeAdded():
            checkForAllNegativesInRow(killerWeaponRoom, announces)
        def functionsToCallIfNegativeRemoved():
            pass   
        
        # Dealing with changes to Y
        def functionsToCallIfYAdded():
            processYsHorizontal()
            processYsVertical()
            checkForLastRemainingQuestionMarksInCategory()
        def functionsToCallIfYRemoved():
            pass
    
        # Dealing with changes to turnNumbers
        def functionsToCallIfTurnNumberAdded():
            processYsVertical()
            checkForSingleTurnNumbersInColumn()
        def functionsToCallIfTurnNumberRemoved():
            checkForSingleTurnNumbersInColumn()
    
        # Dealing with changes to ?
        def functionsToCallIfQuestionMarkAdded():
            checkForLastRemainingQuestionMarksInCategory()
        def functionsToCallIfQuestionMarkRemoved():
            processYsVertical()
            checkForLastRemainingQuestionMarksInCategory()



        for repetitionNumber in range(1):      # this is a lazy way to make sure we process everything.... hopefully change this later
            processYsHorizontal()       # these two (horiz/vert) are run first thing in order to incorporate the user's 3 known cards
            processYsVertical()         # these two (horiz/vert) are run first thing in order to incorporate the user's 3 known cards
            processDecline()
            processRespond()            # there will always be 1 response, and possibly some declines, so always run these

        #add "cleanup" functionality here, in case the previous processes have revealed some important info ... because we want to show this info to the user before the next turn starts

    def analyzeTheData(self):
        self.analyzeData(currentTurnNumber, turnLog, analysisTable, userCharacter, actualKillerWeaponRoom, announcementsHaveBeenMadeForKillerWeaponRoom)

class AnalysisTableScreen(Screen):

    @staticmethod
    def convertTurnToPlayerTurn(turnNum):
        return ((turnNum - 1) % 6) + 1

    def on_enter(self, *args):
        # self.ids.turn_just_finished.text = 'turn ' + str(currentTurnNumber) + ' just finished'
        # self.ids.next_turn_button.text = 'click to start turn ' + str(currentTurnNumber + 1)

        # update all the labels to be current with the analysis table
        

        respondentList = ['', '', '', '', '', '']
        respondentList[0] = str(userCharacter.getNameOnly()) 
        # now identify who 'player1 response' is, who 'player2 response' is, etc
        userTurnNumber = userCharacter.getTurnOrder()
        incrementalVariable = 1
        while incrementalVariable < 6:
            respondentTurnOrder = self.convertTurnToPlayerTurn(userTurnNumber + incrementalVariable)
            for player in playerList:
                if player.getTurnOrder() == respondentTurnOrder:
                    respondentList[incrementalVariable] = str(player.getNameOnly())
            incrementalVariable += 1
        # now put those players' names onto the screen
        self.ids.player_name.text = str(respondentList[0])
        self.ids.respondent1_name.text = str(respondentList[1])
        self.ids.respondent2_name.text = str(respondentList[2])
        self.ids.respondent3_name.text = str(respondentList[3])
        self.ids.respondent4_name.text = str(respondentList[4])
        self.ids.respondent5_name.text = str(respondentList[5])

        for row in range(21):
            for column in range(6):
                # print("row: " + str(row) + " colum: " + str(column))
                for key, val in self.ids.items():
                    # print("asdfasdfasdfasfd " + str(val.text))

                    # print("val.row: " + str(val.row) + "     val.column: " + str(val.column))

                    if val.position[0] == row and val.position[1] == column:            # position[0] is the row number, position[1] is the column number
                        print("********* the row: " + str(val.position[0]) + "   the column: " + str(val.position[1]) + "rowrow: " + str(row) + " colcol: " + str(column))
                        val.text = str(analysisTable[row][column])
                        # val.text = "TTTTT"


        return super().on_enter(*args)


    @staticmethod
    def incrementTurnNumber(self):
        global currentTurnNumber
        currentTurnNumber += 1

    def startNextTurn(self):
        pass

    # def analyzeData(turnNumber, turnData, analyTable, user, killerWeaponRoom, announces):
    @staticmethod
    def printAnalysisTable(table, actualKillerWeaponRoom):
        print("ANALYSIS TABLE:")
        print("# of function calls: " + str(numberOfFunctionCalls))
        print("                             Killer is: " + str(actualKillerWeaponRoom[0]))
        print("                             Weapon is: " + str(actualKillerWeaponRoom[1]))
        print("                             Room is: " + str(actualKillerWeaponRoom[2]))
        print("----------------------------------------------------------------------------------------------------------------------")    
        print("".ljust(20, " "), end="")
        print("scarlett".center(15, ' '), "green".center(15, ' '), "peacock".center(15, ' '), "plum".center(15, ' '), "mustard".center(15, ' '), "orchid".center(15, ' '), " |")
        for row in range(21):
            # create a blank row to separate each category of cards:
            if row == 6 or row == 12 or row == 17:
                print("                                                                                                                     |")
            print(cardList[row].getNumberAndName().ljust(20, " "), end="")
            for column in range(6):
                # if the output would be "-" then just leave it blank, otherwise print it
                if "-" in table[row][column]:
                    print("-".center(15, ' '), end=" ")
                # elif table[row][column] == ['?']:
                #     print('?'.center(15, ' '), end=" ")
                else:
                    print(str(table[row][column]).center(15, ' '), end=" ")
            print(" |")
        print("----------------------------------------------------------------------------------------------------------------------")    
        print(" ")

    def printTheAnalysisTable(self):
        self.printAnalysisTable(analysisTable, actualKillerWeaponRoom)
        global numberOfFunctionCalls
        numberOfFunctionCalls = 0

class LoadGameScreen(Screen):
    # filename = StringProperty('')
    global fileName                         #### we need to set fileName so we can continue saving to the same file
    filename = ObjectProperty()
    
    def on_enter(self, *args):
        path = os.getcwd()
        self.ids.fileChooser.rootpath = path
        return super().on_enter(*args)

    def selected(self, file):
        self.filename = file
        print("file selected: " + str(self.filename))
        self.ids.next_button.disabled = False

    def confirmLoadGame(self):
        with open(self.filename[0]) as fileObject:
            fileContents = fileObject.readlines()
        playerName = str(fileContents[0]).strip()        # .strip() will remove the /n newline character     # line 0 is the player name
        print("Game loaded.... playerName: " + str(playerName))
        global userCharacter
        for player in playerList:
            if playerName == player.getNameOnly():
                userCharacter = player
        playerCard1 = int(fileContents[1].strip())       #   line 1 2 3 are the player's 3 cards
        playerCard2 = int(fileContents[2].strip())
        playerCard3 = int(fileContents[3].strip())

        # identify the card objects, and then .add them to the player character... they will then be processed in the first part of the analyzeData() function
        userCharacter.resetCardList()
        for card in cardList:
            cardNum = card.getPlaceInCardList()
            if playerCard1 == cardNum:
                userCharacter.addToCardList(card)
            if playerCard2 == cardNum:
                userCharacter.addToCardList(card)
            if playerCard3 == cardNum:
                userCharacter.addToCardList(card)

        # next we set the player order 
        playerOrderList = fileContents[4].strip()       # line 4 is the player order... need to ensure that this is saved as an actual list, because right now it's a string
        newPlayerOrderList = playerOrderList.replace('[', '')       # get rid of the extra characters before we convert it into a list with " " as delimiter
        newPlayerOrderList = newPlayerOrderList.replace(']', '')    # get rid of the extra characters before we convert it into a list with " " as delimiter
        newPlayerOrderList = newPlayerOrderList.replace('\'', '')   # get rid of the extra characters before we convert it into a list with " " as delimiter
        newPlayerOrderList = newPlayerOrderList.replace(',', '')    # get rid of the extra characters before we convert it into a list with " " as delimiter
        playerOrderList = list(newPlayerOrderList.split(" "))       # finally, convert the stripped string into a list
        x = 1
        for element in playerOrderList:
            for player in playerList:
                if player.getNameOnly() == element:
                    player.setTurnOrder(x)
                    player.turnOrderConfirmedSetTrue()
                    x += 1

        global turnLog
        turnLog = ast.literal_eval(fileContents[5].strip())     # line 5 is the turnDataDictionary
        # turnLog = fileContents[5].strip()     # this line doesn't work on a dictionary object

        global currentTurnNumber
        currentTurnNumber = int(fileContents[6].strip())       # line 6 is the last completed turn number
        currentTurnNumber += 1



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


