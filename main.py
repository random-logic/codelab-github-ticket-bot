import requests
import os

USE_LLM_TO_DETERMINE_FIT = os.environ.get("USE_LLM_TO_DETERMINE_FIT", False)
SIMILARITY_THRESHOLD = os.environ.get("SIMILARITY_THRESHOLD", 0.1)
GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "Codelab-Davis")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "codelab-ui-components")
POLLING_RATE_PER_HOUR = os.environ.get("POLLING_RATE_PER_HOUR", 60 * 60)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if GITHUB_TOKEN is None:
  raise Exception("GITHUB_TOKEN environment variable not set")

# TODO: Move these functions into new file and make it a Class
def post_github_comment(issue_number, comment):
  url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_number}/comments"
  headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
  }
  data = {"body": comment}

  response = requests.post(url, headers=headers, json=data)
  return response.json()

def poll_github():
  url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/events"
  response = requests.get(url)

  if response.status_code == 200:
    events = response.json()
    for event in events:
      print(event["type"], event.get("payload", {}))
  else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response: {response.text}")
