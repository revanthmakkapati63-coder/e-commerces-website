import re

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text)

def clean_input(text):
    text = strip_html(text)
    text = re.sub(r'[;\'"\\`]', '', text)
    return text