# UoE-iGEM2020-resources
Resources for UoE iGEM 2020 team

Clone this repository to a local drive using

`git clone https://github.com/nadanai263/UoE-iGEM2020-resources.git`

#### 1.1 Installing python

To run:
`sudo docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ igem`

This command creates a Docker container from the igem image, and launches it with the following options:
* `-p 8888:8888` exposes ports
* `--rm` deletes the container and associated files at exit
* `-it` runs in interactive mode
* `-v "$PWD":/home/jovyan/` starts the container in your current directory


To build:
`sudo docker build -t igem .`
