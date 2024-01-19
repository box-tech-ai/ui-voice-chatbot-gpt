## UI-Enabled voice Chatbot powered by ChatGPT

This application is a voice-enabled chatbot with UI to display the conversation, powered by ChatGPT, built using Python and PyQt5. 
It listens to the user's voice, processes the speech, generates responses using OpenAI's GPT models, 
and speaks back to the user. The speeches are shown in a UI window.

## Features

- **Voice Recognition and Speech Synthesis**: Listens to user input through a microphone and speaks responses using Text-To-Speech (TTS).
- **ChatGPT Integration**: Leverages OpenAI's GPT models for generating conversational responses.
- **Customizable TTS Engine**: Supports different TTS engines like Google's Text-to-Speech (GTTS) and potentially OpenAI's speech synthesis.
- **User Interface**: Built with PyQt5, offering a graphical user interface for interaction.

## Installing

1. **First, you need to have an OpenAI API key**: Create an account to get an API key here: https://openai.com/api/ .
It is recommended to set the API key in your environmental variables, and then get by api_key=os.getenv('OPENAI_API_KEY').


2. **Clone the Repository**: Clone this repository to your local machine.

    ```
    git clone [repository URL]
    ```

3. **Install Dependencies**: Install the required Python libraries.
   The code is developed on MacOS, you need to install portaudio by:
    ```
    brew install portaudio
    ```
    ```
    pip install requirements.txt
    ```

3. **API Key Configuration**: Ensure you have an OpenAI API key and set it in your environment variables or directly in the `openai_generator.py` script.

## Running the Application

To run the chatbot, execute the `pipeline` script in the terminal. There are two TTS engines used in the script: "google" or "openai" in line 147 in pipeline.py. Config it yourself.
In order to stop the script, simple say "exit".

## Example video

https://github.com/box-tech-ai/ui-voice-chatbot-gpt/assets/157038099/43f94ee3-3315-42c7-b1ea-d38afad78a1b


