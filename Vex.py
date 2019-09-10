# Vex lib
import math
import Environment
from MyMaths import sgn



def VecFromList(lst):
    sz = len(lst)
    if sz == 2:return Vex(lst[0], lst[1])
    if sz == 3:return Vex(lst[0], lst[1], lst[2])

class Vex:
    def __init__(self, x, y, z=0):
        self.pos = [x, y, z]
 
# Constructors 
    def copy(self):return Vex(self.pos[0], self.pos[1], self.pos[2])

# Set
    def set(self, x, y, z):self.pos[0] = x;self.pos[1] = y;self.pos[2] = z;return self
    def set2D(self, x, y):self.pos[0] = x;self.pos[1] = y;return self
    def setX(self, x):self.pos[0] = x;return self
    def setY(self, y):self.pos[1] = y;return self
    def setZ(self, z):self.pos[2] = z;return self
    def setVector(self, setter):self.set(setter.pos[0], setter.pos[1], setter.pos[2]);return self
    def assign(self, a):self.set(a.pos[0], a.pos[1], a.pos[2]);return self

# Get
    def Pos(self):return self.pos
    def x(self):return self.pos[0]
    def y(self):return self.pos[1]
    def z(self):return self.pos[2]
    def X(self):return self.pos[0]
    def Y(self):return self.pos[1]
    def Z(self):return self.pos[2]
    def getX(self):return self.pos[0]
    def getY(self):return self.pos[1]
    def getZ(self):return self.pos[2]
    def p2D(self):return [self.pos[0], self.pos[1]]

# Scalars
    def integer(self):return Vex(int(self.pos[0]), int(self.pos[1]), int(self.pos[2]))
    def scale(self, a):return Vex(self.pos[0] * a, self.pos[1] * a,  self.pos[2] * a)
    def offset(self, a):return Vex(self.pos[0] + a, self.pos[1] + a,  self.pos[2] + a)
    def selfScale(self, a):return self.set(self.pos[0] * a, self.pos[1] * a, self.pos[2] * a)
    def translate(self, x, y, z):self.pos[0] += x;self.pos[1] += y;self.pos[2] += z;return self
    def dot(self, a):return self.pos[0] * a.pos[0] + self.pos[1] * a.pos[1] + self.pos[2] * a.pos[2]
    def crossP(self, a):return self.pos[0] * a.pos[0] - self.pos[1] * a.pos[1] - self.pos[2] * a.pos[2]
    def length(self):return math.sqrt(self.pos[0] * self.pos[0] + self.pos[1] * self.pos[1] + self.pos[2] * self.pos[2])
    def sqrLength(self):return self.pos[0]**2 + self.pos[1]**2 + self.pos[2]**2
    def dist(self, a):return math.sqrt((self.pos[0] - a.pos[0])**2 + (self.pos[1] - a.pos[1])**2 + (self.pos[2] - a.pos[2])**2)
    def dist2D(self, a):return math.sqrt((self.pos[0] - a.pos[0])**2 + (self.pos[1] - a.pos[1])**2)
    def inverse(self):return Vex(-self.x(), -self.y(), -self.z())
    def project(self, a):return self*(a.dot( self) / self.dot( self))
    def cross(self, a):
        return Vex(self.pos[1]*a.pos[2] - self.pos[2]*a.pos[1],
                   self.pos[2]*a.pos[0] - self.pos[0]*a.pos[2],
                   self.pos[0]*a.pos[1] - self.pos[1]*a.pos[0])
    
    def normalize(self):
        l = self.length()
        if l > .0000001:
            l = 1.0/l
            return Vex(self.pos[0]*l, self.pos[1]*l, self.pos[2]*l)
        x_ = sgn(self.pos[0])
        y_ = sgn(self.pos[1])
        z_ = sgn(self.pos[2])
        if ((x_ != 0) or (y_!=0)or(z_!=0)):
            l = 1.0/math.sqrt(x_**2+y_**2+z_**2)
            return Vex(x_*l, y_*l, z_*l)
        return Vex(0, 0, 1)
    
    def selfNormalize(self):
        l = self.length()
        if l > .0000001:l = 1.0/l;return self.set( self.pos[0]*l, self.pos[1]*l, self.pos[2]*l)
        x_ = sgn(self.pos[0]);y_ = sgn(self.pos[1]);z_ = sgn(self.pos[2])
        if ((x_ != 0) or (y_!=0)or(z_!=0)):l = 1.0/math.sqrt(x_**2+y_**2+z_**2);return self.set(x_*l, y_*l, z_*l)
        return self.set( 0, 1, 0)
    def setLength(self, s):
        l = self.sqrLength()
        if l > .0000001:l = s/math.sqrt(l);return self.scale(l)
        self.pos[0] = sgn(self.pos[0]);self.pos[1] = sgn(self.pos[1]);self.pos[0] = sgn(self.pos[2])
        if ((self.pos[0] != 0) or (self.pos[1] != 0) or (self.pos[2] != 0)):l = 1.0/self.length();return self.scale(l)
        return self.set(0, s, 0)
        	
