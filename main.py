import datetime
from dis import dis
from fileinput import filename
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
import datetime
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox


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
    def getCardFromCardList(self, integer):
        return self.cardList[integer]
    
    # def addCard1(self, card):
    #     self.card1 = card
    # def addCard2(self, card):
    #     self.card2 = card
    # def addCard3(self, card):
    #     self.card3 = card
    # def getCard1(self):
    #     return self.card1
    # def getCard2(self):
    #     return self.card2
    # def getCard3(self):
    #     return self.card3

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

        analyzeData(turnNumber, turnLog, analysisTable, userCharacter, actualKillerWeaponRoom, announcementsHaveBeenMadeForKillerWeaponRoom)
        printAnalysisTable(analysisTable, actualKillerWeaponRoom)
        # print(turnLog)
        turnNumber += 1







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


