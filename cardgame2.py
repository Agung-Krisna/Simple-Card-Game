import random as rnd

class Card:
    def __init__(self, typeA, faceA, valueA):
        self.type = typeA
        self.face = faceA
        self.value = valueA
        
    def showCards(self):
        print(self.type, self.face, self.value)
    
    def returnCards(self):
        return "{} {} {}".format(self.type, self.face, self.value)

    def returnIndividual(self):
        return (self.type, self.face, self.value)


class PlayingCards(Card):
    def __init__(self):
        self.cardSets = []
        
    def createPlayingCards(self):
        self.types = ["Heart", "Diamond", "Club", "Spade"]
        face = "Ace 2 3 4 5 6 7 8 9 10 Jack Queen King" #making a space separated string, so that I can split it easier
        self.faces = face.split(" ")
        self.values = [x for x in range(1, len(self.faces) + 1)] #using list comprehension, because I'm lazy 
        for _type in range (len(self.types)):
            for face in range (len(self.faces)):
                self.cardSets.append(Card(self.types[_type], self.faces[face], self.values[face]))
        
    def mixPlayingCards(self):
        for num in range (len(self.cardSets)):
            temp = self.cardSets[num]
            randNum = rnd.randint(0, len(self.cardSets) - 1)
            self.cardSets[num] = self.cardSets[randNum]
            self.cardSets[randNum] = temp
    
    def showPlayingCards(self):
        for card in self.cardSets:
            card.showCards()
            
    def printCardIndex(self, index):
        self.cardSets[index].showCards()
    
    def returnCardIndex(self, index):
        self.cardSets[index].returnCards()
    
    def returnCardIndividual(self, index):
        _type, face, value = self.cardSets[index].returnIndividual()
        return _type, face, value
    
    def listCards(self):
        cardList = []
        for card in self.cardSets:
            items = card.returnCards()
            cardList.append(items)
        return cardList


class Player:
    def __init__(self, name):
        self.name = name   
        self.playerCards = PlayingCards()
        self.playerWin = 0
    
    def addPlayerCard(self, card):
        self.playerCards.cardSets.append(card)
        
    def showPlayerCards(self):
        print(self.playerCards.listCards())
    
    def showPlayerName(self):
        return (self.name)

    
class Game:
    def __init__(self, maxCards = 5):
        self.gameCards = PlayingCards()
        self.players = []
        self.maxCards = maxCards
        self.curPlayer = ""
        
    def addPlayer(self, name):
        self.players.append(Player(name))
        
    def initiateGame(self):
        self.gameCards.createPlayingCards()
        self.gameCards.mixPlayingCards()
        
        for player in self.players:
            for num in range (self.maxCards):
                player.addPlayerCard(self.gameCards.cardSets[0])
                self.gameCards.cardSets.pop(0)

        
    def showGame(self):
        for player in self.players:
            print(player.showPlayerName())
            player.showPlayerCards()
        print("=" * 30)
        self.gameCards.showPlayingCards()

    def playerNextTurn(self):
        listOfLoses = []
        for player in self.players:
            if player.playerWin >= 1:
                print("This turn would be started by:", player.showPlayerName())
                self.curPlayer = player.showPlayerName()
                player.showPlayerCards()
                cardForTable = int(input("Enter the card index that you want to put into the table\n"))
                self._type, self.face, self.value = player.playerCards.returnCardIndividual(cardForTable - 1)
                print("Card on the table is {} {} {}".format(self._type, self.face, self.value))
                player.playerCards.cardSets.pop(cardForTable - 1)
                player.playerWin = 0
                break
            else:
                listOfLoses.append(player.playerWin)
        if len(listOfLoses) == len(self.players):
            for player in range (len(self.players)):
                temp = self.players[player]
                randNum = rnd.randint(0, len(self.players) - 1)
                self.players[player] = self.players[randNum]
                self.players[randNum] = temp
                
    def playerTurn(self):
        done = False
        for player in self.players:
            if self.curPlayer == player.showPlayerName():
                continue
            if len(player.playerCards.cardSets) == 0:
                done = True
            player.playerWin = 0
            print(player.showPlayerName())
            player.showPlayerCards()
            while True:
                try:
                    choiceA = int(input("Do you have the card? 1 for yes 0 for no\n"))
                    break
                except ValueError:
                    continue
            if choiceA == 1:
                while True:
                    try:
                        cardIndex = int(input("Enter the card Index "))
                        break
                    except ValueError:
                        continue
                _type, face, value = player.playerCards.returnCardIndividual(cardIndex - 1)
                if self._type == _type:
                    if self.value < value:
                        print("You win")
                        player.playerWin += 1
                        player.playerCards.cardSets.pop(cardIndex - 1)
                    else:
                        print("next turn")
                        player.playerCards.cardSets.pop(cardIndex - 1)
                        continue
                else:
                    print("Card type doesn't match, try again")
            elif choiceA == 0:
                self.takeNewCard(player)
                _type, face, value = player.playerCards.returnCardIndividual(-1)
                if self.value < value:
                    print("You win")
                    player.playerWin += 1
                    player.playerCards.cardSets.pop(-1)
                else:
                    print("next turn")
                    player.playerCards.cardSets.pop(-1)
            else:
                print("Try again")
    
    def takeNewCard(self, player):
        beforeNewCard = len(player.playerCards.listCards())
        while True:
            try:
                _type, face, value = self.gameCards.returnCardIndividual(0)
            except IndexError:
                print("No cards left on the table, please proceed to the game.")
                return
                break
            player.addPlayerCard(self.gameCards.cardSets[0])
            self.gameCards.cardSets.pop(0)
            if _type == self._type:
                break
        afterNewCard = len(player.playerCards.listCards())
        player.showPlayerCards()
        print("{} Card(s) added to {}'s deck".format(afterNewCard - beforeNewCard - 1, player.showPlayerName())) #-1 because the last card is always going to be put to the table

    def startGame(self):
        print("First Card given by the table")
        self.gameCards.printCardIndex(0)
        self._type, self.face, self.value = self.gameCards.returnCardIndividual(0)
        self.gameCards.cardSets.pop(0)
        done = False
        while done != True:
            self.playerNextTurn()
            done = self.playerTurn()

a = Game()
a.addPlayer("GamerBoi")
a.addPlayer("BruhGamer")
a.addPlayer("Kittiplier")
a.initiateGame()
a.startGame()
a.showGame()