#		; Transform
#			; vs Vex
    def add(self, a):return Vex(self.pos[0] + a.pos[0], self.pos[1] + a.pos[1], self.pos[2] + a.pos[2])
    def selfAdd(self, a):return self.set(self.pos[0] + a.pos[0], self.pos[1] + a.pos[1], self.pos[2] + a.pos[2])
    def selfAdd2D(self, x, y):return self.set2D(self.pos[0] + x, self.pos[1] + y)
    def AddSelf(self, x, y, z):return self.set(self.pos[0] + x, self.pos[1] + y, self.pos[2] + z)
    def sub(self, a):return Vex(self.pos[0] - a.pos[0], self.pos[1] - a.pos[1], self.pos[2] - a.pos[2])
    def selfSub(self, a):return self.set(self.pos[0] - a.pos[0], self.pos[1] - a.pos[1], self.pos[2] - a.pos[2])
    def mul(self, a):return Vex(self.pos[0] * a.pos[0], self.pos[1] * a.pos[1], self.pos[2] * a.pos[2])
    def selfMul(self, a):return self.set(self.pos[0] * a.pos[0], self.pos[1] * a.pos[1], self.pos[2] * a.pos[2])
    def div(self, a):return Vex(self.pos[0] / a.pos[0], self.pos[1] / a.pos[1], self.pos[2] / a.pos[2])
    def selfDiv(self, a):return self.set(self.pos[0] / a.pos[0], self.pos[1] / a.pos[1], self.pos[2] / a.pos[2])
    def __add__(self, a):
        if isinstance(a, Vex):
            return Vex(self.pos[0] + a.pos[0], self.pos[1] + a.pos[1], self.pos[2] + a.pos[2])
        return self.offset(a)
    def __sub__(self, a):
        if isinstance(a, Vex):
            return Vex(self.pos[0] - a.pos[0], self.pos[1] - a.pos[1], self.pos[2] - a.pos[2])
        return self.offset(-a)
    def __mul__(self, a):
        if isinstance(a, Vex):
            return Vex(self.pos[0] * a.pos[0], self.pos[1] * a.pos[1], self.pos[2] * a.pos[2])
        return self.scale(a)
    def __div__(self, a):
        if isinstance(a, Vex):
            return Vex(self.pos[0] / a.pos[0], self.pos[1] / a.pos[1], self.pos[2] / a.pos[2])
        return self.scale(1.0/a)
    def __eq__(self, a):return (self.pos == a.pos)
    def __iadd__(self, a):return self.set(self.pos[0] + a.pos[0], self.pos[1] + a.pos[1], self.pos[2] + a.pos[2])
    def __isub__(self, a):return self.set(self.pos[0] - a.pos[0], self.pos[1] - a.pos[1], self.pos[2] - a.pos[2])
    def __imul__(self, a):return self.set(self.pos[0] * a.pos[0], self.pos[1] * a.pos[1], self.pos[2] * a.pos[2])
    def __idiv__(self, a):return self.set(self.pos[0] / a.pos[0], self.pos[1] / a.pos[1], self.pos[2] / a.pos[2])
    def __neg__(self):return Vex(-self.pos[0],-self.pos[1],-self.pos[2])
    def __str__(self):
        return str(self.pos)
    
    def ang2D(self, a):
        dx = self.X() - a.X()
        dy = self.Y() - a.Y()
        return math.atan2(dy,dx)
    
#    def rotate2d(pos, angle_rad):
#        x, y = pos
#        s, c = math.sin(angle_rad), math.cos(angle_rad)
#        return x * c - y * s, y * c + x * s
    def addVector(self, mag, angle_rad):
        self += Vex(math.sin(angle_rad)*mag, math.cos(angle_rad)*mag)
        return self
        
    def rotate2dXY(self,  angle_rad):
        if not isinstance(angle_rad, list):
            s, c = math.sin(angle_rad), math.cos(angle_rad)
        else:
            s, c = angle_rad
        return Vex(self.pos[0] * c - self.pos[1] * s, self.pos[1] * c + self.pos[0] * s, self.z())
        
    def rotate2dXZ(self,  angle_rad):
        if not isinstance(angle_rad, list):
            s, c = math.sin(angle_rad), math.cos(angle_rad)
        else:
            s, c = angle_rad
        return Vex(self.pos[0] * c - self.pos[2] * s, self.x(), self.pos[2] * c + self.pos[0] * s)
        
    def rotate2dYZ(self, offset, angle_rad):
        y = self.pos[1]+offset
        if not isinstance(angle_rad, list):
            s, c = math.sin(angle_rad), math.cos(angle_rad)
        else:
            s, c = angle_rad
        return Vex(self.x(), y * c - self.pos[2] * s, self.pos[2] * c + y * s)
    
#env, cam, self.pos, self.ang
    def projectedPos(self,  cam):
        env = Environment.Environment
        v = (Vex(0, 0, 0)- cam.pos+self).rotate2dXY(cam.rot[1]).rotate2dYZ(cam.mov[2], cam.rot[0])
        f = env.fov / (v.z() +.00000001)
        if(f < env.lim):
            f = 1000
        v = v * f
        if f < 0:f = 0
        if f >100:f = 100
        v.setZ(f)
        v += env.center
        if env.inScreen(v.p2D()):
            return (True, v)
        return (False, v)

#ZERO = Vex(0, 0)
#vs = []
#vs += [Vex(21, -2)]
#vs += [Vex(221, -2)]
#vs += [Vex(211, -2)]
#vs += [Vex(1, -2)]
#
#vs.sort(key = lambda x: x.dist2D(ZERO))
#
#for v in vs:
#    print (str(v))
