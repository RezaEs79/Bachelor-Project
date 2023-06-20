from math import pi,cos,sin,tan,sqrt,log10,exp
import pygame
import random
from multipledispatch import dispatch
WIDTH, HEIGHT = 800, 800
FPS = 60
Train_seed=6
Test_seed=64
mysd=Test_seed
lensys = 500
NOS = 6   # number of satellites
NOU = 30  # number of users
rEarth=200
rspotbeam=20
side_dispersion_usr=200
WHITE = (255, 255, 255)
RED = (188, 39, 50)
Pale_Pink = (255, 228, 225)
Sky_Blue = (135, 206, 235)
Mustard_Yellow = (246, 214, 94)
Light_Gray = (211, 211, 211)
Light_Purple = (221, 160, 221)
Peach = (255, 218, 185)
Teal = (0, 128, 128)
Olive_Green = (128, 128, 0)
Navy_Blue = (0, 0, 128)
Coral = (255, 127, 80)
Lavender = (230, 230, 250)
Mint_Green = (152, 251, 152)
Dark_Red = (139, 0, 0)
Beige = (245, 245, 220)
Dark_Purple = (128, 0, 128)
colors = [Pale_Pink, Sky_Blue, Mustard_Yellow, Light_Gray, Light_Purple, Peach, Teal,
          Olive_Green, Navy_Blue, Coral, Lavender, Mint_Green, Dark_Red, Beige, Dark_Purple]
pygame.init()
FONT = pygame.font.SysFont("comicsans", 10)
def hexagons(radius,W,H):
    # Define the points of the hexagon
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = angle_deg * pi / 180
        x = W + radius * cos(angle_rad)
        y = H + radius * sin(angle_rad)
        points.append((x, y))
    return points

def beam(radius,W,H):
    # Define the points of the seven-hexagon
    points = []
    phase=30 * pi / 180
    points1=hexagons(radius,W,H)
    points2=hexagons(radius,W+radius*2*cos(phase),H)
    points3=hexagons(radius,W-radius*2*cos(phase),H)
    points4=hexagons(radius,W+radius*cos(phase),H+(radius+radius*sin(phase)))
    points5=hexagons(radius,W-radius*cos(phase),H+(radius+radius*sin(phase)))
    points6=hexagons(radius,W+radius*cos(phase),H-(radius+radius*sin(phase)))
    points7=hexagons(radius,W-radius*cos(phase),H-(radius+radius*sin(phase)))
    points.extend([points1,points2,points3,points4,points5,points6,points7 ])
    
    return points

