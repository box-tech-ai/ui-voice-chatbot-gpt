import pygame
from io import BytesIO


class TTS:
    def __init__(self, generator, tts_engine):
        self.generator = generator
        self.tts_engine = tts_engine

    def text_to_speech(self, text):
        return self.generator.text_to_speech(text)

    def play_speech(self, text):
        speech = self.text_to_speech(text)
        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Load the audio content
        if self.tts_engine == "openai":
            audio_file = BytesIO(speech)
            pygame.mixer.music.load(audio_file)
        else:
            audio_file = BytesIO()
            speech.write_to_fp(audio_file)
            audio_file.seek(0)
            pygame.mixer.music.load(audio_file, "mp3")

        # Play the audio
        pygame.mixer.music.play()

        # Keep the script running until the audio is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()