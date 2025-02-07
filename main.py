import atexit
import threading
from datetime import datetime
import os
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler

from camper import Camper
from model import Model

from dotenv import load_dotenv
load_dotenv()

USE_LLM_TO_DETERMINE_FIT = os.environ.get("USE_LLM_TO_DETERMINE_FIT", False)
SIMILARITY_THRESHOLD = float(os.environ.get("SIMILARITY_THRESHOLD", 0))
SECONDS_PER_POLL = float(os.environ.get("SECONDS_PER_POLL", 1))
COMMENT_TO_POST = os.environ.get("COMMENT_TO_POST")
ISSUE_QUERY = os.environ.get("ISSUE_QUERY")
if ISSUE_QUERY is None:
  raise Exception("ISSUE_QUERY environment variable not set")
if COMMENT_TO_POST is None:
  raise Exception("COMMENT_TO_POST environment variable not set")

EXIT_AFTER_SUCCESS = True
SCHEDULER_MAX_INSTANCES = 1

def main():
  camper = Camper()
  model = Model()
  embedded_query = model.embed(ISSUE_QUERY)
  stop_polling_flag = threading.Event() # No race condition

  def comment(issue):
    if stop_polling_flag.is_set():
      return

    camper.post_comment(issue.number, COMMENT_TO_POST)

    if camper.is_first_commenter(issue.number):
      print(f"We got the first comment on issue number {issue.number}")
      stop_polling_flag.set()
      if EXIT_AFTER_SUCCESS:
        print("Exiting program")
        sys.exit(0)

  # Ran on different thread
  def poll():
    if stop_polling_flag.is_set():
      return

    print("Attempting to poll website")
    try:
      issues = camper.read_issues_without_lock_or_first_comment()
      # TODO: Add concurrency
      for issue in issues:
        if not USE_LLM_TO_DETERMINE_FIT:
          comment(issue)
          continue

        # Get similarity between query and issue
        issue_desc = '\n'.join([issue.title, issue.body])
        embedded_issue = model.embed(issue_desc)
        similarity = model.cosine_similarity(embedded_issue, embedded_query)

        if similarity >= SIMILARITY_THRESHOLD:
          comment(issue)
        else:
          print(f"Issue number {issue.number} does not match preferences")

      print("Didn't find any matches")
      print("Retrying on next poll...")
    except SystemExit:
      pass
    except Exception as e:
      print(f"Polling failed with exception: {e}")
      print("Retrying on next poll...")

  scheduler = BackgroundScheduler()
  scheduler.add_job(poll, 'interval', seconds=SECONDS_PER_POLL, next_run_time=datetime.now(), max_instances=SCHEDULER_MAX_INSTANCES)
  scheduler.start()
  atexit.register(scheduler.shutdown)

  # Keep polling indefinitely
  while not stop_polling_flag.is_set():
    time.sleep(1)

if __name__ == "__main__":
  main()