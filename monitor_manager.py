from datetime import datetime
import os
from pathlib import Path
from typing import Dict

from praw.models import ListingGenerator
from praw.reddit import Submission
from reddit import reddit

from config import config
from vote_monitor import MonitoredSubmission


Path('monitored').mkdir(parents=True, exist_ok=True)
Path('monitored_archive').mkdir(parents=True, exist_ok=True)


monitored_submissions: Dict[str, MonitoredSubmission] = dict()


def is_datetime_recent(utc_candidate: datetime):
    utc_now = datetime.utcnow()
    return (utc_now - utc_candidate).days < config['submission_monitoring_duration_d']


def add_new_monitored_submissions(subreddit: str):
    new: ListingGenerator = reddit.subreddit(subreddit).new(limit=20)
    for item in new:
        if item.id not in monitored_submissions:
            monitored_submissions[item.id] = MonitoredSubmission(item.id)


def reload_serialized_submissions():
    for filename in os.listdir('monitored'):
        id, extension = os.path.splitext(filename)
        if extension != '.json':
            continue
        submission = reddit.submission(id)
        created_utc = datetime.utcfromtimestamp(submission.created_utc)
        if is_datetime_recent(created_utc):
            monitored_submissions[id] = MonitoredSubmission(id)
        else:
            archive_submission(id)


def archive_submission(id):
    os.rename('monitored/' + id + '.csv', 'monitored_archive/' + id + '.csv')
    os.rename('monitored/' + id + '.json', 'monitored_archive/' + id + '.json')


def archive_old_submissions():
    global monitored_submissions

    if len(monitored_submissions) <= config['minimum_monitored_submissions']:
        return
    
    recent_monitored_submissions = {}
    for id, submission in monitored_submissions.items():
        created_utc = datetime.utcfromtimestamp(submission.submission.created_utc)
        if is_datetime_recent(created_utc):
            recent_monitored_submissions[id] = submission
        else:
            archive_submission(id)
    monitored_submissions = recent_monitored_submissions
