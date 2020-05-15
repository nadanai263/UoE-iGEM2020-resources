# UoE-iGEM2020-resources
Resources for UoE iGEM 2020 team

Clone this repository to a local drive using

`git clone https://github.com/nadanai263/UoE-iGEM2020-resources.git`

#### 1.1 Installing python
Install python 3.7 using the Anaconda framework (https://www.anaconda.com/distribution/). Then navigate to the directory containing the file `msc2020.yml` (which by default is the same as the one in which this notebook is located). Run

`conda env create --file msc2020.yml`

This creates a clone of the python 3.7 *environment* as specified in the file, called MSc2020. NB if cloning doesn't work see section 1.2 below. The purpose of environments is to keep track of the versions of the all the packages you use. Once this is done, go to the command line and test the installation. Type

`conda env list`

and this should show your new environment in addition to the 'base' environment. When you start work you can activate your environment using

`conda activate MSc2020`. And when you finish don't forget to deactivate using `conda deactivate`. Go ahead and activate your environment now.

To see installed packages run `conda list`. *There are two ways of installing packages, using either the pip or conda commands: you can read more about the differences here (https://www.anaconda.com/using-pip-in-a-conda-environment/)*. You will probably need to install a number of packages throughout the project, so please see the documentation for how to do this.

You can now skip to section 2.1 below.

#### 1.2 If cloning doesn't work
If cloning doesn't work, create an environment manually using the following command:

`conda create --name MSc2020 python=3.7`

Then activate the new environment:

`conda activate MSc2020`

Install packages using the following command:

`conda install jupyter numpy=1.18.1 pandas=0.25.1 scipy=1.3.1 seaborn=0.10.0 matplotlib=3.1.1`


#### 2.1 Setting up jupyter notebook
In order to get jupyter notebook to work, you must add your environment to jupyter by running

`python -m ipykernel install --user --name=MSc2020`.

Finally, to run jupyter notebook, type

`jupyter notebook` on the command line.

#### 3.1 Installing julia
Download and install julia 1.4 (https://julialang.org/downloads/), and start up the julia REPL ('read-eval-print-loop') by running

`julia`

on the command line. Use the following two commands to call up the package manager, then install IJulia

`using Pkg`

`Pkg.add("IJulia")`

This will integrate the julia installation with jupyter notebook.

Next run the following commands to install packages:

`Pkg.add("CSV")`

`Pkg.add("DataFrames")`

`Pkg.add("Plots")`

`Pkg.add("Sundials")`

`Pkg.add("Interpolations")`

`Pkg.add("ProgressBars")`

(To do this more quickly, press `]` from the Julia REPL to start the Pkg REPL, then run `add CSV DataFrames Plots Sundials Interpolations ProgressBars` in one command. Exit the Pkg REPL by pressing Ctl+C.)

### Project Resources
I will keep this repository updated with the latest information during the lifetime of the project. If you follow the repository you can be notified every time there is an update.
