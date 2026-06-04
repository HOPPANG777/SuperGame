# Lecture13_02 핵심 기능 구현 — 완성도 점검

**기준:** `Lecture13_02_핵심 기능 구현 (1).pdf`  
**프로젝트:** Super Game (기획서 + 강의 통합)

## 강의 검점 리스트 (슬라이드 27)

| 검점 항목 | 상태 | 비고 |
|-----------|------|------|
| 플레이어 이동이 자연스러운가? | ✅ | WASD + 가속/마찰 (`scripts/player.py`) |
| 적이 주기적으로 생성되는가? | ✅ | `get_ticks()` 타이머, 기본 1000ms |
| 무기가 적을 맞추면 적이 사라지는가? | ✅ | `groupcollide` (총알 대신 회전 무기) |
| BGM·효과음이 잘 나오는가? | ✅ | `입브금2.wav` BGM + SFX 6종 |
| 게임 오버 후 재시작이 되는가? | ✅ | R 키 → `start_play()` |

## 오늘의 미션 (슬라이드 2)

| 미션 | 상태 |
|------|------|
| Enemy 자동 생성 | ✅ |
| BGM/SFX | ✅ |
| 점수 + 게임 오버 상태 | ✅ (+ CLEAR 상태, 기획서 3분 클리어) |

## 실습 체크 (슬라이드 16~18)

| 실습 | 상태 |
|------|------|
| 1초(1000ms)마다 적 생성 | ✅ `BASE_SPAWN_DELAY = 1000` |
| 화면 밖 이탈 적 자동 삭제 | ✅ `cull_offscreen_enemies()` |
| BGM 무한 반복 | ✅ `play(-1)` |
| 효과음 + 볼륨 조절 | ✅ |
| GAME OVER 빨간 텍스트 + 정지 | ✅ |

## 강의 권장 구조 vs 현재

| 항목 | 강의 | 현재 |
|------|------|------|
| Sprite Group | ✅ | `enemies`, `fragments`, 무기 `group` |
| spritecollide / groupcollide | ✅ | `scripts/collision.py` |
| 상태 머신 | TITLE/PLAY/GAMEOVER | + CLEAR (기획서) |
| 재시작 | score=0, enemies.empty() | ✅ `start_play()` |
| 난이도 상승 | 점수·시간 | ✅ 점수 500/1000 + 경과 시간 |
| 파일 분리 | sprites.py + main | ✅ `scripts/` + `game.py` |
| mixer.pre_init 512 | ✅ | ✅ |

## 다음 주(다듬기) — 미구현 · 선택

| 항목 | 상태 | 필요 에셋 |
|------|------|-----------|
| 폭발 이펙트 애니메이션 | ❌ | `explosion_1.png` ~ `explosion_N.png` (2~4장) |
| 무한 배경 스크롤 | ❌ | `bg_scroll_1.png`, `bg_scroll_2.png` (가로 타일 2장) |
| PyInstaller .exe | ❌ | 없음 (빌드만 하면 됨) |

## 보유 에셋

### images (`assets/images/`)

| 파일 | 사용 |
|------|------|
| Player.png | ✅ 플레이어 |
| Enemy.png | ✅ 적 |
| Weapon.png | ✅ 회전 무기 |
| Piece.png | ✅ 조각 |
| background.png | ✅ 배경 (고정) |
| bird.png | ⚪ 미사용 |
| spaceship.png | ⚪ 미사용 |

### sounds (`assets/sounds/`)

| 파일 | 사용 |
|------|------|
| 입브금2.wav | ✅ BGM |
| 80_Start_01.wav | ✅ 시작 |
| 25_Clear_01.wav | ✅ 클리어 |
| 44_Defeat_01.wav | ✅ 패배 |
| 59_Hit_01.wav | ✅ 적 처치 |
| 87_exp_up_1_short.wav | ✅ 조각 |
| 73_Lvl_up_01.wav | ✅ 무기 증가 |
| 68_Die_01.wav | ⚪ 미사용 (44_Defeat로 대체) |

## 종합 평가

**핵심 기능 구현 주차 기준 약 85~90% 완료.**

- **이번 주에 끝내야 할 것:** 적/충돌/사운드/점수/재시작 사이클 → **완료**
- **다음 주 다듬기:** 폭발 연출, 배경 스크롤, exe 빌드, HUD 렌더 캐싱(최적화)
