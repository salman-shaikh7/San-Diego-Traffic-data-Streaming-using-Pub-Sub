#!/usr/bin/env python3

# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import gzip
import logging
import argparse
import datetime
from google.cloud import pubsub_v1

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TOPIC = 'sandiego'
INPUT = 'sensor_obs2008.csv.gz'

def publish(publisher, topic, events):
    numobs = len(events)
    if numobs > 0:
        logging.info('Publishing {0} events from {1}'.format(numobs, get_timestamp(events[0])))
        for event_data in events:
            publisher.publish(topic, event_data)

def get_timestamp(line):
    line = line.decode('utf-8')  # Convert from bytes to str
    timestamp = line.split(',')[0]  # Look at the first field of the row
    return datetime.datetime.strptime(timestamp, TIME_FORMAT)

def simulate(topic, ifp, firstObsTime, programStart, speedFactor):
    def compute_sleep_secs(obs_time):
        time_elapsed = (datetime.datetime.utcnow() - programStart).seconds
        sim_time_elapsed = ((obs_time - firstObsTime).days * 86400.0 + (obs_time - firstObsTime).seconds) / speedFactor
        return sim_time_elapsed - time_elapsed

    topublish = []

    for line in ifp:
        event_data = line  # Entire line of input CSV is the message
        obs_time = get_timestamp(line)  # From the first column

        if compute_sleep_secs(obs_time) > 1:
            publish(publisher, topic, topublish)  # Notify accumulated messages
            topublish = []  # Empty out list

            to_sleep_secs = compute_sleep_secs(obs_time)
            if to_sleep_secs > 0:
                logging.info('Sleeping {} seconds'.format(to_sleep_secs))
                time.sleep(to_sleep_secs)

        topublish.append(event_data)

    # Left-over records; notify again
    publish(publisher, topic, topublish)

def peek_timestamp(ifp):
    pos = ifp.tell()
    line = ifp.readline()
    ifp.seek(pos)
    return get_timestamp(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send sensor data to Cloud Pub/Sub in small groups, simulating real-time behavior')
    parser.add_argument('--speedFactor', help='Example: 60 implies 1 hour of data sent to Cloud Pub/Sub in 1 minute', required=True, type=float)
    parser.add_argument('--project', help='Example: --project $DEVSHELL_PROJECT_ID', required=True)
    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    publisher = pubsub_v1.PublisherClient()
    event_type = publisher.topic_path(args.project, TOPIC)

    print(f"Event type (topic path): {event_type}")  # Debugging output

    try:
        # Check if the topic exists
        publisher.get_topic(event_type)
        logging.info('Reusing pub/sub topic {}'.format(TOPIC))
    except Exception as e:
        logging.warning('Could not find topic, creating new one: {}'.format(e))
        # Create the topic directly using the topic path
        publisher.create_topic(name=event_type)
        logging.info('Creating pub/sub topic {}'.format(TOPIC))

    programStartTime = datetime.datetime.utcnow()
    with gzip.open(INPUT, 'rb') as ifp:
        header = ifp.readline()  # Skip header
        firstObsTime = peek_timestamp(ifp)
        logging.info('Sending sensor data from {}'.format(firstObsTime))
        simulate(event_type, ifp, firstObsTime, programStartTime, args.speedFactor)
