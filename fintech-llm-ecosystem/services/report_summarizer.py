from models.model_router import ModelRouter
from utils.logger import get_logger

logger = get_logger(__name__)

class ReportSummarizer:
    def __init__(self, model_router):
        self.model_router = model_router
        
    def summarize(self, report_text):
        prompt = f"""
        [INST] Summarize this financial report into key points:
        {report_text}
        
        Use markdown formatting with sections:
        - Key Financials
        - Performance Highlights
        - Risk Factors
        - Future Outlook [/INST]
        """
        return self.model_router.get_response(prompt, max_tokens=512)