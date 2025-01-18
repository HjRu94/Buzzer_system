def start_gui(args):
    from typing import List
    import client.players
    import pygame
    import sys
    import time

    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (200, 200, 200)
    FONT_COLOR = (0, 0, 0)
    FONT = pygame.font.Font(None, 36)

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

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Quiz Show Buzzer System')

    # Functions for button actions
    start_time = None
    timer = False

    def on_timer():
        nonlocal timer
        nonlocal start_time
        if not timer:
            start_time = time.time()
            players.set_hadicap_time(time.time())
            timer = True
        else:
            timer = False
            players.set_hadicap_time(float('inf'))
            start_time = None

    def on_reset():
        nonlocal timer
        if timer:
            on_timer()
        players.reset_buzzers()

    def on_add15():
        pass

    def on_add10():
        pass

    def on_sub5():
        pass

    # Helper function to draw buttons
    def draw_button(rect, text, callback):
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Outline
        label = FONT.render(text, True, FONT_COLOR)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        return rect, callback

    # Define buttons:
    buttons = []
    buzzers_rect: List[pygame.Rect] = []
    buzzers_rect.append(pygame.Rect(50, 50, 150, 50))
    buzzers_rect.append(pygame.Rect(225, 50, 150, 50))
    buzzers_rect.append(pygame.Rect(400, 50, 150, 50))

    # Draw reset and timer buttons
    reset_rect = pygame.Rect(75, 150, 200, 50)
    timer_rect = pygame.Rect(325, 150, 200, 50)
    # Draw scoring buttons
    add15_rect = pygame.Rect(100, 250, 100, 50)
    add10_rect = pygame.Rect(250, 250, 100, 50)
    sub5_rect = pygame.Rect(400, 250, 100, 50)

    # Main loop
    running = True
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

        # Draw buzzer buttons
        buttons = []

        for i in range(n_players):
            rect = buzzers_rect[i]
            buttons.append(draw_button(rect, players[i].name, players[i].buzz))
        buzzed_player = players.who_buzzed()
        if buzzed_player is not None:
            pygame.draw.rect(screen, RED, buzzers_rect[buzzed_player], 5)


        timer_text = 'Start Timer' if not timer else str(int(time.time() - start_time))

        buttons.append(draw_button(reset_rect, 'Reset Buzzers', on_reset))
        buttons.append(draw_button(timer_rect, timer_text, on_timer))

        buttons.append(draw_button(add15_rect, '+15', on_add15))
        buttons.append(draw_button(add10_rect, '+10', on_add10))
        buttons.append(draw_button(sub5_rect, '-5', on_sub5))

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()
