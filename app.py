from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

# ======= Labirin 8x8 =======
mazes = {
    'maze1': [[0,1,0,0,1,0,1,0],
              [0,1,0,1,0,0,0,0],
              [0,0,0,1,1,1,1,0],
              [1,1,0,0,0,0,1,0],
              [0,0,0,1,1,0,0,0],
              [0,1,1,1,0,1,1,0],
              [0,0,0,0,0,0,0,0],
              [1,1,1,1,1,1,0,0]],
    'maze2': [[0,1,1,1,1,0,0,0],
              [0,0,0,1,1,1,1,0],
              [1,1,0,0,0,1,0,0],
              [0,1,1,1,0,1,0,1],
              [0,0,0,1,0,0,0,0],
              [1,1,0,1,1,1,1,0],
              [0,0,0,0,0,0,0,0],
              [1,1,1,1,1,1,1,0]],
    'maze3': [[0,0,1,0,0,0,0,0],
              [1,0,1,0,1,1,1,0],
              [0,0,0,0,0,0,1,0],
              [0,1,1,1,1,0,1,0],
              [0,0,0,0,1,0,0,0],
              [1,1,1,0,1,1,1,0],
              [0,0,0,0,0,0,0,0],
              [1,1,1,1,1,1,0,0]],
    'maze4': [[0,1,0,0,0,1,0,0],
              [0,1,0,1,0,1,0,1],
              [0,0,0,1,0,0,0,1],
              [1,0,1,0,1,1,0,0],
              [0,0,0,0,0,1,1,0],
              [0,1,1,1,0,0,0,0],
              [0,0,0,1,1,1,1,0],
              [1,1,0,0,0,0,0,0]],
    'maze5': [[0,0,0,1,1,1,1,1],
              [0,1,0,1,0,0,0,1],
              [0,1,0,1,0,1,0,1],
              [0,1,0,1,0,1,0,1],
              [1,1,1,1,0,1,0,1],
              [1,0,0,0,0,1,0,1],
              [1,0,1,1,1,1,0,1],
              [1,0,0,0,0,0,0,0]]
}


current_maze = 'maze1'
maze = mazes[current_maze]

start = (0,0)
goal = (7,7)

# ======= BFS =======
def bfs(maze, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    explored = []
    while queue:
        pos, path = queue.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        explored.append(pos)
        if pos == goal:
            return explored, path
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = pos[0]+dx, pos[1]+dy
            if 0 <= nx < 8 and 0 <= ny < 8 and maze[nx][ny] != 1 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
    return explored, None

# ======= DFS =======
def dfs(maze, start, goal):
    stack = [(start, [start])]
    visited = set()
    explored = []
    while stack:
        pos, path = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        explored.append(pos)
        if pos == goal:
            return explored, path
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = pos[0]+dx, pos[1]+dy
            if 0 <= nx < 8 and 0 <= ny < 8 and maze[nx][ny] != 1 and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))
    return explored, None

@app.route('/')
def index():
    return render_template('index.html', maze=maze)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    algo = data.get('algo')

    if algo == 'bfs':
        explored, path = bfs(maze, start, goal)
    elif algo == 'dfs':
        explored, path = dfs(maze, start, goal)
    else:
        explored, path = [], None

    return jsonify({'path': path if path else [], 'explored': explored, 'algo': algo})

@app.route('/change_maze', methods=['POST'])
def change_maze():
    global current_maze, maze
    data = request.get_json()
    maze_name = data.get('maze')
    if maze_name in mazes:
        current_maze = maze_name
        maze = mazes[maze_name]
        return jsonify({'success': True, 'maze': maze})
    return jsonify({'success': False})

if __name__ == "__main__":
    app.run(debug=True)