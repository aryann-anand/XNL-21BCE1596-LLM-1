from .llama_wrapper import LlamaModel
from utils.logger import get_logger

logger = get_logger(__name__)

class ModelRouter:
    def __init__(self, config):
        self.primary = LlamaModel(config['models']['primary'], config)
        self.secondary = LlamaModel(config['models']['secondary'], config)
        self.max_retries = config['system']['max_retries']

    def get_response(self, prompt, max_tokens=256):
        """Get response with automatic failover"""
        for attempt in range(self.max_retries):
            try:
                if attempt % 2 == 0:
                    return self.primary.generate(prompt, max_tokens)
                else:
                    return self.secondary.generate(prompt, max_tokens)
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                continue
        raise Exception("All model instances failed to respond")