# 강의 기본 체크리스트

| 항목 | 상태 | 근거 |
|------|------|------|
| 기획서 작성 | [x] | `docs/기획서_요약.md` |
| 프로젝트 폴더 구조 | [x] | `assets/`, `scripts/`, `game.py` |
| 핵심 이미지 에셋 | [x] | `assets/images/` |
| Player 클래스 | [x] | `scripts/player.py` |
| Enemy 클래스 | [x] | `scripts/enemy.py` |
| 충돌 처리 | [x] | `scripts/collision.py` |
| 파일 분리 (강의) | [x] | 객체·기능별 `scripts/` 모듈 |

## 모듈 구조

```
game.py                 ← 실행만
scripts/
  game_manager.py       ← 상태 머신·루프
  play_session.py       ← 플레이 로직
  player.py
  enemy.py
  enemy_spawner.py
  orbiting_weapons.py
  fragment.py
  collision.py
  hud.py / lives_ui.py
  screens.py
  audio_manager.py
  background.py
  sprite_anim.py
  constants.py / fonts.py / paths.py
  high_score.py         고득점 (score.txt)
  ui_button.py          메뉴 버튼
  hit_effect.py / levelup_effect.py
```

## Lecture 14 (폴리싱)

| 항목 | 상태 |
|------|------|
| 타이틀·승패 UI | [x] |
| 고득점 저장 | [x] |
| PyInstaller 경로 | [x] |
| build.bat | [x] |
| 보고서·영상·exe zip 제출 | [ ] 직접 |
