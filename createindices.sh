#!/bin/sh

echo "Install Curl for making the API call to Elasticsearch"
apk add curl

echo "Create indices"
curl --silent --show-error --fail -I "elasticsearch:9200/logstash-03-hayabusajson?pretty"
status=$?
if [ $status -ne 0 ]; then
    echo 'Index does not exists'
    echo "$res"
    curl -X PUT "elasticsearch:9200/logstash-03-hayabusajson?pretty" -H 'Content-Type: application/json' -d'
    {
        "settings": {
            "index.mapping.total_fields.limit": "2000"
        },
    "mappings": {
	 "properties": {
 	  "Details": {
	   "properties": {
         "Action": { "type":"text" }
	    }
      },
 	  "ExtraFieldInfo": {
	   "properties": {
         "fileLength": { "type":"text" },
         "RemotePorts": { "type":"text" },
         "LocalPorts": { "type":"text" },
         "ProcessId": { "type":"text" },
         "bytesTotal": { "type":"text" }
	    }
      }
     }
    }
    }
    '
else
    echo 'Hayabusa index exists. Skipping.'
fi

curl --silent --show-error --fail -I "elasticsearch:9200/logstash-02-chainsawjson?pretty"
status=$?
if [ $status -ne 0 ]; then
    echo 'Index does not exists'
    echo "$res"
    curl -X PUT "elasticsearch:9200/logstash-02-chainsawjson?pretty" -H 'Content-Type: application/json' -d'
    {
        "settings": {
            "index.mapping.total_fields.limit": "2000"
        }
    }
    '
else
    echo 'Chainsaw index exists. Skipping.'
fi

echo "Done"


