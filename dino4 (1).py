import pygame
import random

pygame.init()
# Обязательно инициализируем микшер для звука
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run: Audio Edition")

WHITE = (255, 255, 255)
GREEN = (144, 238, 144)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
try:
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    jump_sfx = pygame.mixer.Sound("jump.mp3")
    crash_sfx = pygame.mixer.Sound("collision.mp3")
except:
    print("Внимание: Звуковые файлы не найдены. Играем в тишине.")
    jump_sfx = None
    crash_sfx = None
try:
    dino_img = pygame.image.load("dino.png")
    cactus_img = pygame.image.load("cactus.png")
except:
    dino_img = pygame.Surface((60, 70))
    dino_img.fill((50, 50, 50))
    cactus_img = pygame.Surface((40, 60))
    cactus_img.fill((0, 100, 0))

clock = pygame.time.Clock()
fps = 60


class Dino:
    def __init__(self):
        self.image = pygame.transform.scale(dino_img, (60, 70))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.reset()

    def reset(self):
        self.x = 50
        self.y = 300
        self.is_jumping = False
        self.jump_power = 10
        self.current_jump = self.jump_power

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def jump_logic(self):
        if self.is_jumping:
            if self.current_jump >= -self.jump_power:
                neg = 1
                if self.current_jump < 0:
                    neg = -1
                self.y -= (self.current_jump ** 2) * 0.5 * neg
                self.current_jump -= 1
            else:
                self.is_jumping = False
                self.current_jump = self.jump_power


class Obstacle:
    def __init__(self, speed):
        self.width = random.randint(40, 70)
        self.height = random.randint(50, 90)
        self.image = pygame.transform.scale(cactus_img, (self.width, self.height))
        self.x = SCREEN_WIDTH
        self.y = 370 - self.height
        self.speed = speed + random.uniform(0, 2)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= self.speed


def display_ui(score, speed, game_over):
    font = pygame.font.SysFont("Arial", 25)
    score_txt = font.render(f"Очки: {score}  Скорость: {round(speed, 1)}", True, BLACK)
    screen.blit(score_txt, (10, 10))
    if game_over:
        big_font = pygame.font.SysFont("Arial", 40)
        msg = big_font.render("ИГРА ОКОНЧЕНА! Нажми R для рестарта", True, RED)
        screen.blit(msg, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 1.5))


dino = Dino()
game_speed = 7.0
obstacles = [Obstacle(game_speed)]
score = 0
running = True
game_over = False
waiting_for_start = True
while waiting_for_start:
    screen.fill(WHITE)
    font = pygame.font.SysFont("Arial", 40)
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    start_txt = font.render("Нажми SPACE для старта", True, (50, 50, 50))
    screen.blit(start_txt, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_for_start = False
while running:
    bg_color = GREEN if score >= 100 else WHITE
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dino.is_jumping and not game_over:
                dino.is_jumping = True
                if jump_sfx: jump_sfx.play()

            if event.key == pygame.K_r and game_over:
                dino.reset()
                game_speed = 7.0
                score = 0
                obstacles = [Obstacle(game_speed)]
                game_over = False
                pygame.mixer.music.play(-1)

    if not game_over:
        dino.jump_logic()
        game_speed += 0.002
        for obs in obstacles[:]:
            obs.move()
            dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
            obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)

            if dino_rect.colliderect(obs_rect):
                game_over = True
                pygame.mixer.music.stop()
                if crash_sfx: crash_sfx.play()

            if obs.x + obs.width < 0:
                obstacles.remove(obs)
                obstacles.append(Obstacle(game_speed))
                score += 10

    dino.draw()
    for obs in obstacles:
        obs.draw()
    display_ui(score, game_speed, game_over)
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
