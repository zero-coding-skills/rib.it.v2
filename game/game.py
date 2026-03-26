import pygame

# TODO:
#   move everything when player reaches the camera box edge
#   map grid
#   gravity
#   player controls
#   more menu options
#   music and sfx
#   graphics

pygame.init()

scale = 2  # scales the size of everything

max_x, max_y = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((max_x, max_y), pygame.FULLSCREEN)

clock = pygame.time.Clock()
default_font = pygame.font.Font("assets/jersey10.ttf", 100 * scale)

running = True
show_menu = False
frame_rate = 60
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
        self.gravity = gravity

    @property
    def position(self):
        return self.world_x, self.world_y

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, pos):
        self.rect.x = max(min(pos, 0.6 * max_x - self.rect.width), 0.4 * max_x)

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, pos):
        self.rect.y = max(min(pos, 0.6 * max_y - self.rect.height), 0.4 * max_y)


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
frog = Player(0, 0, 1)
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

    screen.fill("#242424")

    if not render_menu():

        main_group.draw(screen)

    pygame.display.flip()
    dt = clock.tick(frame_rate) / 1000

pygame.quit()


