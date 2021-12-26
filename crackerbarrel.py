from copy import deepcopy
import time

start_board = [[False] if y==1 else [True for x in range(y)] for y in range(1,6)]

def get_moves(board):
    moves = []
    for y in range(len(board)):
        for x in range(y+1):
            if not board[y][x]:
                continue
            pos = (y,x)
            neighbors = get_neighbors(pos)
            for neighbor in neighbors:
                ny, nx = neighbor
                # Neighbor must be there
                if not board[ny][nx]:
                    continue
                dy = ny-y
                dx = nx-x
                dest = (ny+dy,nx+dx)
                desty, destx = dest
                # Destination can't be taken
                if not is_on_board(dest) or board[desty][destx]:
                    continue
                moves.append((pos,neighbor,dest))
    return moves

def is_on_board(pos):
    y,x = pos
    return y >= 0 and y < len(start_board) and x >= 0 and x <= y

def get_neighbors(pos):
    y,x = pos
    neighbors = []
    # Diagonals
    for dy in (-1,1):
        for dx in (0,dy):
            neighbor = (y+dy,x+dx)
            if not is_on_board(neighbor):
                continue
            neighbors.append(neighbor)

    # Horizontals
    for dx in (-1,1):
        neighbor = (y, x+dx)
        if not is_on_board(neighbor):
            continue
        neighbors.append(neighbor)

    return neighbors

def apply_move(board, move):
    board = deepcopy(board)
    y, x = move[0]
    ny, nx = move[1]
    desty, destx = move[2]
    board[y][x] = False
    board[ny][nx] = False
    board[desty][destx] = True
    return board
    

def get_games(board=start_board, moves=[]):
    wins = []
    losses = []
    next_moves = get_moves(board)
    for move in next_moves:
        moved = apply_move(board, move)
        new_moves = deepcopy(moves)
        new_moves.append(move)
        new_wins, new_losses = get_games(moved, new_moves)
        wins.extend(new_wins)
        losses.extend(new_losses)
    if len(next_moves) == 0:
        left = sum([sum(row) for row in board])
        if left == 1:
            wins.append(moves)
            track_win()
        else:
            losses.append(moves)
    return wins, losses

def moves_str(moves):
    return ", ".join([f"{move[0]} -> {move[2]}" for move in moves])

def board_str(board):
    str_rows = [", ".join([str(val) for val in row]) for row in board]
    longest = max([len(row) for row in str_rows])
    return "\n".join([row.center(longest) for row in str_rows])

def track_win():
    global num_wins
    global start
    num_wins += 1
    if num_wins % 1000 == 0:
        elapsed = time.time() - start
        print(f"{num_wins} wins found over {round(elapsed)}s at {round(num_wins/elapsed,2)}w/s")

num_wins = 0
start = time.time()
wins, losses = get_games()
with open("wins.txt", "w") as f:
    for game in wins:
        f.write(moves_str(game)+"\n")
print(f"Done.  Found {len(losses)} losses.")
