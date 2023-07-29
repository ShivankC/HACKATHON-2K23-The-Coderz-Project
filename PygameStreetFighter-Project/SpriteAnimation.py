import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, sprite_type, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        if sprite_type == "idle":
            image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
            print("blah")
        if sprite_type == "move": 
            image.blit(self.sheet, (0, 48), ((frame * width), 0, width, height))
            print ("0hello")
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image