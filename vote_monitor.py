import csv
import json
from datetime import datetime

import os
import praw

from config import config
from reddit import reddit


class DefaultEncoder(json.JSONEncoder):
        def default(self, o):
            return ""

class MonitoredSubmission:

    def __init__(self, id) -> None:
        self.id = id
        self.log_file = open('monitored/' + id + '.csv', 'a+')
        self.csv_writer = csv.writer(self.log_file)
        self.submission: praw.reddit.Submission = None
        self.last_log: datetime = None
        self.load_submission()
        self.write_description()

    def load_submission(self):
        self.submission = reddit.submission(self.id)
        self.submission.title  # needed to load submission data

    def write_description(self):
        filename = 'monitored/' + self.id + '.json'
        
        if os.path.exists(filename):
            return
        
        with open(filename, 'w+', encoding='utf8') as description_file:
            self.load_submission()
            json.dump(vars(self.submission),
            description_file,
            cls=DefaultEncoder,
            ensure_ascii=False,
            sort_keys=True, indent=4, separators=(',', ': '))

    def log_score(self):
        self.load_submission()

        now = datetime.now()
        self.last_log = now

        self.csv_writer.writerow((
            now.astimezone().replace(microsecond=0).isoformat(),
            str(self.submission.score),
            str(self.submission.upvote_ratio)
        ))

        self.log_file.flush()

    def last_log_old(self) -> bool:
        if self.last_log is None:
            return True
        if ((datetime.now() - self.last_log).total_seconds() > config['submission_log_minimum_period_s']):
            return True
        return False

    def log_score_if_needed(self):
        if (self.last_log_old()):
            self.log_score()
