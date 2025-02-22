#api init.py
from .vision_api import vision_api_call
from .text_api import text_api_call

__all__ = [
    'vision_api_call',
    'text_api_call',
]