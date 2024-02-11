import pygame
import sys
import random

# Initiate game --
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (157, 230, 240)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the character image
        self.image = pygame.image.load("mario.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT  
        self.speed = 5
        self.jump_height = -15
        self.gravity = 1
        self.velocity = [0, 0]
        self.max_health = 100  # Maximum health
        self.health = self.max_health
        self.lives = 2  # Set initial lives to the desired value
        self.hit = False  # Flag to track if player has been hit
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity[0] = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity[0] = self.speed

        if keys[pygame.K_UP] and self.rect.bottom == HEIGHT - 50:
            self.jump()

        self.velocity[1] += self.gravity

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocity[1] = 0

    def jump(self):
        self.velocity[1] = self.jump_height

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, "right")
        projectiles.add(projectile)
        all_sprites.add(projectile)

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

# HealthRefill Class
class HealthRefill(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the health refill image
        self.image = pygame.image.load("firstaid.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()  # Remove the health refill when it goes off-screen

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the mushroom image
        self.image = pygame.image.load("mushroom.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - 50)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()  # Remove the enemy when it goes off-screen

    def drop_health_refill(self):
        if random.randint(0, 100) < 10:  # 10% chance to drop health refill
            health_refill = HealthRefill(self.rect.centerx, self.rect.centery)
            health_refills.add(health_refill)
            all_sprites.add(health_refill)

# Game Over Screen Function
def game_over_screen():
    global screen, all_sprites, projectiles, enemies, health_refills  # Declare global variables
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press R to Restart", True, (255, 0, 0))

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
                    # Reset the game
                    all_sprites = pygame.sprite.Group()
                    projectiles = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    health_refills = pygame.sprite.Group()
                    main()

# Initialize groups globally
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
health_refills = pygame.sprite.Group()

# Main game function
def main():
    global screen, all_sprites, projectiles, enemies, health_refills  # Declare global variables

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Side-Scrolling Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)  # Font initialization for displaying lives

    player = Player()
    all_sprites.add(player)

    # Load the background image
    background_image = pygame.image.load("background.jpg").convert()
    background_rect = background_image.get_rect()

    

    shooting_cooldown = 0
    max_cooldown = 30  # Adjust the cooldown value

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and player.rect.bottom == HEIGHT:
            player.jump()

        if keys[pygame.K_l] and shooting_cooldown == 0:
            player.shoot()
            shooting_cooldown = max_cooldown  # Set cooldown when shooting

        if shooting_cooldown > 0:
            shooting_cooldown -= 1

        if random.randint(0, 100) < 2:
            enemy = Enemy(WIDTH, HEIGHT - 50)
            enemies.add(enemy)
            all_sprites.add(enemy)

        all_sprites.update()
        projectiles.update()
        enemies.update()
        health_refills.update()

        # Check for collision between projectiles and enemies
        collisions = pygame.sprite.groupcollide(projectiles, enemies, True, True)

        # Update score based on the number of enemies hit
        for enemy_group in collisions.values():
            for enemy in enemy_group:
                player.score += 1
                enemy.drop_health_refill()

        # Check for collision with health refills
        health_collisions = pygame.sprite.spritecollide(player, health_refills, True)
        for health_refill in health_collisions:
            player.health = min(player.max_health, player.health + int(player.max_health * 0.1))

        # Check for collision with enemies
        for enemy in pygame.sprite.spritecollide(player, enemies, False):
            if enemy.rect.right < 0 and not player.hit:
                continue  # Skip enemies that have already been killed
            if not player.hit:
                player.hit = True  # Set hit flag to True
                reduction_amount = int(player.max_health * 0.2)
                player.health -= reduction_amount  # Decrease player health by 20%
                player.health = max(0, player.health)  # Ensure health doesn't go below 0
                enemy.kill()  # Remove the enemy when it makes the first contact
                enemy.drop_health_refill()  # Drop health refill when enemy is killed

        if not pygame.sprite.spritecollide(player, enemies, False):
            player.hit = False  # Reset hit flag when no longer in contact with enemies

        if player.health <= 0:
            player.lives -= 1

            if player.lives <= 0:
                game_over_screen()
                break

            player.health = max(0, player.health)  # Ensure health doesn't go below 0

        # Blit the background image onto the screen
        screen.blit(background_image, background_rect)

        # Draw the health bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, player.max_health * 2, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, player.health * 2, 20))

        # Draw the number of lives
        lives_text = font.render(f"Lives: {max(0, player.lives)}", True, (255, 255, 255))
        screen.blit(lives_text, (WIDTH - 150, 10))

        # Draw the score
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 150, 40))

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
