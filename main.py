from cards import deck, card, card_back
import random
import curses
import sys
from gameplay import Game

status = ['Hit (H)', 'Stand (S)', 'Double (D)', 'Bet (B)']

dealer_yx = (4, 36)
player_yx = (7, 16)

def main():
    curses.wrapper(cursesMain)

def cursesMain(w):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    drawNewGame(w)
    play(w)
    w.getch()
    curses.curs_set(1)

def getInput(w):
    inputStr = ""
    while char := w.getch():
        if(char == 10):
            break
        if(char == curses.KEY_BACKSPACE):
            y, x = w.getyx()
            inputStr = inputStr[:-1]
            w.addch(y,x-1, " ")
            w.move(y, x-1)
        else:
            w.addch(chr(char))
            inputStr += chr(char)
        w.refresh()
    return inputStr

def drawNewGame(w):
    w.erase()
    selected = 3
    w.move(22, 21)
    for i in range(0, len(status)):
        w.addstr("|")
        if i == selected:
            w.addstr(status[i], curses.color_pair(1))
        else:
            w.addstr(status[i])
    w.addstr("|")

    w.refresh()

def play(w):
    bank = 100
    bet = 5
    
    w.move(21, 33)
    w.addstr("Bet using ↑ and ↓")
    w.move(23, 32)
    w.addstr(f"Bank: {bank} | Bet: {bet}")
    w.refresh()

    bet = menu(w, bet, bank)
   
    game = Game(bet, bank, w)
    while True:
        game.bank -= game.bet
        w.move(23, 32)
        w.addstr(f"Bank: {game.bank} | Bet: {game.bet}            ")
        if game.deal():
            hide_dealer = []
            hide_dealer.append(game.dealer[0])
            hide_dealer.append("XX")
            showHand(w, game.player, player_yx)
            w.move(player_yx[0], player_yx[1]-5)
            w.addstr(str(game.calcHand(game.player)))
            showHand(w, hide_dealer, dealer_yx)
            w.move(dealer_yx[0], dealer_yx[1]-5)
            w.addstr(str(game.dealer[0][:-1]))
            gameLoop(w, game)
            if game.calcHand(game.player) <= 21:
                if [i for i in game.dealer if 'A' in i]:
                    game.soft = True
                else:
                    game.soft = False
                while game.calcHand(game.dealer) < 17 or (game.soft and game.calcHand(game.dealer) == 17 ):
                    game.playDealer()
                    w.move(dealer_yx[0], dealer_yx[1]-5)
                    w.addstr(str(game.calcHand(game.dealer)))
        
        showHand(w, game.player, player_yx)
        w.move(player_yx[0], player_yx[1]-5)
        w.addstr(str(game.calcHand(game.player)))
        showHand(w, game.dealer, dealer_yx)
        w.move(dealer_yx[0], dealer_yx[1]-5)
        w.addstr(str(game.calcHand(game.dealer)))

        if game.findWinner() == 'player':
            win = game.calcWin()
            w.move(20, 33)
            w.addstr("You win %s chips!" % win)
        elif game.findWinner() == 'push':
            game.bank += game.bet
            w.move(20, 38)
            w.addstr("Push.")
        else:
            w.move(20, 35)
            w.addstr("You lose.")
        w.move(21, 28)
        w.addstr("Press any key to play again")
        w.getch()
        drawNewGame(w)
        game.bet = bet
        w.move(21, 33)
        w.addstr("Bet using ↑ and ↓")
        w.move(23, 32)
        w.addstr(f"Bank: {game.bank} | Bet: {game.bet}")
        game.bet = menu(w, game.bet, game.bank)

