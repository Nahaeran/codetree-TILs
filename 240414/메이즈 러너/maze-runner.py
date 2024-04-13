N, M, K = map(int, input().split())
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

board = [list(map(int, input().split())) for _ in range(N)]
p_board = [[[] for _ in range(N)] for _ in range(N)]

for _ in range(M):
    x,y = map(int, input().split())
    p_board[x - 1][y - 1].append(0)

e_x, e_y = map(int, input().split())
e_x -= 1
e_y -= 1
board[e_x][e_y] = -1
score = 0


def move():
    global board, p_board, e_x, e_y, score,no_player
    new_p_board = [[[] for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if p_board[x][y]:
                for k in range(len(p_board[x][y])):
                    moved=False
                    for i in range(4):
                        nx = x + dx[i]
                        ny = y + dy[i]
                        if 0 > nx or nx >= N or 0 > ny or N <= ny:
                            continue
                        if board[nx][ny] == 0 and abs(x - e_x) + abs(y - e_y) > abs(nx - e_x) + abs(ny - e_y):
                            cnt = p_board[x][y][k]
                            new_p_board[nx][ny].append(cnt + 1)
                            score += 1
                            moved = True
                            break
                        if board[nx][ny] == -1:
                            score += 1
                            moved = True
                            break
                            
                    if not moved:
                        new_p_board[x][y].append(p_board[x][y][k])
    p_board = new_p_board
    

def find_square():
    global p_board, board
    for length in range(2, N + 1):
        for x in range(N + 1- length):
            for y in range(N+1-length):
                has_player,has_exit=False,False
                for i in range(length):
                    for j in range(length):
                        if p_board[x+i][y+j]:
                            has_player=True
                        if board[x+i][y+j]==-1:
                            has_exit=True
                if has_player and has_exit:
                    return (x,y,length)


def end():
    global p_board
    for x in range(N):
        for y in range(N):
            if p_board[x][y]:
                return False
    return True


def rotate_square(x, y, length):
    global p_board, board, e_x, e_y
    new_p_board = [[[] for _ in range(N)] for _ in range(N)]
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(length):
        for j in range(length):
            new_board[i][j] = board[x + length - 1 - j][y + i]
            if new_board[i][j] >= 1:
                new_board[i][j] -= 1
            new_p_board[i][j] = p_board[x + length -1 - j][y + i]
    for i in range(length):
        for j in range(length):
            board[x + i][y + j] = new_board[i][j]
            if new_board[i][j]==-1:
                e_x, e_y = x + i, y + j
            p_board[x + i][y + j] = new_p_board[i][j]


for _ in range(K):
    move()
    if not end():
        x, y, length = find_square()
        rotate_square(x, y, length)
    else:
        break

print(score)
print(e_x + 1, e_y + 1)