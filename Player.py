import numpy as np

class Player:
    def __init__(self,
                 pos_x: float = 0,
                 pos_y: float = 0,
                 pos_z: float = 0,
                 roll: float = 0,
                 pitch: float = 0,
                 yaw: float = 0,
                 speed: float = 300):
        self.pos = np.array([pos_x, pos_y, pos_z], dtype=float)
        self.orientation = np.array([roll, pitch, yaw], dtype=float)  # roll pitch yaw les noms sont pas forcément bons
        self.speed: float = speed
        self.cpt = 0

    def add_mouvement(self, orientation: str, time: float):
        dist = self.speed * time
        ang = .5 * time
        match orientation:
            case "av":
                self.pos[2] += dist
            case "ar":
                self.pos[2] -= dist
            case "h":
                self.pos[1] += dist
            case "b":
                self.pos[1] -= dist
            case "d":
                self.pos[0] += dist
            case "g":
                self.pos[0] -= dist
            case "x+":
                self.orientation[0] += ang
            case "x-":
                self.orientation[0] -= ang
            case "y+":
                self.orientation[1] += ang
            case "y-":
                self.orientation[1] -= ang
            case "z+":
                self.orientation[2] += ang
            case "z-":
                self.orientation[2] -= ang
        self.cpt += 1
        # if self.cpt%100 == 0:
        print(self.pos)
        print(self.orientation)

    def moove_camera(self, horizontal, vertical):
        raise "on vas s'en occuper plus tard"
