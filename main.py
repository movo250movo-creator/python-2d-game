import random
import sys

import pygame


# ----------------------------
# Game settings
# ----------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_WIDTH = 55
PLAYER_HEIGHT = 55
PLAYER_SPEED = 7

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
STARTING_ENEMY_SPEED = 5
ENEMY_SPAWN_DELAY = 800  # milliseconds


# ----------------------------
# Colors
# ----------------------------
WHITE = (255, 255, 255)
BLACK = (20, 20, 25)
BLUE = (50, 140, 255)
RED = (230, 60, 70)
YELLOW = (255, 220, 70)
GRAY = (170, 170, 170)


def draw_text(
    screen: pygame.Surface,
    text: str,
    size: int,
    color: tuple[int, int, int],
    x: int,
    y: int,
    center: bool = False,
) -> None:
    """Draw text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    screen.blit(text_surface, text_rect)


def reset_game() -> tuple[pygame.Rect, list[pygame.Rect], int, int, bool]:
    """Reset all game values."""
    player = pygame.Rect(
        SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
        SCREEN_HEIGHT - PLAYER_HEIGHT - 25,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )

    enemies: list[pygame.Rect] = []
    score = 0
    enemy_speed = STARTING_ENEMY_SPEED
    game_over = False

    return player, enemies, score, enemy_speed, game_over


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Block Dodger")

    clock = pygame.time.Clock()

    # Custom event for creating enemies.
    spawn_enemy_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_enemy_event, ENEMY_SPAWN_DELAY)

    player, enemies, score, enemy_speed, game_over = reset_game()

    running = True

    while running:
        clock.tick(FPS)

        # ----------------------------
        # Event handling
        # ----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == spawn_enemy_event and not game_over:
                enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)

                enemy = pygame.Rect(
                    enemy_x,
                    -ENEMY_HEIGHT,
                    ENEMY_WIDTH,
                    ENEMY_HEIGHT,
                )

                enemies.append(enemy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game_over and event.key == pygame.K_r:
                    player, enemies, score, enemy_speed, game_over = reset_game()

        # ----------------------------
        # Player movement
        # ----------------------------
        if not game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= PLAYER_SPEED

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += PLAYER_SPEED

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.y -= PLAYER_SPEED

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.y += PLAYER_SPEED

            # Keep player inside the screen.
            player.x = max(0, min(player.x, SCREEN_WIDTH - PLAYER_WIDTH))
            player.y = max(0, min(player.y, SCREEN_HEIGHT - PLAYER_HEIGHT))

            # ----------------------------
            # Enemy movement
            # ----------------------------
            for enemy in enemies[:]:
                enemy.y += enemy_speed

                # Remove enemies that leave the screen.
                if enemy.top > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    score += 1

                    # Increase difficulty every 10 points.
                    if score % 10 == 0:
                        enemy_speed += 1

                # Check collision.
                elif player.colliderect(enemy):
                    game_over = True

        # ----------------------------
        # Drawing
        # ----------------------------
        screen.fill(BLACK)

        # Decorative road lines.
        for line_y in range(0, SCREEN_HEIGHT, 80):
            pygame.draw.rect(
                screen,
                GRAY,
                (SCREEN_WIDTH // 2 - 4, line_y, 8, 45),
            )

        pygame.draw.rect(screen, BLUE, player, border_radius=8)

        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy, border_radius=8)

        draw_text(screen, f"Score: {score}", 36, WHITE, 15, 15)
        draw_text(screen, f"Speed: {enemy_speed}", 28, YELLOW, 15, 55)

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            draw_text(
                screen,
                "GAME OVER",
                80,
                RED,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 70,
                center=True,
            )

            draw_text(
                screen,
                f"Final Score: {score}",
                45,
                WHITE,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                center=True,
            )

            draw_text(
                screen,
                "Press R to restart",
                35,
                YELLOW,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 60,
                center=True,
            )

            draw_text(
                screen,
                "Press ESC to quit",
                28,
                GRAY,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 105,
                center=True,
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
