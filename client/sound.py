class SoundObject:
    def __init__(self, sound_file):
        from pygame import mixer
        self.sound_effect = mixer.Sound(sound_file)

    def play(self):
        self.sound_effect.play()
