import pygame
import pygame.gfxdraw


import Objects
from DungeonEngine import DungeonGenerator
from Vex import Vex
from Line import Line
from MyMaths import rand2D
from DrawINFO import DrawINFO
from ParticleEngine import Emitter
from Ship import Ship
from Shot import Shot
from Asteroid import Asteroid
from Mind import Mind
from Background import Stars
from Sun import Sun


class Environment:
    useController = True
    player = None
    sun = None
    seed = 1
    gridsize = 10000
    world_edges = []
    edge_colors = []
    visible_creatures = []
    visible_objects = []
    image_buffer = []
    fov = 500
    lim = 0.0
    zbf = 5
    zdp = -300
    screen_height = None
    screen_width = None
    center_x = None
    center_y = None
    center = None
    screen = None
    interact = False
    error = 0
    renderDist = 400
    gpos = Vex(0, 0)
    LEFT = None
    RIGHT = None
    TOP = None
    BOTTOM = None
    bounds = []
   
    def __init__(self, screen_width=896, screen_height=504):
        Environment.screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
        Environment.screen_width = screen_width
        Environment.screen_height = screen_height
        Environment.center_x = screen_width / 2
        Environment.center_y = screen_height / 2
        Environment.center = Vex(Environment.center_x, Environment.center_y)
        # left
        Environment.LEFT = Line(Vex(0, 0), Vex(0, screen_height))
        # right
        Environment.RIGHT = Line(Vex(screen_width, 0), Vex(screen_width, screen_height))
        # top
        Environment.TOP = Line(Vex(0, 0), Vex(screen_width, 0))
        # bottom
        Environment.BOTTOM = Line(Vex(0, screen_height), Vex(screen_width, screen_height))
        ### Bind Screen ###
        Environment.bounds += [Environment.LEFT, Environment.RIGHT, Environment.TOP, Environment.BOTTOM]
        
        # Create SOl
        Environment.refreshSOL()

        Objects.Objects.init()

        DungeonGenerator.init()
        
        
        
    @staticmethod
    def getScreen():
        return Environment.screen
    
    @staticmethod
    def sw():
        return Environment.screen_width

    @staticmethod
    def sh():
        return Environment.screen_height

    @staticmethod
    def cx():
        return Environment.center_x

    @staticmethod
    def cy():
        return Environment.center_y

    @staticmethod
    def clear_visible():
        Environment.visible_creatures = []
    
    @staticmethod
    def add_visible(obj):
        Environment.visible_creatures += [obj]
    
    @staticmethod
    def clear_visible_objects():
        Environment.visible_objects = []
    
    @staticmethod
    def add_visible_object(obj):
        Environment.visible_objects += [obj]
        
    @staticmethod
    def clear_edges():
        Environment.world_edges = []
        Environment.image_buffer = []
        #Environment.edge_colors = []
    
    @staticmethod
    def add_edge(color, edge, width = 1, style = 0, height = 0 , fs=[0, 0]):  # (a point, b point)
        Environment.world_edges.append([style, color, edge, width, height, fs])
        #Environment.edge_colors.append()
    @staticmethod
    def add_image(img, pos):
        Environment.image_buffer += [image(img, pos)]
        
    @staticmethod
    def draw():
        Environment.image_buffer.sort(key=lambda image: image.z)
        for i in Environment.image_buffer:
            Environment.screen.blit(i.img, i.pos)
        for e in Environment.world_edges:  
            if e[0] == 0:
                pygame.draw.line(Environment.getScreen(), e[1], e[2][0], e[2][1], e[3])
                #pygame.gfxdraw.line(Environment.getScreen(), int(e[2][0][0]), int(e[2][0][1]), int(e[2][1][0]), int(e[2][1][1]), e[1])
            if e[0] == 1:
                pygame.draw.polygon(Environment.getScreen(), e[1], ((e[2][0][0], e[2][0][1]), (e[2][1][0], e[2][1][1]), (e[2][1][0], e[2][1][1]+e[4]*e[5][1]), (e[2][0][0], e[2][0][1]+e[4]*e[5][0])), e[3])
                #pygame.gfxdraw.polygon(Environment.getScreen(), ((e[2][0][0], e[2][0][1]), (e[2][1][0], e[2][1][1]), (e[2][1][0], e[2][1][1]+e[4]*e[5][1]), (e[2][0][0], e[2][0][1]+e[4]*e[5][0])), e[1])
            
            if e[0] == 2:
                #print(e[2])
                try:
                    pygame.draw.polygon(Environment.getScreen(), e[1], e[2], e[3])
                except:
                    pass
                #pygame.gfxdraw.polygon(Environment.getScreen(), e[2], e[1])

    @staticmethod
    def inScreen( point):
        if point[0] < 0-Environment.error or point[0] > Environment.screen_width+Environment.error:
            return False
        elif point[1] < 0-Environment.error or point[1] > Environment.screen_height+Environment.error:
            return False
        return True
    @staticmethod
    def inScreen2( points):
        
        if points[0] <= 0-Environment.error or points[0] >= Environment.screen_width+Environment.error:
            return False
        elif points[1] <= 0-Environment.error or points[1] >= Environment.screen_height+Environment.error:
            return False
        return True
    @staticmethod
    def inDepth( ys):
        return ys<Environment.zbf and ys>Environment.zdp
    @staticmethod
    def vexInScreen( v):
        if v.X() <= 0 or v.X() >= Environment.screen_width:
            return False
        elif v.Y() <= 0 or v.Y() >= Environment.screen_height:
            return False
        return True
    
    @staticmethod
    def screenClip2(line):
        v1 = Vex(line[0][0], line[0][1])
        v2 = Vex(line[1][0], line[1][1])
        ln = Line(v1, v2)
        alt = False
        inSc = False
        
        for v in range(len(ln.seg)):
            if not Environment.vexInScreen(ln.seg[v]):
                for b in Environment.bounds:
                    o = b.find_intersection(ln)
                    if o:
                        ln.seg[v].assign(o)
                        alt = True
                        break
            else:
                inSc = True
        return (inSc, alt , ln.toList())
            
        
    @staticmethod
    def outCode(x, y):
        code = 0
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8
        if x<0:
            code |= LEFT
        elif x > Environment.screen_width:
            code |= RIGHT
        if y<0:
            code |= BOTTOM
        elif y > Environment.screen_height:
            code |= TOP
        
        return code
        
    @staticmethod
    def screenClip(l):
        x0, y0 = l[0]
        x1, y1 = l[1]
        
        code1 = Environment.outCode(x0, y0)
        code2 = Environment.outCode(x1, y1)
        ymax = Environment.screen_height
        xmax = Environment.screen_width
        ymin = 0
        xmin = 0
        
        accept = False
        
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8
        while True:
            if not (code1|code2):
                accept = True
                break
            elif (code1 & code2):
                break
            else:
                x = 0
                y = 0
                ocode = 0
                if code1:
                    ocode = code1
                else:
                    ocode = code2
                
                if (ocode & TOP):# {           // point is above the clip rectangle
                    x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                    y = ymax
                elif (ocode & BOTTOM):# { // point is below the clip rectangle
                    x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                    y = ymin
                elif (ocode & RIGHT):# {  // point is to the right of clip rectangle
                    y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                    x = xmax
                elif (ocode & LEFT):# {   // point is to the left of clip rectangle
                    y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                    x = xmin
                
                #// Now we move outside point to intersection point to clip
                #// and get ready for next pass.
                if (ocode == code1):
                    x0 = x
                    y0 = y
                    code1 = Environment.outCode(x0, y0)
                else:
                    x1 = x
                    y1 = y
                    code2 = Environment.outCode(x1, y1)
                
        return (accept, ((x0, y0), (x1, y1)))
        
    # Returns the X location of the mouse at Z_Depth
    @staticmethod
    def X_3D(Z_Depth, x):
        return -(x- Environment.center_x)/Environment.screen_width*(Z_Depth* float(Environment.screen_width/ Environment.center_x))
    
    # Returns the Y location of the mouse at Z_Depth
    @staticmethod
    def Y_3D(Z_Depth, y):
        return float(y- Environment.center_y)/Environment.screen_height*(Z_Depth* float(Environment.screen_height/ Environment.center_y))
    
    @staticmethod
    def XY_3D(Z_Depth, x, y):
        return (Environment.X_3D(Z_Depth, x), Environment.Y_3D(Z_Depth, y))

    @staticmethod
    def getSeed():
        return rand2D(Environment.gpos.x(), Environment.gpos.y(), Environment.seed)
        
    @staticmethod
    def updateGlobalPosition(localPosition):
        refresh = False
        if(localPosition.x() > Environment.gridsize):
            localPosition.setX( localPosition.x()-Environment.gridsize*2)
            Environment.gpos.setX(Environment.gpos.x()+1)
            refresh = True
        if(localPosition.x() < -Environment.gridsize):
            localPosition.setX( localPosition.x()+Environment.gridsize*2)
            Environment.gpos.setX(Environment.gpos.x()-1)
            refresh = True
        if(localPosition.y() > Environment.gridsize):
            localPosition.setY( localPosition.y()-Environment.gridsize*2)
            Environment.gpos.setY(Environment.gpos.y()+1)
            refresh = True
        if(localPosition.y() < -Environment.gridsize):
            localPosition.setY( localPosition.y()+Environment.gridsize*2)
            Environment.gpos.setY(Environment.gpos.y()-1)
            refresh = True
        if refresh:
            Environment.refreshSOL()
            
    @staticmethod
    def refreshSOL():
        Environment.sun = Sun((0, 0), Environment.getSeed())
    
    
    @staticmethod
    def update(cam):

        env = Environment
        env.clear_visible_objects()
        env.getScreen().fill((0, 0, 0))
        env.clear_edges()
        if not env.player.inatmosphere:
            cam.top = False
            Stars.update(cam)
            Asteroid.updateTempAsteroids(cam)
        else:
            cam.top = True
        #Objects.Update(cam)
        env.sun.update2(cam)
        Emitter.update(cam)
        Shot.update(cam)
        env.player.update(cam)
        Mind.update(cam)
        Ship.updateUnOccupied(cam)
        DrawINFO.update(cam)
        env.draw()
        
        
    @staticmethod
    def freeMouse():
        pygame.mouse.set_visible(1)
        pygame.event.set_grab(0)
    
    @staticmethod
    def lockMouse():
        pygame.mouse.set_visible(0)
        pygame.event.set_grab(1)
    
class image():
    def __init__(self, image, position):
        self.img = image
        self.pos = position.p2D()
        self.z = position.z()
