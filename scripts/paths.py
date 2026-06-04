"""프로젝트 경로 및 리소스 로드."""
import os

import pygame

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(ROOT_DIR, "assets", "images")
FONT_DIR = os.path.join(ROOT_DIR, "assets", "fonts")
SOUND_DIR = os.path.join(ROOT_DIR, "assets", "sounds")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")

FONT_MAPLE_BOLD = "Maplestory Bold.ttf"
FONT_MAPLE_LIGHT = "Maplestory Light.ttf"

IMAGE_TITLE_BG = "NordicLumberjacTitle.png"
IMAGE_PANEL = "Panel1.png"
IMAGE_DEFEAT_BG = "막혔다2.png"
IMAGE_CLEAR_BG = "이겼다2.png"


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
BGM_VOLUME = 0.12  # 효과음보다 낮게 — 은은한 배경용


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
