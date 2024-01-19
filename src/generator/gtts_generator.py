from gtts import gTTS


class GTTSGenerator:
    def __init__(self):
        pass

    def text_to_speech(self, text):
        return gTTS(text, lang='en', tld='us')