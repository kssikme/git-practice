import pygame
import random

# 게임 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS = SCREEN_WIDTH // GRID_SIZE
ROWS = SCREEN_HEIGHT // GRID_SIZE

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
SHAPES_COLORS = [
    (0, 255, 255),  # I: 청록
    (255, 255, 0),  # O: 노랑
    (128, 0, 128),  # T: 보라
    (0, 255, 0),    # S: 초록
    (255, 0, 0),    # Z: 빨강
    (0, 0, 255),    # J: 파랑
    (255, 165, 0)   # L: 주황
]

# 테트리스 블록 모양 (4x4 그리드 기반)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

class Tetris:
    def __init__(self):
        self.grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = SHAPES[shape_idx]
        self.color = SHAPES_COLORS[shape_idx]
        self.x = COLUMNS // 2 - len(self.current_piece[0]) // 2
        self.y = 0

    def valid_move(self, piece, offset_x, offset_y):
        for r, row in enumerate(piece):
            for c, val in enumerate(row):
                if val:
                    new_x = self.x + c + offset_x
                    new_y = self.y + r + offset_y
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def rotate_piece(self):
        # 시계 방향 회전
        rotated = [list(row) for row in zip(*self.current_piece[::-1])]
        if self.valid_move(rotated, 0, 0):
            self.current_piece = rotated

    def lock_piece(self):
        for r, row in enumerate(self.current_piece):
            for c, val in enumerate(row):
                if val:
                    self.grid[self.y + r][self.x + c] = self.color
        self.clear_lines()
        self.new_piece()
        if not self.valid_move(self.current_piece, 0, 0):
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        cleared = ROWS - len(new_grid)
        self.score += cleared * 100
        for _ in range(cleared):
            new_grid.insert(0, [BLACK for _ in range(COLUMNS)])
        self.grid = new_grid

    def drop(self):
        if self.valid_move(self.current_piece, 0, 1):
            self.y += 1
        else:
            self.lock_piece()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("파이썬 테트리스")
    clock = pygame.time.Clock()
    game = Tetris()
    
    fall_time = 0
    fall_speed = 500  # 블록이 떨어지는 속도 (밀리초 단위)

    while not game.game_over:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        # 일정 시간마다 블록 하강
        if fall_time >= fall_speed:
            game.drop()
            fall_time = 0

        # 키 입력을 통한 이동 및 회전
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.valid_move(game.current_piece, -1, 0):
                    game.x -= 1
                elif event.key == pygame.K_RIGHT and game.valid_move(game.current_piece, 1, 0):
                    game.x += 1
                elif event.key == pygame.K_DOWN and game.valid_move(game.current_piece, 0, 1):
                    game.y += 1
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:  # 하드 드롭
                    while game.valid_move(game.current_piece, 0, 1):
                        game.y += 1
                    game.lock_piece()

        # 고정된 그리드 블록 그리기
        for r in range(ROWS):
            for c in range(COLUMNS):
                pygame.draw.rect(screen, game.grid[r][c], (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, GRAY, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # 현재 조종 중인 블록 그리기
        for r, row in enumerate(game.current_piece):
            for c, val in enumerate(row):
                if val:
                    px = (game.x + c) * GRID_SIZE
                    py = (game.y + r) * GRID_SIZE
                    pygame.draw.rect(screen, game.color, (px, py, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, WHITE, (px, py, GRID_SIZE, GRID_SIZE), 1)

        pygame.display.update()

    print(f"게임 오버! 최종 점수: {game.score}")
    pygame.quit()

if __name__ == "__main__":
    main()