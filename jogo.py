# Alien Planet - Repair the Ship
# usei python 3.12 pra poder usar o PgZero sem problemas

import pgzrun
import random
from pygame import Rect

# configurações da tela e do jogo
WIDTH = 900
HEIGHT = 500
TITLE = "Alien Planet - Repair the Ship"

GRAVITY = 0.6
PLAYER_SPEED = 4
JUMP_FORCE = -12
MAX_PHASE = 3

game_state = "menu"  # estado atual do jogo: menu, playing, win, game_over
music_on = False
phase = 1
# Funções de música
def start_music():
    global music_on
    if not music_on:
        try:
            music.play("background")
            music.set_volume(0.5)
            music_on = True
        except Exception:
            pass

def stop_music():
    global music_on
    music.stop()
    music_on = False
# Classe do jogador
class Player:
    def __init__(self):
        # cria o personagem
        self.actor = Actor("character_beige_idle", (80, 300))
        self.actor.scale = 0.6
        self.vy = 0  # velocidade vertical
        self.on_ground = False
        self.lives = 3
        self.invincible_timer = 0
        self.frame = 0
        self.anim_timer = 0

    def update(self):
        self.apply_gravity()
        self.move()
        self.animate()
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def apply_gravity(self):
        self.vy += GRAVITY
        self.actor.y += self.vy
        self.on_ground = False
        # checa colisão com plataformas
        for p in platforms:
            if self.actor.colliderect(p) and self.vy >= 0:
                self.actor.bottom = p.top
                self.vy = 0
                self.on_ground = True

    def move(self):
        moving = False
        if keyboard.left:
            self.actor.x -= PLAYER_SPEED
            moving = True
        if keyboard.right:
            self.actor.x += PLAYER_SPEED
            moving = True
        if keyboard.space and self.on_ground:
            self.vy = JUMP_FORCE
            try:
                sounds.sfx_jump.set_volume(0.4)
                sounds.sfx_jump.play()
            except Exception:
                pass
        if not moving:
            self.actor.image = "character_beige_idle"

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 2
            if keyboard.left or keyboard.right:
                self.actor.image = "character_beige_walk_a" if self.frame == 0 else "character_beige_walk_b"

    def take_damage(self):
        if self.invincible_timer == 0:
            self.lives -= 1
            self.invincible_timer = 60
            try:
                sounds.sfx_hurt.set_volume(0.4)
                sounds.sfx_hurt.play()
            except Exception:
                pass
# classe dos inimigos
class Worm:
    def __init__(self, x, y, speed):
        self.actor = Actor("worm_ring_rest", (x, y))
        self.actor.scale = 0.5
        self.speed = speed
        self.direction = -1
        self.frame = 0
        self.anim_timer = 0

    def update(self):
        # movimento e rebote nas paredes
        self.actor.x += self.direction * self.speed
        if self.actor.left <= 0:
            self.direction = 1
        elif self.actor.right >= WIDTH:
            self.direction = -1
        self.animate()

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer >= 15:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 2
            self.actor.image = "worm_ring_move_a" if self.frame == 0 else "worm_ring_move_b"

    def hitbox(self):
        return Rect((self.actor.x - 15, self.actor.y - 10), (30, 20))

# Classe das peças da nave
class ShipPart:
    def __init__(self, x, y):
        self.actor = Actor("ship_part", (x, y))
        self.actor.scale = 0.35
        self.collected = False

    def draw(self):
        if not self.collected:
            self.actor.draw()

    def collect(self):
        if not self.collected:
            self.collected = True
            try:
                sounds.sfx_gem.set_volume(0.4)
                sounds.sfx_gem.play()
            except Exception:
                pass

# Plataformas e fases
def generate_platforms(level):
    platforms = [Rect((0, 460), (900, 40))]  # chão
    x, y = 150, 380
    for _ in range(4):
        platforms.append(Rect((x, y), (70, 20)))
        x += random.randint(180, 250)
        y -= random.randint(40, 70)
        y = max(150, y)
    return platforms

def load_phase(level):
    global platforms, worms, ship_parts
    platforms = generate_platforms(level)
    worms = [Worm(300 + i * 180, 440, 1.5 + level * 0.4) for i in range(level + 1)]
    ship_parts = [ShipPart(200 + i * 200, 200 - i * 40) for i in range(level + 1)]

# Inicialização
player = Player()
platforms, worms, ship_parts = [], [], []
ship_fixed = Actor("ship_fixed", (450, 340))
ship_fixed.scale = 0.7
load_phase(phase)


# botões do jogo
start_button = Rect((350, 200), (200, 50))
music_button = Rect((350, 270), (200, 50))
exit_button = Rect((350, 340), (200, 50))

music_playing_button = Rect((WIDTH - 110, 10), (100, 40))
exit_playing_button = Rect((WIDTH - 110, 60), (100, 40))

music_final_button = Rect(600, 300, 200, 40)
menu_final_button = Rect(600, 360, 200, 40)
exit_final_button = Rect(600, 420, 200, 40)