def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    for i in range(n):
        j = (i + 1) % n
        if ((polygon[i][1] > y) != (polygon[j][1] > y)) and \
           (x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            inside = not inside
    return inside

class Satellite:
    object_counter=1000
    instances = []
    def __init__(self, r, color,vel=0.01):
        Satellite.instances.append(self)
        self.flag=10
        self.speed = vel
        # Generate a random angle between 40 and 50 degrees
        random.seed(mysd)
        list_angle = [random.uniform(41, 49) for _ in range(NOS)]
        self.id = Satellite.object_counter
        Satellite.object_counter += 1
        if self.id==1000:
            angle_deg =45
        else:
            angle_deg =list_angle[self.id-1001]
        # Convert the angle to radians
        self.angle_rad = angle_deg * pi / 180
        self.list_u_id=[]
        self.x=r
        self.y=r
        self.points=beam(rspotbeam,self.x,self.y)
        self.color=color
        self.capacity=5
        random.seed(mysd)
        list_height = [random.randint(600, 900) for _ in range(NOS)]
        scale_list_height = [(num*2*2.66*rspotbeam)/3600 for num in list_height]
        if self.id==1000:
            self.height =33.83
        else:
            self.height =scale_list_height[self.id-1001]

    def draw(self, win):
        pygame.draw.circle(
            win,  self.color, (self.x, self.y), 2)
        # pygame.draw.circle(
        #     win,  self.color, (self.x, self.y), 2.66*rspotbeam, 1)
        for count, element in enumerate(self.points):
            if isinstance(self.flag,list) and count in self.flag:
                pygame.draw.polygon(win, self.color, element)  
            else:    
                pygame.draw.polygon(win, self.color, element,1)  

    def update_position(self):
        self.x += self.speed*tan(self.angle_rad)
        self.y += self.speed

        if self.x<0 or self.x>WIDTH:
            self.x=self.x%WIDTH
        if self.y<0 or self.y>HEIGHT:
            self.y=self.y%HEIGHT
        self.points=beam(rspotbeam,self.x,self.y)

    def shadow(self, list_user):
        my_attribute_list = [obj.connect_id for obj in list_user]
        tuples = [(x, y) for (x, y) in [my_attribute_list[i] for i in range(len(my_attribute_list)) if isinstance(my_attribute_list[i], tuple)] if x == self.id]
        if tuples:
            # print(f"{self.id}= {tuples}")
            # result = [t[1] for t in tuples] # it is useful for show how many user are in cell
            result=list(set([x[1] for x in tuples]))
            self.flag=result
        else:
            self.flag=10

    @classmethod
    def find_height_by_id(cls, id):
        for obj in cls.instances:
            if obj.id == id:
                return obj.height
        return None
    @classmethod
    def change_capacity_by_id(cls, id):
        for obj in cls.instances:
            if obj.id == id:
                obj.capacity-=1
                return obj.capacity
        return None
    
    
    @classmethod
    def find_height_by_ids(cls, ids):
        heights = []
        for obj in cls.instances:
            if isinstance(obj, Satellite) and obj.id in ids:
                heights.append(obj.height)
        return heights

def genrating_Sat():
    construct=[]
    import numpy as np
    # Set the seed value for reproducibility
    np.random.seed(mysd)
    # Generate random numbers for each column
    col1 = np.random.uniform(75, 150, size=(NOS, 1))
    col2 = np.random.randint(0, 14, size=(NOS, 1))
    col3 = np.random.uniform(0.1, 0.3, size=(NOS, 1))
    # Concatenate columns to form the matrix
    matrix = np.hstack((col1, col2, col3))
    if NOS!=3:
        for i in range(NOS):
            construct.append(Satellite(matrix[i][0],colors[int(matrix[i][1])],matrix[i][2]))
            # construct.append(Satellite(rEarth+random.uniform(55, 100),colors[random.randint(0, len(colors)-1)],random.uniform(0.05, 0.15) ))
        return construct
    else:
        A=Satellite(rEarth+80,Pale_Pink, 0.015)
        B=Satellite(rEarth+50,  Mint_Green)
        C=Satellite(rEarth+100, Sky_Blue, 0.05)
        # construct.extend([A])
        construct.extend([A,B,C])
        return construct

class User:
    Existing_users = []
    U_counter=2000
    def __init__(self):
        User.Existing_users.append(self)
        self.uid = User.U_counter
        User.U_counter += 1
        self.connect_id=0
        self.ULP=[]
        self.dist=[]
        self.abs_rss=[]
        self.capacity=[]
        import random
        # Set the random seed to a fixed value
        random.seed(mysd)
        # Generate two random vectors of length
        vector1 = [random.uniform(WIDTH/2-side_dispersion_usr, WIDTH/2+side_dispersion_usr) for _ in range(10000)]
        vector2 = [random.uniform(HEIGHT/2-side_dispersion_usr, HEIGHT/2+side_dispersion_usr) for _ in range(10000)]
        self.x_u= vector1[self.uid-2000]
        self.y_u= vector2[self.uid-2000]

    def connect_to_provider(self, providers):
        insight=[]
        for pr in providers:
            for i in range(7):
                list_insight=point_in_polygon((self.x_u,self.y_u), pr.points[i])
                if list_insight:
                    insight.append(((pr.id,i),(round(pr.x, 2),round(pr.y, 2))))            
        if insight:
            # new_list_insight = [item[0] for item in insight]
            return insight
        else:
            self.connect_id = 0
        return insight

    def distances(self,points):
        x1, y1 = points
        return  sqrt((x1 - self.x_u)**2 + (y1 - self.y_u)**2)

    # @classmethod  
    # def draw(self, win):
    #     for user in User.Existing_users:
    #         pygame.draw.circle(win, RED, (user.x_u, user.y_u), 3)
    @dispatch(pygame.Surface,list)
    def draw(self, win, usrlist):
        for user in usrlist:
            pygame.draw.circle(win, RED, (user.x_u, user.y_u), 3)
    

def genrating_Usr(count):
    myli=[]
    for _ in range(count):
        myli.append(User())
    return myli

# Declare variables and compute RSS
# Part 1: Computations independant of the random variable
# for shadow fading

from numpy import random
def CalcRSS(distance):
    # distance = 200
    g = 150
    Pt = 20
    Po = 38
    grad1 = 2
    grad2 = 2
    alpha = exp(-1/85)
    sigma1 = sqrt(8)
    sigma2 = sqrt(sigma1**2 * (1 - alpha**2))
    # Path Loss
    RSS01 = Pt - Po - (10 * grad1 * log10(distance) +
                    10 * grad2 * log10(distance/g))
    #  Part 2: Adding the random variable for shadow fading
    # s(d) = is the correlated log normal fading
    s1 = sigma1 * random.normal()
    s2 = alpha * s1 + sigma2 * random.normal()
    RSS1 = RSS01 + s2
    return RSS1


def chord_length(a, b):
    # Calculate the length of the hypotenuse using the Pythagorean theorem
    return sqrt(a**2 + b**2)