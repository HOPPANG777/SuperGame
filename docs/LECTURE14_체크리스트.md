# Lecture 14 — 폴리싱 & 빌드 체크리스트

## 완료 (코드)

| 항목 | 상태 | 위치 |
|------|------|------|
| 타이틀 화면 (TITLE 상태) | ✅ | `screens.py`, `game_manager.py` |
| 메뉴 UI (배경·버튼·폰트) | ✅ | `screens.py`, `ui_button.py` |
| Press 힌트 깜빡임 | ✅ | `screens.draw_title` |
| 고득점 저장 (score.txt) | ✅ | `high_score.py` |
| 승리/패배 화면 점수·신기록 표시 | ✅ | `screens.py` |
| PyInstaller 경로 처리 | ✅ | `paths.py` (`assets_root`, `SCORE_FILE`) |
| 빌드 스크립트 | ✅ | `build.bat` |
| exe 아이콘 | ✅ | `assets/images/HOPPANG_2.ico` |
| README / 크레딧 | ✅ | `README.md`, `docs/CREDITS.md` |

## 직접 진행 (제출용)

| 항목 | 형식 | 비고 |
|------|------|------|
| exe 빌드 | `build.bat` 실행 | `dist\` zip |
| 최종 QA | 체크리스트 | 아래 참고 |
| 보고서 | PDF | 게임소개·조작·기술·트러블슈팅·결론 |
| 플레이 영상 | MP4 | 1~3분 시연 |
| GitHub (선택) | README 스크린샷 | 포트폴리오 |

## Final QA (강의 19페이지)

- [ ] zip 압축 해제 후 `SuperGame.exe` + `assets` 폴더로 실행
- [ ] BGM·효과음 정상 재생
- [ ] 재시작 / 타이틀 / 종료 버튼 동작
- [ ] `score.txt` 고득점 저장·불러오기
- [ ] 다른 PC에서 실행 테스트 (가능하면)

## 빌드 명령

```bat
build.bat
```

배포 폴더 구조:

```
dist/
  SuperGame.exe
  assets/
    images/
    fonts/
    sounds/
  score.txt   ← 실행 후 자동 생성
```
