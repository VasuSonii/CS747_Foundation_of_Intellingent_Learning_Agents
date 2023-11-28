import os
import sys
import random 
import json
import math
import utils
import time
import config
import numpy
random.seed(73)

def best_hole(ball_pos, holes, modified_holes):
    ans = {}
    besthole = []
    for ball, pos in ball_pos.items():
        if ball != 'white' and ball != 0:
            nearest_hole = find_nearest_hole(ball_pos[ball], holes)
            # print(nearest_hole, ball, distance_between_points(pos, nearest_hole))
            if distance_between_points(pos, nearest_hole) < 50:
                besthole.append((pos[0]-10,pos[1]-10))
                ans[ball] = besthole
                continue
            for hole in modified_holes:
                if deviation(ball_pos[0], pos, hole) < 82:
                    besthole.append(hole)
            # if ball_pos[0][0] <= pos[0]:
            #     besthole = [x for x in modified_holes if x[0] > pos[0]]
            # else:
            #     besthole = [x for x in modified_holes if x[0] < pos[0]]
            # if ball_pos[0][1] <= pos[1]:
            #     besthole = [x for x in besthole if x[1] > pos[1]]
            # else:
            #     besthole = [x for x in besthole if x[1] < pos[1]]
            ans[ball] = besthole
    return ans    

def deviation(white, ballpos, hole):
    return abs(find_angle(white, ballpos) - find_angle(ballpos, hole))*180


def find_angle(C1, C2):
    deltax= C2[0]-C1[0]
    deltay = C2[1]-C1[1]
    angle = math.atan2(deltay ,deltax)
    if angle >= 0 and angle < math.pi/2:
        angle = -(math.pi/2 + angle)/math.pi 
    elif angle >= math.pi/2:
        angle = -(angle-3*math.pi/2)/math.pi 
    elif angle < 0 and angle > -math.pi/2:
        angle = -(math.pi/2 - abs(angle))/math.pi 
    elif angle <= -math.pi/2:
        angle = (abs(angle)-math.pi/2)/math.pi 
    return angle

def move_along_line(x, angle, distance):
    angle1 = math.pi * angle
    # Calculate the new coordinates
    new_x = x[0] + distance*math.sin(angle1)
    new_y = x[1] + distance*math.cos(angle1)
    return new_x, new_y

def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Function to find the nearest hole
def find_nearest_hole(pos, hole_positions):
    nearest_hole = None  # Initialize with the first hole
    nearest_distance = float('inf')

    for hole in hole_positions:
        if distance_between_points(hole, pos) < nearest_distance:
            nearest_distance = distance_between_points(hole, pos)
            nearest_hole = hole
    return nearest_hole