def menu(w, bet, bank):
    selected = 3
    while char := w.getch():
        if char == 259 and selected == 3:
            if bet < bank:
                bet += 5
            w.move(23, 32)
            w.addstr(f"Bank: {bank} | Bet: {bet}          ")
        elif char == 258 and selected == 3:
            if bet > 5:
                bet -= 5
            w.move(23, 32)
            w.addstr(f"Bank: {bank} | Bet: {bet}          ")
        elif char == 260:
            if selected > 0:
                selected -= 1
            w.move(22, 21)
            for i in range(0, len(status)):
                w.addstr("|")
                if i == selected:
                    w.addstr(status[i], curses.color_pair(1))
                else:
                    w.addstr(status[i])
            w.addstr("|")
        elif char == 261:
            if selected < 3:
                selected += 1
            w.move(22, 21)
            for i in range(0, len(status)):
                w.addstr("|")
                if i == selected:
                    w.addstr(status[i], curses.color_pair(1))
                else:
                    w.addstr(status[i])
            w.addstr("|")
        elif char == 10:
            break
        w.refresh()
    return bet

def showHand(w, hand, yx):
    w.move(yx[0], yx[1])
    for i in range(0, len(hand)):
        if 'XX' != hand[i]:
            w.move(yx[0]+i, yx[1] + (i*5))
            w.addstr(card[0])
            w.move(yx[0]+i+1, yx[1] + (i*5))
            w.addstr(card[1] % hand[i][:-1].ljust(2))
            w.move(yx[0]+i+2, yx[1] + (i*5))
            w.addstr(card[2] % hand[i][-1:])
            w.move(yx[0]+i+3, yx[1] + (i*5))
            w.addstr(card[3] % hand[i][:-1].rjust(2))
            w.move(yx[0]+i+4, yx[1] + (i*5))
            w.addstr(card[4])
        else:
            w.move(yx[0]+i, yx[1] + (i*5))
            w.addstr(card_back[0])
            w.move(yx[0]+i+1, yx[1] + (i*5))
            w.addstr(card_back[1])
            w.move(yx[0]+i+2, yx[1] + (i*5))
            w.addstr(card_back[2])
            w.move(yx[0]+i+3, yx[1] + (i*5))
            w.addstr(card_back[3])
            w.move(yx[0]+i+4, yx[1] + (i*5))
            w.addstr(card_back[4])

def gameLoop(w, game):
    selected = 0
    w.move(22, 21)
    for i in range(0, len(status)):
        w.addstr("|")
        if i == selected:
            w.addstr(status[i], curses.color_pair(1))
        else:
            w.addstr(status[i])
    w.addstr("|")
    while char := w.getch():
        if char == 260:
            if selected > 0:
                selected -= 1
            w.move(22, 21)
            for i in range(0, len(status)):
                w.addstr("|")
                if i == selected:
                    w.addstr(status[i], curses.color_pair(1))
                else:
                    w.addstr(status[i])
            w.addstr("|")
        elif char == 261:
            if selected < 3:
                selected += 1
            w.move(22, 21)
            for i in range(0, len(status)):
                w.addstr("|")
                if i == selected:
                    w.addstr(status[i], curses.color_pair(1))
                else:
                    w.addstr(status[i])
            w.addstr("|")
        elif char == 10:
            if selected == 0:
                v = game.hit(w)
                showHand(w, game.player, player_yx)
                w.move(player_yx[0], player_yx[1]-5)
                w.addstr(str(game.calcHand(game.player)))
                if not v:
                    break
            if selected == 1:
                break
            if selected == 2:
                game.double(w)
                w.move(23, 32)
                w.addstr(f"Bank: {game.bank} | Bet: {game.bet}            ")
                showHand(w, game.player, player_yx)
                w.move(player_yx[0], player_yx[1]-5)
                w.addstr(str(game.calcHand(game.player)))
                break
        elif char == chr('h'):
            game.hit(w)
            showHand(w, game.player, player_yx)
            w.move(player_yx[0], player_yx[1]-5)
            w.addstr(str(game.calcHand(game.player)))
        elif char == chr('s'):
            break
        elif char == chr('d'):
            game.double(w)
            showHand(w, game.player, player_yx)
            w.move(player_yx[0], player_yx[1]-5)
            w.addstr(str(game.calcHand(game.player)))
            break
        w.refresh()

if __name__ == '__main__':
    main()
