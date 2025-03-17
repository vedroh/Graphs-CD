import pygame
import random

pygame.init()

# Размеры окон
window_width, window_height = 600, 600
grid_window_width, grid_window_height = 500, 500

# Размеры сетки
width, height = 500, 500
cell_size = 50
rows, cols = height // cell_size, width // cell_size

indent_x = (window_width - width) // 2
indent_y = (window_height - height) // 2

# Цвета
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создание двух окон
screen_main = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игровое окно")

screen_grid = pygame.display.set_mode((grid_window_width, grid_window_height))
pygame.display.set_caption("Вспомогательное окно")

# Генерация координат объектов
used_coordinates = []

# Почтальон в верхнем левом углу
postman_x, postman_y = indent_x, indent_y
postman_cell = (postman_x, postman_y)

# Генерация домов
count_of_houses = random.randint(3, 8)
houses = []
while len(houses) < count_of_houses:
    x = random.randint(0, cols - 1) * cell_size + indent_x
    y = random.randint(0, rows - 1) * cell_size + indent_y
    if (x, y) not in houses and (x, y) != postman_cell:
        houses.append((x, y))

running = True
while running:
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ОЧИЩАЕМ ОКНА
    screen_main.fill(WHITE)
    screen_grid.fill(WHITE)

    # ОТРИСОВКА ОСНОВНОГО ОКНА (игра)
    postman_start = pygame.image.load('почтальон стоит.png')
    postman_start = pygame.transform.scale(postman_start, (50, 50))
    screen_main.blit(postman_start, (postman_x, postman_y))

    for x, y in houses:
        house = pygame.image.load('домик.png')
        house = pygame.transform.scale(house, (50, 50))
        screen_main.blit(house, (x, y))

    # ОТРИСОВКА ВСПОМОГАТЕЛЬНОГО ОКНА (сетка + кружки)
    for row in range(rows):
        for col in range(cols):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen_grid, BLACK, (x, y, cell_size, cell_size), 1)  # Сетка

    # Почтальон (кружок)
    pygame.draw.circle(screen_grid, BLUE, (postman_x + cell_size // 2, postman_y + cell_size // 2), 20)

    # Домики (кружки)
    for x, y in houses:
        pygame.draw.circle(screen_grid, RED, (x + cell_size // 2, y + cell_size // 2), 20)

    # Обновление экранов
    pygame.display.flip()

pygame.quit()
