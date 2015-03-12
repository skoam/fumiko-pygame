import images
import pygame
from common import random_id, Position, Size


class GameObject:
    def __init__(self, name=None, position=None, size=None, image=None):
        default_name = "gameobject " + str(random_id())
        
        self.name = name if name is not None else default_name

        def sizeAndPosition():
          self.position = position if position is not None else Position(0, 0)
          self.size = size if size is not None else Size(0, 0)

        def define_image():
          if not image:
              self.image = images.get_image(images.resources["empty"])
          else:
              self.image = image

          self.image = pygame.transform.scale(self.image, (self.size.width, self.size.height))
          self.rect = pygame.Rect(self.position.x, self.position.y, self.size.width, self.size.height)
          self.color = False

        sizeAndPosition()
        define_image()

    def chimg(self, img):
        self.image = images.get_image(images.resources[img])

    def chscale(self, scale):
        self.image = pygame.transform.scale(self.image, (self.size.width * scale, self.size.height * scale))
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.width * scale, self.size.height * scale)
