import random
import cv2
ONE = 0
TWO = 1
THREE = 2
RED = 0
PURPLE = 1
GREEN = 2
SQUIGGLE = 0
DIAMOND = 1
OVAL = 2
SOLID = 0
STRIPED = 1
EMPTY = 2

def checkColor(card1, card2, card3):
    if (card1.color == card2.color and card1.color == card3.color):
        return True
    elif(card1.color != card2.color and card1.color != card3.color
        and card2.color != card3.color):
        return True
    return False

def checkNumber(card1, card2, card3):
    if (card1.number == card2.number and card1.number == card3.number):
        return True
    elif(card1.number != card2.number and card1.number != card3.number
        and card2.number != card3.number):
        return True
    return False

def checkShape(card1, card2, card3):
    if (card1.shape == card2.shape and card1.shape == card3.shape):
        return True
    elif(card1.shape != card2.shape and card1.shape != card3.shape
        and card2.shape != card3.shape):
        return True
    return False

def checkShading(card1, card2, card3):
    if (card1.shading == card2.shading and card1.shading == card3.shading):
        return True
    elif(card1.shading != card2.shading and card1.shading != card3.shading
        and card2.shading != card3.shading):
        return True
    return False

def findThird(card1, card2):
    if (card1.color == card2.color):
        color = card1.color
    else:
        set = [0,1,2]
        set.remove(card1.color)
        set.remove(card2.color)
        color = set[0]

    if (card1.shape == card2.shape):
        shape = card1.shape
    else:
        set = [0,1,2]
        set.remove(card1.shape)
        set.remove(card2.shape)
        shape = set[0]

    if (card1.number == card2.number):
        number = card1.number
    else:
        set = [0,1,2]
        set.remove(card1.number)
        set.remove(card2.number)
        number = set[0]

    if (card1.shading == card2.shading):
        shading = card1.shading
    else:
        set = [0,1,2]
        set.remove(card1.shading)
        set.remove(card2.shading)
        shading = set[0]

    return Card(color, number, shape, shading)



class Card:
    def __init__(self, color, number, shape, shading):
        self.color = color
        self.number = number
        self.shape = shape
        self.shading = shading
        self.image = None
        self.loc = None

    def __repr__(self):
        rep = ""
        if self.number == ONE:
            rep += "one "
        elif self.number == TWO:
            rep += "two "
        else:
            rep += "three "

        if self.shading == EMPTY:
            rep += "empty "
        elif self.shading == STRIPED:
            rep += "striped "
        else:
            rep += "solid "

        if self.color == RED:
            rep += "red "
        elif self.color == PURPLE:
            rep += "purple "
        else:
            rep += "green "

        if self.shape == DIAMOND:
            rep += "diamond(s)"
        elif self.shape == SQUIGGLE:
            rep += "squiggle(s)"
        else:
            rep += "oval(s)"
        return rep

    def get_filename(self):
        filename = repr(self).replace(" ", "_")
        filename += ".png"
        #filename = "imgs/one_red_solid_squiggle(s).png"
        filename = "imgs/" + filename
        return filename

    def set_image(self, img):
        self.image = img

    def get_image(self):
        return self.image

    def set_loc(self, x, y):
        self.loc = (x,y)

    def set_loc_tuple(self, pos):
        self.loc = pos

    def get_loc(self):
        return self.loc

    def __eq__(self, other):
        if (self.color == other.color and self.shape == other.shape
            and self.number == other.number and self.shading == other.shading):
            return True
        return False

class Deck:
    def __init__(self):
        self.cards = None
        self.generate_deck()
        self.board = Board()

    def __str__(self):
        rep = ""
        rep += "Board:\n" + str(self.board) + "\n"
        rep += "Cards in deck: " + str(len(self.cards))
        return rep

    def get_board(self):
        return self.board

    def get_cards(self):
        return self.cards

    def generate_deck(self):
        cards = []
        for i in range(81):
            temp = i
            shading = temp//27
            temp = temp%27
            shape = temp//9
            temp = temp%9
            color = temp//3
            temp = temp%3
            number = temp
            cards.append(Card(color, number, shape, shading))
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_board(self):
        self.board.clear()
        for i in range(12):
            self.board.add_card(self.cards.pop())

    def deal(self):
        for i in range(3):
            self.board.add_card(self.cards.pop())

    def clear_set(self, cards):
        if (len(self.cards) >= 3):
            self.deal()
            self.board.get_layout()[len(self.board.get_layout())-1].set_loc_tuple(cards[2].get_loc())
            self.board.get_layout()[len(self.board.get_layout())-2].set_loc_tuple(cards[1].get_loc())
            self.board.get_layout()[len(self.board.get_layout())-3].set_loc_tuple(cards[0].get_loc())
        self.board.clear_set(cards)


class Board:

    def __init__(self):
        self.layout = []

    def __str__(self):
        rep = ""
        for i in range(len(self.layout)//3):
            for j in range(3):
                rep += str(3*i+j) + ": "
                rep += str(self.layout[3*i+j])
                rep += "    "
            rep += "\n"
        return rep

    def get_layout(self):
        return self.layout

    def add_card(self, card):
        self.layout.append(card)

    def clear(self):
        self.layout = []

    def check_set(self, card1, card2, card3):
        if (self.in_board(card1) and self.in_board(card2) and self.in_board(card3)):
            if (checkColor(card1, card2, card3) == True):
                if (checkNumber(card1, card2, card3) == True):
                    if (checkShape(card1, card2, card3) == True):
                        if (checkShading(card1, card2, card3) == True):
                            return True
        return False

    def check_set_arr(self, cards):
        if (len(cards) == 3 and self.check_set(cards[0], cards[1], cards[2])):
            return True
        return False

    def clear_set(self, cards):
        for card in cards:
            self.layout.remove(card)

    def in_board(self, card):
        for check_card in self.layout:
            if card == check_card:
                return True
        return False

    def find_sets(self):
        sets = []
        for i in range(len(layout)):
            for j in range(i, len(layout)):
                third = findThird(layout[i], layout[j])
                if (self.in_board(third) == True):
                    sets.append([i, j, third])
        return sets

def generate_filenames():
    deck = Deck()
    img = cv2.imread("imgs/one_red_solid_squiggle(s).png")
    for card in deck.cards:
        cv2.imwrite(card.get_filename(), img)


if (__name__ == '__main__'):
    print('hello')
