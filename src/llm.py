import ollama
import asyncio
import logging

# Set up logging configuration
logging.basicConfig(
    filename='logs/llm.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMInterface:
    def __init__(self, model_name="llama3.1:8b"):
        self.model = model_name
        logger.info(f"Initialized LLM interface with model: {model_name}")

    async def chat(self, message: str, context: list = None) -> str:
        """Send message to LLM and get response"""
        try:
            if len(message) > 1000: message_log = f"Sending chat request with message:\n{message[:500]}\n...\n...\n{message[-500:]}"
            else: message_log = f"Sending chat request with message:\n{message}"
            logger.info(message_log)
            # Run ollama.chat in a thread pool since it's blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful planning assistant. You help manage tasks and deadlines.'},
                    {'role': 'user', 'content': message}
                ]
            ))
            response_content = response['message']['content']
            if len(response_content) > 1000: response_log = f"LLM response:\n{response_content[:500]}\n...\n...\n{response_content[-500:]}"
            else: response_log = f"LLM response:\n{response_content}"
            logger.info(response_log)
            return response_content
        except Exception as e:
            error_msg = f"Error connecting to Ollama: {str(e)}"
            logger.error(error_msg)
            return error_msg

#     async def process_planning_request(self, message: str, current_tasks: list) -> str:
#         """Process planning-specific requests"""
#         context = f"""Current tasks and deadlines:
# {chr(10).join(current_tasks)}

# User request: {message}

# Please help manage these tasks and deadlines."""

#         return await self.chat(context) 