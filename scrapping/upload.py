import requests

with open("token.txt") as f:
    token = f.read()
    
with open("banners.json") as f :
    content = f.read()

owner = "godisdeadLOL"
repo = "ba-schedule"

headers = {"Authorization": f"Bearer {token}"}

response = requests.post(
    f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/main.yaml/dispatches",
    headers=headers,
    json={"ref": "main", "inputs": {"bannersData": content}}
)

print(response.text)