import math
import random

def rand2D(x, y, seed = None):
    if not seed:
        rnd = random.Random()
    else:
        rnd = random.Random(seed)
    rnd2 = random.Random(rnd.randint(1,123456789012345678901234567890)+int(x))
    rnd3 = random.Random(rnd2.randint(1,123456789012345678901234567890)+int(y))
    return rnd3.uniform(-1, 1)

def rand2Dinst(x, y, rnd1):
    rnd2 = random.Random(rnd1.uniform(-1, 1)+x)
    rnd3 = random.Random(rnd2.uniform(-1, 1)+y)
    return rnd3.uniform(-1, 1)
    
def sgn(val):
    rntval = -1
    if val > 0:rntval = 1
    if val == 0.0:rntval = 0
    return rntval
    
def sign(val):
    rntval = -1
    if val > 0:rntval = 1
    if val == 0.0:rntval = 0
    return rntval
    
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    
def rotate2d(pos, angle_rad):
    x, y = pos
    s, c = math.sin(angle_rad), math.cos(angle_rad)
    return x * c - y * s, y * c + x * s

def hex_corner(sides = 10, size = 2):
    hex_list = []
    for i in range(sides):
        angle_deg = (360 / sides) * i + 30
        angle_rad = 3.14159265359 / 180 * angle_deg
        x = 0 + size * math.cos(angle_rad)
        y = 0 + size * math.sin(angle_rad)
        hex_list.append([x, y, 1])
    return hex_list




global __SPHERICAL_BANK__
__SPHERICAL_BANK__ = [0.0, 0.0, 0.0, 0.0, 0.0]

def Spherical(x, y, z, length):
    zen = math.atan2(math.sqrt(x*x+y*y), z)
    azi = math.atan2(y, x)
    __SPHERICAL_BANK__[0] = math.sin(zen)
    __SPHERICAL_BANK__[1] = math.cos(zen)
    __SPHERICAL_BANK__[2] = math.sin(azi)
    __SPHERICAL_BANK__[3] = math.cos(azi)
    __SPHERICAL_BANK__[4] = length
    
def Spherical_X():
    return __SPHERICAL_BANK__[4] * __SPHERICAL_BANK__[0] * __SPHERICAL_BANK__[3]
def SphericalX(dist):
    return dist * __SPHERICAL_BANK__[0] * __SPHERICAL_BANK__[3]

def Spherical_Y():
    return __SPHERICAL_BANK__[4] * __SPHERICAL_BANK__[0] * __SPHERICAL_BANK__[2]
def SphericalY(dist):
    return dist * __SPHERICAL_BANK__[0] * __SPHERICAL_BANK__[2]

def Spherical_Z():
    return __SPHERICAL_BANK__[4] * __SPHERICAL_BANK__[1]
def SphericalZ(dist):
    return dist * __SPHERICAL_BANK__[1]

