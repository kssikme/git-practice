import pygame
import random

# pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("파이썬 버블버블 게임")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (76, 209, 55)
BUBBLE_BLUE = (0, 168, 255)
MONSTER_RED = (232, 65, 24)

clock = pygame.time.Clock()

# --- 클래스 정의 ---

class Player:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = WIDTH // 2
        self.y = HEIGHT - 70
        self.speed = 6
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽

    def draw(self):
        # 플레이어 캐릭터 (초록색 상자)
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # 바라보는 방향 표시
        eye_x = self.x + self.width - 10 if self.direction == 1 else self.x + 5
        pygame.draw.rect(screen, WHITE, (eye_x, self.y + 10, 5, 5))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
            self.direction = 1


class Bubble:
    def __init__(self, x, y, direction):
        self.radius = 12
        self.x = x
        self.y = y
        self.speed = 10 * direction
        self.float_speed = 2
        self.life_time = 0

    def move(self):
        # 일정 거리를 날아간 후 위로 수증기처럼 상승
        if self.life_time < 20:
            self.x += self.speed
        else:
            self.y -= self.float_speed
        self.life_time += 1

    def draw(self):
        pygame.draw.circle(screen, BUBBLE_BLUE, (int(self.x), int(self.y)), self.radius, 2)


class Monster:
    def __init__(self):
        self.width = 35
        self.height = 35
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, 300)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-2, 2])

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # 벽에 부딪히면 튕김
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT - 150:
            self.dy *= -1

    def draw(self):
        pygame.draw.rect(screen, MONSTER_RED, (self.x, self.y, self.width, self.height))


# --- 객체 생성 ---
player = Player()
bubbles = []
monsters = [Monster() for _ in range(5)]
score = 0
font = pygame.font.SysFont("malgungothic", 24)

# --- 메인 게임 루프 ---
running = True
while running:
    clock.tick(60)  # FPS 설정 (60fps)

    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 방울 발사 (플레이어 중앙에서 시작)
                bubble_x = player.x + player.width if player.direction == 1 else player.x
                bubbles.append(Bubble(bubble_x, player.y + 20, player.direction))

    # 2. 이동 및 상태 업데이트
    keys = pygame.key.get_pressed()
    player.move(keys)

    # 방울 이동 및 화면 밖 제거
    for bubble in bubbles[:]:
        bubble.move()
        if bubble.y < -10 or bubble.x < -10 or bubble.x > WIDTH + 10:
            bubbles.remove(bubble)

    # 몬스터 이동 및 충돌 체크
    for monster in monsters[:]:
        monster.move()

        # 방울과 몬스터 충돌 감지
        monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
        for bubble in bubbles[:]:
            bubble_rect = pygame.Rect(bubble.x - bubble.radius, bubble.y - bubble.radius, bubble.radius * 2, bubble.radius * 2)
            
            if monster_rect.colliderect(bubble_rect):
                if monster in monsters:
                    monsters.remove(monster)
                if bubble in bubbles:
                    bubbles.remove(bubble)
                score += 100
                break

    # 3. 화면 그리기
    screen.fill(BLACK)

    # 바닥 그리기
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 30, WIDTH, 30))

    player.draw()

    for bubble in bubbles:
        bubble.draw()

    for monster in monsters:
        monster.draw()

    # 점수 표시
    score_text = font.render(f"점수: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 몬스터를 다 처치했을 경우
    if not monsters:
        win_text = font.render("모든 적을 처치했습니다! 승리!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()