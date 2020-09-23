import pygame as pg
import math
from pygame import gfxdraw

pg.init()

w = 1000
h = 1000
pi = 3.14159265359

global color_1
global color_2

screen = pg.display.set_mode((w, h))

class Sphere() :
    def __init__(self, x, y, z, r, dist, color) :
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.dist = dist
        self.color = color
        
    def render(self) :
        pass

class Plane() :
    def __init__(self, a, b, c, d, dist, color_1, color_2) :
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.dist = dist
        self.color_1 = color_1
        self.color_2 = color_2

class Point() :
    def __init__(self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z

class vec() :
    def __init__(self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z


def isCollision(ray, obj) :
    if type(obj) == Sphere :
        delta = 4*(cam.x*ray.x + cam.y*ray.y + cam.z*ray.z - ray.x*obj.x - ray.y*obj.y - ray.z*obj.z)**2 - 4*(ray.x**2 + ray.y**2 + ray.z**2)*(-2*cam.x*obj.x - 2*cam.y*obj.y - 2*cam.z*obj.z + cam.x**2 + cam.y**2 + cam.z**2 + obj.x**2 + obj.y**2 + obj.z**2 - obj.r**2)
        
        if delta > 0 :
            t = (-2*(cam.x*ray.x + cam.y*ray.y + cam.z*ray.z - ray.x*obj.x - ray.y*obj.y - ray.z*obj.z) - math.sqrt(delta)) / 2*(pow(ray.x, 2) + pow(ray.y, 2) + pow(ray.z, 2))
            
            return t

        else :
            return False

    if type(obj) == Plane :
        if obj.a*ray.x + obj.b*ray.y + obj.c*ray.z != 0 :
            
            t = -(obj.a*cam.x + obj.b*cam.y + obj.c*cam.z + obj.d) / (obj.a*ray.x + obj.b*ray.y + obj.c*ray.z)
            if t >= 0 :
                return t
            else :
                return False
        else :
            return False

def shadow(ray, obj) : # cherche s'il y a des ombres
    
    if type(obj) == Plane :
        inter = Point(cam.x + dists[obj]*ray.x, cam.y + dists[obj]*ray.y, cam.z + dists[obj]*ray.z)
        light_ray = vec(light.x - inter.x, light.y - inter.y, light.z - inter.z)

        shadow = False
        
        for obj_2 in dists :
            
            if type(obj_2) == Sphere :
                delta_2 = 4*pow(inter.x*light_ray.x + inter.y*light_ray.y + inter.z*light_ray.z - light_ray.x*obj_2.x - light_ray.y*obj_2.y - light_ray.z*obj_2.z, 2) - 4*(pow(light_ray.x, 2) + pow(light_ray.y, 2) + pow(light_ray.z, 2))*(-2*inter.x*obj_2.x - 2*inter.y*obj_2.y - 2*inter.z*obj_2.z + pow(inter.x,2) + pow(inter.y,2) + pow(inter.z,2) + pow(obj_2.x,2) + pow(obj_2.y,2) + pow(obj_2.z,2) - pow(obj_2.r,2))
                if delta_2 >= 0 :

                    a, b, c = obj.color_1
                    d, e, f = obj.color_2

                    a, b, c, d, e, f = a/2.5, b/2.5, c/2.5, d/2.5, e/2.5, f/2.5

                    shadow = True
                        
        if shadow :
            return (a, b, c), (d, e, f)
        else :
            return obj.color_1, obj.color_2

    if type(obj) == Sphere :
        inter = Point(cam.x + dists[obj]*ray.x, cam.y + dists[obj]*ray.y, cam.z + dists[obj]*ray.z)
        light_ray = vec(light.x - inter.x, light.y - inter.y, light.z - inter.z)

        shadow = False
        
        for obj_2 in dists :
            
            if type(obj_2) == Sphere :
                delta_2 = pow(2*inter.x*light_ray.x + 2*inter.y*light_ray.y + 2*inter.z*light_ray.z - 2*light_ray.x*obj_2.x - 2*light_ray.y*obj_2.y - 2*light_ray.z*obj_2.z, 2) - 4*(pow(light_ray.x, 2) + pow(light_ray.y, 2) + pow(light_ray.z, 2))*(-2*inter.x*obj_2.x - 2*inter.y*obj_2.y - 2*inter.z*obj_2.z + pow(inter.x,2) + pow(inter.y,2) + pow(inter.z,2) + pow(obj_2.x,2) + pow(obj_2.y,2) + pow(obj_2.z,2) - pow(obj_2.r,2))
                
                if delta_2 >= 0 :
                    r_1 = (-2*(inter.x*light_ray.x + inter.y*light_ray.y + inter.z*light_ray.z - light_ray.x*obj_2.x - light_ray.y*obj_2.y - light_ray.z*obj_2.z) - math.sqrt(delta_2)) / 2*(pow(light_ray.x, 2) + pow(light_ray.y, 2) + pow(light_ray.z, 2))
                    r_2 = (-2*(inter.x*light_ray.x + inter.y*light_ray.y + inter.z*light_ray.z - light_ray.x*obj_2.x - light_ray.y*obj_2.y - light_ray.z*obj_2.z) + math.sqrt(delta_2)) / 2*(pow(light_ray.x, 2) + pow(light_ray.y, 2) + pow(light_ray.z, 2))
                        
                    if abs(r_1) < r_2 :
                        a, b, c = obj.color

                        a, b, c = a/2.5, b/2.5, c/2.5

                        shadow = True
                        
        if shadow :
            return (a, b, c)
        else :
            return obj.color

        
        
def draw_pixel(ray, obj) :      # dessine le pixel
    if type(obj) == Plane :
        col_1, col_2 = shadow(primray, obj)
        if (int(cam.y+dists[obj]*ray.y)/2 == int((cam.y+dists[obj]*ray.y) / 2) and not int(cam.x+dists[obj]*ray.x) / 2 == int((cam.x+dists[obj]*ray.x) / 2)) or (not int(cam.y+dists[obj]*ray.y)/2 == int((cam.y+dists[obj]*ray.y) / 2) and int(cam.x+dists[obj]*ray.x) / 2 == int((cam.x+dists[obj]*ray.x) / 2)):
            pg.gfxdraw.pixel(screen, x, y, col_1)
        else :
            pg.gfxdraw.pixel(screen, x, y, col_2)
            
    if type(obj) == Sphere :
        col = shadow(primray, obj)
        pg.gfxdraw.pixel(screen, x, y, col)


def find_key(v): 
    for k, val in dists.items(): 
        if v == val: 
            return k
    

# on déclare tous nos objets de la scène (x, y, z, rayon, bool miroir 0 ou 1, tuple couleur) :

sphere = Sphere(-1, 9, 0, 1, 0, (0, 0, 255))
sphere_2 = Sphere(0, 7, 0, 1, 0, (255, 0, 255))
sphere_3 = Sphere(1, 5, 0, 1, 0, (255,255,0))
sphere_4 = Sphere(4, 7, 3, 1, 0, (255, 255, 255))
plane = Plane(0, 0, -0.5, -1, 0, (0, 255, 0), (255, 0, 0))

dists = {sphere : 0,sphere_2 : 0,plane : 0, sphere_3 : 0, sphere_4 : 0}


# on déclare les objets nécessaire au rendu (caméra, lumière) :

cam = Point(0, 0, 0)
light = Point(0, 3, 10)
cam_vec = vec(0, 1, 0)


cor = Point(0, 0, 0) # déclaration du coin en haut à gauche de l'écran
dist = [0, 0, 0]

cam_angle_x = math.acos(cam_vec.x / math.sqrt(2))
cam_angle_y = math.acos(cam_vec.y / math.sqrt(2))
cam_angle_x += pi / 4
cam_angle_y += pi / 4

cor.x = math.cos(cam_angle_x) * math.sqrt(2)
cor.y = math.cos(cam_angle_y) * math.sqrt(2)
cor.z = math.cos(cam_vec.z / math.sqrt(2) + pi / 4) * math.sqrt(2)


# vecteur directeur du rayon incident
primray = vec(0, 0, 0)
primray.x = cam_vec.x + cor.x
primray.y = cam_vec.y + cor.y
primray.z = cam_vec.z + cor.z

for y in range(1, h) :
    for x in range(1, w) :

        primray.x = x * (2/w) + cor.x
        primray.z = cor.z - y * (2/h)
        
        min_dist = False
        for obj in dists :
            if min_dist == False :
                min_dist = isCollision(primray, obj)

        if min_dist != False :
            for obj in dists :
                dists[obj] = isCollision(primray, obj)
                if dists[obj] != False :
                    if dists[obj] < min_dist :
                        min_dist = dists[obj]

            draw_pixel(primray, find_key(min_dist))

        else :
            pg.gfxdraw.pixel(screen, x, y, (0, 0, 0))
                        
    pg.display.flip()
