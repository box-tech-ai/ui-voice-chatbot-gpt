import sys
import signal

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QStatusBar, QMainWindow
from PyQt5.QtCore import pyqtSignal, QThread, Qt

from generator.gtts_generator import GTTSGenerator
from speaker.tts import TTS
from listener.microphone_listener import MicrophoneListener
from generator.openai_generator import OpenaiGenerator


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)


class SpeechTextDisplay(QThread):
    """
    This class handles speech recognition and response generation in a separate thread.
    """
    speaking = pyqtSignal()
    listening = pyqtSignal()
    updated_text = pyqtSignal(str)
    show_image_signal = pyqtSignal()

    def __init__(self, listener, generator, tts_engine, tts, exit_word="exit"):
        super().__init__()
        self.listener = listener
        self.generator = generator
        self.tts = TTS(tts_engine, tts)
        self._exit_word = exit_word.lower()
        self.is_running = True

    def run(self):
        """
        Main loop for processing speech and generating responses.
        """
        self._greet_user()
        while self.is_running:
            text = self._listen_to_user()
            if self._is_exit_word(text):
                response_text = 'Goodbye! You can close the window now.'
                break

            response_text = self._generate_response(text)
            self.speaking.emit()  # Emit signal before speaking
            self._speak(response_text)
            self.listening.emit()  # Emit signal after speaking

        self.updated_text.emit(f"Bot: {response_text}")
        self._speak(response_text)

    def _greet_user(self):
        welcome_text = "Bot: Hello, how can I help you today?"
        self.updated_text.emit(f"{welcome_text}")
        self.tts.play_speech(welcome_text)

    def _listen_to_user(self):
        text = self.listener.listen()
        self.updated_text.emit(f"<font color='green'>You: {text}</font>")
        return text

    def _is_exit_word(self, text):
        return text.lower().startswith(self._exit_word)

    def _generate_response(self, text):
        response_text = self.generator.general_generate(text, word_limit=30)
        self.updated_text.emit(f"Bot: {response_text}")
        return response_text

    def _speak(self, response_text):
        self.tts.play_speech(response_text)

    def stop(self):
        """
        Stops the thread safely.
        """
        self.is_running = False
        self.wait()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.imageWindow = ImageWindow()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Create a QTextEdit for displaying text
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)  # Make the QTextEdit read-only
        self.textEdit.setWordWrapMode(True)  # Enable word wrapping

        self.layout.addWidget(self.textEdit)

        self.setWindowTitle('Say Whatever You Like')

        # Set a fixed size for the window
        self.setFixedSize(500, 400)

        # Create and add a status bar
        self.statusBar = QStatusBar(self)
        self.layout.addWidget(self.statusBar)
        self.statusBar.showMessage("I am listening")

    def run(self, listener, generator, tts_engine, tts):
        # Initialize and start the external function thread
        self.ext_func = SpeechTextDisplay(listener, generator, tts_engine, tts)
        self.ext_func.updated_text.connect(self.update_text)
        self.ext_func.start()

        # Connect signals to slots
        self.ext_func.speaking.connect(lambda: self.update_status("I am speaking"))
        self.ext_func.listening.connect(lambda: self.update_status("I am listening"))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # Check for Esc key
            self.close()
        elif event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.close()

    def update_text(self, text):
        self.textEdit.append(text)
        self.textEdit.ensureCursorVisible()

    def update_status(self, message):
        self.statusBar.showMessage(message)

    def closeEvent(self, event):
        self.ext_func.stop()
        QApplication.quit()
        super().closeEvent(event)


def main():
    listener = MicrophoneListener()
    generator = OpenaiGenerator()
    tts = "openai"
    if tts == "google":
        tts_engine = GTTSGenerator()
    else:
        tts_engine = generator

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.run(listener, generator, tts_engine, tts)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
