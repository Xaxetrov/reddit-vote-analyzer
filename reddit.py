import json
import praw


with open('.secret.json') as secret_file:
    connection_arguments = json.load(secret_file)
    connection_arguments['user_agent'] = 'python:vote-analyzer: (by u/Xaxetrov)'

reddit = praw.Reddit(
    **connection_arguments
)