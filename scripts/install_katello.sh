#!/bin/sh

# Assumes that "install_rpm_setup.sh" has already been run
source ./functions.sh

# Install EPEL Repository Definition
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm || {
    echo "Unable to install EPEL"
    exit 1;
}

# Install Katello Nightly Repository Definition
rpm -Uvh http://fedorapeople.org/groups/katello/releases/yum/nightly/RHEL/6/x86_64/katello-repos-latest.rpm || {
    echo "Unable to install Katello Nightly"
    exit 1;
} 

# Install Pulp Repository Definition
cd /etc/yum.repos.d && wget http://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo || {
    echo "Unable to download Pulp repo file"
    exit 1;
}

# Set hostname of instance to EC2 public hostname
HOSTNAME=`curl -s http://169.254.169.254/latest/meta-data/public-hostname`
hostname ${HOSTNAME}
sed -i "s/^HOSTNAME.*/HOSTNAME=${HOSTNAME}/" /etc/sysconfig/network

# Install Katello
yum --disablerepo="pulp-v2-stable" --enablerepo="pulp-v2-beta" install -y katello-all
echo "RPMs installed: `date`"

# Configure Katello
katello-configure --user-pass=admin
katello-configure --user-pass=admin
echo "Completed: `date`"
