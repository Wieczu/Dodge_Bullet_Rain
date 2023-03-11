import pygame
import random
import sys
from pygame import mixer

pygame.init()
mixer.init()
global player_name

# MAIN WINDOW
pygame.display.set_caption('DODGE BULLET RAIN!')
window_x = 700
window_y = 700
screen = pygame.display.set_mode((window_x, window_y))
highscores_img = pygame.image.load("assets/Highscores.png")
highscores_options = pygame.image.load("assets/highlights_key_options.png")
lost_options = pygame.image.load("assets/lost_options.png")
provide_name = pygame.image.load("assets/provide_name.png")
instructions_option = pygame.image.load("assets/Instructions.png")
instruction_title = pygame.image.load("assets/Instruction_title.png")
player_instructions = pygame.image.load("assets/player_instructions.png")
escape_instructions = pygame.image.load("assets/escape_instruction.png")

try:
    scores_file = open("scores.txt", "x")
except FileExistsError:
    pass


def instructions():
    mixer.music.load("music/menu_song_2.wav")
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)

    instruction = True

    while instruction:

        for instr_event in pygame.event.get():
            if instr_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if instr_event.type == pygame.KEYDOWN:
                if instr_event.key == pygame.K_ESCAPE:
                    instruction = False
                    menu()

        screen.fill((55, 0, 0))
        screen.blit(instruction_title, (32, 70))
        screen.blit(player_instructions, (32, 150))
        screen.blit(escape_instructions, (32, 600))
        pygame.display.update()


def player_name_func():
    name_font = pygame.font.Font("assets/RAVIE.TTF", 30)
    name = ""
    global player_name
    name_loop = True
    while name_loop:
        global player_name
        for pn_event in pygame.event.get():
            if pn_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pn_event.type == pygame.KEYDOWN:
                if pn_event.key != pygame.K_SPACE:
                    name += pn_event.unicode
                if pn_event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                if pn_event.key == pygame.K_RETURN:
                    name_loop = False
                    name = str(name)
                    player_name = name.strip()
                    menu()

        screen.fill((55, 0, 0))
        text_surface = name_font.render(name, True, (172, 120, 18))
        screen.blit(text_surface, (250, 300))
        screen.blit(provide_name, (32, 100))
        pygame.display.update()


def highscores():
    mixer.music.load("music/Highscores.wav")
    mixer.music.set_volume(0.2)
    hs_visible = False
    highscores_clock = pygame.time.Clock()
    high_x = 280
    high_y = 200
    high_list = []
    highscores_font = pygame.font.Font("assets/RAVIE.TTF", 20)
    highscores_file = open("scores.txt", "r")
    highscores_lines = highscores_file.readlines()
    mixer.music.play(loops=-1)
    if len(highscores_lines) < 1:
        hs = False
        line_text = highscores_font.render("No Results Recorded", True, (172, 120, 18))

        while not hs:
            screen.fill((55, 0, 0))
            screen.blit(line_text, (215, 200))
            screen.blit(highscores_img, (32, 70))
            screen.blit(highscores_options, (250, 260))
            pygame.display.update()
            highscores_clock.tick(60)
            for no_highscores_event in pygame.event.get():
                if no_highscores_event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if no_highscores_event.type == pygame.KEYDOWN:
                    if no_highscores_event.key == pygame.K_SPACE:
                        hs = False
                        menu()
                    if no_highscores_event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    elif len(highscores_lines) >= 1:
        hs = True
        for lane in highscores_lines:
            high_dict = {}
            key = lane.partition(":")[0]
            value = lane.partition(" ")[-1]
            final = value.partition(" ")[0]
            final = int(final)
            high_dict['name'] = key
            high_dict['points'] = final
            high_list.append(high_dict)

        high_list_sorted = sorted(high_list, key=lambda x: x['points'], reverse=True)
        high_list_sorted = high_list_sorted[:20]
        hs_count = 0

        while hs:

            screen.fill((55, 0, 0))

            for highscore_event in pygame.event.get():
                if highscore_event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if highscore_event.type == pygame.KEYDOWN:
                    if highscore_event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if highscore_event.key == pygame.K_SPACE:
                        hs = False
                        mixer.music.stop()
                        menu()

            if hs_count == 0:
                hs_visible = False
            if hs_count == len(high_list_sorted):
                hs_visible = True

            if not hs_visible:
                for player_score in high_list_sorted:
                    line_text = highscores_font.render(player_score['name'] + ": " + str(player_score['points']), True,
                                                       (172, 120, 18))
                    screen.blit(line_text, (high_x, high_y))
                    hs_count = hs_count + 1
                    high_y = high_y + 23
                screen.blit(highscores_img, (32, 70))
                screen.blit(highscores_options, (10, 260))
                pygame.display.update()

            highscores_clock.tick(60)


