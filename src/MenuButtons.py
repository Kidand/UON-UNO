import pygame

pygame.init()


# create button class
class MenuButton:
    def __init__(self, x, y, image, scale, image_glow):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
        width2 = image_glow.get_width()
        height2 = image_glow.get_height()
        self.image_glow = pygame.transform.scale(image_glow, (int(width2 * scale), int(height2 * scale)))

    def draw(self, screen):
        boolean_value = False
        mouse_point = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_point):  # is mouse cursor colliding with point on button
            screen.blit(self.image_glow, (self.rect.x - 15, self.rect.y - 15))
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:  # for left click
                self.click = True
                boolean_value = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return boolean_value
