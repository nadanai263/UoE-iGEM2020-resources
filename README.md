# UoE-iGEM2020-resources
Resources for UoE iGEM 2020 team

Clone this repository to a local drive using the command line

`git clone https://github.com/nadanai263/UoE-iGEM2020-resources.git`

or by direct download.

#### 1.1 Installing Docker and running a container
Install Docker following instructions on their [website](https://www.docker.com/) (on Windows you may need to update the Linux kernel - just follow instructions). Then navigate to the repository using a terminal and run (on Mac, Linux):
`sudo docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ nadanai263/uoeigem2020:001`

or on Windows:
`docker run -p 8888:8888 --rm -it -v "%CD%":/home/jovyan/ nadanai263/uoeigem2020:001`

This will pull a Docker container from the DockerHub repository, and launch Jupyter notebook on your machine. If the notebook doesn't automatically launch, you just need to copy the URL given in your terminal into a browser window. You can now interact with the python code directly on your machine, through the Docker container. 

#### More advanced options
To build the Docker image from the Dockerfile, navigate to the folder containing the Dockerfile and run
`sudo docker build -t uoeigem2020 .`

The run command in more detail: 
`sudo docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ uoeigem2020:001`
This command creates a Docker container from the igem image, and launches it with the following options:
* `-p 8888:8888` exposes the container's internal ports
* `--rm` deletes the container and associated files at exit
* `-it` runs in interactive mode
* `-v "$PWD":/home/jovyan/` starts the container in your current directory
* uoeigem2020:001 is the image:tag, corresponding to a specific image on DockerHub

#### Local python environments
Using Docker is recommended because it ensures we all use exactly the same environment. If you are confident about building your own environment, you can use the requirements.txt file in the repository to regenerate an environment. Recommended tools for local environment management are [Anaconda](https://www.anaconda.com/) and the [PyCharm IDE](https://www.jetbrains.com/pycharm/).