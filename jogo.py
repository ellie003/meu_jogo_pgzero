# projeto desenvolvido em Python 3.12 utilizando PgZero.
# a versão do Python foi escolhida por compatibilidade técnica.

#não usar pygame, mas pode usar Rect
#menu tem que ter três opções: jogar, musica(on ou off) e opção de sair feitos

import pgzrun
from pygame import Rect


WIDTH = 800
HEIGHT = 600
TITLE = "Main Menu"

game_state = "menu"
sound_on = False  #aqui faz o som começar desligado para não ter autoplay 


start_button = Rect(300, 200, 200, 60) # botão de inicio
sound_button = Rect(300, 300, 200, 60) # botão do som
exit_button = Rect(300, 400, 200, 60) # botão para sair

#configuração do main menu
def draw():
    screen.clear()
    draw_menu()


def draw_menu():
    screen.fill("darkblue")

    screen.draw.text(
        "Meu Jogo de Plataforma",
        center=(WIDTH // 2, 100),
        fontsize=50,
        color="white"
    )

#configuração dos botões

    for rect in (start_button, sound_button, exit_button):
        screen.draw.filled_rect(rect, "gray")

    screen.draw.text(
        "Start Game",
        center=start_button.center,
        fontsize=30,
        color="black"
    )

    screen.draw.text(
        f"Sound: {'on' if sound_on else 'off'}",
        center=sound_button.center,
        fontsize=30,
        color="black"
    )

    screen.draw.text(
        "Quit",
        center=exit_button.center,
        fontsize=30,
        color="black"
    )

#comportamento do som na tela main menu
def on_mouse_down(pos):
    global sound_on

    if sound_button.collidepoint(pos):
        sound_on = not sound_on

        if sound_on:
            music.set_volume(0.5)
            music.play("musica_fundo")
        else:
            music.stop()

    elif start_button.collidepoint(pos):
        print("Start Game clicked")

    elif exit_button.collidepoint(pos):
        quit()


pgzrun.go()

