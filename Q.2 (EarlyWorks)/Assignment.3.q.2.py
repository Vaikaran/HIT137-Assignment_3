
import pygame
pygame.init()

window_surface = pygame.display.set_mode((1920, 1080), vsync=1)
pygame.display.set_caption("Platformer Side-Scrolling Game")

char = pygame.image.load(' .png')
bg = pygame.image.load(' .jpg')
strollLHS = [pygame.image.load(' .png'), pygame.image.load(' .png')]
strollRHS = [pygame.image.load(' .png'), pygame.image.load(' .png')]
clock = pygame.time.Clock()

class Player1(object):
    def __init__(self,horizontal_axis, vertical_axis, stature, breadth):
        self.horizontal_axis = horizontal_axis
        self.vertical_axis = vertical_axis
        self.stature = stature
        self.breadth = breadth
        self.vel = 10
        self.isLeap = False
        self.leapCount = 20
        self.RHS=False
        self.LHS=False
        self.strollCount=0
        self.leapCount=20
        self.pose=True
        self.shotbox= (self.horizontal_axis +40, self.vertical_axis,56,120)
        
        def draw(self, victory):
            if strollCount + 2 >= 54:
                self.strollCount = 0
            if not(self.pose):
                if self.LHS:
                    victory.blit(strollLHS[self.strollCount//3])
                self.strollCount += 1
            elif self.RHS:
                victory.blit(strollRHS[self.strollCount//3],(self.horizontal_axis,self.vertical_axis))
                self.strollCount += 1
            else:
                if self.RHS:
                    victory.blit(strollRHS[0],(self.horizontal_axis,self.vertical_axis))
                else:
                    victory.blit(strollLHS[0], (self.horizontal_axis, self.vertical_axis))
                    self.shootbox = (self.horizontal_axis + 20, self.vertical_axis, 56, 120)
                    pygame.draw.rect(victory, (255,0,0), self.shootbox,2)
        
class projectile(object):
    def __init__(self, x , y, color, facing, radius):
        self.radius=radius
        self.facing = facing
        self.x =x
        self.y=y
        self.color=color
        self.vel=8 * facing
        
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        
class enemy(object):
    strollRHS = [pygame.image.load(' .png'), pygame.image.load(' .png')]
    strollLHS = [pygame.image.load(' .png'), pygame.image.load(' .png')]
    def __init__(self, vertical, horizontal, finish, height,breadth):
        self.vertical=vertical
        self.horizontal=horizontal
        self.breadth=breadth
        self.height=height
        self.finish=finish
        self.path=[self.horizontal,self.finish]
        self.strollCount=0
        self.vel=6
        self.shootbox= (self.horizontal + 40, self.vertical, 56, 120)
        pygame.draw.rect(victory,(255,0,0), self.shootbox, 2)
        
    def draw(self,win):
        self.move()
        if self.strollCount + 1 >= 33:
            self.strollCount = 0
        if vel > 0:
            victory.blit(self.strollRHS[self.strollCount//3], (self.horizontal,self.vertical))
            self.strollCount += 1
        else:
            victory.blit(self.strollLHS[self.strollCount //3],(self.horizontal,self.vertical))
            self.strollCount += 1
            
    def move(self):
        if self.vel > 0:
            if self.horizontal + self.vel < self.path[1]:
                self.horizontal += self.vel
            else:
                self.vel = self.vel * -1
                self.strollCount = 0
        else:
            if self.horizontal - self.vel > self.path[0]:
                self.horizontal += self.vel
            else:
                self.vel = self.vel * -1
                self.strollCount = 0
    def shot(self):
        print('shot')
        pass
    
    x = 50
    y = 400
    height = 50
    width = 50
    vel = 5
    isLeap = False
    leapCount = 10
    LHS = False
    RHS = False
    strollCount = 0
    
    def redrawGameWindow():
        victory.blit(bg,(0,0))
        guy.draw(victory)
        for bullet in bullets:
            bullet.draw(victory)
            
        pygame.display.update()
        
    guy = player1(300,410,50,64)
    bandit = enemy(100,410,50,450)
    shotLoop=[]
    bullets=[]
    run=True
    while run:
        clock.tick(27)
        
        if shotLoop>0:
            shotLoop +=1
        if shotLoop>3:
            shotLoop=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                
    for bullet in bullets:
        if bullet.y - bullet.radius <bandit.hitbox[1]+bandit.shotbox[3] and bullet.y + bullet.radius >bandit.hitbox[1]:
            if bullet.x + bullet.radius > bandit.shootbox[0] and bullet.x - bullet.radius<bandit.shootbox[0] + bandit.shootbox[2]:
                bandit.hit()
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if guy.LHS:
            facing = -1
    else:
        facing = 1
    if len(bullets) < 5:
        bullets.append(projectile(round(guy.x + guy.width //2),round(guy.y + guy.height//2),6,(0,0,0),facing))
    shootLoop=1
    if keys[pygame.K_LEFT] and guy.x > guy.vel:
        guy.x -= vel
        guy.left = True
        guy.right = False
        guy.standing = False
    elif keys[pygame.K_RIGHT] and guy.x < 500 - guy.width - guy.vel:
        guy.x +=guy.vel
        guy.right = True
        guy.left = False
        guy.standing = False
    else:
        guy.standing = False
        guy.walkCount = 0
        
    if not(guy.isLeap):
        if keys[pygame.K_UP]:
            guy.isLeap = True
            guy.right = False
            guy.left = False
            guy.walkCount = 0
    else:
        if guy.leapCount >= -20:
            neg = 1
            if guy.leapCount < 0:
                guy.y -= (leapCount **2) * 0.5 * neg
            guy.leapCount -= 1
        else:
            guy.isLeap = False
            guy.leapCount = 20
            
    redrawGameWindow
    
pygame.quit()
            