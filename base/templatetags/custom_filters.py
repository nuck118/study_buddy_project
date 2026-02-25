from django import template
import re

register = template.Library()

@register.filter(name='youtube_embed')
def youtube_embed(url):
    """
    Converts a standard YouTube URL into an embeddable URL.
    """
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    
    if match:
        return f"https://www.youtube.com/embed/{match.group(1)}"
    return url