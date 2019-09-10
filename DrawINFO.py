# draw text at point for duration
import pygame
import Environment
from MyMaths import rotate2d

class DrawINFO:
    infos = []
    def __init__(self, x, y, z, text, color = [255, 0, 0]):
        DrawINFO.infos.extend([self])
        self.x = x
        self.y = y
        self.z = z
        self.text = text
        self.color = color
        self.timer = pygame.time.get_ticks()
        pass
    
    @staticmethod
    def update(cam):
        env = Environment.Environment
        for i in reversed(DrawINFO.infos):
            i.z -= .1
            if pygame.time.get_ticks()-i.timer <= 1000:
                x = i.x
                y = i.y
                z = i.z
                myfont = pygame.font.SysFont("monospace", 15)
                
                x -= cam.pos.X()
                y -= cam.pos.Y()
                z -= cam.pos.Z()
                
                x, y = rotate2d((x, y), cam.rot[1])  # roll
                y, z = rotate2d((y + cam.mov[2], z), cam.rot[0])  # pitch

                #y, z = rotate2d((y, z), cam.rot[0])  # pitch

                f = env.fov / (z +.00000001)
                x, y = x * f, y * f
                point = [env.cx() + int(x), env.cy() + int(y)]
              
                label = myfont.render(str(i.text), 1, (255, 255, 0))
                if env.inScreen(point):
                    env.screen.blit(label, (point))
            else:
                DrawINFO.infos.remove(i)
                
