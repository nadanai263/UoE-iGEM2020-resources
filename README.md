# UoE-iGEM2020-resources
Resources for UoE iGEM 2020 team

Clone this repository to a local drive using the command line

`git clone https://github.com/nadanai263/UoE-iGEM2020-resources.git`

or by direct download.

#### Installing Docker and running Jupyter notebook in a container
Install Docker following instructions on their [website](https://www.docker.com/) (on Windows you may need to update the Linux kernel - just follow instructions). Then navigate to the repository using a terminal and run (on Mac, Linux):

`docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ nadanai263/uoeigem2020:001`

or on Windows:

`docker run -p 8888:8888 --rm -it -v "%CD%":/home/jovyan/ nadanai263/uoeigem2020:001`

This will pull a Docker container from the DockerHub repository, and launch Jupyter notebook on your machine (subsequent calls will be faster as you'll already have the image on your computer). If the notebook doesn't automatically launch, you just need to copy the URL given in your terminal into a browser window. You can now interact with the Jupyter notebook directly on your machine, through the Docker container. 

#### More advanced options 1: running Python through a Docker container
You can use another Docker image which contains a version of Python with required dependencies. Inside the repository, you can execute python scripts using the following command (Mac, Linux):

`docker run --rm -v "$PWD":/app nadanai263/uoeigem2020-py:001 python app/run_modelTXO.py`

or on Windows:

`docker run --rm -v "%CD%":/app nadanai263/uoeigem2020-py:001 python app/run_modelTXO.py`

where here we are running the script `run_modelTXO.py`. To start a Python interpreter interactively, run

`docker run -it --rm nadanai263/uoeigem2020-py:001`

#### More advanced options 2: building your own Dockerfile
To build the Docker image from the Dockerfile (which you can freely edit), navigate to the folder containing the Dockerfile and run

`docker build -f Dockerfile_jupyter -t <yournewimagename> .`

The run command in more detail: 

`docker run -p 8888:8888 --rm -it -v "$PWD":/home/jovyan/ uoeigem2020:001`

This command creates a Docker container from the igem image, and launches it with the following options:
* `-p 8888:8888` exposes the container's internal ports
* `--rm` deletes the container and associated files at exit
* `-it` runs in interactive mode
* `-v "$PWD":/home/jovyan/` starts the container in your current directory
* uoeigem2020:001 is the image:tag, corresponding to a specific image on DockerHub

#### Local python environments
Using Docker is recommended because it ensures we all use exactly the same environment. If you are confident about building your own environment, you can use the requirements.txt file in the repository to regenerate an environment, or the Pipfile to generate a [pipenv](https://pipenv.pypa.io/en/latest/). Recommended tools for local environment management are [Anaconda](https://www.anaconda.com/) and the [PyCharm IDE](https://www.jetbrains.com/pycharm/).

#### Cleaning up
To see which Docker images are on your computer run

`docker image ls -a`

and to remove images run

`docker image rm <imagename>`

Much more documentation is available online. 

