# Super Game

**조승영 (202613111)** · Python / pygame-ce 생존 액션 게임 (Vampire Survivors 스타일)

## 실행 방법

### 개발 환경

```bat
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python.exe game.py
```

### 배포용 exe

```bat
build.bat
```

빌드 후 `dist\SuperGame.exe`와 `dist\assets\` 폴더를 **함께** zip으로 묶어 제출합니다.

## 조작법

| 입력 | 동작 |
|------|------|
| WASD | 이동 |
| SPACE / 버튼 | 게임 시작 |
| — | 3분 생존 시 클리어 |
| R / 다시하기 | 재시작 (패배 화면) |
| ESC / 타이틀로 | 타이틀 복귀 |

## 게임 규칙

- 목숨 3개, 피격 시 약 1.5초 무적
- 적 처치 시 조각 드롭 → 근거리에서 흡입
- 조각 16개마다 회전 무기 +1
- 최고 점수는 `score.txt`에 자동 저장

## 폴더 구조

```
game.py              # 실행 진입점
scripts/             # 게임 로직 모듈
assets/images/       # 스프라이트·UI
assets/fonts/        # Maplestory 폰트
assets/sounds/       # BGM·SFX
docs/                # 기획·체크리스트
```

## 핵심 기술

- **상태 머신**: TITLE → PLAY → CLEAR / DYING → GAMEOVER
- **충돌**: `groupcollide` + 축소 히트박스
- **애니메이션**: 스프라이트 시트 + `FrameAnimator`
- **고득점**: `score.txt` File I/O (`scripts/high_score.py`)
- **배포**: PyInstaller, `assets/`는 exe 옆에 배치

## 제출물 (강의 14)

| 항목 | 형식 |
|------|------|
| 소스 코드 | `.py` (주석 포함) |
| 실행 파일 | `.exe` + `assets` (zip) |
| 보고서 / 플레이 영상 | `.pdf` / `.mp4` |

## 에셋 크레딧

무료·수업용 에셋 사용. 상세 출처는 [docs/CREDITS.md](docs/CREDITS.md) 참고.
