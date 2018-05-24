from math import sqrt
from point2d import Point2D
from graphics import egi
from random import randrange
from fsm import FiniteStateMachine


class Agent(object):
    def __init__(self, mode, world):
        self.world = world
        self.mode = mode
        if self.mode == "Agent":
            self.my_box = next((box for box in self.world.boxes if box.kind != 'X'), None)
        else:
            self.health = 3
            sentinel = False
            while not sentinel:
                self.my_box = self.world.boxes[randrange(len(self.world.boxes) - 1)]
                if ((self.world.boxes[self.my_box.idx].kind != 'X') and (self.world.agent.idx != self.my_box.idx)):
                    sentinel = True
        self.idx = self.my_box.idx
        self.my_x = self.my_box._vc.x
        self.my_y = self.my_box._vc.y
        if self.mode == "Enemy":
            self.my_y -= 10
        self.start_x = self.my_x
        self.start_y = self.my_y
        self.path_step = 1
        self.fsm = False
        self.box_corrected = False
        self.start_idx = self.idx

    def round_points(self):
        self.my_x = round(self.my_x, 0)
        self.my_y = round(self.my_y, 0)
        self.start_x = round(self.start_x, 0)
        self.start_y = round(self.start_y, 0)
        if self.fsm:
            if self.fsm.next_waypoint:
                self.fsm.next_waypoint = round(self.fsm.next_waypoint, 0)
            if self.fsm.projectile:
                self.fsm.projectile.x = round(self.fsm.projectile.x, 0)
                self.fsm.projectile.y = round(self.fsm.projectile.y, 0)
            if self.fsm.proj_target:
                self.fsm.proj_target.x = round(self.fsm.proj_target.x, 0)
                self.fsm.proj_target.y = round(self.fsm.proj_target.y, 0)
            if self.fsm.vel_x:
                self.fsm.vel_x = round(self.fsm.vel_x, 0)
            if self.fsm.vel_y:
                self.fsm.vel_y = round(self.fsm.vel_y, 0)

    def draw(self):
        if self.mode == "Agent":
            if self.fsm:
                self.fsm.update()
                self.fsm.draw()
            egi.blue_pen()
        else:
            egi.red_pen()
        egi.set_stroke(4)
        egi.circle(Point2D(self.my_x, self.my_y), 10)

    def update(self):
#        self.round_points()
        if ((self.mode == "Agent") and (self.box_corrected)):
            if not self.fsm:
                self.fsm = FiniteStateMachine(self.world)
            self.fsm.update()
        while self.my_box.kind == 'X':
            if self.mode == "Agent":
                self.my_box = next((box for box in self.world.boxes if box.kind != 'X'), None)
            else:
                sentinel = False
                while not sentinel:
                    self.my_box = self.world.boxes[randrange(len(self.world.boxes) - 1)]
                    if ((self.world.boxes[self.my_box.idx].kind != 'X') and (self.world.agent.idx != self.my_box.idx)):
                        sentinel = True
            self.idx = self.my_box.idx
            self.my_x = self.my_box._vc.x
            self.my_y = self.my_box._vc.y
            if self.mode == "Enemy":
                self.my_y -= 10
            self.start_x = self.my_x
            self.start_y = self.my_y
        self.box_corrected = True

#    def path_to_goal(self):
#        target_box = next((box for box in self.world.boxes if box.idx == self.world.path.path[self.path_step]), None)
#        self.my_x += (target_box._vc.x - self.start_x) / 10
#        self.my_y += (target_box._vc.y - self.start_y) / 10
#        if ((round(self.my_x, 2) == round(target_box._vc.x, 2)) and (round(self.my_y, 2) == round(target_box._vc.y, 2))):
#            self.path_step += 1
#            self.start_x = self.my_x
#            self.start_y = self.my_y
#        if ((round(self.my_x, 2) == round(self.end_box._vc.x, 2)) and (round(self.my_y, 2) == round(self.end_box._vc.y, 2))):
#            self.at_goal = True
