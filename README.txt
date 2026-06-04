Super Game (조승영 202613111)
===========================

실행
----
  venv\Scripts\python.exe game.py

폴더 구조 (강의 권장 + scripts 분리)
------------------------------------
  game.py              메인 실행
  assets/images/       Player.png, Enemy.png, Weapon.png, Piece.png
  assets/sounds/
    입브금2.wav          BGM (플레이 중 은은하게 무한 반복)
    80_Start_01.wav      게임 시작 / 재시작
    25_Clear_01.wav      3분 클리어
    44_Defeat_01.wav     게임 오버
    59_Hit_01.wav        적 처치
    87_exp_up_1_short.wav  조각 획득
    73_Lvl_up_01.wav     무기 추가(조각 16개)
  scripts/player.py    Player 클래스
  scripts/enemy.py     Enemy 클래스
  scripts/collision.py 충돌 처리
  docs/CHECKLIST.md    강의 체크리스트

체크리스트는 docs/CHECKLIST.md 참고.
