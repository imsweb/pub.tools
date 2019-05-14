FROM centos:centos7

RUN yum -y install gcc \
 && yum -y install libxml2-devel \
 && yum -y install libxslt-devel \
 && yum -y install epel-release \
 && yum -y install python-pip \
 && yum -y install python-devel \
 && yum -y install python-virtualenv \
 && yum -y install git \
 && virtualenv -p python2.7 ./venv2 \
 && source ./bin/activate \
 && pip install --upgrade pip \
 && cd ~/

CMD ["/bin/bash"]
