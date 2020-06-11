import pygame as pg
import math
from pygame import gfxdraw

pg.init()

h = 1000
w = 1000

pi = 3.14159265359

screen = pg.display.set_mode((w, h))

sphere = [0,7,1,2, 1]

plane = [0,0,-0.25,-1]

light = [2,2,10]

inter_sph = [0,0,0]

diam_vec = [0, 0, 0]

ray = [0,0,0]
light_ray = [0,0,0]

a = 0
b = 0
c = 0
cam_vec = [0,1,0,0,0]

cam_vec[3] = math.acos(cam_vec[0] / math.sqrt(2))
cam_vec[4] = math.asin(cam_vec[1] / math.sqrt(2))
cam_vec[3] += pi / 4
cam_vec[4] += pi / 4

cor_x = math.cos(cam_vec[3]) * math.sqrt(2)
cor_y = math.cos(cam_vec[4]) * math.sqrt(2)
cor_z = math.cos(cam_vec[2] / math.sqrt(2) + pi / 4) * math.sqrt(2)

ray[0] = cam_vec[0] + cor_x
ray[1] = cam_vec[1] + cor_y
ray[2] = cam_vec[2] + cor_z


for y in range(1, h) :
    for x in range(1, w) :

        ray[0] = x * (2/w) + cor_x
        ray[2] = cor_z - y * (2/h)

        delta = 4*pow(a*ray[0] + b*ray[1] + c*ray[2] - ray[0]*sphere[0] - ray[1]*sphere[1] - ray[2]*sphere[2], 2) - 4*(pow(ray[0], 2) + pow(ray[1], 2) + pow(ray[2], 2))*(-2*a*sphere[0] - 2*b*sphere[1] - 2*c*sphere[2] + pow(a,2) + pow(b,2) + pow(c,2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))
        
        if delta > 0 :
            t = (-2*(a*ray[0] + b*ray[1] + c*ray[2] - ray[0]*sphere[0] - ray[1]*sphere[1] - ray[2]*sphere[2]) - math.sqrt(delta)) / 2*(pow(ray[0], 2) + pow(ray[1], 2) + pow(ray[2], 2))

        if plane[0]*ray[0] + plane[1]*ray[1] + plane[2]*ray[2] != 0 :
            t_2 = -(plane[0]*a + plane[1]*b + plane[2]*c + plane[3]) / (plane[0]*ray[0] + plane[1]*ray[1] + plane[2]*ray[2])

        if t_2 > 0 and delta > 0 :
            if t_2 > t :
                inter_sph[0] = a+t*ray[0]
                inter_sph[1] = b+t*ray[1]
                inter_sph[2] = c+t*ray[2]

                light_ray[0] = light[0] - inter_sph[0]
                light_ray[1] = light[1] - inter_sph[1]
                light_ray[2] = light[2] - inter_sph[2]

                if sphere[4] == 0 :
                    delta_2 = 4*pow(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2], 2) - 4*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))*(-2*inter_sph[0]*sphere[0] - 2*inter_sph[1]*sphere[1] - 2*inter_sph[2]*sphere[2] + pow(inter_sph[0],2) + pow(inter_sph[1],2) + pow(inter_sph[2],2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))

                    if delta_2 >= 0 :
                        r_1 = (-2*(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2]) - math.sqrt(delta_2)) / 2*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))
                        r_2 = (-2*(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2]) + math.sqrt(delta_2)) / 2*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))
                    
                        if abs(r_1) > abs(r_2) :
                            color = (0,0,255)
                        else :
                            color = (0,0,255 - (r_2*255)/(abs(r_1)+r_2))
                    else :
                        color = (0,0,255)
                else :
                    diam_vec[0] = inter_sph[0] - sphere[0]
                    diam_vec[1] = inter_sph[1] - sphere[1]
                    diam_vec[2] = inter_sph[2] - sphere[2]

                    k = (diam_vec[0]*(a - sphere[0]) + diam_vec[1]*(b - sphere[1]) + diam_vec[2]*(c - sphere[2])) / (pow(diam_vec[0], 2) + pow(diam_vec[1], 2) + pow(diam_vec[2], 2))
                    l = (pow(diam_vec[0], 2) + pow(diam_vec[1], 2) + pow(diam_vec[2], 2))*pow(k, 2) + 2*(diam_vec[0]*(a - sphere[0]) + diam_vec[1]*(b - sphere[1]) + diam_vec[2]*(c - sphere[2])) + (pow(sphere[0] - a, 2) + pow(sphere[1] - b, 2) + pow(sphere[2] - c, 2))

                    proj = [k*diam_vec[0] + sphere[0] , k*diam_vec[1] + sphere[1] , k*diam_vec[2] + sphere[2]]

                    refl = [2*(proj[0] - a) + a , 2*(proj[1] - b) + b , 2*(proj[2] - c) + c]
                    reflect = [refl[0] - inter_sph[0] , refl[1] - inter_sph[1] , refl[2] - inter_sph[2]]

                    if plane[0]*reflect[0] + plane[1]*reflect[1] + plane[2]*reflect[2] != 0 :
                        t_2 = -(plane[0]*inter_sph[0] + plane[1]*inter_sph[1] + plane[2]*inter_sph[2] + plane[3]) / (plane[0]*reflect[0] + plane[1]*reflect[1] + plane[2]*reflect[2])
                        
                        if t_2 > 0 :
                            
                            if (int(inter_sph[0]+t_2*reflect[0])/2 == int((inter_sph[0]+t_2*reflect[0]) / 2) and not int(inter_sph[1]+t_2*reflect[1]) / 2 == int((inter_sph[1]+t_2*reflect[1]) / 2)) or (not int(inter_sph[0]+t_2*reflect[0])/2 == int((inter_sph[0]+t_2*reflect[0]) / 2) and int(inter_sph[1]+t_2*reflect[1]) / 2 == int((inter_sph[1]+t_2*reflect[1]) / 2)):
                                color = (0,255,0)
                            else :
                                color = (255,0,0)   
                            inter_sph[0] = inter_sph[0]+t_2*reflect[0]
                            inter_sph[1] = inter_sph[1]+t_2*reflect[1]
                            inter_sph[2] = inter_sph[2]+t_2*reflect[2]
                
                            light_ray[0] = light[0] - inter_sph[0]
                            light_ray[1] = light[1] - inter_sph[1]
                            light_ray[2] = light[2] - inter_sph[2]

                            delta_2 = 4*pow(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2], 2) - 4*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))*(-2*inter_sph[0]*sphere[0] - 2*inter_sph[1]*sphere[1] - 2*inter_sph[2]*sphere[2] + pow(inter_sph[0],2) + pow(inter_sph[1],2) + pow(inter_sph[2],2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))
                            if delta_2 >= 0 :
                                if color == (255, 0, 0) :
                                    color = (100, 0, 0)
                                else :
                                    color = (0, 100, 0)
                        else :
                            color = (0, 0, 0)
                            
            else :
                if (int(b+t_2*ray[1])/2 == int((b+t_2*ray[1]) / 2) and not int(a+t_2*ray[0]) / 2 == int((a+t_2*ray[0]) / 2)) or (not int(b+t_2*ray[1])/2 == int((b+t_2*ray[1]) / 2) and int(a+t_2*ray[0]) / 2 == int((a+t_2*ray[0]) / 2)):
                    color = (0,255,0)
                else :
                    color = (255,0,0)
                inter_sph[0] = a+t_2*ray[0]
                inter_sph[1] = b+t_2*ray[1]
                inter_sph[2] = c+t_2*ray[2]
                
                light_ray[0] = light[0] - inter_sph[0]
                light_ray[1] = light[1] - inter_sph[1]
                light_ray[2] = light[2] - inter_sph[2]

                delta_2 = 4*pow(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2], 2) - 4*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))*(-2*inter_sph[0]*sphere[0] - 2*inter_sph[1]*sphere[1] - 2*inter_sph[2]*sphere[2] + pow(inter_sph[0],2) + pow(inter_sph[1],2) + pow(inter_sph[2],2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))
                if delta_2 >= 0 :
                    if color == (255, 0, 0) :
                        color = (100, 0, 0)
                    else :
                        color = (0, 100, 0)
                
        elif t_2 > 0 and delta < 0 :
            if (int(b+t_2*ray[1])/2 == int((b+t_2*ray[1]) / 2) and not int(a+t_2*ray[0]) / 2 == int((a+t_2*ray[0]) / 2)) or (not int(b+t_2*ray[1])/2 == int((b+t_2*ray[1]) / 2) and int(a+t_2*ray[0]) / 2 == int((a+t_2*ray[0]) / 2)) :
                color = (0,255,0)
            else :
                color = (255,0,0)

            inter_sph[0] = a+t_2*ray[0]
            inter_sph[1] = b+t_2*ray[1]
            inter_sph[2] = c+t_2*ray[2]
            
            light_ray[0] = light[0] - inter_sph[0]
            light_ray[1] = light[1] - inter_sph[1]
            light_ray[2] = light[2] - inter_sph[2]

            delta_2 = 4*pow(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2], 2) - 4*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))*(-2*inter_sph[0]*sphere[0] - 2*inter_sph[1]*sphere[1] - 2*inter_sph[2]*sphere[2] + pow(inter_sph[0],2) + pow(inter_sph[1],2) + pow(inter_sph[2],2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))
            
            if delta_2 > 0 :
                if color == (255, 0, 0) :
                    color = (100, 0, 0)
                else :
                    color = (0, 100, 0)

        elif delta >= 0 and t_2 <= 0 :
            inter_sph[0] = a+t*ray[0]
            inter_sph[1] = b+t*ray[1]
            inter_sph[2] = c+t*ray[2]
            
            light_ray[0] = light[0] - inter_sph[0]
            light_ray[1] = light[1] - inter_sph[1]
            light_ray[2] = light[2] - inter_sph[2]
            
            if sphere[4] == 0 :
                delta_2 = 4*pow(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2], 2) - 4*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))*(-2*inter_sph[0]*sphere[0] - 2*inter_sph[1]*sphere[1] - 2*inter_sph[2]*sphere[2] + pow(inter_sph[0],2) + pow(inter_sph[1],2) + pow(inter_sph[2],2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))

                if delta_2 >= 0 :
                    r_1 = (-2*(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2]) - math.sqrt(delta_2)) / 2*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))
                    r_2 = (-2*(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2]) + math.sqrt(delta_2)) / 2*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))
                    
                    if abs(r_1) > abs(r_2) :
                        color = (0,0,255)
                    else :
                        color = (0,0,255 - (r_2*255)/(abs(r_1)+r_2))
                else :
                    color = (0,0,255)
            else :
                diam_vec[0] = inter_sph[0] - sphere[0]
                diam_vec[1] = inter_sph[1] - sphere[1]
                diam_vec[2] = inter_sph[2] - sphere[2]

                k = (diam_vec[0]*(a - sphere[0]) + diam_vec[1]*(b - sphere[1]) + diam_vec[2]*(c - sphere[2])) / (pow(diam_vec[0], 2) + pow(diam_vec[1], 2) + pow(diam_vec[2], 2))
                l = (pow(diam_vec[0], 2) + pow(diam_vec[1], 2) + pow(diam_vec[2], 2))*pow(k, 2) + 2*(diam_vec[0]*(a - sphere[0]) + diam_vec[1]*(b - sphere[1]) + diam_vec[2]*(c - sphere[2])) + (pow(sphere[0] - a, 2) + pow(sphere[1] - b, 2) + pow(sphere[2] - c, 2))

                proj = [k*diam_vec[0] + sphere[0] , k*diam_vec[1] + sphere[1] , k*diam_vec[2] + sphere[2]]

                refl = [2*(proj[0] - a) + a , 2*(proj[1] - b) + b , 2*(proj[2] - c) + c]
                reflect = [refl[0] - inter_sph[0] , refl[1] - inter_sph[1] , refl[2] - inter_sph[2]]

                if plane[0]*reflect[0] + plane[1]*reflect[1] + plane[2]*reflect[2] != 0 :
                    t_2 = -(plane[0]*inter_sph[0] + plane[1]*inter_sph[1] + plane[2]*inter_sph[2] + plane[3]) / (plane[0]*reflect[0] + plane[1]*reflect[1] + plane[2]*reflect[2])
                
                    if t_2 > 0 :
                            
                        if (int(inter_sph[1]+t_2*reflect[1])/2 == int((inter_sph[1]+t_2*reflect[1]) / 2) and not int(inter_sph[0]+t_2*reflect[0]) / 2 == int((inter_sph[0]+t_2*reflect[0]) / 2)) or (not int(inter_sph[1]+t_2*reflect[1])/2 == int((inter_sph[1]+t_2*reflect[1]) / 2) and int(inter_sph[0]+t_2*reflect[0]) / 2 == int((inter_sph[0]+t_2*reflect[0]) / 2)):
                            color = (0,255,0)
                        else :
                            color = (255,0,0)   
                        inter_sph[0] = inter_sph[0]+t_2*reflect[0]
                        inter_sph[1] = inter_sph[1]+t_2*reflect[1]
                        inter_sph[2] = inter_sph[2]+t_2*reflect[2]
                
                        light_ray[0] = light[0] - inter_sph[0]
                        light_ray[1] = light[1] - inter_sph[1]
                        light_ray[2] = light[2] - inter_sph[2]

                        delta_2 = 4*pow(inter_sph[0]*light_ray[0] + inter_sph[1]*light_ray[1] + inter_sph[2]*light_ray[2] - light_ray[0]*sphere[0] - light_ray[1]*sphere[1] - light_ray[2]*sphere[2], 2) - 4*(pow(light_ray[0], 2) + pow(light_ray[1], 2) + pow(light_ray[2], 2))*(-2*inter_sph[0]*sphere[0] - 2*inter_sph[1]*sphere[1] - 2*inter_sph[2]*sphere[2] + pow(inter_sph[0],2) + pow(inter_sph[1],2) + pow(inter_sph[2],2) + pow(sphere[0],2) + pow(sphere[1],2) + pow(sphere[2],2) - pow(sphere[3],2))

                        if delta_2 >= 0 :
                            if color == (255, 0, 0) :
                                color = (100, 0, 0)
                            else :
                                color = (0, 100, 0)
                    else :
                        color = (0, 0, 0)

        else :
            color = (0,0,0)

        pg.gfxdraw.pixel(screen, x, y, color)
            
    pg.display.flip()




