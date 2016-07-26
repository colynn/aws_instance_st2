#!/usr/bin/env python
#

import time
import AwsConfig
import AwsInstance
# import log

CONFIGFILE=".aws_instance_st2.conf"

# defined time_tag, '22' means stopped,  '8' means running.
time_tag = time.strftime("%H")


def main():
    cnf = AwsConfig(CONFIGFILE)
    if not cnf.status:
        print "ERROR: Can't load config file: %s" % CONFIGFILE
        cnf.write_config()
        sys.exit(0)
    aws_conf_dict = cnf.awscnf
    aws_conf_dict['time_tag'] = time_tag

    ec2_instance = AwsInstance(aws_conf_dict)
    instance_list = ec2_instance.instance_manage_list()
    if instance_list:
        if time_tag == aws_conf_dict['start_time']:
            ec2_instance.start(instance_list)
        else:
            ec2_instance.stop(instance_list)
    else:
        print "this time no instances need start or stop."

if __name__ == "__main__":
    main()


