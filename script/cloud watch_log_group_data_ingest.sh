#!/bin/bash
for group_name in $(aws cloudwatch list-metrics --namespace AWS/Logs --metric-name IncomingBytes | jq '.Metrics[].Dimensions[].Value')
do
cat <<EOF > /tmp/cloudwatch.json
{
    "MetricDataQueries": [
        {
            "Id": "req1",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/Logs",
                    "MetricName": "IncomingBytes",
                    "Dimensions": [
                        {
                            "Name": "LogGroupName",
                            "Value": $group_name
                        }
                    ]
                },
                "Period": 2592000,
                "Stat": "Sum",
                "Unit": "Bytes"
            },
            "ReturnData": true
        }
    ],
    "StartTime": "2021-01-10T00:00:0000",
    "EndTime": "2021-02-09T00:00:0000"
}
EOF
log_size=$(aws cloudwatch get-metric-data --cli-input-json file:///tmp/cloudwatch.json| jq '.MetricDataResults[0] .Values[0]')
log_size_in_mb=$((log_size / 1000/1000))
echo "$group_name,$log_size_in_mb"
done
