from sys import platform
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class TranscriberWhisper:
    def __init__(self):
        if platform == "darwin":
            device = torch.device("mps")
        else:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch_dtype = torch.float16

        model_id = "openai/whisper-large-v3"

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=8,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )


if __name__ == '__main__':
    transcriber = TranscriberWhisper()
