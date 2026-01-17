import logging
import json
from datetime import datetime
from typing import Dict, Any
import os

class MonitoringManager:
    def __init__(self, log_file: str = "data/app_logs.log"):
        self.log_file = log_file
        self.setup_logging()
        self.kpis = {
            "chatbot_questions": 0,
            "chatbot_correct_responses": 0,
            "chatbot_avg_response_time": 0,
            "evaluations_processed": 0,
            "active_users": 0
        }
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
    
    def log_chatbot_interaction(self, question: str, response: str, confidence: float, user_id: str):
        logger = logging.getLogger(__name__)
        logger.info(f"Chatbot: User={user_id}, Question={question}, Confidence={confidence}")
        self.kpis["chatbot_questions"] += 1
    
    def log_evaluation_processing(self, file_name: str, total_records: int):
        logger = logging.getLogger(__name__)
        logger.info(f"Evaluation: File={file_name}, Records={total_records}")
        self.kpis["evaluations_processed"] += total_records
    
    def log_user_login(self, username: str):
        logger = logging.getLogger(__name__)
        logger.info(f"Login: User={username}")
        self.kpis["active_users"] += 1
    
    def log_security_event(self, event_type: str, details: str):
        logger = logging.getLogger(__name__)
        logger.warning(f"Security: Type={event_type}, Details={details}")
    
    def get_kpis(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "kpis": self.kpis
        }
    
    def export_kpis(self, output_file: str):
        with open(output_file, 'w') as f:
            json.dump(self.get_kpis(), f, indent=2)
