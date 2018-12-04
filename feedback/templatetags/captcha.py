from django import template
from django.conf import settings
import random

register = template.Library()

@register.inclusion_tag("feedback/captcha.html")
def captcha():
    captchas = getattr(settings, 'FEEDBACK_CAPTCHAS', {})
    if captchas:
        question = random.randint(0, len(captchas) - 1)
        return {
            "question": captchas[question][0],
            "question_id": captchas[question][0]
        }
    return {}
