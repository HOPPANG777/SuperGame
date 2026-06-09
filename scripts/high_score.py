"""고득점 저장·불러오기 (강의 14 — File I/O)."""
from scripts.paths import SCORE_FILE


def load_high_score() -> int:
    """score.txt에서 최고 점수 불러오기. 없거나 오류 시 0."""
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_high_score(score: int) -> None:
    """최고 점수를 score.txt에 저장."""
    try:
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            f.write(str(score))
    except OSError:
        pass


def submit_score(score: int) -> tuple[int, bool]:
    """
    점수 제출. 갱신되면 저장.
    반환: (현재 최고 점수, 이번에 신기록 여부)
    """
    best = load_high_score()
    if score > best:
        save_high_score(score)
        return score, True
    return best, False
