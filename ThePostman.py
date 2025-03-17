import pygame
import random

pygame.init()

window_width = 600
window_height = 600

width, height = 500, 500 # field
cell_size = 50
rows = height // cell_size
cols = width // cell_size

indent_x = (window_width - width) // 2
indent_y = (window_height - height) // 2

# Цвета
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

used_coordinates = []

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Postman")


count_of_points = random.randint(3, 8)
points = []
for i in range(count_of_points):
    x = random.randint(0, cols - 1) * cell_size + indent_x
    y = random.randint(0, rows - 1) * cell_size + indent_y
    points.append((x, y))
    used_coordinates.append((x, y))

# # __FACTORY COORDINATES__
# x_factory = random.randint(0, cols - 2) * cell_size + indent_x
# y_factory = random.randint(0, rows - 2) * cell_size + indent_y
# if (x_factory, y_factory) not in used_coordinates:
#     used_coordinates.append((x_factory, y_factory))
#
#
#
# # __SCHOOL COORDINATES__
# x_school = random.randint(0, cols - 2) * cell_size + indent_x
# y_school = random.randint(0, rows - 2) * cell_size + indent_y
# if (x_school, y_school) not in used_coordinates:
#     used_coordinates.append((x_school, y_school))


running = True
while running:
    screen.fill(WHITE)

    # ПОЛЕ
    for row in range(width // cell_size):
        for col in range(height // cell_size):
            x = indent_x + col * cell_size
            y = indent_y + row * cell_size
            pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 1)

    # __POSTMAN__
    postman_start = pygame.image.load('почтальон стоит.png')
    postman_start = pygame.transform.scale(postman_start, (50, 50))
    screen.blit(postman_start, (cell_size, cell_size))


    # __HOUSES__
    for x, y in points:
        if x != 100 and y != 100:
            house = pygame.image.load('домик.png')
            house = pygame.transform.scale(house, (50, 50))
            screen.blit(house, (x, y))

    # # __FACTORY__
    # factory = pygame.image.load('завод.png')
    # factory = pygame.transform.scale(factory, (100, 100))
    # screen.blit(factory, (x_factory, y_factory))
    #
    # # __SCHOOL__
    # school = pygame.image.load('школа.png')
    # school = pygame.transform.scale(school, (150, 150))
    # screen.blit(school, (x_school, y_school))

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()

