#pip install google-cloud-monitoring.Create a service account with Project owner permission and set environment variable
#export GOOGLE_APPLICATION_CREDENTIALS=/Users/viny/Downloads/a.json 

import time
from google.cloud import monitoring_v3
project_id=""
RANDOM_SUFFIX='20'
client = monitoring_v3.MetricServiceClient()
project_name = client.project_path(project_id)
series = monitoring_v3.types.TimeSeries()
series.metric.type='custom.googleapis.com/failed_data_proc_jobs' + RANDOM_SUFFIX
series.resource.type = 'global'
point = series.points.add()
point.value.double_value = 6
now = time.time()
point.interval.end_time.seconds = int(now)
point.interval.end_time.nanos = int((now - point.interval.end_time.seconds) * 10**9)
client.create_time_series(project_name, [series])
