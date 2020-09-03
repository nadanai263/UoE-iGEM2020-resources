# UoE-iGEM2020-resources
Resources for UoE iGEM 2020 team

Clone this repository to a local drive using

`git clone https://github.com/nadanai263/UoE-iGEM2020-resources.git`

#### 1.1 Installing Docker and running a container
Install Docker following instructions on their [website](https://www.docker.com/). Then navigate to the repository folder and run:
`sudo docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ nadanai263/uoeigem2020`


#### More advanced options

To build the Docker image from the Dockerfile, navigate to the folder containing the Dockerfile and run
`sudo docker build -t uoeigem2020 .`

The run command in more detail: 
`sudo docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ uoeigem2020`
This command creates a Docker container from the igem image, and launches it with the following options:
* `-p 8888:8888` exposes ports
* `--rm` deletes the container and associated files at exit
* `-it` runs in interactive mode
* `-v "$PWD":/home/jovyan/` starts the container in your current directory



