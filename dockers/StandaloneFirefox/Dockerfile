FROM ubuntu:trusty
#== based on the official dockerfile
MAINTAINER VulcanoAhab
USER root

RUN apt-get update
RUN apt-get -y install python-software-properties
RUN apt-get -y install software-properties-common

# Install Java.
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN apt-get install -y oracle-java8-installer
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /var/cache/oracle-jdk8-installer

# Define working directory.
WORKDIR /data

# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

RUN apt-get update
RUN apt-get install -y firefox xvfb dbus-x11 wget
RUN mkdir -p /etc/selenium
RUN cd /etc/selenium
RUN wget https://goo.gl/Lyo36k

ADD xvfb.init /etc/init.d/xvfb
RUN chmod +x /etc/init.d/xvfb
RUN update-rc.d xvfb defaults
CMD service xvfb start; export DISPLAY=:10; java -jar selenium-server-standalone-3.0.1.jar

EXPOSE 4444
