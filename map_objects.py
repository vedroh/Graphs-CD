import pygame


class MapObject:
    def __init__(self, position, cell_index, cell_size, id=None):
        self.rect = pygame.Rect(position[0], position[1], cell_size, cell_size)
        self.id = id
        self.position = position
        self.cell_index = cell_index

    def get_center(self):
        return self.rect.center

    def draw(self, surface):
        raise NotImplementedError("Метод draw должен быть определён в подклассах.")

class House(MapObject):
    def __init__(self, image_path, position, cell_index, cell_size, id=None):
        super().__init__(position, cell_index, cell_size, id)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Waypoint(MapObject):
    def __init__(self, position, cell_index, cell_size, id=None):
        super().__init__(position, cell_index, cell_size, id)

    def draw(self, surface):
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
        pass

class Postman(House):
    def __init__(self, image_path, position, cell_index, cell_size, id=None):
        super().__init__(image_path, position, cell_index, cell_size, id)
        self.rect = self.image.get_rect(topleft=position)
        self.path = []
        self.speed = 30
        self.next_index = 1
        self.current_position = pygame.Vector2(self.position)


    def set_path(self, path):
        self.path = path

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dt):
        if self.next_index >= len(self.path):
            return
        target = pygame.Vector2(self.path[self.next_index])
        direction = (target - self.current_position).normalize()
        distance_to_target = (target - self.current_position).length()
        if self.speed * dt >= distance_to_target:
            self.current_position = target
            self.next_index += 1
        else:
            self.current_position += (self.speed * dt) * direction
        self.rect.topleft = (round(self.current_position.x), round(self.current_position.y))

