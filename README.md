# San Diego Traffic data Streaming using Pub/Sub.


## Overview 

Google Cloud Pub/Sub is a fully-managed real-time messaging service that allows you to send and receive messages between independent applications. We can Use Cloud Pub/Sub to publish and subscribe to data from multiple sources, then use Google Cloud Dataflow to understand your data, all in real time.

In this Project, we will be using San Diego traffic sensor data into a Pub/Sub topic for later to be processed by Dataflow pipeline before finally ending up in a BigQuery table for further analysis.


## Objectives

*   Create a Pub/Sub topic and subscription.
*   Simulate your traffic sensor data into Pub/Sub.

## PART 1 : You will be running a sensor simulator from the training VM. 

There are several files and some setup of the environment required.


```bash
export DEVSHELL_PROJECT_ID=$(gcloud config get-value project)
```

Task 2. Create Pub/Sub topic and subscription

```bash
gcloud pubsub topics create sandiego
```

```bash
gcloud pubsub topics publish sandiego --message "hello"
```
```bash
gcloud pubsub subscriptions create --topic sandiego mySub1
```
```bash
gcloud pubsub subscriptions pull --auto-ack mySub1
```

```bash
gcloud pubsub subscriptions delete mySub1
```

## Task 3. Simulate traffic sensor data into Pub/Sub 

*   We don't have any real time data streaming for this project instead we will create simulated streaming using Python code.
*   We will use GCP training dataset by google cloud. 

    Dataset Link : gs://cloud-training-demos/sandiego/sensor_obs2008.csv.gz

    Script for simluation Link : 
 [Script for simluation ](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/courses/streaming/publish/send_sensor_data.py)

*   The script extracts the original time of the sensor data and pauses between sending each message to simulate realistic timing of the sensor data. 
*   The value speedFactor changes the time between messages proportionally. 
*   So a speedFactor of 60 means "60 times faster" than the recorded timing. It will send about an hour of data every 60 seconds.


### STEP 1 : download the dataset 

```bash
gsutil cp gs://cloud-training-demos/sandiego/sensor_obs2008.csv.gz .
```


### STEP 2 : download the dataset 



```bash
./send_sensor_data.py --speedFactor=60 --project $DEVSHELL_PROJECT_ID
```




Task 4. Verify that messages are received
<br>


cd ~/training-data-analyst/courses/streaming/publish

```bash
gcloud pubsub subscriptions create --topic sandiego mySub2
gcloud pubsub subscriptions pull --auto-ack mySub2
```

Cancel 
```bash
gcloud pubsub subscriptions delete mySub2
```