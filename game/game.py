import pygame

pygame.init()

scale = 2  # scales the size of everything

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font("assets/jersey10.ttf", 100 * scale)

running = True
show_menu = False
frame_rate = 60
player_img = "assets/placeholder.png"
max_x, max_y = pygame.display.get_surface().get_size()
print(max_x, max_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player_img)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
    def __init__(self, text, on_click, x, y, has_border=False):
        pygame.sprite.Sprite.__init__(self)
        self.color = "#92ad8d"
        self.bg = "#242424"
        self.image = font.render(text, True, self.color, self.bg)
        if has_border:
            pygame.draw.rect(self.image, self.color, self.image.get_rect(), 4)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.on_click = on_click

    def update(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            if mouse_click and self.on_click is not None:
                self.on_click()



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


ground = Ground(0, max_y - 10)
frog = Player(max_x / 2 , max_y / 2)
main_group = pygame.sprite.Group(ground, frog)
main_text = UserInterface(" RIB.IT ", None, max_x / 2, max_y * 0.4)
quit_button = UserInterface(" QUIT ", quit_game, max_x / 2, max_y * 0.7, True)
ui = pygame.sprite.Group(quit_button, main_text)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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


