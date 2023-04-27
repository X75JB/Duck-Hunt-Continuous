import pygame
import pygame.time
import math
import random


class ClickableSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, action):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


image_list = ["images/duck/black/duckfly1_blk.png", "images/duck/black/duckfly2_blk.png",
              "images/duck/black/duckfly3_blk.png"]


class Sprite:
    def __init__(self):
        self.x = random.randint(100, 400)  # random starting x position
        self.y = 225  # starting y position at the bottom of the screen
        self.angle = random.randint(225, 315)  # generate random angle
        self.velocity = math.cos(math.radians(self.angle))  # velocity in the x direction
        self.velocity_y = math.sin(math.radians(self.angle))  # velocity in the y direction
        self.image_counter = 0
        self.image = pygame.image.load(image_list[self.image_counter])
        self.width, self.height = self.image.get_size()
        self.last_update_time = pygame.time.get_ticks()
        self.animation_delay = 100

    def update(self):
        global score, health
        self.x += self.velocity * (score / 25 + 1)
        self.y += self.velocity_y * (score / 25 + 1)
        if (self.x < 0 or self.x > width) or (self.y < 0 or self.y > height):
            self.destroy()
            health -= 1
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= self.animation_delay:
            self.image_counter += 1
            if self.image_counter >= len(image_list):
                self.image_counter = 0
            self.image = pygame.image.load(image_list[self.image_counter])
            self.last_update_time = current_time

    def destroy(self):
        global my_sprite
        my_sprite = Sprite()

    def draw(self):
        current_image = pygame.image.load(image_list[self.image_counter])
        if self.velocity < 0:
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(current_image, (int(self.x), int(self.y)))


# Create screen
pygame.init()
width = 500
height = 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Duck Hunt Continuous")
background_image = pygame.image.load("images/background/start.jpg")
screen.blit(background_image, (0, 0))
cursor_image = pygame.image.load("images/crosshair_5050.png")

# Create game states
## This is the highscore menu
MENU = 0
## This is the actual game
PLAY = 1
## This is the starting screen menu
START = 2

# Start game
game_state = START


def startGame():
    global game_state
    game_state = PLAY


first_button = ClickableSprite('images/button/unlimited_play.jpg', 85, 200, startGame)

# Read file in order to display highscores on the front page.
with open("highscores.txt", "r") as f:
    # Read the first line of the file
    first_line = f.readline()
f.close()

# Create a font object for the opening screen highscore
highscore1_font = pygame.font.Font(None, 30)
highscore1_text = highscore1_font.render("Highscore: " + str(first_line), True, (255, 0, 0))
screen.blit(highscore1_text, (200, 200))
pygame.display.update()

# Create a button group, this helps with "killing" and "spawning the buttons"
button_group = pygame.sprite.Group()
button_group.add(first_button)

# define some variables
pygame.mixer.init()
pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("sounds/shot.wav")
clock = pygame.time.Clock()
my_sprite = Sprite()
score = 0
health = 3
score_font = pygame.font.Font(None, 30)
health_font = pygame.font.Font(None, 30)

# Actual Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in button_group:
            button.handle_event(event)
        # If button clicked, if button has landed on the sprites location, destroy sprite
        if event.type == pygame.MOUSEBUTTONDOWN:
            if my_sprite:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (mouse_x > my_sprite.x and mouse_x < my_sprite.x + my_sprite.width) and (
                        mouse_y > my_sprite.y and mouse_y < my_sprite.y + my_sprite.height):
                    # Sprite hit, destroy, add score.
                    if my_sprite:
                        shoot_sound.play()
                        my_sprite.update()
                        my_sprite.draw()
                        score += 1
                        my_sprite = Sprite()
                    pygame.display.update()

    # Change game state, this is where you would put your highscore in
    if game_state == MENU:
        pygame.mouse.set_visible(True)
        background_image = pygame.image.load("images/background/start.jpg")
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 32)

        # Create text box and name variable
        text_box = pygame.Surface((200, 32))
        text_box_x = 250
        text_box_y = 240
        name = ""

        # Load the highscores from the file
        highscores = []
        try:
            with open("highscores.txt", "r") as f:
                highscores = f.read().splitlines()
        except:
            pass

        # Save button
        save_button = pygame.Surface((80, 32))
        save_button_x = 410
        save_button_y = 240
        save_button.fill((255, 0, 0))
        save_button_text = font.render("Save", True, (255, 255, 255))
        save_button.blit(save_button_text,
                         (40 - save_button_text.get_width() // 2, 16 - save_button_text.get_height() // 2))

        # Loop for saving highscore
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check for user input
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalnum() or event.unicode == " ":
                        name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]

                # if save button is pressed:
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if save_button_x - 40 <= mouse_x <= save_button_x + 40 and save_button_y - 16 <= mouse_y <= save_button_y + 16:
                        highscores.append(name + " - " + str(score))

                        # Sort the highscores in descending order while spliting
                        highscores.sort(key=lambda x: int(x.split(" - ")[1]), reverse=True)

                        # Keep only the top 5 highscores
                        highscores = highscores[:5]

                        # Save the highscores to the file
                        with open("highscores.txt", "w") as f:
                            for highscore in highscores:
                                f.write(highscore + '\n')
                        pygame.quit()

            # Render all assets
            text_box.fill((255, 255, 255))
            text = font.render(name, True, (0, 0, 0))
            text_box.blit(text, (100 - text.get_width() // 2, 16 - text.get_height() // 2))
            screen.blit(text_box, (text_box_x - text_box.get_width() // 2, text_box_y - text_box.get_height() // 2))
            screen.blit(save_button,
                        (save_button_x - save_button.get_width() // 2, save_button_y - save_button.get_height() // 2))
            score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (40, 230))

            # Update the display
            pygame.display.update()

    elif game_state == START:
        # create background
        background_image = pygame.image.load("images/background/start.jpg")
        screen.blit(background_image, (0, 0))
        first_button.handle_event(event)
        screen.blit(highscore1_text, (225, 215))
        button_group.draw(screen)
        pygame.display.update()

    elif game_state == PLAY:
        # Hide mouse and find where it is
        pygame.mouse.set_visible(False)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_1 = mouse_x - 25
        mouse_y_1 = mouse_y - 25

        # Change background
        background_image = pygame.image.load("images/background/ingame.png")
        screen.blit(background_image, (0, 0))

        # Update and draw all sprites
        button_group.empty()
        if not my_sprite:
            my_sprite = Sprite()
        elif health == 0:
            game_state = MENU
        else:
            my_sprite.update()
            my_sprite.draw()

        # Cursor image so that it appears over everything
        screen.blit(cursor_image, (mouse_x_1, mouse_y_1))

        # Display the score and health text
        score_text = score_font.render("Score: " + str(score), True, (1, 1, 1))
        screen.blit(score_text, (10, 10))
        health_text = health_font.render("Health: " + str(health), True, (1, 1, 1))
        screen.blit(health_text, (400, 10))
        pygame.display.update()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