class Agent:    
    def __init__(self, table_config) -> None:
        self.table_config = table_config
        self.prev_action = None
        self.curr_iter = 0
        self.state_dict = {}
        self.holes =[]
        self.ns = utils.NextState()
        self.modified_holes = [(64,64),(64,436),(500,50),(500,450),(936,64),(936,436)]

    def set_holes(self, holes_x, holes_y, radius):
        for x in holes_x:
            for y in holes_y:
                self.holes.append((x[0], y[0]))
        self.ball_radius = radius
    
    def find_force(self, white_to_ball, ball_to_hole, deviation):
        v1 = 0.0133*white_to_ball + (0.0133*ball_to_hole + 0.06*0.98)*(0.98/math.cos(math.radians(deviation)))
        F = (v1 + 3/14)/18.428
        return F

    def value(self,nextstate,state, deviation_angle , force):
        n = 0
        #Checkpoint 1
        n += 4*(len(state)-len(nextstate))
        #Checkpoint 2
        besthole = best_hole(nextstate, self.holes, self.modified_holes)
        # print("best" ,besthole)
        for ball,pos in nextstate.items():
            if ball != 'white' and ball != 0 and ball in besthole:
                if distance_between_points(pos, find_nearest_hole(pos, self.holes)) < 50:
                    n += 1
                    # print(ball, nextstate)
                    for hole in besthole[ball]:
                        if hole in [(500,40), (500,460)] and deviation(nextstate[0], pos, hole) < 10:
                            n += 2
                        if hole not in [(500,40), (500,460)] and deviation(nextstate[0], pos, hole) < 10:
                            n += 1
        #Checkpoint 3
        if deviation_angle < 25:
            n += 2  
        if deviation_angle > 85:
            n = n - 5
        #Checkpoint 4
        if force > 0.4:
            n = n - 1
        if force < 0.06:
            n = n - 1000
        
        return n
    def action(self, ball_pos=None):
        bestforce = 0.4
        goodstates = []
        besthole = best_hole(ball_pos, self.holes, self.modified_holes)
        # print(besthole)
        # print(besthole)
        bestangle = 0
        for ball, pos in ball_pos.items():
            if ball != 'white' and ball != 0 and ball in besthole:
                
                # print("ball",ball,"holes",besthole[ball])
                for hole in besthole[ball]:
                    angle = find_angle(pos, hole)
                    new_pos = move_along_line(pos,angle, self.ball_radius*2)
                    angle = find_angle(ball_pos[0],new_pos)
                    force = 0.1+self.find_force(distance_between_points(ball_pos[0], pos), distance_between_points(pos, find_nearest_hole(hole, self.holes)), deviation(ball_pos[0],pos, hole))
                    nextstate = self.ns.get_next_state(ball_pos, (angle,force), 73)
                    goodstates.append((self.value(nextstate, ball_pos,deviation(ball_pos[0],pos, hole), force), (angle,force)))
                    bestangle, bestforce = max(goodstates, key=lambda item: item[0])[1]
                        # print("force",force, "next", len(nextstate), len(ball_pos))
                      #  if len(nextstate) < beststate:
                      #      bestangle = angle
                      #      bestforce = force
                      #      beststate = len(nextstate)
                      #  elif distance_between_points(ball_pos[ball], hole) < holedist:
                      #      bestangle = angle
                      #      if force < bestforce:
                      #          bestforce = force
                      #      beststate = len(nextstate)
                      #      holedist = distance_between_points(ball_pos[ball], hole)
                         
                    # for i,state in enumerate(betterstates):
                    #     bh = best_hole(state, self.holes)
                    #     bs = len(state)
                    #     for b, p in state.items():
                    #         if b != 'white' and b != 0:
                    #             for h in bh[b]:
                    #                 ag = find_angle(p, h)
                    #                 newp = move_along_line(p, ag,self.ball_radius*2)
                    #                 ag = find_angle(state[0], newp)
                    #                 ns = self.ns.get_next_state(state, (ag,0.4), 73)
                    #                 if len(ns) < bs:
                    #                     bs = len(ns)
                    #                     bestangle = betterangle[i]
        if (bestforce < 0.01):
            bestforce = 0.5
        # print("bestforce", bestforce, "angle", abs(bestangle)*180)
        # print(goodstates, max(goodstates, key=lambda item: item[0])[1])
        return(bestangle,bestforce)

        # # print(config.resolution)
        # # print(self.holes)
        # # print(ball_pos['white'])
        # final_angle = []
        # near_hole,near_ball,holes = find_nearest_hole(ball_pos,self.modified_holes)
        # for j in holes:
        #     angle = find_angle(ball_pos[near_ball], j)
        #     new_pos = move_along_line(ball_pos[near_ball],angle, self.ball_radius*2)
        #     final_angle.append(find_angle(ball_pos[0],new_pos))

        # a = distance_between_points(ball_pos[near_ball],near_hole)
        # b = distance_between_points(ball_pos[0],ball_pos[near_ball])
        # force = math.sqrt(a*b)/(a+b)
        # # counts = []
        # # for i in final_angle:
        # #     nextstate = self.ns.get_next_state(ball_pos, (i,0.4), 73)
        # #     counts.append(value(nextstate,self.holes))
        # # counts = numpy.array(counts)
        # angle_deviation = abs(abs(find_angle(ball_pos[0], ball_pos[near_ball]))-abs(find_angle(ball_pos[near_ball],near_hole)))

        # # nextstate = self.ns.get_next_state(ball_pos,(final_angle[0],0.15),73)
        # # if len(nextstate) == len(ball_pos):
        # #     return (final_angle[near_ball], 0.45)
        # # else:
        # return(final_angle[0], 0.15 + angle_deviation)
        # ## Code you agent here ##
        # ## You can access data from config.py for geometry of the table, configuration of the levels, etc.
        # ## You are NOT allowed to change the variables of config.py (we will fetch variables from a different file during evaluation)
        # ## Do not use any library other than those that are already imported.
        # ## Try out different ideas and have fun!
        
        # # return (2*random.random()-1, random.random())
