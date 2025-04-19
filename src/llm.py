import ollama
import asyncio

class LLMInterface:
    def __init__(self, model_name="llama3.1:8b"):
        self.model = model_name

    async def chat(self, message: str, context: list = None) -> str:
        """Send message to LLM and get response"""
        try:
            # Run ollama.chat in a thread pool since it's blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful planning assistant. You help manage tasks and deadlines.'},
                    {'role': 'user', 'content': message}
                ]
            ))
            return response['message']['content']
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    async def process_planning_request(self, message: str, current_tasks: list) -> str:
        """Process planning-specific requests"""
        context = f"""Current tasks and deadlines:
{chr(10).join(current_tasks)}

User request: {message}

Please help manage these tasks and deadlines."""
        
        return await self.chat(context) 