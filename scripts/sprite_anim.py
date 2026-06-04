"""스프라이트 시트 프레임 분할 및 재생."""
import pygame


class SpriteSheet:
    """가로로 이어 붙인 프레임 시트."""

    def __init__(
        self,
        sheet: pygame.Surface,
        frame_width: int,
        frame_height: int | None = None,
        scale: tuple[int, int] | None = None,
    ):
        frame_height = frame_height or sheet.get_height()
        self.frames: list[pygame.Surface] = []
        x = 0
        sheet_w = sheet.get_width()
        while x + frame_width <= sheet_w:
            frame = sheet.subsurface((x, 0, frame_width, frame_height)).copy()
            if scale:
                frame = pygame.transform.scale(frame, scale)
            self.frames.append(frame)
            x += frame_width

    @property
    def frame_count(self) -> int:
        return len(self.frames)


class GridSpriteSheet:
    """행·열 그리드 시트 (예: 3x3 중 7프레임)."""

    def __init__(
        self,
        sheet: pygame.Surface,
        cols: int,
        rows: int,
        frame_count: int,
        scale: tuple[int, int] | None = None,
        colorkey: tuple[int, int, int] | None = None,
    ):
        fw = sheet.get_width() // cols
        fh = sheet.get_height() // rows
        self.frames: list[pygame.Surface] = []
        for i in range(frame_count):
            col = i % cols
            row = i // cols
            frame = sheet.subsurface((col * fw, row * fh, fw, fh)).copy()
            if scale:
                frame = pygame.transform.scale(frame, scale)
            if colorkey is not None:
                frame.set_colorkey(colorkey)
            self.frames.append(frame)


class FrameAnimator:
    """프레임 애니메이션 재생."""

    def __init__(
        self,
        frames: list[pygame.Surface],
        fps: float = 10,
        loop: bool = True,
    ):
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.elapsed_ms = 0.0
        self.finished = False

    def reset(self) -> None:
        self.elapsed_ms = 0.0
        self.finished = False

    def update(self, dt: float) -> None:
        if self.finished or not self.frames:
            return
        self.elapsed_ms += dt
        frame_duration = 1000.0 / self.fps
        if not self.loop:
            last_index = len(self.frames) - 1
            if self.elapsed_ms >= last_index * frame_duration:
                self.elapsed_ms = last_index * frame_duration
                self.finished = True

    def get_surface(self) -> pygame.Surface:
        if not self.frames:
            raise ValueError("No frames in animator")
        frame_duration = 1000.0 / self.fps
        index = int(self.elapsed_ms / frame_duration)
        if self.loop:
            index %= len(self.frames)
        else:
            index = min(index, len(self.frames) - 1)
        return self.frames[index]


def mirror_animator(source: FrameAnimator) -> FrameAnimator:
    """
    R 애니메이션을 좌우 반전해 L 방향 생성.
    L 전용 시트가 역재생처럼 보일 때 R과 동일한 프레임 순서를 유지한다.
    """
    frames = [pygame.transform.flip(frame, True, False) for frame in source.frames]
    return FrameAnimator(frames, fps=source.fps, loop=source.loop)
