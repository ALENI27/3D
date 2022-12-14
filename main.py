import time
from typing import List, Tuple
import pygame
from Player import Player
import numpy as np
# TODO: quand un point est derrière la caméra on flip son affichage


def nanosecond_to_second(nanosec: int) -> float:
    return nanosec/1000000000


def get_all_matrices(orientation: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    # pitch => x // yaw => y // roll => z de ce que j'ai fait a la logique mais il semble que
    # roll => x // pitch => y // yaw => z
    roll, pitch, yaw = orientation
    # le problème est probablement ici, ca projète les coorddonées dans un nouvel espace avant de
    mat1: np.ndarray = np.array([[1, 0, 0], [0, np.cos(roll), np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])
    mat2: np.ndarray = np.array([[np.cos(pitch), 0, -np.sin(pitch)], [0, 1, 0], [np.sin(pitch), 0, +np.cos(pitch)]])
    mat3: np.ndarray = np.array([[+np.cos(yaw), np.sin(yaw), 0], [-np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
    return mat1, mat2, mat3
    # return np.identity(3), np.identity(3), np.identity(3)


def to2D(a: np.ndarray, pl: Player, fov: float) -> np.ndarray:
    # TODO: ya une formule sans matrice, peut etre utiliser ca ou utiliser les deux methodes comme ca les deux existent
    c = pl.pos
    mat1, mat2, mat3 = get_all_matrices(pl.orientation)
    d = mat1.dot(
        mat2.dot(
            mat3.dot(
                np.subtract(a, c)
            )
        )
    )
    e = np.array([0, 0, fov])  # le dernier chiffre cest le FOV
    if d[2] <= 0:  # le truc est derrière
        pass
        # return np.array([-1,-1])
    bx = e[2]/d[2]*d[0]
    by = e[2]/d[2]*d[1]
    return np.array([bx, by])


def to2D_autre(a: np.ndarray, pl: Player, fov: float) -> np.ndarray:
    c = pl.pos
    x, y, z = (a[0]-c[0], a[1]-c[1], a[2]-c[2])
    roll, pitch, yaw = pl.orientation
    cx, cy, cz, sx, sy, sz = (np.cos(roll), np.cos(pitch), np.cos(yaw), np.sin(roll), np.sin(pitch), np.sin(yaw))

    dx = cy*(sz*y-cz*x)-sy*z
    dy = sx*(cy*z+sy*(sz*y+cz*x))+cx*(cz*y-sz*x)
    dz = cx*(cy*z+sy*(sz*y+cz*x))-sx*(cz*y-sz*x)
    ex, ey, ez = 0, 0, fov  # le dernier chiffre cest le FOV
    bx = ez/dz*dx+ex
    by = ez/dz*dy+ey
    return np.array([bx, by])


def coord_to_screen(coords: np.ndarray) -> np.ndarray:
    size = 10
    newCoord = np.array([coords[0]/size*500, coords[1]/size*500])
    return np.add(newCoord, 250)
    # return coords


# format [[Point1,Point2,Point3,...], [Point1,Point2,Point3,...]]
"""ELEMENTS: List[List[np.ndarray]] = [
    [
        np.array([-100, -100, 15]),
        np.array([-100, 100, 15]),
        np.array([100, 100, 15]),
        np.array([100, -100, 15])
    ],
    [
        np.array([-100, -100, -10]),
        np.array([-100, 100, -10]),
        np.array([100, 100, -10]),
        np.array([100, -100, -10])
    ]
]"""
"""    [
        np.array([-100, -100, 10]),
        np.array([-100, -100, 100]),
        np.array([-100, 100, 100]),
        np.array([-100, 100, 10])
    ],"""
ELEMENTS: List[List[np.ndarray]] = [
    [
        np.array([-20, -10, -10]),
        np.array([-20, -10, 100]),
        np.array([-20, 10, 100]),
        np.array([-20, 10, -10])
    ],
    [
        np.array([20, -10, -10]),
        np.array([20, -10, 100]),
        np.array([20, 10, 100]),
        np.array([20, 10, -10])
    ]
]
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("test 3D")
    screen = pygame.display.set_mode((500, 500))
    player: Player = Player(0, 0, -500, 0, 0, 0)
    pressed_keys: List[str] = []
    running: bool = True
    le_fov: float = 30
    fov_inc: bool = False
    fov_dec: bool = False
    clock = pygame.time.Clock()
    last_frame_time: int = time.time_ns()
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_UP:
                            pressed_keys.append("av")
                        case pygame.K_DOWN:
                            pressed_keys.append("ar")
                        case pygame.K_TAB:
                            pressed_keys.append("h")
                        case pygame.K_SPACE:
                            pressed_keys.append("b")
                        case pygame.K_LEFT:
                            pressed_keys.append("g")
                        case pygame.K_RIGHT:
                            pressed_keys.append("d")
                        case pygame.K_i:
                            pressed_keys.append("x+")
                        case pygame.K_k:
                            pressed_keys.append("x-")
                        case pygame.K_o:
                            pressed_keys.append("y+")
                        case pygame.K_l:
                            pressed_keys.append("y-")
                        case pygame.K_p:
                            pressed_keys.append("z+")
                        case pygame.K_m:
                            pressed_keys.append("z-")
                        case pygame.K_u:
                            fov_inc = True
                        case pygame.K_j:
                            fov_dec = True
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_UP:
                            pressed_keys.remove("av")
                        case pygame.K_DOWN:
                            pressed_keys.remove("ar")
                        case pygame.K_TAB:
                            pressed_keys.remove("h")
                        case pygame.K_SPACE:
                            pressed_keys.remove("b")
                        case pygame.K_LEFT:
                            pressed_keys.remove("g")
                        case pygame.K_RIGHT:
                            pressed_keys.remove("d")
                        case pygame.K_i:
                            pressed_keys.remove("x+")
                        case pygame.K_k:
                            pressed_keys.remove("x-")
                        case pygame.K_o:
                            pressed_keys.remove("y+")
                        case pygame.K_l:
                            pressed_keys.remove("y-")
                        case pygame.K_p:
                            pressed_keys.remove("z+")
                        case pygame.K_m:
                            pressed_keys.remove("z-")
                        case pygame.K_u:
                            fov_inc = False
                        case pygame.K_j:
                            fov_dec = False
                case pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    # player.moove_camera()
        if fov_inc:
            le_fov += .1
        if fov_dec:
            if le_fov > .1:
                le_fov -= .1
        surface: pygame.Surface = pygame.Surface((500, 500))
        for elem in ELEMENTS:
            pts = []
            lp = elem[-1]
            lp2D: np.ndarray = to2D(lp, player, le_fov)
            pts.append(lp2D)
            for point in elem:
                # if point[2] < player.pos[2] and lp[2] < player.pos[2]:
                #     continue
                point2D: np.ndarray = to2D(point, player, le_fov)
                pygame.draw.line(surface, pygame.Color(255, 0, 0), coord_to_screen(lp2D), coord_to_screen(point2D), 1)
                lp2D = point2D
                lp = point
                pts.append(lp2D)
            # print(pts)
        for key in pressed_keys:
            player.add_mouvement(key, nanosecond_to_second(time.time_ns()-last_frame_time))
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        last_frame_time: int = time.time_ns()
        clock.tick(200)
    pygame.quit()
