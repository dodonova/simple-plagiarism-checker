def move_from(x, y):
    for ax, ay in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx, ny = x + ax, y + ay
        if nx < 0 or ny < 0 or nx >= m or ny >= n:
            continue
        if area[ny][nx] is None:
            continue
        if any(area[ny][nx]):
            continue
        area[ny][nx] = [x, y]
        move_from(nx, ny)


n, m = map(int, input().split())
area = [[[] for _ in range(m)] for _ in range(n)]
start = (0, 0)
end = (0, 0)
for y in range(n):
    inp = input()
    for x, elem in enumerate(inp):
        if elem == '#':
            area[y][x] = None
        if elem == 'S':
            start = (x, y)
        elif elem == 'F':
            end = (x, y)
area[end[1]][end[0]] = [1]
move_from(*end)
cmds = []
x, y = start
napr = 0
while area[y][x] != 1:
    nx, ny = area[y][x]
    ax, ay = nx - x, ny - y
    need_napr = 0 if ay == 1 else 1 if ax == -1 else 2 if ay == -1 else 3
    #if napr != need_napr:
    #    
print(cmds)