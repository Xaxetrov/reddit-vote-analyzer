# Reddit Vote Analyzer

These tools let you dynamically monitor posts of a subreddit during their early life. The monitoring respects reddit API call limitations and runs live as long as the program runs. It is able to continue monitoring monitoring from previous executions.


## Requirements / Installation

These tools are not packaged yet.

For simple requirements installation, run `pip install -r requirements.txt`.
For better requirements management, install pip tools (`pip install pip-tools`) and run it in the root of the project (`pip-sync`).


## Configuration

Customize *config.json* :
- `loop_minimum_period_s`: Minimum period between two iterations of the main loop.
- `minimum_monitored_submissions`: Minimum number of submissions monitored, disregarding monitoring duration.
- `submission_log_minimum_period_s`: Minimum period between two data points .
- `submission_monitoring_duration_d`: Starting from submission posting on reddit, time after which its monitoring stops if newer submissions arrive.
- `subreddit`: Name of subreddit on which submissions are monitored

Add a *.secret.json* file following this template:
```json
{
    "client_id": "somethingsomethingsomething",
    "client_secret": "somethingelsesomethingelsesomethingelse"
}
```
Fill it with data from https://www.reddit.com/prefs/apps (documentation there: https://github.com/reddit-archive/reddit/wiki/OAuth2).


## Execution

### Monitor

From the root of the project, run `monitor_main.py`.

Do not stop the program until you want the monitoring to stop. For long runs, it is advised to run it as a service.

Monitored submissions are kept in the *monitored* subfoler by the program. Those that are not monitored anymore are moved to the *monitored_archive* subfoler.

### Visualize

From the root of the project, run `visualize_main.py <id>` with \<id\> the identifier of a previously monitored submission stored in the *monitored_archive* subfolder.

A visualization will be displayed while also being stored in the *images* subfolder.
