# Create VM

make sure port forwarding is enabled

## Command Line

# Update VM and install dependencies

## Upgrade/Update

    sudo su
    yum update

# MariaDB & Connector

    https://mariadb.com/resources/blog/how-to-install-mariadb-on-rhel8-centos8/
    https://mariadb.com/docs/ent/connect/programming-languages/c/install/#Installation_via_Package_Repository_(Linux)

## Maria DB

    yum install wget

    wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
    chmod +x mariadb_repo_setup
    ./mariadb_repo_setup

    yum install perl-DBI libaio libsepol lsof boost-program-options
    
    yum install rsync
    yum install libpmem
    yum install socat
    
    yum install --repo="mariadb-main" MariaDB-server
    
    ## mysql_install_db - no need to run this?
    
    systemctl start mariadb.service
    
    systemctl status mariadb.service
    
    ## mysql_secure_installation - wrong for newer versions
    
    mariadb-secure-installation
    
    
## Install MariaDB Connector/C
    
    I could not install this in Fedora to fell back to RHEL

    ## yum install MariaDB-shared MariaDB-devel ## shared already installed
    
    yum install MariaDB-devel

## Check what is installed now

    yum list installed

## install nano

    yum install nano

## podman

    yum -y install podman

    ?sudo yum module enable -y container-tools:rhel8
    ?sudo yum module install -y container-tools:rhel8
    
    ?yum install podman-plugins

## install dependencies

    ?yum install wget yum-utils make gcc openssl-devel bzip2-devel libffi-devel zlib-devel 

    yum install git
    
    ?yum install sqlite-devel

## Upgrade Python to 3.10

    Thank you to : https://tecadmin.net/how-to-install-python-3-10-on-centos-rhel-8-fedora/

    yum install yum-utils make openssl-devel bzip2-devel libffi-devel zlib-devel

    wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz 

    tar xzf Python-3.10.8.tgz 

    cd Python-3.10.8 
    ./configure --with-system-ffi --with-computed-gotos --enable-loadable-sqlite-extensions 

    ./configure --enable-optimizations

    make -j ${nproc} ## this takes a VERY LONG TIME!
    
    make altinstall

    rm Python-3.10.8.tgz

    /usr/local/bin/python3.10 --version
    
    pip install --upgrade pip



## Testing Python3.10 and Pip

/usr/local/bin/python3.10 --version
/usr/local/bin/pip3.10 --version  

## Create env

/usr/local/bin/python3.10 -m venv env

## Python on Server
    
    sudo su
    
    ##yum install python-devel    # for python2.x installs
    
    yum install python3-devel   # for python3.x installs
    
    yum install gcc

    #yum install -y mariadb-server
    
    #yum install mariadb-connector-c-devel


# Establish SSH to Host

## Run on local computer

ssh-keygen -t rsa -f ~/.ssh/key202211020852 -C andrew_gaitskell -b 2048

cd ~/.ssh

cat key202211020852.pub

copy output and paste into VM ssh keys

remove key202203251421.pub at start

connect to vm

ssh-keygen -f "/home/andrewcgaitskell/.ssh/known_hosts" -R "35.214.57.82"

ssh -i ~/.ssh/key202211020852 andrew_gaitskell@35.214.101.196

## Create Project Folder

    do not su

    mkdir projects
    cd projects

## create env

    /usr/local/bin/python3.10 -m venv env -m venv env

## enable env

    source env/bin/activate
    
## upgrade pip

   pip --version
   
   pip install --upgrade pip
   
# Group Shared Folder

    sudo su
    cd /opt
    mkdir tools
    groupadd add tools
    chown root:tools /opt/tools
    chmod 2775 /opt/tools
    useradd myuser
    usermod -a -G tools myuser

# set user password and add to group

    passwd myuser
    usermod -aG tools myuser
