import pygame
from math import pi,cos,sin,sqrt
pygame.init()
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("comicsans", 10)

class Satellite:
    # TIMESTEP = 3600*24  # 1 day
    TIMESTEP = .2  # 1 day
    Satellites_constellation = []
    object_counter = 1000
    def __init__(self, r, greatness, color, vel=0.01):
        Satellite.Satellites_constellation.append(self)
        self.theta = 0
        self.r = r
        self.x = self.r * cos(self.theta) + WIDTH / 2
        self.y = self.r * sin(self.theta) + HEIGHT / 2
        self.greatness = greatness
        self.color = color
        self.vel = vel
        self.footprint = (-pi/24, pi/24)
        self.flag = 0
        self.id = Satellite.object_counter
        Satellite.object_counter += 1
        self.orbit = []
        self.capacity = 10
        # self.capacity = random.randint(1, 10)

    def draw(self, win):
        if self.flag == 1:
            pygame.draw.circle(
                win, self.color, (self.x, self.y), self.greatness)
        else:
            pygame.draw.circle(
                win, self.color, (self.x, self.y), self.greatness, 2)

        pygame.draw.arc(win, self.color, (200, 200, 400, 400), *(tuple(element * pi for element in self.footprint)), 5)
        # SAT_text = FONT.render(f"{self.capacity}", 1, WHITE)
        # SAT_text = FONT.render(f"{round((self.theta/pi)%2,2)} \u03C0", 1, (0,0,0))
        # win.blit(SAT_text, (self.x - SAT_text.get_width() /
        #                          2, self.y - SAT_text.get_height()/2))

    def update_position(self):
        self.distance_to_earth = sqrt(self.x**2+self.y**2)
        self.theta += self.vel * self.TIMESTEP
        self.x = WIDTH / 2 + self.r * cos(self.theta)
        self.y = HEIGHT / 2 - self.r * sin(self.theta)
        self.orbit.append((self.x, self.y))
        self.area = (self.theta-pi/24, self.theta+pi/24)
        # Convert arg to Arg
        divided_tuple = tuple(x / pi for x in self.area)
        remainder_tuple = tuple(x % 2 for x in divided_tuple)
        # Checking that the range is proper for (min,max)
        if remainder_tuple[0] > remainder_tuple[1]:
            upper_bound = remainder_tuple[1]+2
        else:
            upper_bound = remainder_tuple[1]
        self.footprint = (remainder_tuple[0], upper_bound)

    def shadow(self, list_user):
        my_attribute_list = [obj.connect_id for obj in list_user]
        if (self.id in my_attribute_list):
            self.flag = 1
            self.capacity=10-my_attribute_list.count(self.id)
        else:
            self.flag = 0
            self.capacity=10

    def Does_cover_user(self,list_user):
        my_attribute_list=[obj.alpha for obj in list_user]
        list_flag=[]
        # set flag
        for x in my_attribute_list:
            if x >= self.footprint[0] and x <= self.footprint[1]:
                list_flag.append(1)
            else:
                list_flag.append(0)

        self.flag=max(list_flag)
        list_flag.clear()

    @classmethod
    def find_height_by_id(cls, id):
        for obj in cls.Satellites_constellation:
            if obj.id == id:
                # print((obj.theta % (2*pi))/pi)
                return obj.r
        return None
    
    @classmethod
    def find_angle_by_id(cls, id):
        for obj in cls.Satellites_constellation:
            if obj.id == id:
                # print((obj.theta % (2*pi))/pi)
                return (obj.theta % (2*pi))/pi
        return None
    
    @classmethod
    def change_capacity_by_id(cls, id):
        for obj in cls.Satellites_constellation:
            if obj.id == id:
                obj.capacity-=1
                return obj.capacity
        return None