import pandas as pd
import requests
import json

def send_json_to_api(json_log):
    r = requests.post('http://localhost:5000/api/convert', json=json_log)
    print(r.content)


def read_file():
    #Read the test csv file to submit to the converter service
    data = pd.read_csv('date_test.csv')

    # Get the first log and convert it to json
    json_data = data[0:1].to_json()

    # Parse the json to access the object
    open_json = json.loads(json_data)

    # Create the json object to be sent in the POST request
    log_time = open_json['Time']['0']
    log_event_context = open_json['Event context']['0']
    log_user_full_name = open_json['User full name']['0']
    log_affected_user = open_json['Affected user']['0']
    log_component = open_json['Component']['0']
    log_event_name = open_json['Event name']['0']
    log_description = open_json['Description']['0']
    log_origin = open_json['Origin']['0']
    log_ip_address = open_json['IP address']['0']

    log_json = {
        "time": log_time,
        "userFullName": log_user_full_name,
        "affectedUser": log_affected_user,
        "eventContext": log_event_context,
        "component": log_component,
        "eventName": log_event_name,
        "description": log_description,
        "origin": log_origin,
        "ipAddress": log_ip_address
    }

    send_json_to_api(log_json)

if __name__ == '__main__':
    read_file()

