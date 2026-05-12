import math
import os
import random
from collections.abc import Callable
import pygame

pygame.init()

scale = 1  # scales the size of everything
fullscreen = False
max_x, max_y = 500, 800


if fullscreen:
    max_x, max_y = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((max_x, max_y), pygame.FULLSCREEN)
else:
    x, y = max_x // 32, max_y // 32
    if x // 2 < x / 2:
        x -= 1
    max_x, max_y = x * 32, y * 32
    screen = pygame.display.set_mode((max_x, max_y))


file_location = "game/"
clock = pygame.time.Clock()
dt = 0
default_font = pygame.font.Font(f"{file_location}assets/jersey10.ttf", 100 * scale)
if os.path.exists(f"{file_location}assets/level.demo"):
    os.remove(f"{file_location}assets/level.demo")

running = True
show_menu = False
frame_rate = 60

arrow_right = f"{file_location}assets/arrow-right.png"
arrow_left = f"{file_location}assets/arrow-left.png"
player_img = f"{file_location}assets/frogo.png"
break_block_img = f'{file_location}assets/breakable1.png'
movable_block_img = f'{file_location}assets/movable-placeholder.png'
level = f"{file_location}assets/background-500x2000.png"
block_img_count = 3
print("The game's resolution is: " + str(max_x) + "x" + str(max_y))
block_gap = 64
general_x = 0
general_y = 0
map_height = 0
dragging = False