def lost(score):
    # Lose screen
    game_over = "Game Over"
    mixer.music.load("music/lost.wav")
    mixer.music.set_volume(0.2)
    # Score text box
    lose_font = pygame.font.Font("assets/RAVIE.TTF", 60)
    mixer.music.play()
    lost_flag = True
    lost_clock = pygame.time.Clock()

    while lost_flag:
        user_text = "score: " + str(score)
        # To be done -> GameOver screen as a function, new window
        lose_text = lose_font.render(game_over, True, (172, 120, 18))
        score_text = lose_font.render(user_text, True, (172, 120, 18))
        screen.fill((55, 0, 0))
        screen.blit(lose_text, (120, 100))
        screen.blit(score_text, (120, 230))
        for lost_event in pygame.event.get():
            if lost_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if lost_event.type == pygame.KEYDOWN:
                if lost_event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if lost_event.key == pygame.K_SPACE:
                    lost_flag = False
                    mixer.music.stop()
                    menu()
                if lost_event.key == pygame.K_r:
                    lost_flag = False
                    mixer.music.stop()
                    main()
        screen.blit(lost_options, (32, 500))
        lost_clock.tick(60)
        pygame.display.update()


def menu():
    mixer.music.load("music/menu_song_2.wav")
    mixer.music.set_volume(0.2)
    menu_flag = True
    menu_bg = pygame.image.load("assets/dodge_bullet_rain.png")
    menu_options = pygame.image.load("assets/menu_options_all.png")
    menu_clock = pygame.time.Clock()
    mixer.music.play(-1)
    while menu_flag:

        screen.fill((55, 0, 0))
        screen.blit(menu_bg, (0, 0))
        screen.blit(menu_options, (31, 500))
        screen.blit(instructions_option, (31, 605))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    mixer.music.stop()
                    menu_flag = False
                    main()

                elif event.key == pygame.K_h:
                    mixer.music.stop()
                    menu_flag = False
                    highscores()

                elif event.key == pygame.K_i:
                    mixer.music.stop()
                    menu_flag = False
                    instructions()

        menu_clock.tick(60)
        pygame.display.update()


