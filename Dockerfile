# Dockerfile for lanes.py

FROM python:3
MAINTAINER JesterI3D "montes3550@gmail.com" 


ADD lanes.py /

RUN pip3 install numpy && pip3 install opencv-python
  
CMD [ "python", "./lanes.py" ]
