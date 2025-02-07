import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from github import Github
from github.GithubObject import NotSet

load_dotenv()

REPO_NAME = os.environ.get("GITHUB_REPO_NAME")
ACCOUNT_TOKEN = os.environ.get("GITHUB_ACCOUNT_TOKEN")
if not REPO_NAME:
  raise ValueError("GITHUB_REPO_NAME environment variable is not set")

EXCLUDE_ISSUE_NUMBERS = { int(num) for num in os.environ.get("GITHUB_NON_LEGIT_ISSUE_NUMBERS").split(",") }

class Camper:
  def __init__(self, repo_name=REPO_NAME, account_token=ACCOUNT_TOKEN):
    self.g = Github(account_token)
    self.repo = self.g.get_repo(repo_name)

  def post_comment(self, issue_number, comment):
    issue = self.repo.get_issue(issue_number)
    issue.create_comment(comment)

  def is_first_commenter(self, issue_number) -> bool:
    issue = self.repo.get_issue(issue_number)
    comments = issue.get_comments()
    return comments.totalCount > 0 and comments[0].user.login == self.g.get_user().login

  # no permission to use webhooks, so polling is the next best option
  # exclude_numbers tells us which issues to exclude, since some issues aren't legit
  # within_days filters issues within the last X days
  # returns issues that are not taken yet and have 0 comments
  def read_issues_without_lock_or_first_comment(self, exclude_numbers: set[int] = None, within_days: int = None):
    if exclude_numbers is None:
      exclude_numbers = EXCLUDE_ISSUE_NUMBERS
    cutoff_date = datetime.now() - timedelta(days=within_days) if within_days else NotSet
    issues = self.repo.get_issues(state="open", assignee="none", direction="desc", since=cutoff_date)
    issues = [issue for issue in issues if not issue.locked and issue.number not in exclude_numbers and issue.comments == 0]
    return issues