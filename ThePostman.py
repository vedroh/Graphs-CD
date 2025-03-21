import heapq

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

        self.start_button = pygame.Rect(self.window_width//2 - 50, self.height + 55, 100, 30)
        self.start_button_color = (0, 200, 0)
        self.start_button_hover = False

        self.objects_by_id = {}
        self.waypoints = []
        self.connections = []
        self.houses = []
        self.postman = None
        self.grid = None

        if map_file:
            self.load_map(map_file)
        else:
            # Случайная генерация карты
            '''self.grid = Grid(self.width, self.height, self.window_width, self.window_height,
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
            self.connections = []'''
            pass

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
        self.objects_by_id = {}
        for house in self.houses:
            if house.id is not None:
                self.objects_by_id[house.id] = house
        for wp in self.waypoints:
            if wp.id is not None:
                self.objects_by_id[wp.id] = wp
        # Отрисовка дорог между объектами
        for connection in self.connections:
            from_id = connection.get("from")
            to_id = connection.get("to")
            if from_id in self.objects_by_id and to_id in self.objects_by_id:
                start_obj = self.objects_by_id[from_id]
                end_obj = self.objects_by_id[to_id]
                pygame.draw.line(self.screen, self.ROAD_COLOR,
                                 start_obj.get_center(), end_obj.get_center(), 4)
                # Отрисовка расстояний
                mid_x = (start_obj.get_center()[0] + end_obj.get_center()[0]) // 2
                mid_y = (start_obj.get_center()[1] + end_obj.get_center()[1]) // 2
                distance_text = str(int(((start_obj.cell_index[0] - end_obj.cell_index[0]) ** 2 + (start_obj.cell_index[1] - end_obj.cell_index[1]) ** 2)**0.5))
                text_surface = self.font.render(distance_text, True, self.FONT_COLOR)
                self.screen.blit(text_surface, (mid_x, mid_y))

    def create_graph(self):
        graph = {}
        for obj in self.objects_by_id:
            graph[obj] = {}
        for connection in self.connections:
            from_id = connection.get("from")
            to_id = connection.get("to")
            distance = int(((self.objects_by_id[from_id].cell_index[0] - self.objects_by_id[to_id].cell_index[0]) ** 2 + (self.objects_by_id[from_id].cell_index[1] - self.objects_by_id[to_id].cell_index[1]) ** 2)**0.5)
            graph[from_id][to_id] = distance
            graph[to_id][from_id] = distance
        return graph

    def djikstra(self, graph, houses, start):
        total_path = []
        route = []
        # Пока остаются дома, которые нужно посетить
        while houses:
            # Инициализируем словари расстояний и предков для восстановления пути
            distances = {vertex: float('inf') for vertex in graph}
            distances[start] = 0
            pre = {vertex: None for vertex in graph}

            # Множество непосещённых вершин
            unvisited = set(graph.keys())
            priority_queue = [(0, start)]

            # Основной цикл алгоритма Дейкстры
            while priority_queue:
                current_distance, current_vertex = heapq.heappop(priority_queue)
                if current_vertex not in unvisited:
                    continue
                unvisited.remove(current_vertex)
                for neighbor, weight in graph[current_vertex].items():
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        pre[neighbor] = current_vertex
                        heapq.heappush(priority_queue, (distance, neighbor))

            # Поиск дома (из списка houses) с кратчайшим расстоянием от start
            next_house = None
            min_distance = float('inf')
            for house in houses:
                if distances[house] < min_distance and house != start:
                    min_distance = distances[house]
                    next_house = house

            # Если ни один дом не достижим, можно завершать выполнение
            if next_house is None:
                break

            route = []
            # Восстанавливаем маршрут от start до найденного дома
            current = next_house
            while current is not None:
                route.append(current)
                current = pre[current]
            route.reverse()  # чтобы путь шёл от start до next_house

            # Удаляем все дома из маршрута, если они присутствуют в списке houses
            for node in route:
                if node in houses:
                    houses.remove(node)

            # Добавляем найденный маршрут к общему пути
            total_path.extend(route[:-1])

            # Обновляем start для следующей итерации
            start = next_house

        total_path.append(route[-1])

        return [self.objects_by_id[house].position for house in total_path]



    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()
            self.start_button_hover = self.start_button.collidepoint(mouse_pos)
            self.start_button_color = (0, 220, 0) if self.start_button_hover else (0, 200, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.start_button_color = (0, 100, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.start_button_color = (0, 220, 0)
                        if self.start_button_hover:
                            self.postman.set_path(self.djikstra(self.create_graph(), [house.id for house in self.houses], "P"))
                            self.postman.start_moving()

            self.screen.fill(self.WHITE)
            pygame.draw.rect(self.screen, self.start_button_color, self.start_button)
            text = self.font.render("Пуск", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.start_button.center)
            self.screen.blit(text, text_rect)
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