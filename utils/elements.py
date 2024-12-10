import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        image_path,
        text="",
        font_path="./font/LovelyKids-gxly4.ttf",
        action=None,
    ):
        # Load the image and font
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.font = pygame.font.Font(font_path if font_path else None, 35)
        self.action = action if action else lambda: None

        # Resize image if it's too large (optional)
        max_width = 160
        if self.original_image.get_width() > max_width:
            aspect_ratio = (
                self.original_image.get_height() / self.original_image.get_width()
            )
            new_height = int(max_width * aspect_ratio)
            self.original_image = pygame.transform.scale(
                self.original_image, (max_width, new_height)
            )

        # Create a rect and hover_rect
        self.rect = self.original_image.get_rect(center=(x, y))
        self.hover_rect = self.rect.inflate(-5, -5)

        # Render text
        self.text_surface = self.font.render(text, True, (0, 0, 0))

        # Rotation variables
        self.angle = 0
        self.hover = False

    def draw(self, surface):
        # Blit the base image
        if self.hover:
            # Update angle with oscillation
            self.angle = 10

            # Rotate the image
            rotated_image = pygame.transform.rotate(self.original_image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            surface.blit(rotated_image, rotated_rect)

        else:
            # Reset angle when not hovering
            self.angle = 0
            # Draw the original image and text when not hovering
            surface.blit(self.original_image, self.rect)

        # Center the text on the button
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def is_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        return self.hover

    def on_click(self, event):
        if self.hover_rect.collidepoint(event.pos):
            self.action()
