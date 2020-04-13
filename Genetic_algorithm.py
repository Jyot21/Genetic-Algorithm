# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 09:58:17 2020

@author: Jyot Makadiya
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import math

#define window
width = 800
height = 800

#create coordinate datatype to store values of position,velocity and acceleration
class coord():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def add(self, dot):
        self.x = self.x + dot.x
        self.y = self.y + dot.y
    def limit(self,n):
        if self.x > n:
            self.x = n
        if self.y >n :
            self.y = n

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
class Brain():
    def __init__(self,size):
        self.step = 0
        self.directions = [coord(np.random.random()-0.5,np.random.random()-0.5) for i in range(size)]  
    def clone(self):
        clone = Brain(len(self.directions))
        clone.directions = self.directions.copy()
        return clone
    def mutate(self):
        mutateRate = 0.01
        for i in range(len(self.directions)):
            if np.random.random() < mutateRate:
                self.directions[i] = coord(np.random.random()-0.5,np.random.random()-0.5)

class population():
    def __init__(self,size):
        self.gen = 1
        self.fitnessSum = 0
        self.bestDot = 0
        self.dots = [dot() for i in range(size)]
        self.minStep = 1000
        
    def update(self):
        for i in range(len(self.dots)):
            if self.dots[i].brain.step > self.minStep:
                self.dots[i].dead = True
            else:
                self.dots[i].update()
                
    def calculateFitness(self):
        for dot in self.dots:
            dot.calculateFitness()
            
    def allDotsDead(self):
        for dot in self.dots:
            if not dot.dead and not dot.reachedGoal:
                return False
        return True
    
    def  naturalSelection(self):
        newDots = [dot() for i in range(len(self.dots))]
        self.setBestDot()
        self.calculateFitness()
        
        newDots[0] = self.dots[self.bestDot].gimmeBaby()
        newDots[0].isBest = True
        
        for i in range(1,len(self.dots)):
            
            parent = self.selectParent()
            newDots[i] = parent.gimmeBaby()
        
        self.dots = newDots.copy()# or use newDots.copy()
        self.gen+=1
    
    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for dot in self.dots:
            self.fitnessSum += dot.fitness
    
    def selectParent(self):
        rand = np.random.random()*self.fitnessSum
        
        runningSum = 0
        for dot in self.dots:
            runningSum += dot.fitness
            if runningSum > rand:
                return dot
        return None
    
    def mutateDemBabies(self):
        for dot in self.dots:
            dot.brain.mutate()
        
    def setBestDot(self):
        max = 0.0
        maxInd = 0
        for i in range(len(self.dots)):
            if(self.dots[i].fitness > max):
                max = self.dots[i].fitness
                maxInd = i
                
        self.bestDot = maxInd
        if self.dots[self.bestDot].reachedGoal :
            self.minStep = self.dots[self.bestDot].brain.step
            print("step:", self.minStep)

class dot():
    def __init__(self):
        self.pos = coord(width/2, height-10)
        self.brain = Brain(1000)
        #check if dot is dead
        self.dead = False
        self.reachedGoal = False
        self.isBest = False       #check if dot is Best
        
        self.fitness = 0.0
        self.vel = coord(0,0)
        self.acc = coord(0,0)
       
    def move(self):
        if len(self.brain.directions) > self.brain.step:
            acc = self.brain.directions[self.brain.step]
            self.brain.step -=- 1
        else:
            self.dead = True
        self.vel.add(acc)
        self.vel.limit(5)
        self.pos.add(self.vel)
        
    def update(self):
        global dead, reachedGoal, width, height, goal
        if (not self.dead and not self.reachedGoal):
            self.move()
        if self.pos.x < 2 or self.pos.y< 2 or self.pos.x > width-2 or self.pos.y > height -2:
            self.dead = True
        elif distance(self.pos.x, self.pos.y, goal.x, goal.y) < 5 :
            self.reachedGoal = True
        elif self.pos.x > 0 and self.pos.x < 500 and self.pos.y > 300 and self.pos.y < 310:
            self.dead = True
            
    def calculateFitness(self):
        if self.reachedGoal:
            self.fitness = 1.0/16.0 + 10000.0/float(self.brain.step * self.brain.step)
        else:
            distanceToGoal = distance(self.pos.x, self.pos.y, goal.x, goal.y)
            self.fitness = 1.0/distanceToGoal**2
    def gimmeBaby(self):
        baby = dot()
        baby.brain = self.brain.clone()
        return baby


test = population(1000)
goal = coord(400,10)


fig = plt.figure()
ax = plt.axes(xlim=(0, width), ylim=(0, height))
circle = plt.Circle((goal.x, goal.y), 10, color='b', fill=True)
#d, = ax.plot(target.pos.x,target.pos.y, 'ro')
rectangle = plt.Rectangle((0, 300), 500, 10, fc='r')
plt.gca().add_patch(rectangle)

d, = ax.plot([test.dots[i].pos.x for i in range(1000)],[test.dots[i].pos.y for i in range(1000)],'go')
ax.add_artist(circle)

def animate(i):
    
    if test.allDotsDead() :
        test.calculateFitness()
        test.naturalSelection()
        test.mutateDemBabies()
        d.set_data([test.dots[i].pos.x for i in range(1000)],[test.dots[i].pos.y for i in range(1000)])
        return d,
    else:
        test.update()
        d.set_data([test.dots[i].pos.x for i in range(1000)],[test.dots[i].pos.y for i in range(1000)])
        return d,
anim = animation.FuncAnimation(fig, animate, frames=100, interval=10, blit = True)

plt.show()





