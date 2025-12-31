from anthropic import Anthropic
from config.settings import settings
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all AI agents in the PMI system"""

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.conversation_history = []

    @abstractmethod
    def get_system_prompt(self):
        """Return the system prompt for this agent"""
        pass

    def send_message(self, user_message, context=None):
        """Send a message to Claude and get a response"""
        system_prompt = self.get_system_prompt()

        if context:
            user_message = f"Context: {context}\n\n{user_message}"

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            response = self.client.messages.create(
                model=settings.DEFAULT_MODEL,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                system=system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            print(f"Error communicating with Claude: {e}")
            return None

    def reset_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []

    def get_last_response(self):
        """Get the last response from the agent"""
        if self.conversation_history:
            for message in reversed(self.conversation_history):
                if message["role"] == "assistant":
                    return message["content"]
        return None