#
#;#Region	Color Gradient maker
#Restore Planet
#Global DEPTH = 256
#Dim GradientR%(0),GradientG%(0),GradientB%(0),Percent#(0),Red%(0),Green%(0),Blue%(0)
#CreateGradient(10,DEPTH)
#
#.Planet
#Data   0.0,255,255,255   ; white: snow
#Data   20.0,179,179,179   ; grey: rocks
#Data  30.0,153,143, 92   ; brown: tundra
#Data  50.0,115,128, 77   ; light green: veld
#Data  80.0, 42,102, 41   ; green: grass
#Data  87.0,255,246,143   ; gold:Beach
#Data  93.0, 69,108,118   ; light blue: shore
#Data  96.0, 17, 82,112   ; blue: shallow water
#Data  98.0,  9, 62, 92   ; dark blue: water
#Data 100.0,  2, 43, 68   ; very dark blue: deep water
#
#;Color Gradient
#Function CreateGradient(colors%,steps%)
#	
#	Dim GradientR(steps),GradientG(steps),GradientB(steps),Percent(colors),Red(colors),Green(colors),Blue(colors)
#	
#	Local i%,pos1%,pos2%,pdiff%
#	Local rdiff%,gdiff%,bdiff%
#	Local rstep#,gstep#,bstep#
#	Local counter%=1
#	
#    ; read color codes
#	For i=1 To colors : Read Percent(i),Red(i),Green(i),Blue(i) : Next
#	
#    ; calculate gradient
#	While counter<colors
#		
#        ; transform percent value into step position
#		pos1%=Percent(counter)*steps/100
#		pos2%=Percent(counter+1)*steps/100
#		
#        ; calculate position difference
#		pdiff%=pos2-pos1
#		
#        ; calculate color difference
#		rdiff%=Red(counter)-Red(counter+1)
#		gdiff%=Green(counter)-Green(counter+1)
#		bdiff%=Blue(counter)-Blue(counter+1)
#		
#        ; calculate color steps
#		rstep#=rdiff*1.0/pdiff
#		gstep#=gdiff*1.0/pdiff
#		bstep#=bdiff*1.0/pdiff
#		
#        ; calculate "in-between" color codes
#		For i=0 To pdiff
#			
#			GradientR(pos1+i)=Int(Red(counter)-(rstep*i))
#			GradientG(pos1+i)=Int(Green(counter)-(gstep*i))
#			GradientB(pos1+i)=Int(Blue(counter)-(bstep*i))
#			
#		Next
#		
#        ; increment counter
#		counter=counter+1
#		
#	Wend
#	
#End Function
#
#;#End Region
#
#;#region Mesh Deformation
#Global VertXBank = CreateBank()
#Global VertYBank = CreateBank()
#Global VertZBank = CreateBank()
#
#Function InitMeshDeform(Mesh%)
#	; monkey with the verts
#	as1=GetSurface(Mesh,1)
#	; record the locations of the verts
#	VC = CountVertices(as1)
#	ResizeBank (VertXBank , vc*4)
#	ResizeBank (VertYBank , vc*4)
#	ResizeBank (VertZBank , vc*4)
#	For n=0 To VC-1
#		PokeFloat (VertXBank,n*4,VertexX#(as1,n))
#		PokeFloat (VertYBank,n*4,VertexY#(as1,n))
#		PokeFloat (VertZBank,n*4,VertexZ#(as1,n))
#	Next
#End Function
#
#Function MeshDeform(Image,Mesh%,Size,Seed,MinOctaves,MaxOctaves,Multiplyer#,z#,Scale#)
#	; monkey with the verts
#	as1=GetSurface(Mesh,1)
#	IS = TextureWidth(Image)
#	IB = TextureBuffer(Image)
#	
#	LockBuffer IB
#	
#	VC = CountVertices(as1)
#		
#	For n= nnn To vc-1
#		;get UV coordinates
#		u# = VertexU#(as1,n)*IS-1
#		v# = VertexV#(as1,n)*IS-1
#		
#		;get 3D Perlin Noise coordinates
#		VX# = PeekFloat (VertXBank,n*4)
#		VY# = PeekFloat (VertYBank,n*4)
#		VZ# = PeekFloat (VertZBank,n*4)
#		
#		v1# = (VX#+z#)*Scale#
#		v2# = (VY#+z#)*Scale#
#		v3# = (VZ#+z#)*Scale#
#		
#		;Get Perlin 3D noise at 3D Perlin Noise coordinates
#		pn# = Perlin3D#(v1#,v2#,v3#,Size,Seed,MinOctaves,MaxOctaves)
#		If pn# < 0 Then pn# = 0		;Limit Noise to 0 or greater
#		col = Floor(255 - pn#*255)	;Convert Perlin noise to colorGradient
#		If col < 0 Then col = 0		;limit color
#		If col > 255 Then col = 255 ;limit color
#		argb = Get_ARGB_From(GradientR(col),GradientG(col),GradientB(col));Convert color to ARGB
#		WritePixelFast u,v,argb,IB	;Write pixel to Texture
#		
#		
#		Spherical(VX#,VY#,VZ#,1+pn#*Multiplyer)	;Calculate Spherical vector
#		xm# = Spherical_X()	;Get Spherical x vector
#		ym# = Spherical_Y() ;Get Spherical y vector
#		zm# = Spherical_Z()	;Get Spherical z vector
#		
#		VertexCoords as1,n,xm#,ym#,zm#
#		
#	Next
#	
#	UnlockBuffer IB
#	
#End Function
#
#;#end region
#
#Function Get_ARGB_From(r,g,b):		Return b Or(g Shl 8)Or(r Shl 16):	End Function
