import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Размеры экрана
WIDTH = 800
HEIGHT = 600

# Настройки игры
paddle_width = 100
paddle_height = 10
ball_size = 10
paddle_speed = 10
block_width = 75
block_height = 20
star_size = 25
rows_of_blocks = 5
columns_of_blocks = 10

# Устанавливаем начальные значения скорости мяча
ball_speed_x = 2  # Начальная скорость по оси X
ball_speed_y = -2  # Начальная скорость по оси Y

# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Отбивание мяча с блоками и звёздочками")

# Класс блока
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, block_width, block_height)
        self.color = YELLOW
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Класс звезды
class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, star_size, star_size)
        self.color = GREEN
        self.active = True
        self.spawn_time = time.time()
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Класс зеленого мяча
class GreenBall:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ball_size, ball_size)
        self.color = GREEN
        self.active = True
        self.spawn_time = time.time()
        
    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

# Главная функция игры
def game_loop():
    global ball_speed_x, ball_speed_y  # Используем глобальные переменные

    clock = pygame.time.Clock()
    
    # Позиции платформы и мяча
    paddle_x = (WIDTH - paddle_width) / 2
    paddle_y = HEIGHT - paddle_height - 10
    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2

    score = 0
    blocks = [Block(x * (block_width + 10) + 20, y * (block_height + 5) + 50) 
              for y in range(rows_of_blocks) for x in range(columns_of_blocks)]
              
    stars = []
    green_balls = []
    last_star_spawn_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # Движение мяча
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Проверка столкновения с границами
        if ball_x <= 0 or ball_x >= WIDTH - ball_size:
            ball_speed_x = -ball_speed_x  # Отскок от стены

        if ball_y <= 0:
            ball_speed_y = -ball_speed_y  # Отскок от верхней стены

        # Проверка столкновения с платформой
        if (paddle_y < ball_y + ball_size < paddle_y + paddle_height) and (paddle_x < ball_x < paddle_x + paddle_width):
            ball_speed_y = -abs(ball_speed_y)  # Убедимся, что мяч отскакивает вверх
            ball_speed_x *= 1.25  # Увеличиваем скорость мяча по X на 25%
            ball_speed_y *= 1.25  # Увеличиваем скорость мяча по Y на 25%
            # Ограничиваем максимальную скорость мяча
            ball_speed_x = max(2, min(10, ball_speed_x))  
            ball_speed_y = max(2, min(10, ball_speed_y))

        # Проверка столкновения с блоками
        for block in blocks[:]:  # Итерируем по копии списка
            if block.rect.colliderect(pygame.Rect(ball_x, ball_y, ball_size, ball_size)):
                blocks.remove(block)  # Удаляем блок
                ball_speed_y = -ball_speed_y  # Отскок мяча
                score += 5  # Увеличиваем счёт при разбиении блока
                ball_speed_x *= 1.25  # Увеличиваем скорость мяча на 25%
                ball_speed_y *= 1.25  # Увеличиваем скорость мяча на 25%
                # Ограничиваем максимальную скорость мяча
                ball_speed_x = max(2, min(10, ball_speed_x))
                ball_speed_y = max(2, min(10, ball_speed_y))
                break  # Прерываем цикл после столкновения

        # Проверка, упал ли мяч
        if ball_y > HEIGHT:
            print("Вы проиграли! Ваш итоговый счёт:", score)
            running = False

        # Проверка на создание звёздочек
        if time.time() - last_star_spawn_time >= 13:
            star_x = random.randint(int(paddle_x), int(paddle_x + paddle_width - star_size))
            stars.append(Star(star_x, paddle_y - star_size))  # Звезда появится над платформой
            last_star_spawn_time = time.time()

        # Проверка столкновения с звёздочками
        for star in stars[:]:  # Итерируем по копии списка
            if star.active and star.rect.colliderect(pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)):
                stars.remove(star)  # Удаляем звезду
                # Создаем 6 зеленых мячей
                for _ in range(6):
                    green_balls.append(GreenBall(paddle_x + random.randint(-50, 50), paddle_y - 50))
                break  # Прерываем цикл после столкновения

        # Обновляем зеленые мячи
        for green_ball in green_balls[:]:
            # Проверяем время жизни зелёного мяча
            if time.time() - green_ball.spawn_time > 15:
                green_balls.remove(green_ball)  # Удаляем, если прошло 15 секунд

        # Рисуем объекты
        screen.fill(WHITE)  # Очистка экрана
        pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))  # Платформа
        pygame.draw.ellipse(screen, RED, (ball_x, ball_y, ball_size, ball_size))  # Мяч
        
        # Рисуем блоки
        for block in blocks:
            block.draw(screen)

        # Рисуем звёзды
        for star in stars:
            star.draw(screen)

        # Рисуем зеленые мячи
        for green_ball in green_balls:
            green_ball.draw(screen)

        # Отображаем счёт
        font = pygame.font.SysFont("comicsansms", 35)
        score_text = font.render("Счёт: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()  # Обновляем экран
        clock.tick(60)  # Ограничиваем FPS

    pygame.quit()

if __name__ == "__main__":
    game_loop()