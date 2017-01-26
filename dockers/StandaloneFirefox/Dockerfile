FROM ubuntu:trusty
#== based on the official dockerfile
MAINTAINER VulcanoAhab
USER root
RUN apt-get update
RUN apt-get install -y firefox xvfb dbus-x11 wget
RUN mkdir -p /etc/selenium
RUN cd /etc/selenium
RUN wget https://goo.gl/Lyo36k
RUN mkdir -p /opt/selenium/
RUN ln -s selenium-server-standalone-3.0.1.jar /opt/selenium/selenium-server-standalone.jar
#====================================
# Scripts to run Selenium Standalone
#====================================
COPY entry_point.sh /opt/bin/entry_point.sh
RUN chmod +x /opt/bin/entry_point.sh
#USER seluser
EXPOSE 4444
