import time

from praw.models import *

from config import config
import monitor_manager


interval = config['loop_minimum_period_s']

monitor_manager.reload_serialized_submissions()

starttime = time.time()

while True:
    monitor_manager.add_new_monitored_submissions(config['subreddit'])
    monitor_manager.archive_old_submissions()

    for submission in monitor_manager.monitored_submissions.values():
        submission.log_score_if_needed()

    time.sleep(interval - ((time.time() - starttime) % interval))