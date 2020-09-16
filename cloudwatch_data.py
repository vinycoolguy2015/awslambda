import boto.ec2
import boto.utils
import datetime


access_key=''
secret_access_key=''
regions = boto.ec2.regions()



for region in regions:
    try:
        connection=boto.ec2.connect_to_region(region.name,aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
        reservations = connection.get_all_reservations()
        for reservation in reservations:    
            for instance in reservation.instances:
                start_time = boto.utils.parse_ts(instance.launch_time)
                end_time = datetime.datetime.utcnow()
                metric_name = 'CPUUtilization'
                namespace = 'AWS/EC2'
                statistics = 'Average'
                unit = 'Percent'
                cw = boto.connect_cloudwatch(aws_access_key_id='AKIAJNXAUZTSGZPKYNXQ',aws_secret_access_key='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')
                metrics = cw.list_metrics()
                for metric in metrics :
                    if 'InstanceId' in metric.dimensions:
                        if instance.id in metric.dimensions['InstanceId']:
                            datapoints = cw.get_metric_statistics(60, start_time, end_time, metric_name,namespace , statistics, metric.dimensions, unit); 
                print datapoints[0]['Average'],"\n"
        
    except  boto.exception.EC2ResponseError,e:
        if e.code=="AuthFailure":
            print e.message+" in " +region.name
        else:
            raise

            
            


