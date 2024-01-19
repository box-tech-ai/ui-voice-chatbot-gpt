import os
from openai import OpenAI


class OpenaiGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def text_to_image(self, text):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=text,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format='b64_json'
        )
        return response

    def text_to_speech(self, text, speed=1.0):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
            speed=speed
        )
        return response.content

    def content_generate(self, prompt, examples=None, model='gpt-3.5-turbo'):
        system_content = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture. " \
                         "Knowledge cutoff: {2023-04} Current date: {2023-11}"

        messages = [
            {"role": "system", "content": system_content}
        ]
        if examples is not None:
            for example in examples:
                messages.append({"role": "user", "content": example[0]})
                messages.append({"role": "assistant", "content": example[1]})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        answer = response.choices[0].message.content
        return answer

    def general_generate(self, content, word_limit=None):
        if word_limit:
            prompt = f"""
                        You are very knowledgeable because you have read many books.
                        Please generate appropriate response to the {content} with no more than {word_limit} words. 
                        """
        else:
            prompt = f"""
                        You are very knowledgeable because you have read many books.
                        Please generate appropriate response to the {content}. 
                        """
        return self.content_generate(prompt)
