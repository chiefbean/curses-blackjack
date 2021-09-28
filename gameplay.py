from cards import deck, card, card_back
import random
import time

class Game():
    def __init__(self, bet, bank, w):
        self.bet = bet
        self.bank = bank
        self.numDecks = 6
        self.player = []
        self.dealer = []
        self.soft = False
        self.isBlackjack = False
        self.deck = []
        self.playing = True
        self.w = w
        self.shuffle()

    def shuffle(self):
        self.deck = deck*self.numDecks
        deck_x = 69
        deck_y = 2
        self.w.move(deck_y, deck_x)
        self.w.addstr("Shuffling")
        self.w.refresh()
        time.sleep(2)
        self.w.move(deck_y, deck_x)
        self.w.addstr("         ")
        for i in range(len(self.deck)-1,0,-1):
            j = random.randint(0,i+1) 
            self.deck[i],self.deck[j] = self.deck[j],self.deck[i]

    def deal(self):
        self.player = []
        self.dealer = []

        if len(self.deck) < 52:
            self.shuffle()

        self.player.append(self.deck.pop())
        self.dealer.append(self.deck.pop())
        self.player.append(self.deck.pop())
        self.dealer.append(self.deck.pop())
        if self.calcHand(self.player) == 21:
            self.isBlackjack = True
            return 0
        elif self.calcHand(self.dealer) == 21:
            return 0
        return 1

    def hit(self, w):
        self.player.append(self.deck.pop())
        if self.calcHand(self.player) > 21:
            return 0
        return 1
    def double(self, w):
        self.player.append(self.deck.pop())
        self.bank -= self.bet
        self.bet *= 2
    def playDealer(self):
        self.dealer.append(self.deck.pop())

    def calcHand(self, hand):
        total = 0
        for c in hand:
            val = c[:-1]
            if val in ['K', 'Q', 'J']:
                if not [i for i in hand if 'A' in i] or total < 11:
                    self.soft = True
                    total += 10
                else:
                    self.soft = False
            elif val == 'A':
                if (total+11) > 21:
                    total += 1
                else:
                    total += 11
            else:
                if [i for i in hand if 'A' in i] and total + int(c[:-1]) > 21:
                    total -= 10
                total += int(c[:-1])
        return total

    def findWinner(self):
        ptot = self.calcHand(self.player)
        dtot = self.calcHand(self.dealer)
        if (dtot > 21 or ptot > dtot) and ptot <= 21:
            return 'player'
        elif dtot == ptot:
            return 'push'
        else:
            return 'dealer'

    def calcWin(self):
        win = 0
        if self.isBlackjack:
            win = self.bet * (3 / 2) + self.bet
            self.isBlackjack = False
        else:
            win = self.bet * 2
        self.bank += win
        return win

