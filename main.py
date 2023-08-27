import random
import PySimpleGUI as sg

class blackjack():
    def __init__(self):
        vertibas = [2,3,4,5,6,7,8,9,10, 'J', 'Q', 'K', 'A']
        masti = ['♥', '♦', '♣', '♠'] #♥, ♦, ♣, ♠

        self.kava = []
        for x in masti:
            for y in vertibas:
                karts = [x, y]
                self.kava.append(karts)

    def choosecard(self):
        self.karts = random.choice(self.kava)
        self.kava.remove(self.karts)
        return self.karts

    def dealtwocards(self):
        if len(self.kava) < 2:
            self.__init__()
        self.kartis = [blackjack.choosecard(self), blackjack.choosecard(self)]
        return self.kartis

    def dealanother(self, kartis):
        if len(self.kava) < 1:
            self.__init__()
        self.karts = random.choice(self.kava)
        self.kava.remove(self.karts)
        kartis.append(self.karts)
        return kartis

    def returnvalue(self, kartis):
        self.value = 0
        for x in kartis:
            try:
                self.value = self.value + x[1]
            except:
                if x[1] in ['J', 'Q', 'K']:
                    self.value = self.value + 10
                elif x[1] == 'A':
                    self.value = self.value + 11
        if self.value > 21:
            for x in kartis:
                if x[1] == 'A':
                    self.value = self.value - 10
                    if self.value < 22:
                        break

        return self.value

class gameGUI(blackjack):
    def createGUI(self):
        layout = [
            [sg.Push(), sg.Text('BLACKJACK OFFLINE'), sg.Push()],
            [sg.Text('Dealers cards: ', key='dealert', visible=False), sg.Text('', key='dealerc', visible=False), sg.Text('', key='dealerv', visible=False)],
            [sg.Text('Your cards: ', key='yourt', visible=False), sg.Text('', key='yourc', visible=False), sg.Text('', key='yourv', visible=False)],
            [sg.Text('', key='text1', visible=False)],
            [sg.Button('Start', visible=True), sg.Button('Draw', visible=False), sg.Button('Stand', visible=False), sg.Button('Play Again', visible=False)]
        ]

        self.windo = sg.Window('BLACKJACK OFFLINE', layout, finalize=True, ttk_theme='clam')
        return self.windo

    def gameResult(self):
        self.windo['Draw'].update(visible=False), self.windo['Stand'].update(visible=False)
        mansvalue = self.returnvalue(self.tu)
        dileratext = ""
        for x in self.dileris:
            dileratext = dileratext + str(x[0]) + str(x[1]) + ' '
        self.windo['dealerc'].Update(dileratext, visible=True)
        self.windo['dealerv'].Update(self.dileravalue, visible=True)
        if self.dileravalue < 17:
            while self.dileravalue < 17:
                self.dealanother(self.dileris)
                self.dileravalue = self.returnvalue(self.dileris)
                dileratext = ""
                for x in self.dileris:
                    dileratext = dileratext + str(x[0]) + str(x[1]) + ' '
                self.windo['dealerc'].Update(dileratext, visible=True)
                self.windo['dealerv'].Update(self.dileravalue, visible=True)
        if self.dileravalue > 21:
            self.windo['text1'].update(f'Tu uzvarēji!', visible=True)
        else:
            if self.dileravalue < mansvalue:
                self.windo['text1'].update(f'Tu uzvarēji!', visible=True)
            elif self.dileravalue > mansvalue:
                self.windo['text1'].update(f'Tu zaudēji!', visible=True)
            elif self.dileravalue == mansvalue:
                irblackjackd = False
                irblackjackt = False
                if len(self.dileris) == 2:
                    for x in self.dileris:
                        if x[1] == 'A':
                            irblackjackd = True
                if len(self.tu) == 2:
                    for x in self.tu:
                        if x[1] == 'A':
                            irblackjackt = True
                if irblackjackd:
                    if irblackjackt:
                        self.windo['text1'].update('Neizšķirts', visible=True)
                    else:
                        self.windo['text1'].update('Dīleris uzvar, jo viņam ir blackjack', visible=True)
                elif irblackjackt:
                    self.windo['text1'].update('Tu uzvari, jo tev ir blackjack', visible=True)
                else:
                    self.windo['text1'].update('Neizšķirts', visible=True)
        self.windo['Play Again'].update(visible=True), self.windo['Draw'].update(visible=False), self.windo['Stand'].update(visible=False)

    def start(self):
        self.windo['text1'].update(visible=False)
        self.windo['Start'].update(visible=False)
        self.windo['Play Again'].update(visible=False)
        self.dileris = self.dealtwocards()
        self.dileravalue = self.returnvalue(self.dileris)
        self.windo['dealert'].update(visible=True)
        self.windo['dealerv'].update(visible=False)
        dileratext = f'{self.dileris[0][0]}{self.dileris[0][1]}    **'
        self.windo['dealerc'].Update(dileratext, visible=True)
        self.tu = self.dealtwocards()
        mansvalue = self.returnvalue(self.tu)
        manstext = ""
        for x in self.tu:
            manstext = manstext + str(x[0]) + str(x[1]) + ' '
        self.windo['yourt'].update(visible=True)
        self.windo['yourc'].update(manstext, visible=True)
        self.windo['yourv'].update(mansvalue, visible=True)
        if mansvalue < 21:
            self.windo['Draw'].update(visible=True), self.windo['Stand'].update(visible=True)
        else:
            self.gameResult()
                
game = gameGUI()
game.createGUI()
while True:
    event, values = game.windo.read()
    if event == sg.WIN_CLOSED:
        exit()
    elif event in ['Start', 'Play Again']:
        game.start()
    elif event == 'Draw':
            game.tu = game.dealanother(game.tu)
            mansvalue = game.returnvalue(game.tu)
            manstext = ""
            for x in game.tu:
                manstext = manstext + str(x[0]) + str(x[1]) + ' '
                game.windo['yourc'].update(manstext, visible=True)
                game.windo['yourv'].update(mansvalue, visible=True)
            if mansvalue > 21:
                game.windo['text1'].update('Tu sadegi un zaudēji!', visible=True)
                game.windo['Play Again'].update(visible=True), game.windo['Draw'].update(visible=False), game.windo['Stand'].update(visible=False)
            if mansvalue == 21:
                game.gameResult()
                    
    elif event == 'Stand':
        game.gameResult()