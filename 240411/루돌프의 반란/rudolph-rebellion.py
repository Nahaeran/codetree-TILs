N, M, P, C, D = map(int, input().split())

board = [[0] * (N + 1) for _ in range(N + 1)]
results = [0] * (P + 1)
santa_positions = [0] * (P + 1)
santa_drop = [0] * (P + 1)

Rr, Rc = map(int, input().split())
board[Rr][Rc] = "R"

for _ in range(P):
    Pi, Sr, Sc = map(int, input().split())
    board[Sr][Sc] = Pi
    santa_positions[Pi] = [Sr, Sc, 0] # 행, 열, 스턴 여부


def cal_distance(P1, P2):
    return (P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2


# 충돌시 연산 함수 R: 루돌프 좌표, direct: 산타가 밀릴 방향, Si: 산타 번호, F: 밀리는 힘
def crash(R, direct, Si, F, t):
    global board, santa_positions, results
    board[R[0]][R[1]] = "R"

    Sr = R[0] + direct[0] * F
    Sc = R[1] + direct[1] * F
    # F 만큼 점수 적립
    results[Si] += F
    # 만약 게임판 밖이라면 해당 산타는 게임에서 탈락
    if 0 >= Sr or Sr > N  or 0 >= Sc or Sc > N:
        santa_positions[Si] = [Sr, Sc, turn]
        santa_drop[Si] = 1
    # 상호작용
    elif board[Sr][Sc] > 0:
        santa_positions[Si][2] = turn
        temp1 = Si
        r = Sr
        c = Sc
        temp2 = board[r][c]

        while temp2 != 0:
            board[r][c] = temp1
            santa_positions[temp1][0] = r
            santa_positions[temp1][1] = c
            temp1 = temp2
            r += direct[0]
            c += direct[1]
            if 0 < r <= N and 0 < c <= N:
                temp2 = board[r][c]
                if temp2 == 0:
                    board[r][c] = temp1
                    santa_positions[temp1][0] = r
                    santa_positions[temp1][1] = c
                    break
            else:
                santa_drop[temp2] = 1
                break
    # 부딪힌 산타가 게임판 안에 있을 때
    else:
        santa_positions[Si] = [Sr, Sc, turn]
        board[Sr][Sc] = Si


# 산타 이동 Si: 이동할 산타 번호, k: 이동할 방향 (상 우 하 좌), nr, nc: 이동후 좌표, turn: 해당 턴
def move_santa(Si, k, nr, nc, turn):
    global board, santa_positions

    Sr, Sc = santa_positions[Si][0:2]
    board[Sr][Sc] = 0
    santa_positions[i][0] = nr
    santa_positions[i][1] = nc
    if board[nr][nc] == "R":
        crash((Rr, Rc), (-1 * Sdi[k], -1 * Sdj[k]), Si, D, turn)
    else:
        board[nr][nc] = Si


turn = 1
Sdi = [-1, 0, 1, 0]
Sdj = [0, 1, 0, -1]

while turn <= M:
    # 턴마다 루돌프와 가장 가까운 산타 찾기 [r좌표, c좌표, 루돌프 번호]
    near = -1
    dist_near = N ** 2
    for i in range(1, P + 1):
        dist_santa = cal_distance((Rr, Rc), santa_positions[i])
        if not santa_drop[i] and dist_near >= dist_santa:
            if dist_near > dist_santa or (near[0] < santa_positions[i][0] or (near[0] == santa_positions[i][0] and near[1] < santa_positions[i][1])):
                near = [*santa_positions[i][0:2], i]
                dist_near = dist_santa

    # 하 우
    if Rr < near[0] and Rc < near[1]:
        board[Rr][Rc] = 0
        Rr += 1
        Rc += 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (1, 1), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 하
    elif Rr < near[0] and Rc == near[1]:
        board[Rr][Rc] = 0
        Rr += 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (1, 0), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 하 좌
    elif Rr < near[0] and Rc > near[1]:
        board[Rr][Rc] = 0
        Rr += 1
        Rc -= 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (1, -1), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 우
    elif Rr == near[0] and Rc < near[1]:
        board[Rr][Rc] = 0
        Rc += 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (0, 1), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 좌
    elif Rr == near[0] and Rc > near[1]:
        board[Rr][Rc] = 0
        Rc -= 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (0, -1), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 상 우
    elif Rr > near[0] and Rc < near[1]:
        board[Rr][Rc] = 0
        Rr -= 1
        Rc += 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (-1, 1), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 상
    elif Rr > near[0] and Rc == near[1]:
        board[Rr][Rc] = 0
        Rr -= 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (-1, 0), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    # 상 좌
    elif Rr > near[0] and Rc > near[1]:
        board[Rr][Rc] = 0
        Rr -= 1
        Rc -= 1
        if 0 < Rr <= N and 0 < Rc <= N:
            if board[Rr][Rc] > 0:
                crash((Rr, Rc), (-1, -1), near[2], C, turn)
            else:
                board[Rr][Rc] = "R"
    
    # -------------- 산타 이동 --------------
    for i in range(1, P + 1):
        if not santa_drop[i] and not santa_positions[i][2]:
            Sr, Sc = santa_positions[i][0:2]
            dist_santa = cal_distance((Rr, Rc), (Sr, Sc))

            dist = cal_distance((Rr, Rc), (Sr, Sc))
            direct = -1
            for k in range(4):
                nr = Sr + Sdi[k]
                nc = Sc + Sdj[k]
                if 0 < nr <= N and 0 < nc <= N and cal_distance((Rr, Rc), (nr, nc)) < dist and (board[nr][nc] == "R" or board[nr][nc] == 0):
                    dist = cal_distance((Rr, Rc), (nr, nc))
                    direct = k
            
            if direct == -1: continue
            move_santa(i, direct, Sr + Sdi[direct], Sc + Sdj[direct], turn)
    
    # 탈락하지 않은 산타 +1점
    for i in range(1, P + 1):
        if not santa_drop[i]:
            results[i] += 1
        if santa_positions[i][2] > 0 and santa_positions[i][2] + 1 == turn:
            santa_positions[i][2] = 0
    
    if sum(santa_drop[1:]) == P: break

    turn += 1

print(*results[1:])