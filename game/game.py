import pygame
import math

# TODO:
#   move everything when player reaches the camera box edge
#   map grid
#   more menu options
#   music and sfx
#   graphics

pygame.init()

scale = 2  # scales the size of everything
fullscreen = False

if fullscreen:
    max_x, max_y = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((max_x, max_y), pygame.FULLSCREEN)
else:
    max_x, max_y = 1200, 800
    screen = pygame.display.set_mode((max_x, max_y))

clock = pygame.time.Clock()
dt = 0
default_font = pygame.font.Font("assets/jersey10.ttf", 100 * scale)

running = True
show_menu = False
frame_rate = 60

arrow_img = "assets/arrow.png"
player_img = "assets/placeholder.png"
print(max_x, max_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, gravity):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player_img)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.world_x, self.world_y = 0, 0
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.gravity = 10
        self.velocity = 0
        self.max_velocity = 400 * scale
        self.jump_strength = 100
        self.speed_y = 0
        self.speed_x = 0
        self.force = 0
        self.drag = 30
        self.charging = False
        self.jump_angle = 90
        self.is_falling = True
        self.arrow = pygame.image.load(arrow_img)
        self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)

    def charge(self):
        if self.charging:
            self.force = min(10, self.force + 5 * dt)
            print(f'charging force is: {self.force}')
        else:
            if self.force != 0:
                self.velocity = self.jump_strength * self.force
                print(f'final force is: {self.force}')
            self.force = 0


    def move(self):
        self.speed_y += self.velocity * math.sin(self.angle)
        self.speed_x += self.velocity * math.cos(self.angle)
        self.velocity = 0

        self.speed_y += - self.gravity
        # self.speed_x -= self.drag
        self.y -= self.speed_y * scale * dt
        self.x += self.speed_x


    def rotate_arrow(self, pivot):
        # rotate the leg image around the pivot
        image = pygame.Surface((self.arrow.get_width(), self.arrow.get_height() * 2), pygame.SRCALPHA)
        image.blit(self.arrow, (0, 0))
        image = pygame.transform.rotozoom(image, self.angle - 90, 1)
        rect = image.get_rect()
        rect.center = pivot
        return image, rect

    def update(self):
        if not self.is_falling:  # if player is falling
            blit_arrow, arrow_rect = self.rotate_arrow([self.x + self.rect.width * scale * 0.25, self.y - scale * 5])
            screen.blit(blit_arrow, arrow_rect)
            self.speed_y = 0
        self.charge()
        self.move()

    @property
    def position(self):
        return self.world_x, self.world_y

    @property
    def angle(self):
        return self.jump_angle

    @angle.setter
    def angle(self, value):
        self.jump_angle = min(max(value, 0), 180)

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, pos):
        # self.rect.x = max(min(pos, 0.6 * max_x - self.rect.width), 0.4 * max_x)
        self.rect.x = max(min(pos,max_x - self.rect.width), 0)

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, pos):
        self.rect.y = max(min(pos, max_y - self.rect.height), 0)
        if self.y == max_y - self.rect.height:
            self.is_falling = False
        else:
            self.is_falling = True


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, img, breakable, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.breakable = breakable
        self.moving = moving


class Ground(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((max_x, 10))
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class UserInterface(pygame.sprite.Sprite):
    def __init__(self, text, on_click, x, y, has_border=False, font=default_font):
        pygame.sprite.Sprite.__init__(self)

        self.mouse_hover = None
        self.font = font
        self.text = text
        self.color = "#92ad8d"
        self.bg = "#242424"
        self.has_border = has_border
        self.x, self.y = x, y
        self.__update_text()
        self.on_click = on_click

    def __update_text(self):
        self.image = self.font.render(self.text, True, self.color, self.bg)
        if self.has_border:
            pygame.draw.rect(self.image, self.color, self.image.get_rect(), 4)
        if self.mouse_hover:
            self.image = pygame.transform.scale_by(self.image, 0.95)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and self.on_click is not None:
            self.mouse_hover = True
            # self.font.set_underline(True)
            self.color = "#60735d"
            if mouse_click:
                self.on_click()
        else:
            # self.font.set_underline(False)
            self.color = "#92ad8d"
            self.mouse_hover = False
        self.__update_text()


def render_menu():
        if show_menu:
            ui.draw(screen)
            for item in ui:
                item.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
            return True
        return False


def quit_game():
    global running
    running = False


ground = Ground(0, max_y)
frog = Player(0, 0, 1000)
main_group = pygame.sprite.Group(ground, frog)
main_text = UserInterface(" RIB.IT ", None, max_x / 2, max_y * 0.4)
quit_button = UserInterface(" QUIT ", quit_game, max_x / 2, max_y * 0.7, True)
ui = pygame.sprite.Group(quit_button, main_text)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if show_menu:
                    show_menu = False
                else:
                    show_menu = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        frog.charging = True
    else:
        frog.charging = False
    if keys[pygame.K_a]:
        frog.angle += 100 * dt
    if keys[pygame.K_d]:
        frog.angle -= 100 * dt

    screen.fill("#242424")

    if not render_menu():

        main_group.draw(screen)
        frog.update()

    pygame.display.flip()
    dt = clock.tick(frame_rate) / 1000

pygame.quit()


