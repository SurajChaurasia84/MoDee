import pygame
import random
import sys
import os

# --------------------- INIT ---------------------
pygame.init()
pygame.mixer.init() 
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Runner: Modi Edition 🚗")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# --------------------- COLORS ---------------------
WHITE = (255, 255, 255)
SKY = (120, 200, 255)
ROAD_GRAY = (50, 50, 50)
YELLOW = (255, 220, 0)
GOLD = (255, 200, 0)
COIN_HIGHLIGHT = (255, 255, 150)
GAME_OVER_COLOR = (255, 60, 60)
MUSIC_CONTROL_COLOR = (0, 255, 0)

# --------------------- CONSTANTS ---------------------
LANES_X = [WIDTH // 2 - 150, WIDTH // 2, WIDTH // 2 + 150]
GROUND_Y = HEIGHT - 180
GRAVITY = 8
SPEED = 10
FPS = 60
SPEED_INCREASE_RATE = 0.5 
SPEED_INCREASE_INTERVAL = 600 

# --------------------- ASSET SETUP ---------------------
ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)

def load_image(name, size):
    """Loads and scales an image, returning a placeholder if unsuccessful."""
    path = os.path.join(ASSET_DIR, name)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except pygame.error:
            pass
    
    print(f"⚠️ Missing asset: {name}, using placeholder.")
    surf = pygame.Surface(size, pygame.SRCALPHA)
    if 'player' in name:
        pygame.draw.rect(surf, (0, 0, 255, 200), surf.get_rect())
    elif 'enemy' in name:
        pygame.draw.rect(surf, (255, 0, 0, 200), surf.get_rect())
    return surf

player_img = load_image("player.png", (100, 120))
enemy_img = load_image("enemy.png", (100, 100))

# --------------------- SOUND HANDLING ---------------------
BG_MUSIC_PATH = os.path.join(ASSET_DIR, "bg_music.mp3")
# Removed: OVER_SOUND_PATH
# Re-using the sound loading utility for coin if available
COIN_SOUND_PATH = os.path.join(ASSET_DIR, "coin_sound.mp3") 

def load_sfx(path):
    """Loads a sound effect using Sound(), or returns None if file is missing/unsupported."""
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

coin_sfx = load_sfx(COIN_SOUND_PATH)
# Removed: game_over_sfx

music_playing = False

def start_bg_music():
    """Starts background music using mixer.music."""
    global music_playing
    if os.path.exists(BG_MUSIC_PATH):
        try:
            pygame.mixer.music.load(BG_MUSIC_PATH)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
            music_playing = True
        except pygame.error as e:
            print(f"⚠️ Could not play bg_music: {e}")
            music_playing = False
    else:
        print("⚠️ bg_music.mp3 not found — running silent mode.")
        music_playing = False

def toggle_music():
    """Toggles background music playback."""
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_playing = False
    else:
        # Check if music is stopped or just paused
        if pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.unpause()
        else:
            # If not started yet or fully stopped
            start_bg_music() 
        music_playing = True

start_bg_music() # Start music at program launch

