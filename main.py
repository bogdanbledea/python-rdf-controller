from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
import pandas as pd
import requests

# read the test file
data = pd.read_csv('date_test.csv')

# convert date column to datetime, so python can understand
data['Time'] = pd.to_datetime(data['Time'])

# create the scheduler
scheduler = BackgroundScheduler()

# create a variable to increment
initial_moment = pd.to_datetime('19/05/20, 10:54')
time_interval = 1


def periodic_job():
    global initial_moment
    initial_moment += pd.Timedelta(minutes=1)
    next_moment = initial_moment + pd.Timedelta(minutes=1)
    logs = data[(data['Time'] >= initial_moment) & (data['Time'] < next_moment)]
    logs_to_json = logs.to_json(orient="records")
    r = requests.post('http://localhost:5000/api/convert', json=logs_to_json)
    print(r.content)


scheduler.add_job(periodic_job, 'interval', minutes=time_interval, next_run_time=datetime.now())

app = Flask(__name__)


@app.route('/api/start', methods=['POST'])
def start_scheduler():
    scheduler.start()
    return 'started the scheduler!'


@app.route('/api/stop', methods=['POST'])
def stop_scheduler():
    scheduler.shutdown()
    return 'stopped the scheduler!'


if __name__ == '__main__':
    app.run(port=6000)
