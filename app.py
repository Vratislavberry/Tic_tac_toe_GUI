from flask import Flask, render_template
from tic_tac_toe import Tic_tac_toe
import jyserver.Flask as jsf

app = Flask(__name__)
game = Tic_tac_toe()

@jsf.use(app)
class App:
    def __init__(self):
        self.resume_game = True # Kdyz je False, tak policka v piskvorkach nereaguji na kliknuti

    def make_turn(self, x, y):
        # Kontrola, zda se hrac nesnazi kliknout na policko v jiz dohrane hre
        if self.resume_game == False:
            return "Hra jiz byla dohrana"

        # Kontrola, zda policko, na ktere hrac kliknul, jiz neni zabrane
        if game.board[y][x] != "":
            return "Toto policko je jiz zabrane"

        # Vypnuti tlacitek po dobu vykonavani funkce
        self.js.change_buttons_state(True).eval()

        # Zapsani tahu na frontend
        id = "btn_"+str(x)+"_"+str(y)
        self.js.document.getElementById(id).style.color = game.player_color
        self.js.document.getElementById(id).textContent = game.player_on_turn

        # Zapsani tahu do backendu (desky)
        game.make_turn(x, y)


        # Kontrola, zda hrac svym tahem nevyhral hru
        stav_hry = game.game_ended()
        if stav_hry == 1:
            # Zvyrazneni vyhernich policek
            for souradnice in game.win_symbols:
                win_id = "btn_"+str(souradnice[0])+"_"+str(souradnice[1])
                self.js.document.getElementById(win_id).style.background = "yellow"
            # Ukonceni hry
            self.end_game(vyhra=True)

        # Kontrola, zda hrac svym tahem nezpusobil remizu
        elif stav_hry == 2:
            self.end_game(vyhra=False)

        # Zmena hrace
        else:
            game.switch_player()
            self.js.document.getElementById("player_symbol").style.color = game.player_color
            self.js.document.getElementById("player_symbol").textContent = game.player_on_turn

        # zapnuti tlacitek
        self.js.change_buttons_state(False).eval()


    def end_game(self, vyhra):
        # Vypnuti reakce na kliknuti na tlacitko
        self.resume_game = False

        # Nahrazeni zpravy na to, kdo je na rade za zpravu kdo vyhral
        if vyhra == True:
            self.js.document.getElementById("game_status_message").innerHTML = "The winner is: <span  id='player_symbol'></span>"
            self.js.document.getElementById("player_symbol").style.color = game.player_color
            self.js.document.getElementById("player_symbol").textContent = game.player_on_turn
        else:
            self.js.document.getElementById("game_status_message").innerHTML = "It's a tie <span  id='player_symbol'></span>"


    def start_new_game(self):
        # Vypnuti reset tlacitka po dobu resetu
        self.js.document.getElementById("reset_button").disabled = True
        self.js.document.getElementById("reset_button").textContent = "Resetuji..."

        # Reset herniho pole na frontendu
        self.js.reset_symbols().eval()

        # Reset background barvy u vyhernich symbolu (na frontendu)
        for souradnice in game.win_symbols:
            win_id = "btn_" + str(souradnice[0]) + "_" + str(souradnice[1])
            self.js.document.getElementById(win_id).style.background = "rgb(197, 197, 197)"

        # Reset herniho pole na backendu
        game.reset()

        # Zmena status zpravy na default
        self.js.document.getElementById("game_status_message").innerHTML = "It's turn of player: <span  id='player_symbol'></span>"
        self.js.document.getElementById("player_symbol").style.color = game.player_color
        self.js.document.getElementById("player_symbol").textContent = game.player_on_turn

        # Zapnuti tlacitek v hracim poli
        self.resume_game = True

        # Zapnuti reset tlacitka
        self.js.document.getElementById("reset_button").disabled = False
        self.js.document.getElementById("reset_button").textContent = "Reset"


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/game_screen')
def game_screen():
    #Pokud hrac hru jiz zacal a pote refreshnul stranku, tak se refreshne i jeho hra
    #O refresh na frontendu se neni nutne starat, protoze jakekoliv zmeny pri refreshnuti stranky u klienta zmizi
    game.reset()

    # Pokud by hrac refreshnul stranku, kdyz by hra byla vyhrana,
    # tak by tato promenna byla na False a v dalsim kole by neslo pokladat znaky
    App.set("resume_game", True)
    return App.render(render_template("game_screen.html", game=game))


if __name__ == '__main__':
    app.run()
