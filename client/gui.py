def start_gui(args):
    import os
    from typing import List
    import client.players
    import client.sound
    import client.client
    import pygame
    import sys
    import time

    ip = args.ip
    port = args.port

    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 500
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (200, 200, 200)
    FONT_COLOR = (0, 0, 0)
    # choose a font where all the characters have the same width
    FONT = pygame.font.Font(pygame.font.match_font('courier'), 20)

    # Initialize variables
    n_players = int(input('Enter the number of players: '))
    players = client.players.Players(n_players)
    for i, player in enumerate(players):
        player.set_name(input(f'Enter the name of player {i + 1}: '))
        handicap = input(f'Enter the handicap of player {i + 1} in seconds: ')
        if handicap != '':
            player.set_handicap(int(handicap))
        else:
            player.set_handicap(None)
        # set the buzzer sound
        # list all files in the buzzer_sounds directory
        buzzer_sounds = os.listdir('buzzer_sounds')
        print('Choose a buzzer sound for player', i + 1)
        for j, sound in enumerate(buzzer_sounds):
            print(j + 1, sound)
        sound_index = input('Enter the index of the sound you want to use: ')
        try:
            sound_index = int(sound_index)
            player.set_sound(client.sound.SoundObject(f'buzzer_sounds/{buzzer_sounds[sound_index - 1]}'))
        except ValueError:
            print('Using no sound')
        gpio_pin = input(f'Enter the GPIO pin of player {i + 1}: ')
        try:
            player.gpio_pin = int(gpio_pin)
        except ValueError:
            print('Using no GPIO pin')
    if args.physical_buzzers:
        connector = client.client.ConnectionObject(ip, port)

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Quiz Show Buzzer System')

    # Functions for button actions
    timer_start: float = 0
    timer = False

    def on_timer():
        nonlocal timer
        nonlocal timer_start
        if not timer:
            timer_start = time.time()
            players.set_hadicap_time(time.time())
            timer = True
        else:
            timer = False
            players.set_hadicap_time(float('inf'))
            timer_start = 0

    def on_reset():
        nonlocal timer
        if timer:
            on_timer()
        players.reset_buzzers()

    def on_wrong():
        nonlocal timer_start
        players.wrong_answer(timer_start)

    buzzed_player = None

    def on_add():
        nonlocal buzzed_player
        if buzzed_player is not None:
            players[buzzed_player].add_to_score()

    def on_sub():
        nonlocal buzzed_player
        if buzzed_player is not None:
            players[buzzed_player].sub_to_score()

    # Helper function to draw buttons
    def draw_button(rect, text, callback):
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Outline
        label = FONT.render(text, True, FONT_COLOR)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        return rect, callback

    # Helper function to draw an X
    def draw_x(surface, rect, color=(255, 255, 255), width=1):
        """
        Draws an X of lines connecting the corners of the given rect on the surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            rect (pygame.Rect): The rectangle whose corners will be connected.
            color (tuple): The color of the lines (default is white).
            width (int): The width of the lines (default is 1).
        """
        # Coordinates for the corners of the rect
        top_left = (rect.left, rect.top + 2)
        top_right = (rect.right - 1, rect.top + 2)
        bottom_left = (rect.left, rect.bottom - 3)
        bottom_right = (rect.right - 1, rect.bottom - 3)

        # Draw lines connecting the corners
        pygame.draw.line(surface, color, top_left, bottom_right, width)
        pygame.draw.line(surface, color, top_right, bottom_left, width)

    # Define buttons:
    buttons = []
    buzzers_rect: List[pygame.Rect] = []
    # Define evenly spaced buttons based on the number of players:
    margin = 50
    button_margin = 20

    button_width = (SCREEN_WIDTH - 2 * margin - (n_players - 1) * button_margin) // n_players
    for i in range(n_players):
        buzzers_rect.append(pygame.Rect(margin + i * (button_width + button_margin), 50, button_width, 100))

    # Draw reset and timer buttons
    reset_rect = pygame.Rect(50, 200, 300, 100)
    timer_rect = pygame.Rect(400, 200, 300, 100)
    wrong_rect = pygame.Rect(750, 200, 300, 100)

    # Draw app and subtrackt buttons

    add_rect = pygame.Rect(50, 350, 475, 100)
    sub_rect = pygame.Rect(575, 350, 475, 100)
    # Main loop
    running = True
    previous_buzzed_player = None
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for rect, callback in buttons:
                    if rect.collidepoint(pos):
                        callback()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    on_reset()
                elif event.key == pygame.K_t:
                    on_timer()
                elif event.key == pygame.K_y:
                    on_wrong()
                elif event.key == pygame.K_f:
                    on_add()
                elif event.key == pygame.K_g:
                    on_sub()
                for i in range(n_players):  # Iterate over player indices (1, 2, 3)
                    if event.key == getattr(pygame, f"K_{i + 1}") and n_players >= i:
                        players[i].buzz()
        # None pygame event handling
        if args.physical_buzzers:
            buzzer_info = connector.get_gpio_states()

            if buzzer_info is not None:
                buzzer_info = [1 if buzzer_info[str(player.gpio_pin)] == 'HIGH' else 0 for player in players]
                for i, buzzer in enumerate(buzzer_info):
                    if buzzer:
                        players[i].buzz()

        # Draw buzzer buttons
        buttons = []

        for i in range(n_players):
            rect = buzzers_rect[i]
            buttons.append(draw_button(rect, str(players[i]), players[i].buzz))

        buzzed_player = players.who_buzzed(timer_start)
        if buzzed_player != previous_buzzed_player:
            if buzzed_player is not None:
                if players[buzzed_player].sound is not None:
                    players[buzzed_player].sound.play()
            previous_buzzed_player = buzzed_player

        if buzzed_player is not None:
            pygame.draw.rect(screen, RED, buzzers_rect[buzzed_player], 5)

        # Draw X

        for i, player in enumerate(players):
            if player.wrong:
                draw_x(screen, buzzers_rect[i], color=RED, width=5)

        timer_text = 'Start Timer' if not timer else f'{(time.time() - timer_start):.2f} s'

        buttons.append(draw_button(reset_rect, 'Reset Buzzers', on_reset))
        buttons.append(draw_button(timer_rect, timer_text, on_timer))
        buttons.append(draw_button(wrong_rect, 'Wrong Answer', on_wrong))

        buttons.append(draw_button(add_rect, '+1', on_add))
        buttons.append(draw_button(sub_rect, '-1', on_sub))

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()
