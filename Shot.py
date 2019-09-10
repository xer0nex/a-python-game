"""
    Shot
    todo:
    1) use a que of shots
    
"""
import math
from operator import add
import Environment
from Vex import Vex
import Mind
import Planets
import Asteroid
import Sun
import Player

# shot
class Shot:
    
    shots = []
    verts = [
            [[.5, .5], [ .5, -.5], [-.5, -.5],[-.5, .5]], 
            [[.5, .5], [ -.5, .5], [0.0, -.5]], 
            [[.5, .5], [ -.5, .5], [0.0, 0.0], [.5, -.5], [-.5, -.5], [0.0, 0.0]], 
            [[.5,.25], [ -.5, .25], [0.0, -.5], [.5, -.25], [-.5, -.25], [0.0, .5]], 
            [[.5, .5], [.5,-150.5], [-.5, -150.5],[-.5, .5]],
            ]
    shape_edges = [
                  [[0, 1], [1, 2], [2, 3], [3, 0]], 
                  [[0, 1], [1, 2], [2, 0]], 
                  [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]], 
                  [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]], 
                  [[0, 1], [1, 2], [2, 3], [3, 0]],
                  ]
                  
    # initialize shot
    def __init__(self, ant, pos=[0, 0, 0], rot=[0.0, 0.0, 0.0], scale=[1, 1, 1], angle_rad=0, speed=1, damage=0, shape=0, color=[255, 0, 0], offset = -1, dst=1):
        tv = Vex(pos[0], pos[1])
        self.source = ant
        self.pos = tv.selfAdd2D(math.sin(angle_rad)*offset, math.cos(angle_rad)*offset)
        self.lpos = Vex(0, 0)
        self.rot = [0.0, 0.0, 0.0]
        self.scale = Vex(scale[0], scale[1], scale[2])
        self.rotation = rot
        self.angle_rad = angle_rad
        self.speed = speed
        self.damage = damage
        self.shape = shape
        self.color = color
        self.dst = dst
        self.projectedPoints = [(0, 0) for x in Shot.verts[self.shape]]
        self.shots.extend([self])
    
    # update shot
    @staticmethod
    def update(cam):
        env = Environment.Environment
        for sh in reversed(Shot.shots):
            sh.lpos = sh.pos.copy()
            sh.pos.setX( sh.pos.x() - math.sin(sh.angle_rad)*sh.speed*cam.delta)
            sh.pos.setY( sh.pos.y() - math.cos(sh.angle_rad)*sh.speed*cam.delta)
            
            sh.rot = list(map(add, sh.rot, sh.rotation))
            # this should be less of a test, need to test for planet collision as well
            if not Player.Player.testShotHit(sh) and not Planets.Planets.testShotHit(sh) and not Mind.Mind.testShotHit(sh) and not Asteroid.Asteroid.testShotHit(sh) and not Sun.Sun.testShotHit(sh) and cam.pos.dist2D(sh.pos)<sh.dst:
                
                for i, p in enumerate(Shot.verts[sh.shape]):
                    v = Vex(p[0], p[1])
                    v = (v * sh.scale).rotate2dXY(sh.rot[1]-sh.angle_rad).rotate2dYZ(0, sh.rot[0])-cam.pos+sh.pos
                    v = v.rotate2dXY(cam.rotSC[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])
                    f = env.fov / (v.z()+.000000001)
                    if(f < env.lim):
                        f = 1000
                    v = v * f + env.center
                    sh.projectedPoints[i] = v.p2D()
      
                env.add_edge(sh.color, sh.projectedPoints, 1, 2)
            else:
                Shot.shots.remove(sh)


                # update shot

    @staticmethod
    def update_in_dungeon(cam):
        env = Environment.Environment

        for sh in reversed(Shot.shots):
            sh.lpos = sh.pos.copy()
            sh.pos.setX(sh.pos.x() - math.sin(sh.angle_rad) * (sh.speed * cam.delta))
            sh.pos.setY(sh.pos.y() - math.cos(sh.angle_rad) * (sh.speed * cam.delta))

            sh.rot = list(map(add, sh.rot, sh.rotation))
            # this should be less of a test, need to test for planet collision as well
            d = cam.pos.dist2D(sh.pos)
            #print(str(sh.speed)+'   '+str(cam.pos)+'  '+str(sh.lpos)+'   '+str(sh.pos) + '   dist: '+str(d)+'     lim: '+str(sh.dst))
            if not Player.Player.testShotHit(sh) and d < sh.dst:

                for i, p in enumerate(Shot.verts[sh.shape]):
                    v = Vex(p[0], p[1])
                    v = (v * sh.scale).rotate2dXY(sh.rot[1] - sh.angle_rad)\
                            .rotate2dYZ(0,sh.rot[0]) - cam.pos + sh.pos
                    v = v.rotate2dXY(-cam.rot[0]).rotate2dYZ(cam.mov[2], cam.rotSC[1])
                    f = env.fov / (v.z() + .000000001)
                    if (f < env.lim):
                        f = 1000
                    v = v * f + env.center
                    sh.projectedPoints[i] = v.p2D()

                env.add_edge(sh.color, sh.projectedPoints, 0, 2)
            else:

                Shot.shots.remove(sh)

                
