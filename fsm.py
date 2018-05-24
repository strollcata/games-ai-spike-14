from math import sqrt
from point2d import Point2D
from graphics import egi
from random import randrange

class FiniteStateMachine(object):
    def __init__(self, world):
        self.world = world
        self.hl_state = "Patrol"
        self.ll_state = "Search"
        self.next_waypoint = None
        self.vel_x = False
        self.vel_y = False
        self.projectile = None
        self.proj_target = None
        self.proj_vel_x = False
        self.proj_vel_y = False
        self.clip = 10
        self.visited = []

    def update(self):
        if self.hl_state == "Patrol":
            self.agent_patrol()
        else:
            self.agent_attack()

    def draw(self):
        if self.projectile:
            egi.green_pen()
            egi.set_stroke(10)
            egi.circle(self.projectile, 3)

    def agent_attack(self):
        if self.ll_state == "Shoot":
            self.agent_shoot()
        elif self.ll_state == "Reload":
            self.agent_reload()
        else:
            self.agent_clean()

    def agent_patrol(self):
        if self.ll_state == "Walk":
            self.agent_walk()
        elif self.ll_state == "Search":
            self.agent_search()
        else:
            self.agent_path()

    def agent_shoot(self):
        if self.projectile:
            if ((self.proj_vel_x) or (self.proj_vel_y)):
                if ((self.projectile.x >= self.proj_target.x - 2) and (self.projectile.x <= self.proj_target.x + 2) and (self.projectile.y >= self.proj_target.y - 2) and (self.projectile.y <= self.proj_target.y + 2)):
                    self.proj_vel_x = False
                    self.proj_vel_y = False
                    self.projectile = False
                    self.proj_target = False
                    self.world.enemy.health -= 1
                    if ((self.world.enemy.health <= 0) or (self.clip <= 0)):
                        self.ll_state = "Reload"
                else:
                    self.projectile.x += self.proj_vel_x / 3
                    self.projectile.y += self.proj_vel_y / 3
            else:
                self.proj_vel_x = self.proj_target.x - self.projectile.x
                self.proj_vel_y = self.proj_target.y - self.projectile.y
        else:
            print("Firing...")
            self.projectile = Point2D(self.world.agent.my_x, self.world.agent.my_y)
            self.proj_target = Point2D(self.world.enemy.my_x, self.world.enemy.my_y)
            self.clip -= 1

    def agent_reload(self):
        print("Reloading...")
        self.clip = 10
        if self.world.enemy.health <= 0:
            self.ll_state = "Clean"

    def agent_clean(self):
        print("Cleaning up enemy...")
        self.world.create_agents()
        self.hl_state = "Patrol"
        self.ll_state = "Search"

    def agent_walk(self):
        if self.next_waypoint:
            if ((self.vel_x) or (self.vel_y)):
                if ((self.world.agent.my_x >= self.next_waypoint.x - 2) and (self.world.agent.my_x <= self.next_waypoint.x + 2) and (self.world.agent.my_y >= self.next_waypoint.y - 2) and (self.world.agent.my_y <= self.next_waypoint.y + 2)):
                    self.vel_x = False
                    self.vel_y = False
                    for box in self.world.boxes:
                        if box._vc == self.next_waypoint:
                            self.world.agent.my_box = box
                            self.world.agent.idx = box.idx
                            self.visited.append(box.idx)
                    self.world.agent.my_x = self.world.agent.my_box._vc.x
                    self.world.agent.my_y = self.world.agent.my_box._vc.y
                    self.ll_state = "Search"
                else:
                    self.world.agent.my_x += self.vel_x / 3
                    self.world.agent.my_y += self.vel_y / 3
            else:
                print("Walking...")
                self.vel_x = self.next_waypoint.x - self.world.agent.my_x
                self.vel_y = self.next_waypoint.y - self.world.agent.my_y                    

    def agent_search(self):
        print("Searching...")
        if self.world.path:
            sep_dist = int((self.world.agent.my_box.coords[0] - self.world.agent.my_box.coords[2]) * 1.2)
            for box in self.world.boxes:
                if ((self.world.agent.my_x >= box._vc.x - sep_dist) and (self.world.agent.my_x <= box._vc.x + sep_dist) and (self.world.agent.my_y >= box._vc.y - sep_dist) and (self.world.agent.my_y <= box._vc.y + sep_dist) and (box == self.world.enemy.my_box)):
                    self.hl_state = "Attack"
                    self.ll_state = "Shoot"
                    self.proj_target = box._vc
                    break
                self.proj_target = False
            if not self.proj_target:
                self.ll_state = "Path"

    def agent_path(self):
        print("Pathing...")
        if self.world.path:
            erase_visited = True
            for chkbox in self.world.boxes:
                if ((chkbox.idx not in self.visited) and (chkbox.kind != 'X')):
                    erase_visited = False
            if ((erase_visited) and (self.world.agent.idx == self.world.agent.start_idx)):
                print("Restarting patrol...")
                self.visited = []
            new_places = []
            for key, value in self.world.path.route.items():
                if value == self.world.agent.idx:
                    if ((key != self.world.agent.idx) and (key not in self.visited)):
                        new_places.append(key)
            if new_places != []:
                place_select = new_places[randrange(len(new_places))]
                self.next_waypoint = self.world.boxes[place_select]._vc
            else:
                for key, value in self.world.path.route.items():
                    if key == self.world.agent.idx:
                        if value != self.world.agent.idx:
                            self.next_waypoint = self.world.boxes[value]._vc
            self.ll_state = "Walk"
