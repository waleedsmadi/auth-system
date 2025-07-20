from django.utils.text import slugify
from uuid import uuid4

def generate_unique_slug_by_content(content:str) -> str:
    words = content.split(' ')[:5]
    short_title = ' '.join(words)
    return f'{slugify(short_title)}-{uuid4().hex[:8]}'

