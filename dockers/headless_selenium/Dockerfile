FROM selenium/node-firefox:3.0.1-fermium
MAINTAINER VulcanoAhab
USER root
RUN apt-get install -y xvfb
RUN mkdir /tmp/.X11-unix
RUN chmod 1777 /tmp/.X11-unix
RUN chown root /tmp/.X11-unix/
#====================================
# Scripts to run Selenium Standalone
#====================================
USER seluser
EXPOSE 4444
CMD Xvfb :10 -screen 0 1600x1200x16; export DISPLAY=:10 & java -jar /opt/selenium/selenium-server-standalone.jar
