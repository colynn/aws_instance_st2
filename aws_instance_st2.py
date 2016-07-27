#!/usr/bin/env python
#

import sys
import boto3

region = 'cn-north-1'
ec2 = boto3.client('ec2', region)
tag_list = "ansible"


def instances_get():
    """
        will return dict type
        {'i-123456':{"tag": "srv-nc-test1", "status": "stopped"}}
    """
    desc_instances = ec2.describe_instances()['Reservations']
    instances = {}
    for reservation in desc_instances:
        instance_info = reservation['Instances'][0]

        for tag in instance_info['Tags']:
            # Note: If the tag of hosts is not unique, the item of instances dict will generate multiple times.
            if tag['Key'] == 'Name':
                instances[instance_info['InstanceId']] = {'tag': tag['Value'], 'status': instance_info['State']['Name']}
            continue
    return instances


def match_tag(instance_tag_name):
    for t in tag_list.split(','):
        if instance_tag_name.find(t.strip()) != -1:
            return True
    return False


def instance_manage_list(action):
    """
    {'i-123456':{"tag": "srv-nc-test1", "status": "stopped"}}

    return
    """
    instance_dict = instances_get()
    instance_list = []
    for iid in instance_dict:
        instance = instance_dict[iid]
        if match_tag(instance['tag']):
            if instance['status'] == action:
                instance_list.append(iid)
    if len(instance_list) == 0:
            print "Didn't find the host instance matching tag."
            return False
    return instance_list


def start(self, instance_list):
    self.ec2.start_instances(InstanceIds=instance_list)
    # log.get_logger().log("hello, world")


def stop(self, instance_list):
    self.ec2.stop_instances(InstanceIds=instance_list)


def main():
    if len(sys.argv) != 2:
        print "Usage: python " + sys.argv[0] +  " {start|stop}"
        sys.exit(1)
    action = sys.argv[1]
    if action == 'start':
        instance_list = instance_manage_list('stopped')
    elif action == 'stop':
        instance_list = instance_manage_list('running')
    else:
        print "argument invalid, An bu zhi dao, you want to do what, lol."
    if instance_list:
        print instance_list
        # if time_tag == aws_conf_dict['start_time']:
        #    ec2_instance.start(instance_list)
        # else:
        #    ec2_instance.stop(instance_list)
    # else:
        # print "this time no instances need start or stop."

if __name__ == "__main__":
    main()


