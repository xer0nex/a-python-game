
import random
import time
import math

class Noise:
 
    Limit=256
    PermutationBank = [None] * (Limit*2)
    GradientBank = [None] * (Limit*2)
    
    def __init__(self):
        
        # create a temp bank of values
        perm = list(range(1, Noise.Limit+1))
        
        # randomize the values
        for i in range(0, Noise.Limit):
            j = random.randint(0, Noise.Limit-1)
            t = perm[j]
            perm[j] = perm[i]
            perm[i] = t

        # fill PermutationBank and GradientBank
        for i in range(0, Noise.Limit):
            Noise.PermutationBank[i]=perm[i]
            Noise.PermutationBank[Noise.Limit+i] = perm[i]
            Noise.GradientBank[i] = random.uniform(-.7, .7)
            Noise.GradientBank[Noise.Limit+i] = random.uniform(-.7, .7)
            
        return

    @staticmethod
    def fade( t ): 
        s = t * t * t * (t * (t * 6 - 15) + 10)
        return s
    
    @staticmethod
    def lerp( t, a, b):
        z = a + t * (b - a)
        return z

    @staticmethod
    def SmoothNoise( x, y, z, seed=0):
        x = x + seed; y = y + seed; z = z + seed
        x1 = abs( math.floor(x) % (Noise.Limit-1) )    # FIND UNIT CUBE THAT
        y1 = abs( math.floor(y) % (Noise.Limit-1) )    # CONTAINS POINT.
        z1 = abs( math.floor(z) % (Noise.Limit-1) )    #
        x = x - math.floor( x )                        # FIND RELATIVE X,Y,Z
        y = y - math.floor( y )                        # OF POINT IN CUBE.
        z = z - math.floor( z )                        #
        u = Noise.fade(x)                       # COMPUTE FADE CURVES
        v = Noise.fade(y)                       # FOR EACH OF x,y,z.
        w = Noise.fade(z)                       #
        a  = Noise.PermutationBank[x1] + y1     #
        aa = Noise.PermutationBank[a] + z1      #
        ab = Noise.PermutationBank[a + 1] + z1  # HASH COORDINATES OF
        b  = Noise.PermutationBank[x1 + 1] + y1 #
        ba = Noise.PermutationBank[b] + z1      #
        bb = Noise.PermutationBank[b+1] + z1    # THE 8 CUBE CORNERS,
        
        g1 = Noise.GradientBank[bb+1]
        g2 = Noise.GradientBank[ab+1]
        g3 = Noise.GradientBank[ba+1]
        g4 = Noise.GradientBank[aa+1]
        g5 = Noise.GradientBank[bb]
        g6 = Noise.GradientBank[ab]
        g7 = Noise.GradientBank[ba]
        g8 = Noise.GradientBank[aa]
        l1 = Noise.lerp(u, g2, g1)
        l2 = Noise.lerp(u, g4, g3)
        l3 = Noise.lerp(v, l2, l1)
        l4 = Noise.lerp(u, g6, g5)
        l5 = Noise.lerp(u, g8, g7)
        l6 = Noise.lerp(v, l5, l4)
        l7 = Noise.lerp(w, l6, l3)
        return l7
    
    @staticmethod
    def Millisecs():
        return int(round(time.time() * 1000))
    
    @staticmethod
    def Perlin3D(x, y, z, size=64, seed=0, MinOctaves=4 , MaxOctaves=10):
        if seed == 0:
            seed = Noise.MilliSecs()
            
        x = x + seed
        y = y + seed
        z = z + seed
        # Set the initial value and initial size
        value = 0.0
        initialSize = size
        
        for i in range(MinOctaves):
            size = size/2
        
        # Add finer and finer hues of smoothed noise together
        while (size >= 1.0) and MaxOctaves > MinOctaves:
    
            value = value + Noise.SmoothNoise(x / size, y / size, z / size, seed) * size
            size = size / 2.0
            MaxOctaves = MaxOctaves - 1
        
        
        # Return the result over the initial size
        return  (value / initialSize)


#           THIS IS NOT GOOD, REWRITE FOR IMAGE?
#    @staticmethod
#    def Perlin2D( Image , ImageType , Seed , z# , MinOctaves , MaxOctaves )
#        If ImageType = 0 Then IB = ImageBuffer(Image):size = ImageWidth(Image)
#        If ImageType = 0 Then LockBuffer IB
#        If ImageType = 1 Then IB = TextureBuffer(Image):size = TextureWidth(Image)
#        If ImageType = 1 Then LockBuffer IB
#        For x = 0 To size-1
#            For y = 0 To size-1
#                col# = ( Perlin3D#( Float x, Float y , Float z , size , Seed, MinOctaves , MaxOctaves )) * (255/2)
#                If col < 0 Then col = 0
#                If col > 255 Then col = 255
#                rgb = Get_ARGB_From(col,col,col)
#                WritePixelFast x,y,rgb,IB
#            Next
#        Next
#        UnlockBuffer IB
