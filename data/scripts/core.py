import pygame 

def img(path, id, scale):
    img = pygame.image.load(f"{path}/{id}.png")
    img_h = img.get_height()
    img_w = img.get_width()
    img = pygame.transform.scale(img, (img_w * scale, img_h * scale))
    return img