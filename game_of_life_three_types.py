import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# --- 參數設定 ---
GRID_SIZE = 80
STEPS = 200
NUM_BLOCKS = 10
NUM_BLINKERS = 10
NUM_GLIDERS = 10

# --- 網格初始化（用整數表示不同型態）---
# 0 = 死亡 / 空白
# 1 = Block (穩定)
# 2 = Blinker (震盪)
# 3 = Glider (移動)
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# --- 三種圖樣定義 ---
BLOCK = np.array([[1, 1],
                  [1, 1]])

BLINKER = np.array([[1, 1, 1]])

GLIDER = np.array([[0, 1, 0],
                   [0, 0, 1],
                   [1, 1, 1]])

# --- 放置函式（用不同數字代表來源）---
def place_pattern(pattern, grid, code):
    px, py = pattern.shape
    x = random.randint(0, GRID_SIZE - px - 1)
    y = random.randint(0, GRID_SIZE - py - 1)
    for i in range(px):
        for j in range(py):
            if pattern[i, j] == 1:
                grid[x+i, y+j] = code

# --- 隨機生成多個 ---
for _ in range(NUM_BLOCKS):
    place_pattern(BLOCK, grid, 1)
for _ in range(NUM_BLINKERS):
    place_pattern(BLINKER, grid, 2)
for _ in range(NUM_GLIDERS):
    place_pattern(GLIDER, grid, 3)

# --- Conway's Game of Life 更新規則 ---
def count_neighbors(x, y, grid):
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            total += (grid[(x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE] > 0)
    return total

def update(frame_num, img, grid):
    new_grid = np.copy(grid)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbors = count_neighbors(x, y, grid)
            alive = grid[x, y] > 0
            if alive and (neighbors < 2 or neighbors > 3):
                new_grid[x, y] = 0  # 死亡
            elif not alive and neighbors == 3:
                # 出生的細胞繼承周圍最多的顏色
                neighbor_vals = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        val = grid[(x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE]
                        if val > 0:
                            neighbor_vals.append(val)
                if neighbor_vals:
                    new_grid[x, y] = max(set(neighbor_vals), key=neighbor_vals.count)
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return (img,)

# --- 自訂顏色映射（不同型態不同顏色）---
from matplotlib.colors import ListedColormap
cmap = ListedColormap([
    "black",      # 0 死亡
    "yellow",     # 1 Block
    "cyan",       # 2 Blinker
    "red"         # 3 Glider
])

# --- 動畫 ---
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap=cmap, interpolation="nearest", vmin=0, vmax=3)
ax.set_title("Color Game of Life: Block (Yellow) / Blinker (Cyan) / Glider (Red)")
ax.axis("off")

ani = animation.FuncAnimation(fig, update, fargs=(img, grid),
                              frames=STEPS, interval=150, save_count=50)
plt.show()
ani.save("game_of_life_random.gif", writer="pillow", fps=10)
