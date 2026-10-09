import os
from dotenv import load_dotenv
import requests

load_dotenv()
headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}
response = requests.get('https://api.groq.com/openai/v1/models', headers=headers)
models = response.json().get('data', [])
print([m['id'] for m in models])
