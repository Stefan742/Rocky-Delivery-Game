import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocky Delivery")

# Load images
menu_image = pygame.image.load("menu/menu.jpg")  # Menu image (background)
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))
player = pygame.image.load("assets/truck.png")  # Truck image
package_image = pygame.image.load("assets/package.png")  # Package image
yellow_car_image = pygame.image.load("assets/yellow.png")  # Yellow car image
white_car_image = pygame.image.load("assets/white.png")  # White car image

# Scale the truck image based on screen width
player_width = 70
player_height = int(player.get_height() * (player_width / player.get_width()))
player = pygame.transform.scale(player, (player_width, player_height))

# Scale the package image (make sure it's a suitable size for the game)
package_width = 100
package_height = int(package_image.get_height() * (package_width / package_image.get_width()))
package_image = pygame.transform.scale(package_image, (package_width, package_height))

# Scale the car images
car_width = 50
# Scaling the yellow car image
yellow_car_width = 50
yellow_car_height = int(800 * (yellow_car_width / 372))  # Keeping the aspect ratio

yellow_car_image = pygame.transform.scale(yellow_car_image, (yellow_car_width, yellow_car_height))

# Scaling the white car image
white_car_width = 80
white_car_height = 80  # Keeping the aspect ratio

white_car_image = pygame.transform.scale(white_car_image, (white_car_width, white_car_height))

car_height = int(yellow_car_image.get_height() * (car_width / yellow_car_image.get_width()))
yellow_car_image = pygame.transform.scale(yellow_car_image, (car_width, car_height))
white_car_image = pygame.transform.scale(white_car_image, (white_car_width, white_car_height))

collect_sound = pygame.mixer.Sound("audio/collect.mp3")
crash_sound = pygame.mixer.Sound("audio/crash.mp3")
song = pygame.mixer.Sound("audio/song.mp3")
engine = pygame.mixer.Sound("audio/engine.mp3")
beep = pygame.mixer.Sound("audio/beep.mp3")

# Load the road image
road = pygame.image.load("assets/road.jpg")

# Resize the road image to fit the screen (600x800)
road = pygame.transform.scale(road, (WIDTH, HEIGHT))

# Create two copies of the road for scrolling effect
road1_y = 0
road2_y = -HEIGHT  # The second road image starts just above the first one

# Road width and horizontal constraints for the truck
road_width = 400
road_left = (WIDTH - road_width) // 2  # The left bound of the road
road_right = road_left + road_width  # The right bound of the road

# Define the four lanes
lane_width = road_width // 4
lanes = [road_left + i * lane_width for i in range(4)]  # x positions for the 4 lanes

# Player's starting position
player_x = WIDTH // 2 - player.get_width() // 2
player_y = HEIGHT - player.get_height() - 10

# Movement speed
speed = 5

# Score
score = 0
high_score = 0

# Load the high score from a file if it exists
if os.path.exists("assets/high_score.txt"):
    with open("assets/high_score.txt", "r") as file:
        high_score = int(file.read())

# Game loop flag
running = True
game_started = False

# Define the start button area (position and size)
button_x = WIDTH // 2 - 100  # Centered button
button_y = HEIGHT - 150  # Slightly towards the bottom
button_width = 200
button_height = 50
corner_radius = 25  # Radius for rounded corners

# Font for text on the button and score
font = pygame.font.Font(None, 36)
button_text = font.render("Start Game", True, (255, 255, 255))
high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))

# Function to draw a button with rounded corners
def draw_rounded_button(surface, color, x, y, width, height, radius, text):
    # Draw rounded rectangle
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=radius)
    # Draw the text on the button
    surface.blit(text, (x + (width - text.get_width()) // 2, y + (height - text.get_height()) // 2))

# Class to represent a package
class Package(pygame.sprite.Sprite):
    def __init__(self, lane, y_position):
        super().__init__()
        self.image = package_image
        self.rect = self.image.get_rect()
        self.rect.x = lane
        self.rect.y = y_position

    def update(self, speed):
        # Move the package down the road
        self.rect.y += speed
        if self.rect.y > HEIGHT:
            self.kill()  # Remove the package when it goes off the screen

# Class to represent a car
class Car(pygame.sprite.Sprite):
    def __init__(self, lane, y_position, color):
        super().__init__()
        self.color = color
        if self.color == "yellow":
            self.image = yellow_car_image
        else:
            self.image = white_car_image
        self.rect = self.image.get_rect()
        self.rect.x = lane
        self.rect.y = y_position

    def update(self, speed):
        # Move the car down the road
        self.rect.y += speed
        if self.rect.y > HEIGHT:
            self.kill()  # Remove the car when it goes off the screen

# Game loop for the menu
while not game_started:
    # Event handling for menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_started = True  # Exit the game loop if window is closed
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                game_started = True  # Start the game if button is clicked
        if event.type == pygame.KEYDOWN:
            game_started = True  # Start the game if any key is pressed

    # Draw the menu background
    screen.blit(menu_image, (0, 0))

    # Draw the start button (with sky blue color and rounded corners)
    draw_rounded_button(screen, (135, 206, 235), button_x, button_y, button_width, button_height, corner_radius, button_text)

    # Draw the high score text below the start button
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, button_y + button_height + 20))

    # Update the display
    pygame.display.update()
    all_sprites = pygame.sprite.Group()
