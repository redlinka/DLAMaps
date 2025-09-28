import numpy as np
from fltk import *
from random import choice

# Grid parameters
size = nbH = nbL = int(input("enter tree resolution (recommended: 150: "))
grid = np.zeros((nbH, nbL), dtype=int)

# Visualization parameters
h = l = 1000
n = int(input("enter tree size in number of points (recommended: 2000: "))


# A modest implementation of the DLA algorythm
def DLA(grid, n):
    x1, y1 = len(grid) // 2, len(grid[0]) // 2
    grid[x1, y1] = True

    # zones de spawn des pts definie par les cotes de la fenetre
    spawn_points = [
        (0, np.random.randint(0, grid.shape[1])),
        (grid.shape[0] - 1, np.random.randint(0, grid.shape[1])),
        (np.random.randint(0, grid.shape[0]), grid.shape[1] - 1),
        (np.random.randint(0, grid.shape[0]), 0)
    ]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  #(1, 1), (-1, 1), (1, -1), (-1, -1)
                  ]

    for i in range(n):

        #nouveau pt
        x2, y2 = choice(spawn_points)

        while True:
            dx, dy = choice(directions)
            new_x, new_y = x2 + dx, y2 + dy

            if 0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1]:
                if grid[new_x, new_y]:

                    # le pt colle
                    grid[x2, y2] = True
                    break

                # on bouge le pt
                x2, y2 = new_x, new_y

        #affichage periodique
        if i % 10 == 0:
            efface('frame')
            visuel(grid)
            mise_a_jour()

    #affichage final
    efface('frame')
    visuel(grid)
    mise_a_jour()

def detecter_piece(M, i, j):
    piece = set()
    stack = [(i, j)]
    piece.add((i, j))
    
    while stack:
        x, y = stack.pop()
        
        # Check all 4 directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < M.shape[0] and 0 <= ny < M.shape[1]:  # Bounds check
                if M[nx, ny] == M[x, y] and (nx, ny) not in piece:
                    piece.add((nx, ny))
                    stack.append((nx, ny))
    
    return piece


def affiche_case(c, grid, color):
    
        rectangle(
            c[0] * (h / nbH), c[1] * (l / nbL),
            c[0] * (h / nbH) + (h / nbH), c[1] * (l / nbL) + (l / nbL),
            color, color, tag='frame'
        )

def visuel(grid):
    
    for i in range(nbL):
        for j in range(nbH):
            if grid[i, j]:
                affiche_case((i, j), grid,'white')
            if grid[i, j] == 2:
                affiche_case((i, j), grid,'black')
            

if __name__ == '__main__':
    cree_fenetre(h, l)
    rectangle(0,0,h,l,'black','black',5)
    DLA(grid, n)
    p = detecter_piece(grid,0,0)
    p = p.union(detecter_piece(grid,grid.shape[0]-1,0))
    p = p.union(detecter_piece(grid,0,grid.shape[1]-1))
    p = p.union(detecter_piece(grid,grid.shape[0]-1,grid.shape[1]-1))
    for coo in p:
        grid[coo] = 2
    visuel(grid)
    for i in range(nbL):
        for j in range(nbH):
            if grid[i,j]  == 0:
                affiche_case((i, j), grid,'white')

    attend_fermeture()