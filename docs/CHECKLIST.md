# 강의 기본 체크리스트

| 항목 | 상태 | 근거 |
|------|------|------|
| 기획서(A4 반 페이지) 작성 완료 | [x] | `docs/기획서_요약.md` (원본: 게임 스크립트 프로그래밍_조승영_202613111.pdf) |
| 프로젝트 폴더 구조 생성 및 정리 | [x] | `assets/`, `scripts/`, `docs/`, `game.py` |
| 핵심 이미지 에셋(주인공, 적) 확보 | [x] | `assets/images/Player.png`, `Enemy.png` |
| Player 클래스로 캐릭터 표시 | [x] | `scripts/player.py` |
| Enemy 클래스로 적 생성·표시 | [x] | `scripts/enemy.py` |
| 충돌 처리 정상 동작 | [x] | `scripts/collision.py` (`groupcollide`, `spritecollide`) |

## 프로젝트 구조

```
SuperGame/
├── game.py                 # 메인 루프
├── assets/
│   ├── images/             # Player, Enemy, Weapon, Piece, background
│   └── sounds/             # 효과음
├── scripts/
│   ├── player.py           # Player
│   ├── enemy.py            # Enemy
│   ├── fragment.py         # Fragment
│   ├── orbiting_weapons.py # 무기 + Sprite Group
│   ├── collision.py        # 충돌 처리
│   └── paths.py            # 리소스 경로
└── docs/
    ├── CHECKLIST.md
    └── 기획서_요약.md
```
