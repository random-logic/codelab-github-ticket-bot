import os

USE_LLM_TO_DETERMINE_FIT = os.environ.get("USE_LLM_TO_DETERMINE_FIT", False)
SIMILARITY_THRESHOLD = os.environ.get("SIMILARITY_THRESHOLD", 0.1)
GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "Codelab-Davis")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "codelab-ui-components")
POLLING_RATE_PER_HOUR = os.environ.get("POLLING_RATE_PER_HOUR", 60 * 60)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if GITHUB_TOKEN is None:
  raise Exception("GITHUB_TOKEN environment variable not set")
