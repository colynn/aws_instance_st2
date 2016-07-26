
import boto3
import log


class AwsInstance(object):

    def __init__(self, aws_conf_dict):
        self.LOG_FILE = "/var/log/aws_instances_manage.log"
        self.region = aws_conf_dict['region']
        self.tag_list = aws_conf_dict['tag_list']
        self.start_time = aws_conf_dict['start_time']
        self.stop_time = aws_conf_dict['stop_time']
        self.time_tag = aws_conf_dict['time_tag']
        self.ec2 = boto3.client('ec2', self.region)

    def instances_get(self):
        """
            will return dict type
            {'i-123456':{"tag": "srv-nc-test1", "status": "stopped"}}
        """
        desc_instances = self.ec2.describe_instances()['Reservations']
        instances = {}
        for reservation in desc_instances:
            instance_info = reservation[Instances][0]

            for tag in instance_info['Tags']:
                # Note: If the tag of hosts is not unique, the item of instances dict will generate multiple times.
                if tag['Key'] == 'Name':
                    instances[instance_info['InstanceId']] = {'tag': tag['Value'], 'status': instance_info['State']['Name']}
                continue
        return instances

    # Just for convenience, integrated into class.
    def instance_manage_list(self):
        """
        {'i-123456':{"tag": "srv-nc-test1", "status": "stopped"}}

        return
        """
        instance_dict = self.instances_get()

        instance_list = []
        for iid in instance_dict:
            if self.time_tag == self.start_time:
                if [instance_dict[iid]['status'] == 'stopped']:
                    instance_list.append(iid)
            elif self.time_tag == self.stop_time:
                if [instance_dict[iid]['status'] == 'stopped']:
                    instance_list.append(iid)
            else:
                print "current is not specific manage start/stop time."
                instance_list = False
        return instance_list

    def start(self, instance_list):
        self.ec2.start_instances(InstanceIds=instance_list)
        log.get_logger().log("hello, world")

    def stop(self, instance_list):
        self.ec2.stop_instances(InstanceIds=instance_list)
