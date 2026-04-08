import math
import random
import pygame

# TODO:
#   move everything when player reaches the camera box edge
#   map grid
#   more menu options
#   music and sfx
#   graphics
#   reset angle of arrow upon hitting the ground

pygame.init()

scale = 2  # scales the size of everything
fullscreen = False
file_location = "game/"

if fullscreen:
    max_x, max_y = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((max_x, max_y), pygame.FULLSCREEN)
else:
    max_x, max_y = 500, 800
    screen = pygame.display.set_mode((max_x, max_y))

clock = pygame.time.Clock()
dt = 0
default_font = pygame.font.Font(f'{file_location}assets/jersey10.ttf', 100 * scale)

running = True
show_menu = False
frame_rate = 60

arrow_right = f'{file_location}assets/arrow-right.png'
arrow_left = f'{file_location}assets/arrow-LEFT.png'
player_img = f'{file_location}assets/placeholder.png'
level = f'{file_location}assets/map-placeholder.png'
print(max_x, max_y)
general_x = 0
general_y = 0
on_ground = True


class Player(pygame.sprite.Sprite):
    """
    Player object used for creating the player, managing position and everything player-wise.
    """
    def __init__(self, x: int, y: int, charge_speed: float):
        """
        create new player object
        :param x: x position on screen
        :param y: y position on screen
        :param charge_speed: how long it takes to charge a full jump
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player_img)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.world_x, self.world_y = 0, 0
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.gravity = 1000
        self.velocity = 0
        self.jump_strength = 65
        self.speed_y = 0
        self.speed_x = 0
        self.force = 0
        self.drag = 500
        self.charging = False
        self.charge_speed = charge_speed
        self.jump_angle = 90
        self.is_falling = True
        self.arrow = pygame.image.load(arrow_img)
        self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)

    def charge(self):
        """
        Updates the force used to calculate jump height when holding space
        When released, set velocity of player to jump strength * force
        """
        if self.charging:
            self.force = min(10, self.force + self.charge_speed * dt)
        else:
            if self.force != 0:
                self.velocity = self.jump_strength * self.force
                print(f"final force is: {self.force}")
            self.force = 0

    def move(self):
        """
        Calculate the vertical and horizontal speed
        Calculate gravity and air resistance
        Move the player by speed in both axis
        """
        self.speed_y += self.velocity * math.sin(math.radians(self.angle))
        self.speed_x += self.velocity * math.cos(math.radians(self.angle))
        self.velocity = 0
        if self.is_falling:
            self.speed_y += -self.gravity * dt

        self.y -= self.speed_y * scale * dt
        self.x += self.speed_x * scale * dt

        if self.speed_x > 0:
            if self.speed_x < self.drag * dt or not self.is_falling:
                self.speed_x = 0
            else:
                self.speed_x -= (self.drag * dt * math.fabs(math.cos(math.radians(self.angle))) ** 1.5)
        elif self.speed_x < 0:
            if -self.speed_x < self.drag * dt or not self.is_falling:
                self.speed_x = 0
            else:
                self.speed_x += (self.drag * dt * math.fabs(math.cos(math.radians(self.angle))) ** 1.5)

    def rotate_arrow(self, pivot: list):
        """
        :param pivot: the point around which the arrow is rotated
        Rotates the arrow to the direction of jumping
        """
        image = pygame.Surface((self.arrow.get_width(), self.arrow.get_height() * 2), pygame.SRCALPHA)
        image.blit(self.arrow, (0, 0))
        image = pygame.transform.rotozoom(image, self.angle - 90, 1)
        rect = image.get_rect()
        if self.angle > 90:
            self.arrow = pygame.image.load(arrow_left)
            self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)
        else:
            self.arrow = pygame.image.load(arrow_img)
            self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)
        rect.center = pivot
        return image, rect

    def update(self):
        """
        Call all other object functions to update its state
        """
        if not self.is_falling:
            self.speed_y = 0
        if last_y == frog.y:
            blit_arrow, arrow_rect = self.rotate_arrow([self.x + self.rect.width * 0.5, self.y - scale * 5])
            screen.blit(blit_arrow, arrow_rect)
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
        if not self.is_falling:
            self.jump_angle = min(max(value, 0), 180)

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, pos):
        self.rect.x = max(min(pos, max_x - self.rect.width), 0)

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, pos):
        self.rect.y = max(min(pos, max_y - self.rect.height), 0)
        # determine if player is falling
        if self.rect.colliderect(block_1):
            self.rect.y = block_1.rect.y - self.rect.height
            self.is_falling = False
        elif self.rect.colliderect(block_2):
            self.rect.y = block_2.rect.y - self.rect.height
            self.is_falling = False
        elif self.y == max_y - self.rect.height:
            self.is_falling = False
        else:
            self.is_falling = True


class Block(pygame.sprite.Sprite):
    """
    Class for blocks making up the map
    """
    def __init__(self, x, y, img, breakable, moving):
        """
        create new block
        :param x: x position on screen
        :param y: y position on screen
        :param img: image to be rendered
        :param breakable: if this block can break or be broken
        :param moving: if block can move around
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.breakable = breakable
        self.moving = moving


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((max_x, 10))
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Map(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class UserInterface(pygame.sprite.Sprite):
    """
    Class used for handling GUI elements such as text and buttons
    """
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


def generate_blocks(value):
    block_x = random.randint(0, max_x)
    half_y = math.ceil(0.6 * max_y)
    block_y = random.randint(half_y, max_y)
    if value == "x":
        return block_x
    else:
        return block_y


def camera_move(x, y):
    if y > 0.6 * max_y:
        pass # change the map and the block position by the difference in general_y - 0.6 * max_y (i think... i just want to commit)
    if y < 0.3 * max_y: #and if the map position is higher than -2000 - max_y
        pass

last_y = 0

def cords():
    global last_y
    global general_x
    global general_y


    add_y = last_y - frog.y

    general_y = general_y + add_y

    last_y = frog.y
    if general_y < 0:
        general_y = 0

    camera_move(general_x, general_y)


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


block_1 = Block(generate_blocks("x"), generate_blocks("y"), player_img, False, False)
block_2 = Block(generate_blocks("x"), generate_blocks("y"), player_img, False, False)
block_group = pygame.sprite.Group(block_1, block_2)
ground = Ground(0, max_y)
frog = Player(0, max_y - 60, 8)
main_group = pygame.sprite.Group(frog)
main_text = UserInterface(" RIB.IT ", None, max_x / 2, max_y * 0.4)
quit_button = UserInterface(" QUIT ", quit_game, max_x / 2, max_y * 0.7, True)
ui = pygame.sprite.Group(quit_button, main_text)
level_1 = Map(f'{file_location}assets/map-placeholder.png', 0, -2000 - max_y)
levels = pygame.sprite.Group(level_1)

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
        cords()
        levels.draw(screen)
        main_group.draw(screen)
        frog.update()
        block_group.draw(screen)

    pygame.display.flip()
    dt = clock.tick(frame_rate) / 1000

pygame.quit()
