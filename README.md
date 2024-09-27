# San Diego Traffic data Streaming using Pub/Sub.


## Overview 

Google Cloud Pub/Sub is a fully-managed real-time messaging service that allows you to send and receive messages between independent applications. We can Use Cloud Pub/Sub to publish and subscribe to data from multiple sources, then use Google Cloud Dataflow to understand your data, all in real time.

In this Project, we will be using San Diego traffic sensor data into a Pub/Sub topic for later to be processed by Dataflow pipeline before finally ending up in a BigQuery table for further analysis.


## Objectives

*   Create a Pub/Sub topic and subscription.
*   Simulate your traffic sensor data into Pub/Sub.


