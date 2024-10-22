# 사용 사운드 출처: Pixabay(https://pixabay.com/ko/sound-effects/search/%ea%b2%8c%ec%9e%84%20%ec%82%ac%ec%9a%b4%eb%93%9c/?pagi=12)
# 파이게임 라이브러리와 필요한 모듈을 불러옴
import random
import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_SPACE, K_a, Rect

# 파이게임 초기화
pygame.init()

# 사운드 초기화 및 파일 로드
pygame.mixer.init()  # 믹서 초기화
waiting_music = pygame.mixer.Sound('tenefo-73435.mp3')  # 대기 화면 음악
missile_sound = pygame.mixer.Sound('big-hit-sound-effect-241416.mp3')  # 미사일 발사 소리
game_over_sound = pygame.mixer.Sound('game-over-160612.mp3')  # 게임 오버 소리
hit_sound = pygame.mixer.Sound('positive_beeps-85504.mp3')  # 장애물 맞췄을 때 소리

# 게임 창 제목 설정
pygame.display.set_caption('SHOOT_GAME')

# 키 입력 반복 설정 (15ms마다 반복)
pygame.key.set_repeat(15, 15)

# 게임 화면 크기 설정
SURFACE = pygame.display.set_mode((1000, 600))

# 프레임 속도 설정
FPSCLOCK = pygame.time.Clock()

# 큰 폰트와 작은 폰트 설정
Big_font = pygame.font.SysFont(None, 80)
Small_font = pygame.font.SysFont(None, 40)

# 객체를 그리기 위한 클래스 정의
class Draw:
    def __init__(self, col, rect, speed=0):
        # 객체의 색상, 위치(rect), 속도 설정
        self.col = col
        self.rect = rect
        self.speed = speed

    # 객체의 x축 이동
    def move(self):
        self.rect.centerx += self.speed

    # 타원을 그리는 함수
    def draw_E(self):
        pygame.draw.ellipse(SURFACE, self.col, self.rect)

    # 사각형을 그리는 함수
    def draw_R(self):
        pygame.draw.rect(SURFACE, self.col, self.rect)

# 게임 테두리를 그리는 함수
def Game_Border():
    # 시작점과 끝점을 설정하여 선을 그림
    Start_Point = [(100, 150), (100, 150), (100, 550), (900, 150)]
    End_Point = [(100, 550), (900, 150), (900, 550), (900, 550)]
    for index in range(len(Start_Point)):
        pygame.draw.line(SURFACE, (255, 255, 255), Start_Point[index], End_Point[index])

