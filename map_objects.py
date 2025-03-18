import pygame


class MapObject:
    def __init__(self, position, cell_size, id=None):
        self.rect = pygame.Rect(position[0], position[1], cell_size, cell_size)
        self.id = id

    def get_center(self):
        return self.rect.center

    def draw(self, surface):
        raise NotImplementedError("Метод draw должен быть определён в подклассах.")

class House(MapObject):
    def __init__(self, image_path, position, cell_size, id=None):
        super().__init__(position, cell_size, id)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Waypoint(MapObject):
    def __init__(self, position, cell_size, id=None):
        super().__init__(position, cell_size, id)

    def draw(self, surface):
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
        pass

# Скорость почтальона
class Postman(House):
    def __init__(self, image_path, position, cell_size, id=None):
        super().__init__(image_path, position, cell_size, id)
        self.rect = self.image.get_rect(topleft=position)
        self.path = []

    def set_path(self, path):
        self.path = path

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dt):
        pass