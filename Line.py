# Line

import math
import Vex

def Lines_Intersect(Ax, Ay, Bx, By, Cx, Cy, Dx, Dy):
    Rn = (Ay-Cy)*(Dx-Cx) - (Ax-Cx)*(Dy-Cy)
    Rd = (Bx-Ax)*(Dy-Cy) - (By-Ay)*(Dx-Cx)
    Intersection_AB = 0
    Intersection_CD = 0
    if Rd == 0: 
        return False
    else:
        Sn = (Ay-Cy)*(Bx-Ax) - (Ax-Cx)*(By-Ay)
        Intersection_AB = Rn / Rd
        Intersection_CD = Sn / Rd
        IX = Ax + Intersection_AB*(Bx-Ax)
        IY = Ay + Intersection_AB*(By-Ay)
    if Intersection_AB>0 and Intersection_AB<1 and Intersection_CD>0 and Intersection_CD<1:
        return (IX, IY)
    else:
        return False




    
def LineA(pa, pb):
    v1 = Vex.Vex(pa[0], pa[1])
    v2 = Vex.Vex(pb[0], pb[1])
    return Line(v1, v2)
 
def find_intersection( p0, p1, p2, p3 ) :
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0 : return None # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive : return None # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive : return None # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


    # collision detected

    t = t_numer / denom

    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]
    return intersection_point


class Line:
    def __init__(self, pa, pb):
        if isinstance(pa, Vex.Vex) and isinstance(pb, Vex.Vex):
            self.seg = [pa, pb]
        else:
            self.seg = [Vex.Vex(pa[0], pa[1]), Vex.Vex(pb[0], pb[1])]
     
    def Ax(self):return self.seg[0].x()
    def Ay(self):return self.seg[0].y()
    def Bx(self):return self.seg[1].x()
    def By(self):return self.seg[1].y()
    
    def x0(self):return self.seg[0].x()
    def y0(self):return self.seg[0].y()
    def x1(self):return self.seg[1].x()
    def y1(self):return self.seg[1].y()
    
    def swap(self):
        return Line(self.seg[1], self.seg[0])
    
    def selfSwap(self):
        t = self.seg[0]
        self.seg[0] = self.seg[1]
        self.seg[1] = t
    
    def toList(self):
        return [self.seg[0].X(), self.seg[0].Y()], [self.seg[1].X(), self.seg[1].Y()]
    
    def angle(self):
        return math.atan2(self.seg[0].y()-self.seg[1].y(), self.seg[0].x()-self.seg[1].x())
        
    def PointToLine2D(self, p):
       
        ab = self.seg[0].dist2D( self.seg[1])
        bp = self.seg[1].dist2D(p)
        pa = p.dist2D(self.seg[0])
        
        # get the triangle's semiperimeter
        semi = (ab+bp+pa) / 2.0

        # get the triangle's area
        area = math.sqrt( semi * (semi-ab) * (semi-bp) * (semi-pa) )
        
        # return closest distance P to AB
        return (2.0 * (area/ab))
    
    

    def find_intersection(self, ln):
        p0 = self.seg[0].pos
        p1 = self.seg[1].pos
        p2 = ln.seg[0].pos
        p3 = ln.seg[1].pos
        s10_x = p1[0] - p0[0]
        s10_y = p1[1] - p0[1]
        s32_x = p3[0] - p2[0]
        s32_y = p3[1] - p2[1]

        denom = s10_x * s32_y - s32_x * s10_y

        if denom == 0 : return None # collinear

        denom_is_positive = denom > 0

        s02_x = p0[0] - p2[0]
        s02_y = p0[1] - p2[1]

        s_numer = s10_x * s02_y - s10_y * s02_x

        if (s_numer < 0) == denom_is_positive : return None # no collision

        t_numer = s32_x * s02_y - s32_y * s02_x

        if (t_numer < 0) == denom_is_positive : return None # no collision

        if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


        # collision detected

        t = t_numer / denom

        intersection_point = Vex.Vex( p0[0] + (t * s10_x), p0[1] + (t * s10_y) )
        return intersection_point
        
    def __str__(self):
        return ("p1:"+str(self.seg[0])+" p2:"+str(self.seg[1]))
        
    def pDistance(self, pv) :
        x, y = self.seg[0].p2D()
        x1, y1 = self.seg[1].p2D()
        x2, y2 = pv.p2D()
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1
        if (len_sq != 0): #//in case of 0 length line
            param = dot #/ len_sq;

        xx, yy = 0, 0

        if (param < 0):
            xx = x;
            yy = y;
        
        elif (param > 1):
            xx = x1
            yy = y1
        
        else :
            xx = x + param * C
            yy = y + param * D
        

        dx = x - xx
        dy = y - yy
        return (math.sqrt(dx * dx + dy * dy), Vex.Vex(xx, yy))

    def ClosestPointOnLine(self , vPoint ):
        vA = self.seg[0]
        vB = self.seg[1]
        vVector1 = vPoint - vA;
        vVector2 = (vB - vA).normalize()
     
        d = vA.dist2D( vB)
        t = vVector2.dot( vVector1)
     
        if (t <= 0):
            return vA
     
        if (t >= d):
            return vB
     
        vVector3 = vVector2 * t
     
        vClosestPoint = vA + vVector3
     
        return vClosestPoint

    def side(self, p):
        v1 = self.seg[0]-self.seg[1]
        v2 = self.seg[1]-p
        xp = v1.x()*v2.y() - v1.y()*v2.x()  # Cross product
        return xp
