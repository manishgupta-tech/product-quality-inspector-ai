import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("FOUNDRY_API_KEY")
endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")

url = endpoint + "/agents?api-version=v1"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(response.text)