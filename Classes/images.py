import pygame

image_cache = {}


def get_image(key):
    if key not in image_cache:
        image_cache[key] = pygame.image.load(key).convert_alpha()
    return image_cache[key]


resources = {
    'empty': "./images/sprite/charempty.png",
    'rock': "./images/charset/rock.png"
}