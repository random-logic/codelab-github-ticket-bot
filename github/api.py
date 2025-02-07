import requests
import os
from github import Github

REPO_NAME = os.environ.get("GITHUB_REPO_NAME", "Codelab-Davis/codelab-ui-components")
ACCOUNT_TOKEN = os.environ.get("GITHUB_ACCOUNT_TOKEN")

class GithubAPI:
  def __init__(self, repo_name=REPO_NAME, account_token=ACCOUNT_TOKEN):
    self.g = Github(account_token)
    self.repo = self.g.get_repo(repo_name)

  def post_github_comment(self, issue_number, comment):
    url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments"
    headers = {
      "Authorization": f"Bearer {self.account_token}" if self.account_token else "",
      "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}

    response = requests.post(url, headers=headers, json=data)
    return response.json()

  def poll(self):
    for issue in self.repo.get_issues(state='all'):
      print(f"Issue Title: {issue.title}")
      print(f"URL: {issue.html_url}")