package_group = pygame.sprite.Group()
car_group = pygame.sprite.Group()
if not pygame.mixer.music.get_busy():
    pygame.mixer.music.load("audio/song.mp3")
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (range 0.0 to 1.0)
    pygame.mixer.music.play(-1, 0.0)  # Loop music indefinitely

# Game loop after the game starts
# Game loop after the game starts
while running:
    # Reset the game state after a crash and go back to the menu
    
    if not game_started:
        # Check if the current score is greater than the high score and update if needed
        if score > high_score:
            high_score = score
            # Save the new high score to the file
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
        
        # Reset the game state for a new session
        score = 0
        player_x = WIDTH // 2 - player.get_width() // 2
        player_y = HEIGHT - player.get_height() - 10
        # Clear sprite groups
        all_sprites.empty()
        package_group.empty()
        car_group.empty()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if the user clicks the button or presses any key to start the game
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                game_started = True  # Start the game when button is clicked

        if event.type == pygame.KEYDOWN and not game_started:
            game_started = True  # Start the game when any key is pressed

    if game_started:
        # Key press handling for movement
        if not pygame.mixer.get_busy():  # Check if any sound is already playing
            engine.play(-1)  # Loop the engine sound indefinitely
            engine.set_volume(2)  # Adjust the volume to avoid overpowering other sounds
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > road_left:
            player_x -= speed
        if keys[pygame.K_RIGHT] and player_x < road_right - player.get_width():
            player_x += speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player.get_height():
            player_y += speed
            if not pygame.mixer.get_busy():  # Only play if not already playing
                beep.play(-1)
                beep.set_volume(0.5)
            else:
                if beep.get_num_channels() > 0:  # If the beep is playing
                 beep.stop()

        # Move the road images smoothly
        road1_y += 2
        road2_y += 2

        # If a road image goes off the screen, reset its position
        if road1_y >= HEIGHT:
            road1_y = -HEIGHT
        if road2_y >= HEIGHT:
            road2_y = -HEIGHT

        # Fill the screen with the road images (background)
        screen.blit(road, (0, road1_y))  # Draw the first road image
        screen.blit(road, (0, road2_y))  # Draw the second road image

        # Create packages randomly
        if random.randint(0, 100) < 2:  # Adjust the probability (higher value makes packages less frequent)
            lane = random.choice(lanes)  # Random lane
            y_position = -package_height  # Start the package above the screen
            new_package = Package(lane, y_position)
            all_sprites.add(new_package)
            package_group.add(new_package)

        # Create cars randomly
        if random.randint(0, 100) < 2:  # Adjust the probability
            lane = random.choice(lanes)  # Random lane
            y_position = -car_height  # Start the car above the screen
            car_color = random.choice(["yellow", "white"])  # Randomly select yellow or white car
            new_car = Car(lane, y_position, car_color)
            all_sprites.add(new_car)
            car_group.add(new_car)

        # Update all sprites (move packages, cars, and check for collisions)
        all_sprites.update(5)

        # Check for collisions with the truck
        for car in car_group:
            if player_x < car.rect.x + car.rect.width and player_x + player.get_width() > car.rect.x and player_y < car.rect.y + car.rect.height and player_y + player.get_height() > car.rect.y:
                # Collision detected with car
                score = 0  # Reset score on collision
                crash_sound.play()
                game_started = False  # Go back to the menu
                break

        # Check for collisions with packages
        for package in package_group:
            if player_x < package.rect.x + package.rect.width and player_x + player.get_width() > package.rect.x and player_y < package.rect.y + package.rect.height and player_y + player.get_height() > package.rect.y:
                # Package collected
                score += 1
                package.kill()  # Remove the package from the screen
                collect_sound.play()

        # Draw the player (truck)
        screen.blit(player, (player_x, player_y))

        # Display the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Draw all the packages and cars
        all_sprites.draw(screen)

        # Update the display
        pygame.display.update()

    # If the game is not started, show the menu screen
    else:
        # Draw the menu background
        screen.blit(menu_image, (0, 0))

        # Draw the start button (with sky blue color and rounded corners)
        draw_rounded_button(screen, (135, 206, 235), button_x, button_y, button_width, button_height, corner_radius, button_text)

        # Draw the high score text below the start button
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))  # Make sure this gets updated
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, button_y + button_height + 20))

        # Update the display
        pygame.display.update()

    # Frame rate control
    pygame.time.Clock().tick(60)  