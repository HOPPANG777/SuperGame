"""결과 보고서 docx 가독성 리팩토링 (내용 변경 없음)."""
import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SRC = Path(r"c:\Users\a0106\Documents\조승영_202613111_SuperGame.docx")
OUT = Path(__file__).resolve().parent / "조승영_202613111_SuperGame.docx"
BAK = SRC.with_suffix(".docx.bak")


def set_run_font(run, size=11, bold=False, color=None):
    run.font.name = "맑은 고딕"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def add_para(doc, text, style="Normal", size=11, bold=False, space_before=0, space_after=6, indent=0):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.25
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return p


def add_bullet(doc, text, indent=0.5):
    return add_para(doc, f"· {text.lstrip('· ')}", indent=indent, space_after=4)


def build_document():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)

    # 표지
    add_para(doc, "게임 스크립트 프로그래밍 — 결과 보고서", size=18, bold=True, space_after=18)
    for line in [
        "과목: 게임 스크립트 프로그래밍",
        "학번: 202613111",
        "이름: 조승영",
        "게임명: Super Game",
        "개발 환경: Python 3.14, pygame-ce 2.5.7",
    ]:
        add_para(doc, line.strip(), size=11, space_after=4)
    add_para(doc, "", space_after=12)

    # 1. 게임 소개
    add_para(doc, "게임 소개", size=14, bold=True, space_before=6, space_after=10)
    add_para(doc, "1.1 제목 Super Game", bold=True, space_after=4)
    add_para(doc, "1.2 장르 2D 탑뷰 생존 액션 (Vampire Survivors 유형)", space_after=8)
    add_para(doc, "1.3 기획 의도 기획서에서 정한 목표는 다음과 같다.", space_after=6)
    for line in [
        "화면 안에서 3분간 생존하면 클리어한다.",
        "WASD로 이동하며, 화면 밖으로 나갈 수 없다.",
        "플레이어 주위를 Cos/Sin으로 도는 무기가 적을 처치한다.",
        "적은 플레이어 기준 원형 경계 밖에서 Cos/Sin 좌표로 스폰된다.",
        "적 처치 시 조각이 드롭되고, 조각 16개마다 무기가 1개 증가한다.",
        "적과 충돌하면 목숨이 1 감소한다. 목숨은 3개이며, 0이 되면 패배한다.",
        "피격 후 약 1.5초 동안 무적(깜빡임) 상태가 된다.",
    ]:
        add_bullet(doc, line)
    add_para(doc, "위 규칙을 pygame으로 구현했다.", space_before=6, space_after=8)
    add_para(doc, "1.4 승리 / 패배 조건", bold=True, space_after=4)
    add_para(doc, "승리 (CLEAR): 남은 시간 00:00 도달 (3분 생존)", indent=0.5, space_after=4)
    add_para(doc, "패배 (GAMEOVER): 목숨 0 → 사망 애니메이션 후 패배 화면", indent=0.5, space_after=12)

    # 2. 조작법
    add_para(doc, "조작법", size=14, bold=True, space_before=6, space_after=10)
    add_para(doc, "2.1 타이틀 화면", bold=True, space_after=4)
    add_para(doc, "SPACE / ENTER → 게임 시작", indent=0.5, space_after=4)
    add_para(doc, "마우스 클릭 → 「게임 시작」 버튼", indent=0.5, space_after=8)
    add_para(doc, "2.2 플레이 중", bold=True, space_after=4)
    add_para(doc, "W / A / S / D → 상·하·좌·우 이동 (초당 200px)", indent=0.5, space_after=8)
    add_para(doc, "2.3 결과 화면", bold=True, space_after=4)
    for line in [
        "승리 / 버튼·ENTER → 종료",
        "승리 / ESC → 타이틀",
        "패배 / R·「다시하기」 → 재시작",
        "패배 / ESC·「타이틀로」 → 타이틀",
    ]:
        add_para(doc, line, indent=0.5, space_after=4)
    add_para(doc, "2.4 실행 방법", bold=True, space_before=4, space_after=4)
    add_para(doc, "소스 실행: venv\\Scripts\\python.exe game.py", indent=0.5, space_after=4)
    add_para(doc, "exe 실행: SuperGame.exe와 같은 폴더에 assets 폴더 필요", indent=0.5, space_after=12)

    # 3. 핵심 구현
    add_para(doc, "핵심 구현", size=14, bold=True, space_before=6, space_after=10)
    add_para(doc, "3.1 프로젝트 구조", bold=True, space_after=6)
    # 원문 구조 유지: 37-38행 내용을 원래 단락 형태로
    add_para(doc, "game.py 진입점", indent=0.5, space_after=4)
    add_para(doc, "scripts/ game_manager.py 상태 머신,", indent=0.5, space_after=4)
    add_para(
        doc,
        "메인 루프 play_session.py 플레이 업데이트·충돌·렌더 player.py 플레이어 이동·애니메이션 enemy.py 적 이동 enemy_spawner.py 적 생성·난이도 orbiting_weapons.py Cos/Sin 회전 무기 fragment.py 조각 드롭·흡입 collision.py 충돌 판정 screens.py 타이틀·승리·패배 UI high_score.py 고득점 저장 paths.py 리소스 경로 (exe 대응) assets/images/ 스프라이트·UI assets/fonts/ 폰트 assets/sounds/ BGM·SFX",
        indent=0.5,
        space_after=8,
    )

    add_para(doc, "3.2 상태 머신 TITLE → PLAY → CLEAR ↘ DYING → GAMEOVER", bold=True, space_after=6)
    for line in [
        "TITLE: 타이틀 배경, 최고 점수, 시작 버튼",
        "PLAY: 플레이, HUD, 충돌 처리",
        "DYING: 사망 애니메이션 재생",
        "CLEAR: 승리 화면 (이겼다2.png)",
        "GAMEOVER: 패배 화면 (막혔다2.png)",
    ]:
        add_para(doc, line, indent=0.5, space_after=4)
    add_para(doc, "GameManager가 self.state로 상태를 관리한다.", space_before=4, space_after=8)

    add_para(doc, "3.3 주요 클래스", bold=True, space_after=6)
    classes = [
        "GameManager (game_manager.py) — 초기화, 이벤트, 상태 전환",
        "PlaySession (play_session.py) — 플레이 로직·충돌·그리기",
        "Player (player.py) — WASD 이동, Idle/Run/Die 애니메이션",
        "Enemy (enemy.py) — 플레이어 추적 이동",
        "EnemySpawner (enemy_spawner.py) — 시간·점수 기반 스폰",
        "OrbitingWeapons (orbiting_weapons.py) — 무기 개수·각도·Cos/Sin 배치",
        "Fragment (fragment.py) — 드롭, 근거리 흡입, 수집",
        "ScreenRenderer (screens.py) — 메뉴 화면·버튼",
        "high_score.py — score.txt 읽기/쓰기",
    ]
    for line in classes:
        add_para(doc, line, indent=0.5, space_after=4)

    add_para(doc, "3.4 Cos/Sin 활용 무기 배치 (orbiting_weapons.py) wx = cx + cos(angle) * radius wy = cy + sin(angle) * radius", bold=True, space_before=6, space_after=4)
    add_para(doc, "적 스폰 (enemy.py) spawn_x = player_x + cos(θ) * spawn_radius spawn_y = player_y + sin(θ) * spawn_radius", space_after=8)

    add_para(doc, "3.5 충돌 처리 (collision.py)", bold=True, space_after=4)
    for line in [
        "무기 ↔ 적: groupcollide → 적 제거, 점수·조각",
        "플레이어 ↔ 적: spritecollide → 목숨 감소, 무적 시작",
        "플레이어 ↔ 조각: spritecollide → 조각 수집, 무기 증가",
    ]:
        add_para(doc, line, indent=0.5, space_after=4)
    add_para(
        doc,
        "스프라이트 rect보다 판정이 커지지 않도록 hitbox_rect()로 비율 축소 후 collided 콜백에 적용한다. 플레이어: 0.74 / 적: 0.78 / 무기: 0.72",
        space_before=4,
        space_after=8,
    )

    add_para(doc, "3.6 애니메이션", bold=True, space_after=4)
    for line in [
        "SpriteSheet, FrameAnimator로 스프라이트 시트 분할·재생",
        "좌측 방향은 R 시트를 mirror_animator()로 좌우 반전",
        "타격: Hit.png (5×6, 30프레임)",
        "레벨업: Levelup.png 하단 7프레임 링",
    ]:
        add_bullet(doc, line)

    add_para(doc, "3.7 사운드", bold=True, space_before=6, space_after=4)
    sounds = [
        "입브금2.wav — BGM (루프)",
        "80_Start_01.wav — 시작",
        "25_Clear_01.wav — 클리어",
        "44_Defeat_01.wav — 패배",
        "59_Hit_01.wav — 적 처치 / 피격",
        "87_exp_up_1_short.wav — 조각 획득",
        "73_Lvl_up_01.wav — 레벨업",
    ]
    for line in sounds:
        add_para(doc, line, indent=0.5, space_after=3)

    add_para(doc, "3.8 고득점·배포", bold=True, space_before=6, space_after=4)
    for line in [
        "최고 점수: score.txt (try-except, 없을 때 0)",
        "PyInstaller: build.bat → dist\\SuperGame.exe",
        "exe 실행 시 assets/는 exe와 같은 위치에서 로드 (paths.py)",
    ]:
        add_bullet(doc, line)

    add_para(doc, "3.9 게임 수치", bold=True, space_before=6, space_after=4)
    for line in [
        "화면 크기: 1200 × 720",
        "생존 시간: 3분",
        "시작 무기 수: 2",
        "조각당 무기 증가: 16개",
        "목숨: 3",
        "무적 시간: 1.5초",
        "이동 속도: 200 px/s",
    ]:
        add_para(doc, line, indent=0.5, space_after=3)

    # 4. 트러블 슈팅
    add_para(doc, "트러블 슈팅", size=14, bold=True, space_before=12, space_after=10)
    troubles = [
        (
            "4.1 무기 초기화 시 AttributeError",
            [
                "현상: Weapon 생성 직후 self.rect.width 접근 시 rect가 None이라 오류 발생.",
                "원인: pygame-ce Sprite는 초기 rect=None.",
                "해결: _apply_image()에서 rect is not None일 때만 중심 좌표를 유지하도록 분기.",
            ],
        ),
        (
            "4.2 좌측 애니메이션 역재생",
            [
                "현상: L 방향 Idle/Run/Die, 도끼 애니메이션이 거꾸로 재생됨.",
                "원인: L 전용 시트를 별도 로드하면 프레임 순서가 R과 달라짐.",
                "해결: R 시트만 로드하고 mirror_animator()로 좌우 반전 프레임 생성.",
            ],
        ),
        (
            "4.3 충돌 판정이 스프라이트보다 큼",
            [
                "현상: 보이는 캐릭터·적·무기보다 먼저 충돌함.",
                "해결: hitbox_rect()로 rect를 비율 축소 후 collided 콜백에 적용.",
            ],
        ),
        (
            "4.4 히트박스 코드 실행 오류",
            [
                "현상: pygame.Rect.move_center 호출 시 AttributeError.",
                "원인: pygame-ce 버전에 move_center 미지원.",
                "해결: hitbox.center = base.center로 변경.",
            ],
        ),
        (
            "4.5 PyInstaller exe에서 리소스 미로드",
            [
                "현상: exe 실행 시 이미지·사운드 FileNotFoundError.",
                "해결: paths.py에서 exe 위치 기준 assets/ 경로 사용. build.bat으로 dist\\assets를 exe 옆에 복사.",
            ],
        ),
        (
            "4.6 UI 텍스트와 버튼 겹침",
            [
                "현상: 승리·패배 화면에서 점수와 버튼이 같은 y좌표에 배치됨.",
                "해결: 점수(y=488)와 버튼(세로 스택, y=548~) 위치 분리. 버튼 크기 190×59로 조정.",
            ],
        ),
    ]
    for title, lines in troubles:
        add_para(doc, title, bold=True, space_before=6, space_after=4)
        for line in lines:
            add_para(doc, line, indent=0.5, space_after=4)

    # 5. 결론
    add_para(doc, "결론", size=14, bold=True, space_before=12, space_after=10)
    add_para(
        doc,
        "기획서의 3분 생존, Cos/Sin 무기·스폰, 조각 16개당 무기 증가, 목숨 3·무적 규칙을 코드로 구현했다. 강의 13주차의 Player/Enemy 분리, groupcollide/spritecollide, 상태 머신을 적용했고, 14주차의 타이틀 UI, 고득점 저장, PyInstaller exe 빌드를 완료했다.",
        space_after=8,
    )
    add_para(
        doc,
        "scripts/ 폴더로 모듈을 분리했고, 충돌·경로·애니메이션 관련 오류를 단계별로 수정했다. 제출물은 소스, assets, exe, 본 보고서 PDF, 플레이 영상으로 구성한다.",
        space_after=12,
    )

    # 6. 플레이 영상
    add_para(doc, "플레이 영상", size=14, bold=True, space_before=6, space_after=10)
    add_para(doc, "별도 파일 게임플레이.mp4로 제출한다.", space_after=6)
    for line in [
        "파일명: 게임플레이.mp4 (zip 내 동봉)",
        "권장 길이: 1~3분",
        "포함 장면: 타이틀 → 플레이 → 무기 증가 → 클리어 또는 패배",
    ]:
        add_para(doc, line, indent=0.5, space_after=4)

    # 부록
    add_para(doc, "부록 — 에셋 출처", size=14, bold=True, space_before=12, space_after=10)
    add_para(doc, "대부분 자체 에셋입니다.", space_after=6)
    add_para(doc, "자체 에셋이 아닌 경우 아래에 서술합니다.’", space_after=8)
    add_para(doc, "파티클:", bold=True, space_after=4)
    add_para(doc, "https://ragnapixel.itch.io/particle-fx", indent=0.5, space_after=8)
    add_para(doc, "사운드:", bold=True, space_after=4)
    add_para(doc, "https://leohpaz.itch.io/minifantasy-dungeon-sfx-pack", indent=0.5, space_after=8)
    add_para(doc, "이를 제외한 모든 에셋은 직접 제작하여 작업하였습니다.", space_after=6)

    return doc


def main():
    if SRC.exists() and not BAK.exists():
        shutil.copy2(SRC, BAK)
    doc = build_document()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))
    try:
        doc.save(str(SRC))
        print("saved:", SRC)
    except PermissionError:
        print("saved:", OUT)
        print("note: Documents file is open. Close Word and copy OUT over SRC.")
    if BAK.exists():
        print("backup:", BAK)


if __name__ == "__main__":
    main()
