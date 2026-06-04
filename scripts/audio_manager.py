"""BGM / SFX 관리."""
import pygame

from scripts.paths import BGM_VOLUME, init_bgm, load_sound, play_bgm, stop_bgm


class AudioManager:
    """사운드 로드 및 재생."""

    def __init__(self) -> None:
        self.bgm_ready = init_bgm(volume=BGM_VOLUME)
        self.sfx_start = load_sound("80_Start_01.wav", volume=0.55)
        self.sfx_clear = load_sound("25_Clear_01.wav", volume=0.6)
        self.sfx_defeat = load_sound("44_Defeat_01.wav", volume=0.6)
        self.sfx_hit = load_sound("59_Hit_01.wav", volume=0.45)
        self.sfx_pickup = load_sound("87_exp_up_1_short.wav", volume=0.45)
        self.sfx_levelup = load_sound("73_Lvl_up_01.wav", volume=0.55)
        self.sfx_hurt = load_sound("59_Hit_01.wav", volume=0.4)
        self.sfx_die = load_sound("68_Die_01.wav", volume=0.65)

    def play_sfx(self, sound: pygame.mixer.Sound | None) -> None:
        if sound:
            sound.play()

    def start_bgm(self) -> None:
        if self.bgm_ready:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(BGM_VOLUME)
            play_bgm(loop=True, fade_ms=2500)

    def stop_bgm(self) -> None:
        stop_bgm(fade_ms=1000)
