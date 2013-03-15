ec2_scripts
===========
Scripts to provision various EC2 instance configurations

Will provision an EC2 instance running Red Hat Enterprise Linux 6

 * Root filesystem will be expanded to at least 25GB
 * Firewalls will be updated
 * hostname is changed to match external hostname
 * Httpd SSL cert will be auto generated matching hostname
 * RPMS & Config files will be installed/modified for the desired project

Launch scripts for following configurations:

 * Candlepin
 * Pulp v2.1 beta builds
 * Spacewalk
 * Splice
  * Report Server
  * RCS
  * Spacewalk + Candlepin + Spacwalk-Splice-Tool

Examples
---------

 - launch_instance.py
  * Will provision a new ec2 instance with an expanded root partition

 - launch_RCS.py
  * Will provision & configure a new RCS instance in EC2

 - install_rpm_setup.sh
  * Script to use on a provisioned instance, will pull down splice repo and install RPMs

 - launch_Spacewalk.py
  * Provisions a postgres backed Spacewalk by itself

 - launch_Spacewalk_Candlepin.py
  * Provisions a postgres backed Spacewalk with Candlepin Installed
 
 - launch_Pulp.py
  * Provisions Pulp v2 Beta 


Recommend Usage:
----------------

 1. Set the following environment variables in your ~.bashrc
  * export CLOUDE_GIT_REPO=/git/cloude
  * export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
  * export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY

 1. Run the script
  * ./launch_RCS.py
  *  Wait ~10 minutes

 1. ssh into the ec2 hostname printed from the script
  * Completed Splice install on: ec2-107-22-99-233.compute-1.amazonaws.com


Optional, if desired you may override the default settings through command line arguments:
---------------

    $ ./launch_RCS.py --help
    Usage: launch_RCS.py [options]

    Options:
        -h, --help            show this help message and exit
        --product_data=PRODUCT_DATA
                        Product data for splice-certmaker: defaults to
                        /git/cloude/splice/sample-data/sample-certgen-
                        products.json
        --ssh_user=SSH_USER   SSH username
        --ssh_key=SSH_KEY     Path to ssh key, defaults to: /git/cloude/splice/aws
                        /ssh-keys/splice_rsa.pub
        --ami=AMI             AMI, defaults to: ami-cc6af9a5
        --key_name=KEY_NAME   Name for ssh key in EC2, defaults to: splice
        --type=TYPE           Instance type, defaults to: m1.large
        --zone=ZONE           Zone to launch this instance, defaults to: us-east-1d
        --group=GROUP         Security Group, defaults to: devel-testing
        --vol_size=VOL_SIZE   Root volume size, defaults to: 25


To Launch Spacewalk & Candlepin
---------------------------
 * As in above, your "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY" must be specified.
 * Additionally a "Subscription Manifest" must be provided.

><br/>$ ./launch_Spacewalk_Candlepin.py --manifest ~/Splice/Spacewalk_Investigation/manifest/manifest.zip 
><br/>Waiting for instance 'i-49898b39' to come up
<br/>Waited 0 seconds for instance 'i-49898b39' to come up
<br/>Waited 10 seconds for instance 'i-49898b39' to come up
<br/>Waited 20 seconds for instance 'i-49898b39' to come up
<br/>Waiting for instance 'ec2-107-22-56-64.compute-1.amazonaws.com' to listen for ssh requests
<br/>Attempt '1' waiting for ssh to come up on ec2-107-22-56-64.compute-1.amazonaws.com
<br/>Attempt '2' waiting for ssh to come up on ec2-107-22-56-64.compute-1.amazonaws.com
<br/>Resizing /dev/xvde1 on ec2-107-22-56-64.compute-1.amazonaws.com
<br/>Updating firewall rules
</br>Running install script for Spacewalk
</br>Update EC2 tag with RPM version of 'spacewalk' installed on ec2-107-22-56-64.compute-1.amazonaws.com
<br/>Spacewalk 1.8.6 install completed on: ec2-107-22-56-64.compute-1.amazonaws.com in 1344.49916697 seconds