def main():
    global player_name
    # Scores File
    scores = open("scores.txt", "a")
    main_music = pygame.mixer.Sound("music/main_game_song.wav")
    main_music.set_volume(0.2)
    # Images
    # background = pygame.image.load("venv/assets/bg.png")
    bullet = pygame.image.load("assets/bullet2.png")
    bullet2 = pygame.image.load("assets/bullet2.png")
    bullet3 = pygame.image.load("assets/bullet2.png")
    medium_bullet = pygame.image.load("assets/medium_bullet.png")
    medium_bullet2 = pygame.image.load("assets/medium_bullet.png")
    vertical_right = pygame.image.load("assets/vertical_bullet_right.png")
    vertical_left = pygame.image.load("assets/vertical_bullet_left.png")
    player_stand = pygame.image.load("assets/player_stand.png")
    hearts = [pygame.image.load("assets/heart.png"), pygame.image.load("assets/heart.png"),
              pygame.image.load("assets/heart.png"), pygame.image.load("assets/heart.png")]
    single_heart = pygame.image.load("assets/heart.png")

    # Player life and hearts position
    hearts_y = 15
    hearts_x = 640
    player_life = 3

    # Normal Bullet
    bullet_x = random.randint(0, 230)
    bullet_y = 0
    bullet_game_speed = 5

    # Normal Bullet 2
    bullet_x2 = random.randint(230, 460)
    bullet_y2 = 0
    bullet_game_speed2 = 4

    # Normal Bullet 3
    bullet_x3 = random.randint(460, 690)
    bullet_y3 = 0
    bullet_game_speed3 = 2

    # Medium Bullet
    medium_bullet_x = random.randint(0, 335)
    medium_bullet_y = 0
    medium_bullet_game_speed = 3

    # Medium Bullet 2
    medium_bullet_x2 = random.randint(336, 670)
    medium_bullet_y2 = 0
    medium_bullet_game_speed2 = 2

    # Vertical Bullet
    vertical_bullet_x = random.choice([0, 700])
    vertical_bullet_y = random.randint(630, 690)
    vertical_bullet_game_speed = 2

    # Player Attributes
    start_x = window_x / 2
    start_y = window_y - 79
    isJump = False
    score = 0
    jumpCount = 10
    run = True
    main_clock = pygame.time.Clock()

    # Heart Spawn attribute
    heart_score = 0
    heart_x = random.randint(1, 680)
    heart_y = window_y - 20
    # Score text box
    base_font = pygame.font.Font("assets/RAVIE.TTF", 30)
    vertical = 0

    main_music.play(loops=-1)

    while run:
        screen.fill((50, 0, 0))
        user_text = "score: " + str(score)
        text_surface = base_font.render(user_text, True, (172, 120, 18))
        screen.blit(text_surface, (5, 15))

        # Defining which vertical bullet hit box to spawn
        if vertical_bullet_x == 0:
            vertical = vertical_left
            vertical_bullet_x += vertical_bullet_game_speed
        elif vertical_bullet_x == 700:
            vertical = vertical_right
            vertical_bullet_x -= vertical_bullet_game_speed

        # Spawning first bullets and creating hit boxes
        bullet_rect = bullet.get_rect(topleft=(bullet_x, bullet_y))
        bullet2_rect = bullet2.get_rect(topleft=(bullet_x2, bullet_y2))
        bullet3_rect = bullet3.get_rect(topleft=(bullet_x3, bullet_y3))
        medium_bullet_rect = medium_bullet.get_rect(topleft=(medium_bullet_x, medium_bullet_y))
        medium_bullet2_rect = medium_bullet2.get_rect(topleft=(medium_bullet_x2, medium_bullet_y2))
        vertical_rect = vertical.get_rect(topleft=(vertical_bullet_x, vertical_bullet_y))
        screen.blit(vertical, (vertical_bullet_x, vertical_bullet_y))
        screen.blit(bullet, (bullet_x, bullet_y))
        screen.blit(bullet2, (bullet_x2, bullet_y2))
        screen.blit(bullet3, (bullet_x3, bullet_y3))
        screen.blit(medium_bullet, (medium_bullet_x, medium_bullet_y))
        screen.blit(medium_bullet2, (medium_bullet_x2, medium_bullet_y2))

        if vertical == vertical_right:
            vertical_bullet_x -= vertical_bullet_game_speed
        else:
            vertical_bullet_x += vertical_bullet_game_speed

        # Speed of few first bullets of each category
        bullet_y += bullet_game_speed
        bullet_y2 += bullet_game_speed2
        bullet_y3 += bullet_game_speed3
        medium_bullet_y += medium_bullet_game_speed
        medium_bullet_y2 += medium_bullet_game_speed2
        # Bullets speed manipulation based on score
        if 100 < score <= 500:
            bullet_game_speed = 7
            bullet_game_speed2 = 6
            bullet_game_speed3 = 4
            vertical_bullet_game_speed = 4
            medium_bullet_game_speed = 3
            medium_bullet_game_speed2 = 2
        if 500 < score <= 1500:
            bullet_game_speed = 9
            bullet_game_speed2 = 8
            bullet_game_speed3 = 6
            vertical_bullet_game_speed = 6
            medium_bullet_game_speed = 5
            medium_bullet_game_speed2 = 3
        if score > 1500:
            bullet_game_speed = 10
            bullet_game_speed2 = 11
            bullet_game_speed3 = 8
            vertical_bullet_game_speed = 8
            medium_bullet_game_speed = 9
            medium_bullet_game_speed2 = 7

        # Handling player life counter image
        if player_life == 4:
            screen.blit(hearts[3], (hearts_x - 17, hearts_y))
            screen.blit(hearts[0], (hearts_x, hearts_y))
            screen.blit(hearts[1], (hearts_x + 17, hearts_y))
            screen.blit(hearts[2], (hearts_x + 34, hearts_y))
        elif player_life == 3:
            screen.blit(hearts[0], (hearts_x, hearts_y))
            screen.blit(hearts[1], (hearts_x + 17, hearts_y))
            screen.blit(hearts[2], (hearts_x + 34, hearts_y))
        elif player_life == 2:
            screen.blit(hearts[1], (hearts_x + 17, hearts_y))
            screen.blit(hearts[2], (hearts_x + 34, hearts_y))
        elif player_life == 1:
            screen.blit(hearts[2], (hearts_x + 34, hearts_y))
        elif player_life == 0:
            if player_name == "":
                player_name = "Player"
            scores.write("{}: {} points \n".format(player_name, score))
            scores.close()
            main_music.stop()
            run = False
            lost(score)

        # Setting primary character position
        screen.blit(player_stand, (start_x, start_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Listening to key inputs
        key = pygame.key.get_pressed()
        player_stand = pygame.image.load("assets/player_stand.png")
        # Creating character hit box
        player_rect = player_stand.get_rect(topleft=(start_x, start_y))

        # Spawning hearts under condition
        if heart_score == 0:
            if score > 500:
                screen.blit(single_heart, (heart_x, heart_y))
                single_heart_rect = single_heart.get_rect(topleft=(heart_x, heart_y))

                # Heart collision
                if single_heart_rect.colliderect(player_rect):
                    get_life = mixer.Sound("music/heart.wav")
                    get_life.set_volume(0.2)
                    get_life.play()
                    player_life = player_life + 1
                    heart_score = 1
                    heart_x = random.randint(1, 680)
                    heart_y = window_y - 20
            pygame.display.update()

        if heart_score == 1:
            if score > 1500:
                screen.blit(single_heart, (heart_x, heart_y))
                single_heart_rect = single_heart.get_rect(topleft=(heart_x, heart_y))

                # Heart collision
                if single_heart_rect.colliderect(player_rect):
                    get_life = mixer.Sound("music/heart.wav")
                    get_life.set_volume(0.2)
                    get_life.play()
                    if player_life < 4:
                        player_life = player_life + 1
                        score += 30
                    else:
                        score += 300
                    heart_score = 2
                    heart_x = random.randint(1, 680)
                    heart_y = window_y - 20
            pygame.display.update()

        if heart_score == 2:
            if score > 3000:
                screen.blit(single_heart, (heart_x, heart_y))
                single_heart_rect = single_heart.get_rect(topleft=(heart_x, heart_y))

                # Heart collision
                if single_heart_rect.colliderect(player_rect):
                    get_life = mixer.Sound("music/heart.wav")
                    get_life.set_volume(0.2)
                    get_life.play()
                    if player_life < 4:
                        player_life = player_life + 1
                        score += 50
                    else:
                        score += 500
                    heart_score = 3
            pygame.display.update()

        if heart_score == 3:
            if score > 5000:
                screen.blit(single_heart, (heart_x, heart_y))
                single_heart_rect = single_heart.get_rect(topleft=(heart_x, heart_y))

                # Heart collision
                if single_heart_rect.colliderect(player_rect):
                    get_life = mixer.Sound("music/heart.wav")
                    get_life.set_volume(0.2)
                    get_life.play()
                    if player_life < 4:
                        player_life = player_life + 1
                        score += 100
                    else:
                        score += 1000
                    heart_score = 4
            pygame.display.update()

        if heart_score == 4:
            if score > 10000:
                screen.blit(single_heart, (heart_x, heart_y))
                single_heart_rect = single_heart.get_rect(topleft=(heart_x, heart_y))

                # Heart collision
                if single_heart_rect.colliderect(player_rect):
                    get_life = mixer.Sound("music/heart.wav")
                    get_life.set_volume(0.2)
                    get_life.play()
                    if player_life < 4:
                        player_life = player_life + 1
                        score += 500
                    else:
                        score += 5000
                    heart_score = 5
            pygame.display.update()

        # Player movement and screen boundaries
        # Left
        if start_x >= 5:
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                player_stand = pygame.image.load("assets/player_left1.png")
                # Modify speed if character jumps
                if not isJump:
                    start_x -= 5
                if isJump:
                    start_x -= 8
        # Right
        if start_x + 37 <= window_x:
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                player_stand = pygame.image.load("assets/player_right1.png")
                # Modify speed if character jumps
                if not isJump:
                    start_x += 5
                if isJump:
                    start_x += 8
        # Jumping mechanic (no double jump allowed)
        if not isJump:
            if key[pygame.K_SPACE]:
                isJump = True
        else:
            if jumpCount >= -10:
                start_y -= (jumpCount * abs(jumpCount * 0.8)) * 0.6
                jumpCount -= 1
            else:
                jumpCount = 10
                isJump = False

        # Normal bullet collision handling
        if bullet_rect.colliderect(player_rect):
            get_hit = mixer.Sound("music/ouch-sound-effect-30-11844.mp3")
            get_hit.set_volume(0.2)
            get_hit.play()
            player_life = player_life - 1
            bullet_y = 0
            bullet_x = random.randint(0, 690)
            screen.blit(bullet, (bullet_x, bullet_y))

        if bullet_y >= window_y:
            bullet_y = 0
            bullet_x = random.randint(0, 690)
            screen.blit(bullet, (bullet_x, bullet_y))
            score += 20

        # Normal bullet 2 collision handling
        if bullet2_rect.colliderect(player_rect):
            get_hit = mixer.Sound("music/ouch-sound-effect-30-11844.mp3")
            get_hit.set_volume(0.2)
            get_hit.play()
            player_life = player_life - 1
            bullet_y2 = 0
            bullet_x2 = random.randint(0, 690)
            screen.blit(bullet2, (bullet_x2, bullet_y2))

        if bullet_y2 >= window_y:
            bullet_y2 = 0
            bullet_x2 = random.randint(0, 690)
            screen.blit(bullet2, (bullet_x2, bullet_y2))
            score += 20

        # Normal bullet 3 collision handling
        if bullet3_rect.colliderect(player_rect):
            get_hit = mixer.Sound("music/ouch-sound-effect-30-11844.mp3")
            get_hit.set_volume(0.2)
            get_hit.play()
            player_life = player_life - 1
            bullet_y3 = 0
            bullet_x3 = random.randint(0, 690)
            screen.blit(bullet3, (bullet_x3, bullet_y3))

        if bullet_y3 >= window_y:
            bullet_y3 = 0
            bullet_x3 = random.randint(0, 690)
            screen.blit(bullet, (bullet_x3, bullet_y3))
            score += 20

        # Medium bullet collision handling
        if medium_bullet_rect.colliderect(player_rect):
            get_hit = mixer.Sound("music/ouch-sound-effect-30-11844.mp3")
            get_hit.set_volume(0.2)
            get_hit.play()
            player_life = player_life - 1
            medium_bullet_y = 0
            medium_bullet_x = random.randint(0, 670)
            screen.blit(medium_bullet, (medium_bullet_x, medium_bullet_y))

        if medium_bullet_y >= window_y:
            medium_bullet_y = 0
            medium_bullet_x = random.randint(0, 670)
            screen.blit(medium_bullet, (medium_bullet_x, medium_bullet_y))
            score += 20

        # Medium bullet collision handling
        if medium_bullet2_rect.colliderect(player_rect):
            get_hit = mixer.Sound("music/ouch-sound-effect-30-11844.mp3")
            get_hit.set_volume(0.2)
            get_hit.play()
            player_life = player_life - 1
            medium_bullet_y2 = 0
            medium_bullet_x2 = random.randint(0, 670)
            screen.blit(medium_bullet2, (medium_bullet_x2, medium_bullet_y2))

        if medium_bullet_y2 >= window_y:
            medium_bullet_y2 = 0
            medium_bullet_x2 = random.randint(0, 670)
            screen.blit(medium_bullet2, (medium_bullet_x2, medium_bullet_y2))
            score += 20

        # Vertical bullet collision handling
        if vertical_rect.colliderect(player_rect):
            get_hit = mixer.Sound("music/ouch-sound-effect-30-11844.mp3")
            get_hit.set_volume(0.2)
            get_hit.play()
            player_life = player_life - 1
            vertical_bullet_y = random.randint(630, 690)
            vertical_bullet_x = random.choice([0, 700])
            screen.blit(vertical, (vertical_bullet_x, vertical_bullet_y))

        if vertical == vertical_right:
            if vertical_bullet_x <= 0:
                score += 20
                vertical_bullet_y = random.randint(630, 690)
                vertical_bullet_x = random.choice([0, 700])
                if vertical_bullet_x == 0:
                    vertical = vertical_left
                elif vertical_bullet_x == 700:
                    vertical = vertical_right
                screen.blit(vertical, (vertical_bullet_x, vertical_bullet_y))

        if vertical == vertical_left:
            if vertical_bullet_x >= window_x:
                score += 20
                vertical_bullet_y = random.randint(630, 690)
                vertical_bullet_x = random.choice([0, 700])
                screen.blit(vertical, (vertical_bullet_x, vertical_bullet_y))

        main_clock.tick(60)
        pygame.display.update()


player_name_func()