class Player(pygame.sprite.Sprite):
    """
    Player object used for creating the player, managing position and everything player-wise.
    """

    def __init__(self, x: int | float, y: int | float, charge_speed: int | float):
        """
        Create new player object.
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
        self.pre_pos = (0, 0)
        self.jump_angle = 90
        self.is_falling = True
        self.arrow = pygame.image.load(arrow_right)
        self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)

    def charge(self):
        """
        Updates the force used to calculate jump height when holding space.
        When released, set velocity of player to jump strength * force.
        """
        self.pre_pos = (self.rect.x, self.rect.y)
        if self.charging:
            self.force = min(10, self.force + self.charge_speed * dt)
        else:
            if self.force != 0:
                self.velocity = self.jump_strength * self.force
                print(f"final force is: {self.force}")
            self.force = 0

    def move(self):
        """
        Calculate the vertical and horizontal speed.
        Calculate gravity and air resistance.
        Move the player by speed in both axis.
        """
        self.speed_y += self.velocity * math.sin(math.radians(self.angle))
        self.speed_x += self.velocity * math.cos(math.radians(self.angle))
        self.velocity = 0
        if self.is_falling:
            self.speed_y += -self.gravity * dt

        self.y -= self.speed_y * scale * dt
        self.x += self.speed_x * scale * dt
        self.collision()

        if self.speed_x > 0:
            if self.speed_x < self.drag * dt or not self.is_falling:
                self.speed_x = 0
            else:
                self.speed_x -= (
                    self.drag
                    * dt
                    * math.fabs(math.cos(math.radians(self.angle))) ** 1.5
                )
        elif self.speed_x < 0:
            if -self.speed_x < self.drag * dt or not self.is_falling:
                self.speed_x = 0
            else:
                self.speed_x += (
                    self.drag
                    * dt
                    * math.fabs(math.cos(math.radians(self.angle))) ** 1.5
                )

    def rotate_arrow(
        self, pivot: tuple[int, int]
    ) -> tuple[pygame.Surface, pygame.Rect]:
        """
        Rotates the arrow to the direction of jumping.
        :param pivot: the point around which the arrow is rotated
        :return: image and its position
        """
        image = pygame.Surface(
            (self.arrow.get_width(), self.arrow.get_height() * 2), pygame.SRCALPHA
        )
        image.blit(self.arrow, (0, 0))
        image = pygame.transform.rotozoom(image, self.angle - 90, 1)
        rect = image.get_rect()
        if self.angle > 90:
            self.arrow = pygame.image.load(arrow_left)
            self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)
        else:
            self.arrow = pygame.image.load(arrow_right)
            self.arrow = pygame.transform.scale_by(self.arrow, scale / 2)
        rect.center = pivot
        return image, rect

    def collision(self):
        """
        Checks player collision with other blocks.
        Sets player 'is_falling' if there is a block under it.
        """
        col_rect = pygame.Rect(
            (self.rect.x, self.rect.y), (self.rect.width, self.rect.height + 1)
        )
        for block in blocks.sprites():
            if col_rect.colliderect(block):
                if self.pre_pos[1] + self.rect.height <= block.rect.y:
                    self.y = block.rect.y - self.rect.height
                    self.is_falling = False
                    return
                if self.pre_pos[0] + self.rect.width <= block.rect.x:
                    self.x = block.rect.x - self.rect.width
                    self.speed_x = 0
                if self.pre_pos[0] >= block.rect.x + block.rect.width:
                    self.x = block.rect.x + block.rect.width
                    self.speed_x = 0
                if self.pre_pos[1] >= block.rect.y + block.rect.height:
                    self.y = block.rect.y + block.rect.height
                    self.speed_y *= 0.2
        if self.y == max_y - self.rect.height:
            self.is_falling = False
        else:
            self.is_falling = True

    def update(self):
        """
        Call all other object functions to update its state.
        """
        if not self.is_falling:
            self.speed_y = 0
            blit_arrow, arrow_rect = self.rotate_arrow(
                (int(self.x + self.rect.width * 0.5), self.y - scale * 5)
            )
            screen.blit(blit_arrow, arrow_rect)
        if not dragging:
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
    Class used for handling GUI elements such as text and buttons.
    """

    def __init__(
        self,
        text: str,
        x: int | float,
        y: int | float,
        ui_type: str,
        *,
        has_border: bool = False,
        font: pygame.font.Font = default_font,
        on_click: Callable | None = None,
        segments: int = 0,
    ):
        """
        Create new UI element.
        :param text: text to display
        :param ui_type: what type of UI the Object is (text, button, slider)
        :param x: x position on screen
        :param y: y position on screen
        :param has_border: whether to render a border
        :param font: which font to use for text
        :param on_click: function to execute when clicked
        :param segments: number of slider values (set 0 for infinite)
        """
        pygame.sprite.Sprite.__init__(self)

        self.mouse_hover = None
        self.font = font
        self.text = text
        self.color = "#92ad8d"
        self.bg = "#242424"
        self.has_border = has_border
        self.x, self.y = x, y
        self.image = self.font.render(self.text, True, self.color, self.bg)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.on_click = on_click
        self.element = ui_type
        self.segments = segments
        self.value = 0
        self.bar = None

    def update_button(self):
        """
        Update the button element based on current parameters.
        Can change color, size and text.
        """
        if self.mouse_hover:
            self.color = "#60735d"
        else:
            self.color = "#92ad8d"
        self.image = self.font.render(self.text, True, self.color, self.bg)
        if self.has_border:
            pygame.draw.rect(self.image, self.color, self.image.get_rect(), 4)
        if self.mouse_hover:
            self.image = pygame.transform.scale_by(self.image, 0.95)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, mouse_pos, mouse_click):
        """
        Change UI parameters if hovered or clicked.
        Call onclick function if clicked.
        :param mouse_pos: current mouse position
        :param mouse_click: state of mouse button 0 (left click)
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_hover = True
            if mouse_click and self.on_click is not None:
                self.on_click()
        else:
            self.mouse_hover = False
        if self.has_border:
            pygame.draw.rect(self.image, self.color, self.image.get_rect(), 4)
        if self.element == "slider":
            self.update_slider(mouse_click, mouse_pos)
        elif self.element == "button":
            self.update_button()

    def update_slider(self, mouse_click, mouse_pos):
        if self.mouse_hover and mouse_click:
            self.value = (mouse_pos[0] - self.x) / self.rect.width
        pygame.draw.rect(
            self.image,
            self.color,
            (
                self.x + self.rect.width * self.value,
                self.y,
                self.x + self.rect.width * self.value + 20 * scale,
                self.y + self.rect.height,
            ),
        )


c_line = 0
last_pos = None
chars = max_x // (32 * scale)
blocks = pygame.sprite.Group()
flying = pygame.sprite.Group()
breakables = pygame.sprite.Group()
f = False

def drag_frog():
    if dragging:
        frog.x = pygame.mouse.get_pos()[0] - frog.rect.width / 2
        frog.y = pygame.mouse.get_pos()[1] - frog.rect.height / 2


def generate():
    global c_line
    global last_pos
    global f

    lines = level_1.rect.height // ((32 + block_gap) * scale)
    fb = 0
    line = []
    pos = random.randint(1, (chars // 2))

    line.append("--" * (pos - 1))
    chosen = random.randint(1, 3)
    if chosen == 1:
        line.append("nn")
    elif chosen == 2:
        line.append("bb")
    elif chosen == 3:
        num = 1
        line = []
        if chars / 2 > chars // 2:
            num = 0
        line.append("-" * (chars // 2 - num) + "f" + "-" *(chars // 2))
        fb = 1
    else:
        line.append("--")

    if fb != 1:
        line.append((chars // 2 - pos) * "--")

    if pos != last_pos:
        if f and chosen == 3:
            pass
        else:
            with open(f'{file_location}assets/level.demo', "a") as f:
                f.write("".join(line) + "\n")
            c_line += 1
            last_pos = pos
        if chosen == 3:
            f = True
        else:
            f = False

    if c_line < lines:
        generate()
    else:
        c_line = 0
        render()

def render():
    char = 0
    def_block_height = 32
    line = 0
    b = 0
    bimg = 0

    with open(f'{file_location}assets/level.demo', "r") as f:
        while True:
            read_char = f.read(1)
            if not read_char:
                break
            if char + 1 > chars:
                b = 0
                char = 0
                line += 1
            if read_char != "\n":
                if read_char != "-":
                    obj = pygame.sprite.Sprite()
                    if b < 1:
                        bimg = random.randint(0, block_img_count - 1)
                    obj.image = pygame.image.load(f'{file_location}assets/block{bimg}.png')
                    obj.image = pygame.transform.scale_by(obj.image, scale)
                    obj.rect = obj.image.get_rect()
                    height_diff = def_block_height - obj.rect.height
                    obj.rect.x = char * obj.rect.width
                    obj.rect.y = (-2000 + max_y) + line * (obj.rect.height + height_diff + block_gap) * scale
                    if read_char == "n":
                        obj.breakable = False
                        obj.moving = False
                    elif read_char == "f":
                        obj.breakable = False
                        obj.moving = True
                    elif read_char == "b":
                        obj.breakable = True
                        obj.moving = False
                    block = obj
                    blocks.add(block)
                    if obj.moving:
                        flying.add(block)
                    b += 1
                char += 1


def camera_move():
    global general_y
    global map_height
    add_y = 0
    if frog.y < 0.4 * max_y:
        add_y = 0.4 * max_y - frog.y
        for sprite in blocks:
            sprite.rect.y += add_y
        for sprite in levels:
            sprite.rect.y += add_y
        map_height += add_y
        frog.y = 0.4 * max_y
    if frog.y > 0.7 * max_y and map_height > 0:
        add_y = 0.7 * max_y - frog.y
        for sprite in blocks:
            sprite.rect.y += add_y
        for sprite in levels:
            sprite.rect.y += add_y
        map_height += add_y
        frog.y = 0.7 * max_y
    general_y += add_y

last_y = 0
high_score = 0

def cords():
    global last_y
    global general_x
    global general_y
    global high_score

    if frog.y > 0.4 * max_y:
        add_y = last_y - frog.y
        general_y = general_y + add_y

    last_y = frog.y
    if general_y < 0:
        general_y = 0
    if general_y > high_score:
        high_score = general_y

    camera_move()

direction = 1
changed = 0

def move_flying():
    global direction
    global changed

    col_rect = pygame.Rect(
        (frog.rect.x, frog.rect.y), (frog.rect.width, frog.rect.height + 1)
    )
    for sprite in flying:
        if sprite.rect.x >= max_x - 32 * scale and changed == 0 or sprite.rect.x <= 0 and changed == 1:
            direction = -1 * direction
            if changed == 0:
                changed = 1
            else:
                changed = 0
        if col_rect.colliderect(sprite) and not frog.is_falling:
            frog.x += direction * 2
        sprite.rect.x += direction * 2




def render_menu() -> bool:
    """
    Draw UI items to screen if game is paused.
    :return: True if menu has been rendered, False if not
    """
    if show_menu:
        ui.draw(screen)
        for item in ui:
            item.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
        return True
    return False


def quit_game():
    """
    Sets running to False, ending the game.
    """
    global running
    running = False


frog = Player(max_x // 2, max_y - 60, 8)
main_group = pygame.sprite.Group(frog)
main_text = UserInterface(" RIB.IT ", max_x / 2, max_y * 0.4, "text")
quit_button = UserInterface(
    " QUIT ", max_x / 2, max_y * 0.7, "button", has_border=True, on_click=quit_game
)
volume_slider = UserInterface(
    "Volume", max_x / 2, max_y * 0.2, "slider", has_border=True
)
ui = pygame.sprite.Group(quit_button, main_text, volume_slider)
level_1 = Map(level, 0, -2000 + max_y)
levels = pygame.sprite.Group(level_1)

generate()

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

    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        frog.charging = True
    else:
        frog.charging = False
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        frog.angle += 100 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        frog.angle -= 100 * dt

    if frog.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        dragging = True
    elif not pygame.mouse.get_pressed()[0]:
        dragging = False

    drag_frog()


    screen.fill("#242424")

    if not render_menu():
        cords()
        move_flying()
        levels.draw(screen)
        main_group.draw(screen)
        frog.update()
        blocks.draw(screen)

    pygame.display.flip()
    dt = clock.tick(frame_rate) / 1000

print("Your highest score this game was: " + str(int(high_score)))
pygame.quit()
