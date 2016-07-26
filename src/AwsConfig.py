
class AwsConfig(object):
    def __init__(self, cnffile):
        self.awscnf = {}
        self.status = True
        try:
            config = self.read_config(cnffile)
        except Exception, e:
            print '*** Caught exception - Configuration File Error: %s :\n%s: %s\n' % (cnffile, e.__class__, e)
            self.status = False

    def read_config(self, cnfconfig):
        '''
        read config file, return config instance
        '''
        config = ConfigParser.ConfigParser()
        config.readfp(open(cnfconfig))
        return config

    def write_config(self):
        print "[INFO]: Start to config QiNiu Storage Service."

        region = raw_input("Please input your region[default: cn-north-1]: ")
        start_time = raw_input("Please input start the instance's time[default: 8]: ")
        stop_time = raw_input("Please input stop the instance's time[default: 22]: ")
        tag_list = raw_input("Please input the instance's tag[default: web-test, db-test, nc-test)]: ")

        config = ConfigParser.RawConfigParser()
        config.add_section("defaults")

        config.set("defaults", 'region', region)
        config.set("defaults", 'tag_list', tag_list)
        config.set("defaults", 'start_time', start_time)
        config.set("defaults", 'stop_time', stop_time)
        cfgfile = open(CONFIGFILE, 'w+')
        config.write(cfgfile)
        print "Backup Configuration is saved into %s." % CONFIGFILE
        cfgfile.close()
