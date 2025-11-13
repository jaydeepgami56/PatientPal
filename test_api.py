import requests
import json

url = "http://localhost:8000/api/orchestrator/query"
payload = {
    "query": "What are symptoms of diabetes?",
    "show_routing": False
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
