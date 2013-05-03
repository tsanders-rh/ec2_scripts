#!/usr/bin/env python
import os
import sys
import time
from launch_instance import launch_instance, get_opt_parser, ssh_command, scp_to_command, run_command, tag_instance
from optparse import OptionParser

if __name__ == "__main__":
    start = time.time()

    parser = OptionParser()
    parser = get_opt_parser(parser=parser)
    (opts, args) = parser.parse_args()
    instance = launch_instance(opts)
    hostname = instance.dns_name
    ssh_key = opts.ssh_key
    ssh_user = opts.ssh_user
    
    #
    # open firewall
    #
    print "Updating firewall rules"
    ssh_command(hostname, ssh_user, ssh_key, "mkdir -p ~/tmp")
    scp_to_command(hostname, ssh_user, ssh_key, "./etc/sysconfig/iptables", "~/tmp/")
    ssh_command(hostname, ssh_user, ssh_key, "sudo cp ~/tmp/iptables /etc/sysconfig/iptables") 
    ssh_command(hostname, ssh_user, ssh_key, "sudo /sbin/service iptables restart")

    #
    # Run install script
    #
    print "Running install script for Katello"
    scp_to_command(hostname, ssh_user, ssh_key, "./scripts/functions.sh", "~")
    scp_to_command(hostname, ssh_user, ssh_key, "./scripts/install_katello.sh", "~")
    ssh_command(hostname, ssh_user, ssh_key, "sudo chmod +x ./install_katello.sh")
    ssh_command(hostname, ssh_user, ssh_key, "time sudo ./install_katello.sh &> ./katello_rpm_setup.log ")

    #
    # Update EC2 tag with version of RCS installed
    #
    print "Update EC2 tag with RPM version of 'katello' installed on %s" % (hostname)
    status, out, err = ssh_command(hostname, ssh_user, ssh_key, "rpm -q --queryformat \"%{VERSION}\" katello")
    katello_ver = out
    tag = ""
    if instance.__dict__.has_key("tags"):
        all_tags = instance.__dict__["tags"]
        if all_tags.has_key("Name"):
            tag = all_tags["Name"]
    if not tag:
        import getpass
        tag = "%s" % (getpass.getuser())
    tag += " Katello %s" % (katello_ver)
    instance.add_tag("Name","%s" % (tag))

    end = time.time()
    print "Katello %s install completed on: %s in %s seconds" % (katello_ver, hostname, end-start)

