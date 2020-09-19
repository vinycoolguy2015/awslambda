#pip install google-cloud-monitoring.Create a service account with Project owner permission and set environment variable
#export GOOGLE_APPLICATION_CREDENTIALS=/Users/viny/Downloads/playground-s-11-ab600707-8c4e00026839.json 

from google.cloud import monitoring_v3
project_id=""
client = monitoring_v3.MetricServiceClient()
project_name = client.project_path(project_id)
descriptor = monitoring_v3.types.MetricDescriptor()
descriptor.type = 'custom.googleapis.com/failed_data_proc_jobs' + '20'
descriptor.metric_kind = (
    monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE)
descriptor.value_type = (
    monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE)
descriptor.description = 'Custom metric for failed dataproc jobs'
descriptor = client.create_metric_descriptor(project_name, descriptor)
print('Created {}.'.format(descriptor.name))
