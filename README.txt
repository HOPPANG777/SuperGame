Super Game (조승영 202613111)
===========================

실행
----
  venv\Scripts\python.exe game.py

폴더 구조 (강의: 객체·기능별 파일 분리)
------------------------------------
  game.py                  메인 실행만 담당
  scripts/
    game_manager.py        상태 머신·메인 루프
    play_session.py        플레이 중 업데이트/충돌/렌더
    player.py              Player
    enemy.py               Enemy
    enemy_spawner.py       적 생성 타이머
    orbiting_weapons.py    회전 무기
    fragment.py            조각
    collision.py           충돌 처리
    hud.py                 HUD
    lives_ui.py            목숨 UI
    screens.py             타이틀/클리어/사망 화면
    audio_manager.py       BGM·SFX
    background.py          배경
    sprite_anim.py         스프라이트 시트 애니
    constants.py           상수·상태
    fonts.py               폰트
    paths.py               리소스 경로
  assets/images/           Player/, Weapon/, Enemy.png ...
  assets/sounds/
