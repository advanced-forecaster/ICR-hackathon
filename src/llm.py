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

cut_long_message = lambda message: message[:500] + "\n...\n...\n" + message[-500:] if len(message) > 1000 else message

class LLMInterface:
    def __init__(self, model_name="qwen2.5:32b"):
        self.model = model_name
        logger.info(f"Initialized LLM interface with model: {model_name}")

    async def chat(self, messages: list, context: dict = None) -> str:
        """Send message to LLM and get response"""
        try:
            message = messages[-1]['content']
            logger.info(f"Sending chat request with message:\n{cut_long_message(message)}")

            if context:
                messages = build_context(context=context, message_history=messages)

            # print('!!!!', messages)

            # Run ollama.chat in a thread pool since it's blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: ollama.chat(
                model=self.model,
                messages=messages
            ))
            response_content = response['message']['content']

            logger.info(f"LLM response:\n{cut_long_message(response_content)}")
            return response_content
        except Exception as e:
            error_msg = f"Error connecting to Ollama: {str(e)}"
            logger.error(error_msg)
            return error_msg


def build_context(context: dict, message_history: list) -> list:
    # """Build context for LLM"""
    system_prompt = """You are a helpful planning assistant. You help manage tasks and deadlines. 
    There is information from the system about the current date, user study schedule, and daily plans written in text files.
    **Current date:**
    {current_date}
    **Schedule:**
    {schedule}
    **Daily plans:**
    {daily_plans}
    **Current date:**
    {current_date}
    """.format(current_date=context['current_date'], schedule=context['schedule'], daily_plans=context['daily_plans'])

    # Tokenize system prompt to check length
    # token_response = ollama.tokenize(model=self.model, prompt=system_prompt)
    # token_count = len(token_response['tokens'])
    # logger.info(f"System prompt token count: {token_count}")

    messages = [{'role': 'system', 'content': system_prompt}]
    messages.extend(message_history)
    return messages