# funções principais
def update():
    global game_state, phase
    if game_state != "playing":
        return

    player.update()

    for w in worms:
        w.update()
        if player.actor.colliderect(w.hitbox()):
            player.take_damage()

    for p in ship_parts:
        if not p.collected and player.actor.colliderect(p.actor):
            p.collect()

    if all(p.collected for p in ship_parts) and player.actor.x > WIDTH:
        if phase == MAX_PHASE:
            game_state = "win"
        else:
            phase += 1
            player.actor.x = 60
            load_phase(phase)

    if player.lives <= 0:
        game_state = "game_over"

def draw():
    screen.clear()
    #MENU
    if game_state == "menu":
        screen.fill((30, 0, 60))
        screen.draw.text("Alien Planet - Repair the Ship", center=(450, 120), fontsize=60, color=(180, 220, 255))
        screen.draw.filled_rect(start_button, (70, 160, 220))
        screen.draw.filled_rect(music_button, (150, 50, 200))
        screen.draw.filled_rect(exit_button, (200, 40, 40))
        screen.draw.text("START", center=start_button.center, fontsize=32, color="white")
        screen.draw.text(f"MUSIC {'ON' if music_on else 'OFF'}", center=music_button.center, fontsize=26, color="white")
        screen.draw.text("EXIT", center=exit_button.center, fontsize=32, color="white")

    #JOGO
    elif game_state == "playing":
        screen.fill((60, 30, 90) if phase % 2 == 0 else (90, 40, 120))
        for plat in platforms:
            screen.draw.filled_rect(plat, (120, 180, 200))
        for part in ship_parts:
            part.draw()
        for w in worms:
            w.actor.draw()
        if player.invincible_timer % 10 < 5:
            player.actor.draw()

        screen.draw.filled_rect(music_playing_button, (150, 50, 200))
        screen.draw.text(f"MUSIC {'ON' if music_on else 'OFF'}", center=music_playing_button.center, fontsize=18, color="white")
        screen.draw.filled_rect(exit_playing_button, (200, 40, 40))
        screen.draw.text("EXIT", center=exit_playing_button.center, fontsize=18, color="white")

        screen.draw.text(f"Phase: {phase}", (20, 20), fontsize=28, color=(220, 220, 255))
        screen.draw.text(f"Lives: {player.lives}", (20, 50), fontsize=28, color=(220, 220, 255))
        screen.draw.text(f"Ship parts: {sum(p.collected for p in ship_parts)}/{len(ship_parts)}", (20, 80), fontsize=24, color=(220, 220, 255))

    #TELA DE VITÓRIA
    elif game_state == "win":
        screen.fill((30, 0, 80))
        ship_fixed.draw()
        screen.draw.text("SHIP REPAIRED!", center=(450, 140), fontsize=60, color=(200, 255, 200))
        screen.draw.text("You escaped the alien planet", center=(450, 200), fontsize=32, color=(200, 255, 200))
        screen.draw.filled_rect(music_final_button, (150, 50, 200))
        screen.draw.text(f"MUSIC {'ON' if music_on else 'OFF'}", center=music_final_button.center, fontsize=18, color="white")
        screen.draw.filled_rect(menu_final_button, (70, 160, 220))
        screen.draw.text("MENU", center=menu_final_button.center, fontsize=18, color="white")
        screen.draw.filled_rect(exit_final_button, (200, 40, 40))
        screen.draw.text("EXIT", center=exit_final_button.center, fontsize=18, color="white")

    #GAME OVER
    elif game_state == "game_over":
        screen.fill((20, 0, 20))
        screen.draw.text("GAME OVER", center=(450, 250), fontsize=64, color=(255, 80, 80))
        screen.draw.filled_rect(music_final_button, (150, 50, 200))
        screen.draw.text(f"MUSIC {'ON' if music_on else 'OFF'}", center=music_final_button.center, fontsize=18, color="white")
        screen.draw.filled_rect(menu_final_button, (70, 160, 220))
        screen.draw.text("MENU", center=menu_final_button.center, fontsize=18, color="white")
        screen.draw.filled_rect(exit_final_button, (200, 40, 40))
        screen.draw.text("EXIT", center=exit_final_button.center, fontsize=18, color="white")

# clique do mouse
def on_mouse_down(pos):
    global game_state, music_on, phase

    def toggle_music():
        if music_on:
            stop_music()
        else:
            start_music()

    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "playing"
        elif music_button.collidepoint(pos):
            toggle_music()
        elif exit_button.collidepoint(pos):
            quit()
    elif game_state == "playing":
        if music_playing_button.collidepoint(pos):
            toggle_music()
        elif exit_playing_button.collidepoint(pos):
            quit()
    elif game_state in ("win", "game_over"):
        if music_final_button.collidepoint(pos):
            toggle_music()
        elif menu_final_button.collidepoint(pos):
            game_state = "menu"
            phase = 1
            player.lives = 3
            player.actor.x = 80
            load_phase(phase)
        elif exit_final_button.collidepoint(pos):
            quit()

pgzrun.go()
