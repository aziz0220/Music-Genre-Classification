FROM jenkins/jenkins:2.414.3-lts-slim
USER root
RUN apt-get update && apt-get install -y apt-transport-https \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    && apt-get clean

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN apt-key fingerprint 0EBFCD88

RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

RUN apt-get update && apt-get install -y docker-ce-cli


#RUN usermod -aG docker jenkins

EXPOSE 8080

USER jenkins

RUN jenkins-plugin-cli --plugins blueocean:1.24.3

#ENTRYPOINT ["/usr/bin/java", "-Duser.timezone=UTC", "-jar", "/usr/share/jenkins/jenkins.war"]
