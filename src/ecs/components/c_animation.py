class CAnimation:
    def __init__(self, animations) -> None:
        self.number_frames = animations.number_frames
        self.animation_list = [CAnimationData(animation.name, animation.framerate, animation.start, animation.end) for animation in animations.list]
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animation_list[self.current_animation].start


class CAnimationData:
    def __init__(self, name, framerate, start, end):
        self.name = name
        self.framerate = 1.0 / framerate
        self.start = start
        self.end = end
