from dataclasses import dataclass
from typing import Dict, Optional

from messages.entity.chat_message.base_chat_message import BaseChatMessage


@dataclass
class AssistantChatMessage(BaseChatMessage):
    role_name: str
    meta_dict: Optional[Dict[str, str]] = None
    role: str = "user"
    content: str = ""