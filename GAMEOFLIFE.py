import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. 使用 np.roll 計算鄰居
def count_neighbors(grid):
    return sum(
        np.roll(np.roll(grid, i, 0), j, 1)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if not (i == 0 and j == 0)
    )

# 2. 不重疊放置 + 重試機制
def place_pattern(grid, pattern, max_attempts=50):
    rows, cols = grid.shape
    ph, pw = pattern.shape
    for _ in range(max_attempts):
        x = np.random.randint(0, rows - ph)
        y = np.random.randint(0, cols - pw)
        region = grid[x:x+ph, y:y+pw]
        if not np.any(region):
            grid[x:x+ph, y:y+pw] = pattern
            return True
    return False

# 3. 初始化隨機放置
def initialize_grid(rows, cols):
    grid = np.zeros((rows, cols), dtype=int)
    block = np.array([[1, 1],
                      [1, 1]])
    blinker = np.array([[1, 1, 1]])
    glider = np.array([[0, 1, 0],
                       [0, 0, 1],
                       [1, 1, 1]])
    toad = np.array([[0, 1, 1, 1],
                 [1, 1, 1, 0]])

    beacon = np.array([[1, 1, 0, 0],
                   [1, 0, 0, 0],
                   [0, 0, 0, 1],
                   [0, 0, 1, 1]])

    lwss = np.array([[0, 1, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [0, 0, 0, 0, 1],
                 [1, 0, 0, 1, 0]])

    patterns = [block, blinker, glider, toad, beacon, lwss]

    patterns = [block, blinker, glider]
    for pattern in patterns:
        for _ in range(40): # 每種 pattern 嘗試放 40 個
            place_pattern(grid, pattern)
    noise = np.random.rand(rows, cols) < 0.015  # 2% 的隨機活細胞
    grid = np.maximum(grid, noise.astype(int))      
    return grid



# 4. 主程式動畫
def update(frameNum, img, grid):
    neighbors = count_neighbors(grid)
    new_grid = (neighbors == 3) | (grid & (neighbors == 2))
    grid[:] = new_grid.astype(int)
    img.set_data(grid)
    return img,

def main():
    rows, cols = 100, 100
    grid = initialize_grid(rows, cols)

    # 深色背景
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')  
    ax.set_facecolor('black')         

    # 淺灰色細胞
    img = ax.imshow(grid, interpolation='nearest', cmap='gray', vmin=0, vmax=1)

    # 移除刻度線與邊框
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 標題
    ax.set_title("GAME OF LIFE", fontsize=16, color='white', pad=10)

    # 動畫設定
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid),
                                  frames=200, interval=100, blit=True)
    plt.show()

if __name__ == "__main__":
    main()


