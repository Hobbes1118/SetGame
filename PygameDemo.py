import pygame
from pygame.locals import *
import BasicSet as set

CARD_HEIGHT = 68
CARD_LENGTH = 58

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self._deck = None
        self._board = None
        self.selected = []


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._deck = set.Deck()
        for card in self._deck.get_cards():
            filename = card.get_filename()
            img = pygame.image.load(filename)
            card.set_image(img)
        self._deck.deal_board()
        x_coord = 100
        y_coord = 100
        for card in self._deck.get_board().get_layout():
            card.set_loc(x_coord, y_coord)
            if (y_coord >= 260):
                y_coord = 100
                x_coord += 80
            else:
                y_coord += 80

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._deck.deal()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            for card in self._deck.get_board().get_layout():
                if self.onCard(card, mousePos):
                    self.selected.append(card)
                    self.checkSelected()

    def on_loop(self):
        pass
    def on_render(self):
        self.render_board()
        pygame.display.flip()

    def render_board(self):
        for card in self._deck.get_board().get_layout():
            self.show_card(card, card.get_loc())

    def on_cleanup(self):
        pygame.quit()

    def show_card(self, card, pos):
        self._display_surf.blit(card.get_image(), pos)

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def onCard(self, card, mousePos):
        mouse_x, mouse_y = mousePos
        card_x, card_y = card.get_loc()
        return (mouse_x > card_x and mouse_x < card_x + CARD_LENGTH
            and mouse_y > card_y and mouse_y < card_y + CARD_HEIGHT)

    def checkSelected(self):
        if (len(self.selected) != 3):
            return
        if (self._deck.get_board().check_set_arr(self.selected)):
            self._deck.clear_set(self.selected)
        self.selected = []

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
