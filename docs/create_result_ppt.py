"""참고 PPT 양식 복사 → 결과 발표 PPT (3분할·Z자 배치 유지)."""
import shutil
from pathlib import Path

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parent.parent
REF = Path(r"c:\Users\a0106\Downloads\게임 스크립트 프로그래밍_조승영_202613111.pptx")
OUT = ROOT / "docs" / "결과발표_조승영_202613111.pptx"

DARK = RGBColor(0x1E, 0x29, 0x3B)
BODY = RGBColor(0x33, 0x41, 0x55)


def all_tb(slide):
    return sorted(
        [s for s in slide.shapes if s.has_text_frame],
        key=lambda s: (s.top, s.left),
    )


def clear_tb(shape):
    shape.text_frame.clear()


def write_one(shape, text, size=18, bold=False, color=None):
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color or (DARK if bold else BODY)


def write_lines(shape, lines, size=16):
    tf = shape.text_frame
    tf.clear()
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = BODY
        p.space_after = Pt(4)


def page_tb(slide):
    for s in slide.shapes:
        if s.has_text_frame and s.left > 10_800_000 and s.top > 6_200_000:
            return s
    return None


def main():
    shutil.copy2(REF, OUT)
    prs = Presentation(str(OUT))

    # 1. 표지
    s = prs.slides[0]
    for t in all_tb(s):
        clear_tb(t)
    left = [t for t in all_tb(s) if t.left < 5_000_000]
    write_one(left[0], "게임 스크립트 프로그래밍", 36, True)
    write_one(left[1], "Super Game  ·  결과 보고", 26, True)
    name = [t for t in all_tb(s) if t.left > 7_000_000 and t.top > 5_000_000][0]
    write_one(name, "조승영  ·  202613111", 15)
    write_one(page_tb(s), "01", 14)

    # 2. 목차 (Z자 대각 4칸)
    s = prs.slides[1]
    for t in all_tb(s):
        clear_tb(t)
    boxes = [t for t in all_tb(s) if t.top < 5_000_000]
    write_one(boxes[0], "CONTENTS", 28, True)
    write_one(boxes[1], "목차", 22, True)
    z_boxes = [
        t for t in all_tb(s) if 1_800_000 < t.top < 4_500_000 and 700_000 < t.left < 10_500_000
    ]
    nums = sorted([t for t in z_boxes if t.width < 500_000], key=lambda x: (x.top, x.left))
    titles = sorted([t for t in z_boxes if t.width >= 400_000], key=lambda x: (x.top, x.left))
    sections = ["게임 소개", "조작법", "핵심 기술", "트러블 슈팅"]
    for i, n in enumerate(nums[:4]):
        write_one(n, f"{i+1:02d}", 20, True)
    for i, t in enumerate(titles[:4]):
        write_one(t, sections[i], 18, True)
    write_one(page_tb(s), "02", 14)

    # 3. 게임 소개
    s = prs.slides[2]
    for t in all_tb(s):
        clear_tb(t)
    write_one(all_tb(s)[0], "게임 소개", 28, True)
    write_one(all_tb(s)[1], "개요", 22, True)
    body = [t for t in all_tb(s) if 1_900_000 < t.top < 3_500_000 and t.width > 2_000_000][0]
    write_lines(
        body,
        [
            "장르: 2D 탑뷰 생존 액션",
            "목표: 화면 안 3분 생존 시 클리어",
            "패배: 목숨 0 (시작 3, 피격 후 1.5초 무적)",
            "성장: 조각 16개마다 회전 무기 +1 (시작 2개)",
        ],
        17,
    )
    badge = [t for t in all_tb(s) if t.top > 4_500_000 and t.left < 4_000_000][0]
    write_one(badge, "클리어 3분  /  Cos·Sin 무기·스폰", 15)
    write_one(page_tb(s), "03", 14)

    # 4. 조작법 (4카드)
    s = prs.slides[3]
    for t in all_tb(s):
        clear_tb(t)
    write_one(all_tb(s)[0], "조작법", 28, True)
    write_one(all_tb(s)[1], "입력 및 규칙", 22, True)
    card_shapes = [
        t for t in all_tb(s) if 1_500_000 < t.top < 5_200_000 and t.left < 11_000_000
    ]
    headers = sorted(
        [t for t in card_shapes if t.height < 350_000],
        key=lambda x: (x.top, x.left),
    )
    bodies = sorted(
        [t for t in card_shapes if t.height >= 350_000],
        key=lambda x: (x.top, x.left),
    )
    cards = [
        ("이동", ["WASD: 상하좌우 (200px/s)", "화면 밖 이동 불가"]),
        ("시작", ["SPACE / ENTER / 버튼", "타이틀에서 게임 시작"]),
        ("결과 화면", ["승리: ENTER 종료, ESC 타이틀", "패배: R 재시작, ESC 타이틀"]),
        ("기록", ["적 처치 시 점수·조각", "최고 점수 score.txt 저장"]),
    ]

    pairs = []
    bds_rem = list(bodies)
    for h in headers[:4]:
        b = min(bds_rem, key=lambda x: abs(x.top - h.top) + abs(x.left - h.left) * 0.2)
        bds_rem.remove(b)
        pairs.append((h, b))
    pairs.sort(key=lambda x: (x[0].top, x[0].left))
    for i, (h, b) in enumerate(pairs):
        write_one(h, cards[i][0], 16, True)
        write_lines(b, cards[i][1], 15)
    write_one(page_tb(s), "04", 14)

    # 5. 핵심 기술
    s = prs.slides[4]
    for t in all_tb(s):
        clear_tb(t)
    write_one(all_tb(s)[0], "핵심 기술", 28, True)
    write_one(all_tb(s)[1], "구현 요약", 22, True)
    blocks = sorted(
        [t for t in all_tb(s) if t.top > 1_700_000 and t.width > 3_500_000],
        key=lambda x: x.top,
    )
    write_lines(
        blocks[0],
        [
            "모듈: game.py, scripts/ (Player, Enemy, collision 등)",
            "상태: TITLE → PLAY → CLEAR / DYING → GAMEOVER",
            "애니: SpriteSheet, FrameAnimator, mirror_animator",
        ],
        16,
    )
    write_lines(
        blocks[1],
        [
            "충돌: groupcollide, spritecollide + hitbox 축소",
            "무기: wx = cx + cos(θ)·r,  wy = cy + sin(θ)·r",
            "스폰: player + cos(θ)·R,  sin(θ)·R",
            "배포: PyInstaller, exe 옆 assets/",
        ],
        16,
    )
    write_one(page_tb(s), "05", 14)

    # 6. 트러블 슈팅 · 결론
    s = prs.slides[5]
    for t in all_tb(s):
        clear_tb(t)
    big = sorted(
        [t for t in all_tb(s) if t.width > 5_000_000],
        key=lambda x: x.top,
    )
    write_one(big[0], "트러블 슈팅 · 결론", 32, True)
    write_lines(
        big[1],
        [
            "Weapon rect None → 초기화 시 rect 분기",
            "L 애니 역재생 → R 시트 mirror_animator",
            "충돌 과대 → hitbox_rect 비율 축소",
            "exe FileNotFound → paths.py assets 경로",
            "",
            "기획서 규칙 및 강의 요구사항 반영 완료.",
            "제출: 소스 + assets + exe + 보고서 PDF + mp4",
            "",
            "감사합니다.",
        ],
        17,
    )
    write_one(page_tb(s), "06", 14)

    prs.save(str(OUT))
    print("saved:", OUT)


if __name__ == "__main__":
    main()
