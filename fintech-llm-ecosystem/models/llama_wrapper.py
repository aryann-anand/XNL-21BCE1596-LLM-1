from llama_cpp import Llama
import yaml
import time
from threading import Lock
from utils.logger import get_logger

logger = get_logger(__name__)

class LlamaModel:
    def __init__(self, model_path, config):
        self.model = Llama(
            model_path=model_path,
            n_ctx=config['models']['n_ctx'],
            n_gpu_layers=config['models']['n_gpu_layers'],
            verbose=False
        )
        self.lock = Lock()
        self.last_used = time.time()

    def generate(self, prompt, max_tokens=256):
        with self.lock:
            try:
                self.last_used = time.time()
                output = self.model(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=0.2,
                    top_p=0.95,
                    repeat_penalty=1.2
                )
                return output['choices'][0]['text'].strip()
            except Exception as e:
                logger.error(f"Model error: {str(e)}")
                raise