# 메인 게임 함수
def main():
    # 초기 속도 설정
    rock_speed = -5

    # 장애물 크기 설정
    RockWIDTH = 50
    RockHEIGHT = 50

    # 장애물의 초기 위치 설정
    xpos = 880
    ypos = random.randint(0,8)

    # 장애물 리스트
    Rock = []

    # 게임 상태, 놓친 장애물 수, 점수 초기화
    game_start = False
    Miss = 0
    Score = 0
    Beam_Count = 0

    # 플레이어 캐릭터와 미사일 설정
    Cir = Draw((255, 255, 255), Rect(50, 300, 30, 30))
    Beam = Draw((255, 255, 0), Rect(Cir.rect.centerx, Cir.rect.centery, 5, 5), 10)

    # 대기 음악 시작
    waiting_music.play(-1)  # 반복 재생

    # 게임 루프
    while True:
        # 화면에 보여줄 텍스트들
        message_Title = Big_font.render("SHOOT_GAME", True, (255, 255, 255))  # 게임 제목
        message_Score = Small_font.render(f"Score: {Score}", True, (255, 255, 255))  # 점수
        message_Miss = Small_font.render(f"Miss_Point: {Miss}", True, (255, 255, 255))  # 놓친 장애물 수
        message_game_start = Small_font.render("Game_start : Click the Space_Bar", True, (255, 255, 255))  # 게임 시작 메시지
        message_game_over = Big_font.render(f"Game_over_Score : {Score}", True, (255, 255, 255))  # 게임 오버 메시지
        message_caution = Small_font.render("Missile_Button : A , Missile is only one", True, (255, 255, 255))  # 미사일 주의사항

        # 화면을 검은색으로 채움
        SURFACE.fill((0, 0, 0))

        # 이벤트 처리 루프
        for event in pygame.event.get():
            # 게임 종료 이벤트 처리
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 키 입력 처리
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # 스페이스바를 누르면 게임 시작
                    rock_speed = -5
                    Miss = 0
                    Score = 0
                    game_start = True
                    waiting_music.stop()  # 대기 음악 중지
                elif event.key == K_UP:  # 위쪽 방향키를 누르면 플레이어 위로 이동
                    Cir.rect.centery -= 10
                elif event.key == K_DOWN:  # 아래쪽 방향키를 누르면 플레이어 아래로 이동
                    Cir.rect.centery += 10
                elif event.key == K_a and Beam_Count == 0:  # 'A' 키를 누르면 미사일 발사
                    Beam_Count = 1
                    Beam.rect.center = Cir.rect.center
                    missile_sound.play()  # 미사일 발사 소리 재생

        # 게임 시작 시
        if game_start:
            # 화면에 텍스트 출력
            SURFACE.blit(message_Title, (350, 20))
            SURFACE.blit(message_Score, (750, 160))
            SURFACE.blit(message_caution, (280, 100))
            SURFACE.blit(message_Miss, (700, 200))

            # 게임 테두리 그리기
            Game_Border()

            # 플레이어 그리기
            Cir.draw_E()

            # 플레이어 이동 제한 (위아래 벽 충돌 처리)
            if Cir.rect.centery <= 170:
                Cir.rect.centery = 170
            elif Cir.rect.centery >= 530:
                Cir.rect.centery = 530

            # 미사일 발사 처리
            if Beam_Count == 1:
                Beam.draw_E()  # 미사일 그리기
                Beam.move()  # 미사일 이동
                if Beam.rect.centerx >= 900:  # 미사일이 화면 밖으로 나가면 리셋
                    Beam.rect.center = Cir.rect.center
                    Beam_Count = 0

            # 장애물이 없으면 새로 생성
            if len(Rock) == 0:
                Rock.append(Draw((0, 255, 0), Rect(xpos, ypos * 40 + 170, RockWIDTH - ypos * 3, RockHEIGHT - ypos * 3), rock_speed))
            elif len(Rock) == 1:
                Rock[0].draw_R()  # 장애물 그리기
                Rock[0].move()  # 장애물 이동

                # 미사일과 장애물 충돌 시 처리
                if Rock[0].rect.colliderect(Beam.rect):
                    Beam.rect.center = Cir.rect.center
                    Beam_Count = 0
                    Score += 100
                    rock_speed -= 0.25
                    hit_sound.play()  # 장애물 맞췄을 때 소리 재생
                    del Rock[0]
                    ypos = random.randint(0, 8)

                # 장애물이 화면 밖으로 나가면 놓친 것으로 처리
                elif Rock[0].rect.centerx <= 100:
                    Beam.rect.center = Cir.rect.center
                    Beam_Count = 0
                    Miss += 1
                    del Rock[0]
                    ypos = random.randint(0, 8)

            # 놓친 장애물이 3개이면 게임 종료
            if Miss == 3:
                game_start = False
                game_over_sound.play()  # 게임 오버 소리 재생

        # 게임 종료 후
        elif not game_start and Miss == 3:
            SURFACE.blit(message_game_over, (250, 200))  # 게임 오버 메시지 표시
            SURFACE.blit(message_game_start, (300, 300))  # 다시 시작 메시지 표시

        # 게임 시작 전 대기 화면
        else:
            SURFACE.blit(message_Title, (320, 200))
            SURFACE.blit(message_game_start, (300, 300))

        # 화면 업데이트
        pygame.display.update()

        # 초당 30프레임으로 게임 실행
        FPSCLOCK.tick(30)

# 게임 실행
if __name__ == '__main__':
    main()
