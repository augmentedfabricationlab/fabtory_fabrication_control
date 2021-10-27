# ABB Fabtory Simulation and Control Environment

**Quick links:** [compas docs](https://compas-dev.github.io/main/) | [compas_fab docs](https://gramaziokohler.github.io/compas_fab/latest/) | [urdf and moveit tutorials](https://gramaziokohler.github.io/compas_fab/latest/examples/03_backends_ros/07_ros_create_urdf_ur5_with_measurement_tool.html) | [simulation playground](#Alte-Schmiede-Simulation-Playground) | [troubleshooting](#docker-troubleshooting)

## Requirements

* Operating System: **Windows 10 Pro** <sup>(1)</sup>.
* [Rhinoceros 3D 7.0](https://www.rhino3d.com/)
* [Anaconda Python Distribution](https://www.anaconda.com/download/): 3.x
* [Docker Community Edition](https://www.docker.com/get-started): Download it for [Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows). Leave "switch Linux containers to Windows containers" disabled.
* X11 Server: On Windows use [XMing](https://sourceforge.net/projects/xming/), on Mac use [XQuartz](https://www.xquartz.org/) (see details [here](https://medium.com/@mreichelt/how-to-show-x11-windows-within-docker-on-mac-50759f4b65cb)).
* Git: [official command-line client](https://git-scm.com/) or visual GUI (e.g. [Github Desktop](https://desktop.github.com/) or [SourceTree](https://www.sourcetreeapp.com/))
* [ABB RobotStudio](https://new.abb.com/products/robotics/robotstudio/downloads): 6.08 (only available for Windows). After install, **make sure you add RobotWare 6.03.02** (`Add-Ins` -> `RobotApps` -> `RobotWare` and add `6.03.02`).
* [VS Code](https://code.visualstudio.com/) with the following `Extensions`:
  * `Python` (official extension)
  * `EditorConfig for VS Code` (optional)
  * `Docker` (official extension, optional)
  * `RAPID ABB` (Syntax highligher for RAPID files in VS Code, optional)

<sup>(1): Windows 10 Home does not support running Docker.</sup>


## Dependencies

* [COMPAS](https://compas-dev.github.io/)
* [COMPAS FAB](https://gramaziokohler.github.io/compas_fab/latest/)
* [Assembly Information Model](https://github.com/augmentedfabricationlab/assembly_information_model)


## Getting Started

### 1. Setting up the Anaconda environment with COMPAS

#### COMPAS and COMPAS FAB Installation
    
    (base) conda config --add channels conda-forge
    (base) conda create -n ffc compas_fab --yes
    (base) conda activate ffc
    (ffc) python -m compas_rhino.install -v 7.0
    
#### Verify Installation

    (ffc) pip show compas_fab
    
    Name: compas-fab
    Version: 0.19.1
    Summary: Robotic fabrication package for the COMPAS Framework
    ....
    
#### Update COMPAS
 
    (ffc) conda update -n ffc COMPAS

#### Update COMPAS FAB

    (ffc) pip install --upgrade compas_fab
    
or switch to a specific version

    (ffc) pip install compas_fab==0.XX.X
    
and don't forget to install update on Rhino

    (ffc) python -m compas_rhino.install -v 7.0
    
### 2. Cloning and installing the repository

#### Repository Cloning
Then, clone [this repository](https://github.com/augmentedfabricationlab/fabtory_fabrication_control) into your workspace/project folder.  

* Create a workspace directory: C:\Users\YOUR_USERNAME\workspace
* Open Github Desktop, clone the [fabtory_fabrication_control](https://github.com/augmentedfabricationlab/fabtory_fabrication_control) repository into you workspace folder 


### 3. Simulation

#### Robot Artist

* Open the file [rhino/robotic_setup_fabtory_artist.ghx](rhino/robotic_setup_fabtory_artist.ghx) and load the robot model, you can then visualize the robot and move the axis and joints with forward kinematics.

#### Simulation Playground

* Once you opened the file [rhino/robotic_setup_fabtory_simulation.3dm](rhino/robotic_setup_fabtory_simulation.3dm) and [rhino/robotic_setup_fabtory_simulation.ghx](rhino/robotic_setup_fabtory_simulation.ghx) and loaded the robot model, you can start the Docker ROS moveit simulation environment and connect your ROS client to it.
* For starting the __Docker ROS moveit simulation environment__, go to VS code and start the docker containers by:
  * __Running Docker images__: Run the docker image that matches your robot model, in this case [`docker/ros-systems/abb_fabtory/docker-compose.yml`](docker/ros-systems/abb_fabtory/docker-compose.yml) via 
    * right-click on the file `Compose-up` or 
    * type `docker-compose up -d` in the Terminal (cd to folder) to start it.
    * when ending, don't forget to stop the image via `docker-compose down -d`
  * __Building Docker images locally__: If you do this the first time, or no remote image is available, you can build the local [Dockerfile](docker\docker-images\Dockerfile) via 
    * right-click and `Build` (in the input section tag your Docker image as: augmentedfabricationlab/ros-abb-planner-fabtory:latest) or 
    * in the Terminal (cd to folder) via <br/> `docker build --rm -f Dockerfile -t augmentedfabricationlab/ros-abb-planner-fabtory .` 
    * (Building without cache: <br/> `docker build --no-cache --rm -f Dockerfile -t augmentedfabricationlab/ros-abb-planner-fabtory .`)
* For access to the __web UI of the docker image__, start your browser and go to:<br/>
`http://localhost:8080/vnc.html?resize=scale&autoconnect=true`
* In Rhino, you can now __connect the ROS client to the rosbridge__ and query all moveit related services (compute_ik, trajectory planning, etc.)

#### Docker Setup Information
* Docker user name: augmentedfabricationlab
* The [robotic_setups_description](https://github.com/augmentedfabricationlab/robotic_setups_description.git) repository contains the robot descriptions files for the Dockerfile building.
* The [robotic_setups](https://github.com/augmentedfabricationlab/robotic_setups.git) repository contains the catkin workspace for the urdf models and moveit packages for various robotic setups of our lab, for setting up the systems in Linux as described in [this tutorial](https://gramaziokohler.github.io/compas_fab/latest/examples/03_backends_ros/07_ros_create_urdf_ur5_with_measurement_tool.html).
* The `ros-base`, `ros-abb-planner`, `novnc` and further images are remote images and drawn from the [gramaziokohler docker hub organization](https://hub.docker.com/u/gramaziokohler).

#### Moveit on Linux Notes

    
* __Moveit setups on Linux/WSL__: New urdf descriptions for various robot setups of our lab should be created in the [robotic_setups](https://github.com/augmentedfabricationlab/robotic_setups.git) repository (which is a catkin workspace). 
When on Linux/WSL, the repo can be cloned within the home folder via:

    `git clone https://github.com/augmentedfabricationlab/robotic_setups.git`
    
or new urdf descriptions pulled into the existing folder via
    
    git pull origin master

into this repo. After pulling, run
    
    catkin_make
    source devel/setup.bash
 
 then you can configure a new moveit package via
 
    roslaunch moveit_setup_assistant setup_assistant.launch
    
 Careful: Moveit collision matrix for ABB sometimes lacks closeness of link 4 and 6, therefore these lines can be added manually to the srdf file:
 
     <disable_collisions link1="robotA_link_4" link2="robotA_link_6" reason="User"/>
     <disable_collisions link1="robotB_link_4" link2="robotB_link_6" reason="User"/>
 
 Then run again `catkin_make` and `source devel/setup.bash` and run your moveit demo pacakge via:
 
    roslaunch your_package_name_moveit_config  demo.launch rviz_tutorial:=true
    
 Then push the new moveit config files via:
 
    git add --all
    git commit -a
    git push origin master
    
 to the remote repository.
 
 * __Moveit setups for Docker images__: The newly created moveit_config setups should be copied from the [robotic_setups](https://github.com/augmentedfabricationlab/robotic_setups.git) to the [robotic_setups_description](https://github.com/augmentedfabricationlab/robotic_setups_description.git) repository and pushed to the master. This repo is the one from which the Dockerfile will pull, when building a new image. For planning and control of ABB robots, we additionally use the remote images `ros-abb-planner` as a base drawn from the [gramaziokohler docker hub organization](https://hub.docker.com/u/gramaziokohler).

 * __rosbridge between two machines__: When ROS should be connected between two machines via Ethernet (and not via localhost), 
the ROS MASTER and IPP should be changed via: 

    `nano ~/.bashrc`

 and set accordingly:

    export ROS_MASTER_URI=http://10.10.0.1:11311
    export ROS_IP=10.10.0.1

#### Docker Troubleshooting

Sometimes things don't go as expected. Here are some of answers to the most common issues you might bump into:

> Q: Docker does not start. It complains virtualization not enabled in BIOS.

This is vendor specific, depending on the manufacturer of your computer, there are different ways to fix this, but usually, pressing a key (usually `F2` for Lenovo) before Windows even start will take you to the BIOS of your machine. In there, you will find a `Virtualization` tab where this feature can be enabled.

> Q: Cannot start containers, nor do anything with Docker. Error message indicates docker daemon not accessible or no response.

Make sure docker is running. Especially after a fresh install, docker does not start immediately. Go to the start menu, and start `Docker for Windows`.


