#!/usr/bin/env python
#

import sys
import boto3
# from lib import log

region = 'cn-north-1'
ec2 = boto3.client('ec2', region)
tag_list = "ansible-test1, tina-bj-zabbix3.0-test"


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
    """
    :param instance_tag_name: instance tag anme.
    :return: instance tag whether included by tag_list True or False.
    """
    for t in tag_list.split(','):
        if instance_tag_name.find(t.strip()) != -1:
            return True
    return False


def instance_manage_list(instance_dict, action):
    """
    :return need start or stop instance list.
    :return ['i-123456', 'i-4563dba']
    """
    instance_list = []
    for iid in instance_dict:
        instance = instance_dict[iid]
        if match_tag(instance['tag']):
            if instance['status'] == action:
                instance_list.append(iid)
    if len(instance_list) == 0:
            print "Didn't find the host instance matching tag."
            sys.exit(1)
    return instance_list


def start(instance_list):
    respon_data = ec2.start_instances(InstanceIds=instance_list)
    status_code = respon_data['ResponseMetadata']['HTTPStatusCode']
    return status_code
    # waiter = ec2.get_waiter('instance_running')
    # waiter.wait(InstanceIds=instance_list)
    # log.get_logger().log("hello, world")


def stop(instance_list):
    respon_data = ec2.stop_instances(InstanceIds=instance_list)
    status_code = respon_data['ResponseMetadata']['HTTPStatusCode']
    return status_code


def log(code, action, instance_list, instance_dict):
    instance_tags = []
    for i in instance_list:
        instance_tags.append(instance_dict[i]['tag'])
    if code == 200:
        print "[Info] succeed " + action + " " + ','.join(instance_tags)
    else:
        print "[Error] failed " + action + " " + ','.join(instance_tags)


def main():
    if len(sys.argv) != 2:
        print "Usage: python " + sys.argv[0] +  " {start|stop}"
        sys.exit(0)
    action = sys.argv[1]
    instance_dict = instances_get()
    # 
    if action == 'start':
        instance_list = instance_manage_list(instance_dict, 'stopped')
        code = start(instance_list)
    elif action == 'stop':
        instance_list = instance_manage_list(instance_dict, 'running')
        code = stop(instance_list)
    else:
        print "[Error] argument invalid, An bu zhi dao, you want to do what, lol."
        sys.exit(1)
    log(code, action, instance_list, instance_dict)

if __name__ == "__main__":
    main()

