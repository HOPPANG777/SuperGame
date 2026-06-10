"""프로젝트 경로 및 리소스 로드 (개발 / PyInstaller exe 공통)."""
import os
import sys

import pygame


def _project_root() -> str:
    """소스 기준 프로젝트 루트."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _exe_dir() -> str:
    """실행 파일이 있는 폴더 (배포 시 score.txt·assets 위치)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return _project_root()


def assets_root() -> str:
    """
    assets 폴더 경로.
    exe 배포: SuperGame.exe 와 같은 위치의 assets/ (강의 14권장).
    """
    return os.path.join(_exe_dir(), "assets")


ROOT_DIR = _project_root()
IMAGE_DIR = os.path.join(assets_root(), "images")
FONT_DIR = os.path.join(assets_root(), "fonts")
SOUND_DIR = os.path.join(assets_root(), "sounds")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
SCORE_FILE = os.path.join(_exe_dir(), "score.txt")

FONT_MAPLE_BOLD = "Maplestory Bold.ttf"
FONT_MAPLE_LIGHT = "Maplestory Light.ttf"

IMAGE_TITLE_BG = "NordicLumberjacTitle.png"
IMAGE_PANEL = "Panel1.png"
IMAGE_DEFEAT_BG = "막혔다2.png"
IMAGE_CLEAR_BG = "이겼다2.png"
ICON_FILENAME = "HOPPANG_2.png"
WINDOW_ICON_SIZE = (32, 32)


def setup_windows_app_id(app_id: str = "SuperGame.HOPPANG") -> None:
    """Windows 작업 표시줄 아이콘용 AppUserModelID."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except (AttributeError, OSError):
        pass


def apply_window_icon() -> None:
    """실행 중 창·작업 표시줄 아이콘 (HOPPANG_2.png)."""
    path = os.path.join(IMAGE_DIR, ICON_FILENAME)
    if not os.path.isfile(path):
        return
    try:
        icon = pygame.image.load(path)
        if icon.get_width() != WINDOW_ICON_SIZE[0] or icon.get_height() != WINDOW_ICON_SIZE[1]:
            icon = pygame.transform.smoothscale(icon, WINDOW_ICON_SIZE)
        if pygame.display.get_surface() is not None:
            icon = icon.convert_alpha()
        pygame.display.set_icon(icon)
    except pygame.error:
        pass


def load_font(name: str, size: int) -> pygame.font.Font:
    path = os.path.join(FONT_DIR, name)
    return pygame.font.Font(path, size)


def load_image(name: str, size: tuple[int, int] | None = None) -> pygame.Surface:
    path = os.path.join(IMAGE_DIR, name)
    image = pygame.image.load(path)
    if pygame.display.get_surface() is not None:
        image = image.convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


def load_sound(name: str, volume: float = 0.5) -> pygame.mixer.Sound | None:
    path = os.path.join(SOUND_DIR, name)
    if not os.path.isfile(path):
        return None
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except pygame.error:
        return None


BGM_FILENAME = "입브금2.wav"
BGM_VOLUME = 0.35


def init_bgm(filename: str = BGM_FILENAME, volume: float = BGM_VOLUME) -> bool:
    """배경음 로드 (pygame.mixer.music — 스트리밍·반복용)."""
    path = os.path.join(SOUND_DIR, filename)
    if not os.path.isfile(path):
        return False
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        return True
    except pygame.error:
        return False


def play_bgm(loop: bool = True, fade_ms: int = 2000) -> None:
    """BGM 무한 반복 재생."""
    if not pygame.mixer.get_init():
        return
    loops = -1 if loop else 0
    pygame.mixer.music.play(loops, fade_ms=fade_ms)


def stop_bgm(fade_ms: int = 800) -> None:
    """BGM 페이드 아웃."""
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(fade_ms)
