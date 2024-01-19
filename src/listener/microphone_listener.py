import numpy as np
from queue import Queue
from time import sleep

from speech_recognition import (
    AudioData,
    Microphone,
    Recognizer,
)

from transcriber.transcriber_model import TranscriberWhisper


class MicrophoneListener():
    """Class to listen to speech convert it to text"""

    def __init__(self):
        self.transcriber = TranscriberWhisper()
        self._recognizer = Recognizer()
        self._recognizer.energy_threshold = 1000
        self._recognizer.dynamic_energy_threshold = False

    def listen(self):
        """
        Listen on the specified input device for speech and return the heard text.
        :return: the text from the speech listened to.
        """
        phrase_time_limit = 8
        data_queue = Queue()

        def record_callback(_, audio: AudioData) -> None:
            """Callback function to receive audio data when recordings finish."""
            data_queue.put(audio.get_raw_data())

        try:
            with Microphone(sample_rate=16000) as source:
                self._recognizer.adjust_for_ambient_noise(source)
            listening = self._recognizer.listen_in_background(
                source, record_callback, phrase_time_limit=phrase_time_limit
            )

            while True:
                text = self._recognize_text_in_audio(data_queue)
                if text is not None:
                    listening(wait_for_stop=False)
                    return text
                sleep(0.1)

        except Exception as e:
            return None

    def _recognize_text_in_audio(self, data_queue):
        # Pull raw recorded audio from the queue.
        audio_data = b''
        while not data_queue.empty():
            audio_data += data_queue.get()

        if audio_data:
            # Convert in-ram buffer to something the model can use directly without needing a temp file.
            # Convert data from 16-bit wide integers to floating point with a width of 32 bits.
            # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            result = self.transcriber.pipe(audio_np)
            text = result['text'].strip()

            return text

        else:
            return None
