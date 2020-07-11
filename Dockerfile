FROM python:3.8-slim

MAINTAINER jorgeht@usal.es

ARG user
ARG uid
ARG guid

# Creates user docker (1000)
RUN groupadd --gid $guid $user && \
	useradd --gid $uid --uid $guid $user && \
	mkdir -p /home/$user/.ssh && \
	chown -R $user:$user /home/$user

# Install python virtual env module.
RUN pip3 install pipenv

# Clean.
RUN apt autoremove -y && \
	apt clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["python3"]