# --------------------- CLASSES ---------------------
class Player:
    def __init__(self):
        self.lane = 1
        self.x = LANES_X[self.lane]
        self.y = GROUND_Y
        self.jump_vel = 0
        self.is_jumping = False
        self.alive = True

    @property
    def rect(self):
        w, h = player_img.get_size()
        return pygame.Rect(self.x - w // 2, self.y - h, w, h)

    def move_left(self):
        if not self.is_jumping and self.lane > 0: # Added is_jumping check for realism
            self.lane -= 1
            self.x = LANES_X[self.lane]

    def move_right(self):
        if not self.is_jumping and self.lane < 2: # Added is_jumping check for realism
            self.lane += 1
            self.x = LANES_X[self.lane]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_vel = -30

    def update(self):
        if self.is_jumping:
            self.y += self.jump_vel
            self.jump_vel += GRAVITY
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False
    
    def draw(self, surf):
        surf.blit(player_img, (self.x - player_img.get_width() // 2, self.y - player_img.get_height()))

class Enemy:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES_X[self.lane]
        self.y = -100
        self.size = enemy_img.get_size()

    @property
    def rect(self):
        w, h = self.size
        return pygame.Rect(self.x - w // 2, self.y, w, h)

    def update(self, speed):
        self.y += speed

    def draw(self, surf):
        surf.blit(enemy_img, (self.x - self.size[0] // 2, self.y))

class Coin:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES_X[self.lane]
        self.y = -50
        self.r = 20
        self.collected = False

    @property
    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def update(self, speed):
        self.y += speed

    def draw(self, surf):
        pygame.draw.circle(surf, GOLD, (self.x, int(self.y)), self.r)
        pygame.draw.circle(surf, COIN_HIGHLIGHT, (self.x, int(self.y)), self.r, 3)

# --------------------- HELPERS ---------------------
def draw_background(offset):
    """Draws the sky, road, and moving lane markers."""
    screen.fill(SKY)
    pygame.draw.rect(screen, ROAD_GRAY, (0, HEIGHT // 3, WIDTH, HEIGHT))
    
    # Adjusted loop for cleaner scrolling across the screen
    for i in range(15): 
        y = (i * 150 + offset) % (HEIGHT * 2) - HEIGHT
        if y < HEIGHT:
            for lx in LANES_X:
                pygame.draw.rect(screen, YELLOW, (lx - 5, y, 10, 80))

def draw_text_center(text, y, size=50, color=WHITE):
    """Draws centered text on the screen."""
    f = pygame.font.SysFont("Arial", size, True)
    t = f.render(text, True, color)
    screen.blit(t, (WIDTH // 2 - t.get_width() // 2, y))

def draw_hud():
    """Draws score and music status."""
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"High: {high_score}", True, WHITE), (20, 60))
    
    # Music status indicator
    music_status = "ON" if music_playing else "OFF"
    status_color = MUSIC_CONTROL_COLOR if music_playing else GAME_OVER_COLOR
    
    music_text = font.render(f"Music (M): {music_status}", True, status_color)
    screen.blit(music_text, (WIDTH - music_text.get_width() - 20, 20))

def new_game():
    """Resets all game variables for a fresh start. Returns 6 values."""
    return Player(), [], [], 0, SPEED, 0

# --------------------- GAME STATE ---------------------
player, enemies, coins, score, speed, frame = new_game()
high_score = 0
offset = 0 
running = True

# --------------------- MAIN LOOP ---------------------
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            
            # Global Music Toggle (M key)
            if e.key == pygame.K_m:
                toggle_music()
            
            if e.key == pygame.K_ESCAPE:
                running = False
            
            if player.alive:
                if e.key == pygame.K_LEFT: 
                    player.move_left()
                if e.key == pygame.K_RIGHT: 
                    player.move_right()
                if e.key == pygame.K_UP: 
                    player.jump()
            elif e.key == pygame.K_r: # Restart key
                player, enemies, coins, score, speed, frame = new_game() 
                if music_playing:
                    # Only restart music if it was playing before
                    start_bg_music() 

    # --- Game Active Logic ---
    if player.alive:
        player.update()
        
        offset = (offset + speed) % 150 

        if frame % 60 == 0:
            if random.random() < 0.6:
                enemies.append(Enemy())
            else:
                coins.append(Coin())

        for en in enemies: en.update(speed)
        for c in coins: c.update(speed)

        enemies = [en for en in enemies if en.y < HEIGHT + 100]
        coins = [c for c in coins if c.y < HEIGHT + 100 and not c.collected]

        # Collision detection (Enemy)
        for en in enemies:
            if en.rect.colliderect(player.rect):
                player.alive = False
                pygame.mixer.music.stop() # Stop music, regardless of its previous state
                # Removed ALL game over sound logic

        # Collision detection (Coin)
        for c in coins:
            if not c.collected and c.rect.colliderect(player.rect):
                c.collected = True
                score += 1
                if coin_sfx:
                    coin_sfx.play()

        # Score and Speed Increase
        frame += 1
        if frame % SPEED_INCREASE_INTERVAL == 0:
            speed += SPEED_INCREASE_RATE

    # --- Draw Everything ---
    draw_background(offset)
    for en in enemies: en.draw(screen)
    for c in coins:
        if not c.collected: c.draw(screen)
    player.draw(screen)

    draw_hud() # Draw Score and Music Status

    # --- Game Over Screen ---
    if not player.alive:
        draw_text_center("CRASH!", HEIGHT // 2 - 80, 80, GAME_OVER_COLOR)
        draw_text_center(f"Final Score: {score}", HEIGHT // 2, 40)
        draw_text_center("Press R to Restart", HEIGHT // 2 + 80, 30)
        if score > high_score:
            high_score = score
            draw_text_center("New High Score!", HEIGHT // 2 + 120, 30, YELLOW)

    pygame.display.flip()

# --------------------- Cleanup ---------------------
pygame.quit()
sys.exit()