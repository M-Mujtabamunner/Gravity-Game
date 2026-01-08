import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mujtaba  Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 200, 255)
RED = (255, 80, 80)

# Player
player = pygame.Rect(100, HEIGHT // 2, 30, 30)
player_vel = 0
gravity = 0.6
gravity_dir = 1  # 1 = down, -1 = up

# Obstacles
obstacles = []
OBSTACLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_EVENT, 1200)

# Score
score = 0

def reset_game():
    global player, player_vel, gravity_dir, obstacles, score
    player.y = HEIGHT // 2
    player_vel = 0
    gravity_dir = 1
    obstacles.clear()
    score = 0

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gravity_dir *= -1  # Flip gravity
                player_vel = -8 * gravity_dir

        if event.type == OBSTACLE_EVENT:
            h = random.randint(30, 80)
            if random.choice([True, False]):
                obstacles.append(pygame.Rect(WIDTH, 0, 20, h))
            else:
                obstacles.append(pygame.Rect(WIDTH, HEIGHT - h, 20, h))

    # Player physics
    player_vel += gravity * gravity_dir
    player.y += player_vel

    # Clamp to floor / ceiling
    if player.top <= 0:
        player.top = 0
        player_vel = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT
        player_vel = 0

    # Obstacles
    for obs in obstacles[:]:
        obs.x -= 5
        if obs.right < 0:
            obstacles.remove(obs)
            score += 1
        if player.colliderect(obs):
            reset_game()

    # Draw
    pygame.draw.rect(screen, CYAN, player)
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    draw_text(f"Score: {score}", 10, 10)
    draw_text("SPACE = Flip Gravity", 10, 40)

    pygame.display.flip()
