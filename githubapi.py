import requests
import os
from github import Github
from datetime import datetime, timedelta, timezone

REPO_NAME = os.environ.get("GITHUB_REPO_NAME", "Codelab-Davis/codelab-ui-components")
ACCOUNT_TOKEN = os.environ.get("GITHUB_ACCOUNT_TOKEN")

class GitHub:
  def __init__(self, repo_name=REPO_NAME, account_token=ACCOUNT_TOKEN):
    self.g = Github(account_token)
    self.repo = self.g.get_repo(repo_name)

  def post_github_comment(self, issue_number, comment):
    # TODO
    raise NotImplementedError

  def poll(self):
    exclude_numbers = {1, 2} # 1 and 2 aren't legit opportunities
    issues = self.repo.get_issues(state="open", assignee="none", direction="desc")
    issues = [issue for issue in issues if not issue.locked and issue.number not in exclude_numbers]
    return issues
