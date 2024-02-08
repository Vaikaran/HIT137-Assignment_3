import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the character image
        self.image = pygame.image.load("mario.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.jump_height = -15
        self.gravity = 1
        self.velocity = [0, 0]
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity[0] = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity[0] = self.speed

        if keys[pygame.K_SPACE] and self.rect.bottom == HEIGHT:
            self.velocity[1] = self.jump_height

        self.velocity[1] += self.gravity

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity[1] = 0

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8
        self.direction = direction
        self.damage = 10

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the mushroom image
        self.image = pygame.image.load("mushroom.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.health = 20

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()  # Remove the enemy when it goes off-screen

        if random.randint(0, 100) < 2:
            collectible = Collectible(self.rect.centerx, self.rect.centery, "health")
            collectibles.add(collectible)
            all_sprites.add(collectible)

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = type

    def update(self):
        pass

# Game Over Screen Function
def game_over_screen():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))

    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

# Initialize groups globally
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Main game function
def main():
    global all_sprites, projectiles, enemies, collectibles  # Declare global variables

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Side-Scrolling Game")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites.add(player)

    score = 0
    shooting_cooldown = 0
    max_cooldown = 30  # Adjust the cooldown value as needed

    camera_offset = 0  # Initial camera offset

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shooting_cooldown == 0:
            projectile = Projectile(player.rect.centerx, player.rect.centery, "right")
            projectiles.add(projectile)
            all_sprites.add(projectile)
            shooting_cooldown = max_cooldown

        if shooting_cooldown > 0:
            shooting_cooldown -= 1

        if random.randint(0, 100) < 2:
            enemy = Enemy(WIDTH + camera_offset, HEIGHT - 50)
            enemies.add(enemy)
            all_sprites.add(enemy)

        all_sprites.update()
        projectiles.update()
        enemies.update()
        collectibles.update()

        pygame.sprite.groupcollide(projectiles, enemies, True, True)

        for enemy in pygame.sprite.spritecollide(player, enemies, True):
            score += 50  # Increase score when killing an enemy
            collectible = Collectible(enemy.rect.centerx, enemy.rect.centery, "health")
            collectibles.add(collectible)
            all_sprites.add(collectible)

        collected_items = pygame.sprite.spritecollide(player, collectibles, True)
        for item in collected_items:
            if item.type == "health":
                player.health += 20
                if player.health > 100:
                    player.health = 100

        camera_offset = max(player.rect.centerx - WIDTH // 2, 0)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        pygame.draw.rect(screen, (0, 255, 0), (10, 10, player.health * 2, 20))
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20), 2)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
