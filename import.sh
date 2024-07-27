#!/bin/sh

echo "Install Curl for making the API call to Kibana"
apk add curl

echo "Importing the saved objects: dashoards/*.ndjson"
for file in $(ls /tmp/dashboards/*.ndjson);do curl -X POST kibana:5601/api/saved_objects/_import?overwrite=true -H 'kbn-xsrf: true' --form file=@$file; done

echo "Done importing"
