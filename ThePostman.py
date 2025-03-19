import pygame
import random
import json

from map_objects import *


class Grid:
    def __init__(self, width, height, window_width, window_height, cell_size, line_color):
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.indent_x = (window_width - width) // 2
        self.indent_y = (window_height - height) // 2
        self.line_color = line_color

    def draw(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.indent_x + col * self.cell_size
                y = self.indent_y + row * self.cell_size
                pygame.draw.rect(surface, self.line_color, (x, y, self.cell_size, self.cell_size), 1)


class Game:
    WHITE = (255, 255, 255)
    BLACK = (100, 100, 100)
    ROAD_COLOR = (150, 150, 150)
    FONT_COLOR = (0, 0, 0)

    def __init__(self, map_file=None):
        pygame.init()
        # Параметры окна
        self.window_width = 600
        self.window_height = 600
        # Значения по умолчанию для игрового поля
        self.width = 500
        self.height = 500
        self.cell_size = 50
        # Инициализация экрана и шрифта
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Postman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        if map_file:
            self.load_map(map_file)
        else:
            self.grid = Grid(self.width, self.height, self.window_width, self.window_height,
                             self.cell_size, self.BLACK)
            self.postman = Postman('assets/почтальон стоит.png', (self.cell_size, self.cell_size), self.cell_size)
            self.houses = []
            count_of_points = random.randint(3, 8)
            used_coordinates = []
            for _ in range(count_of_points):
                x_index = random.randint(0, self.grid.cols - 1)
                y_index = random.randint(0, self.grid.rows - 1)
                x = x_index * self.cell_size + self.grid.indent_x
                y = y_index * self.cell_size + self.grid.indent_y
                if (x, y) not in used_coordinates:
                    used_coordinates.append((x, y))
                    # Исключаем позицию почтальона
                    if (x, y) != (self.cell_size, self.cell_size):
                        self.houses.append(House('assets/домик.png', (x, y), (x_index, y_index), self.cell_size))
            self.waypoints = []
            self.connections = []

    def load_map(self, filename):
        data = None
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Ошибка чтения карты: {e}")
            return None
        if not data:
            print("Не удалось загрузить данные карты. Будет использована случайная генерация.")
            return
        # Инициализация игрового поля
        grid_data = data.get("grid", {})
        self.width = grid_data.get("width", self.width)
        self.height = grid_data.get("height", self.height)
        self.cell_size = grid_data.get("cell_size", self.cell_size)
        self.grid = Grid(self.width, self.height, self.window_width, self.window_height,
                         self.cell_size, self.BLACK)
        # Инициализация почтальона
        postman_data = data.get("postman", {})
        start_pos = postman_data.get("start_pos", [1, 1])
        postman_pixel_pos = ((start_pos[0] * self.cell_size) + self.grid.indent_x,
                             (start_pos[1] * self.cell_size) + self.grid.indent_y)
        self.postman = Postman('assets/почтальон стоит.png', postman_pixel_pos, (start_pos[0], start_pos[1]), self.cell_size, postman_data.get("id"))
        # Загрузка домов
        self.houses = []
        for house_data in data.get("houses", []):
            col, row = house_data["position"]
            pos = (col * self.cell_size + self.grid.indent_x, row * self.cell_size + self.grid.indent_y)
            self.houses.append(House('assets/домик.png', pos, (col, row), self.cell_size, id=house_data.get("id")))
        # Загрузка промежуточных точек
        self.waypoints = []
        for wp_data in data.get("waypoints", []):
            col, row = wp_data["position"]
            pos = (col * self.cell_size + self.grid.indent_x, row * self.cell_size + self.grid.indent_y)
            self.waypoints.append(Waypoint(pos, (col, row), self.cell_size, id=wp_data.get("id")))
        # Загрузка путей
        self.connections = data.get("connections", [])

    def draw_roads(self):
        objects_by_id = {self.postman.id: self.postman}
        for house in self.houses:
            if house.id is not None:
                objects_by_id[house.id] = house
        for wp in self.waypoints:
            if wp.id is not None:
                objects_by_id[wp.id] = wp
        # Отрисовка дорог между объектами
        for connection in self.connections:
            from_id = connection.get("from")
            to_id = connection.get("to")
            if from_id in objects_by_id and to_id in objects_by_id:
                start_obj = objects_by_id[from_id]
                end_obj = objects_by_id[to_id]
                pygame.draw.line(self.screen, self.ROAD_COLOR,
                                 start_obj.get_center(), end_obj.get_center(), 4)
                # Отрисовка расстояний
                mid_x = (start_obj.get_center()[0] + end_obj.get_center()[0]) // 2
                mid_y = (start_obj.get_center()[1] + end_obj.get_center()[1]) // 2
                distance_text = str(int(((start_obj.cell_index[0] - end_obj.cell_index[0]) ** 2 + (start_obj.cell_index[1] - end_obj.cell_index[1]) ** 2)**0.5))
                text_surface = self.font.render(distance_text, True, self.FONT_COLOR)
                self.screen.blit(text_surface, (mid_x, mid_y))

    def run(self):
        running = True
        # TODO: Удалить
        self.postman.set_path([(50, 50), (100, 50), (100, 100)])
        while running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.WHITE)
            self.grid.draw(self.screen)
            self.draw_roads()
            for house in self.houses:
                house.draw(self.screen)
            for wp in self.waypoints:
                wp.draw(self.screen)
            self.postman.move(dt)
            self.postman.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game(map_file="assets/map.json")
    game.run()