#### Docker Setup Information

* Docker user name: augmentedfabricationlab
* The [robotic_setups_description](https://github.com/augmentedfabricationlab/robotic_setups_description.git) repository contains the robot descriptions files for the Dockerfile building.
* The [robotic_setups](https://github.com/augmentedfabricationlab/robotic_setups.git) repository contains the catkin workspace for the urdf models and moveit packages for various robotic setups of our lab, for setting up the systems in Linux as described in [this tutorial](https://gramaziokohler.github.io/compas_fab/latest/examples/03_backends_ros/07_ros_create_urdf_ur5_with_measurement_tool.html).
* The `ros-base`, `ros-abb-planner`, `novnc` and further images are remote images and drawn from the [gramaziokohler docker hub organization](https://hub.docker.com/u/gramaziokohler).
* __Building Docker images locally__: If you do this the first time, or no remote image is available, you can build the local [Dockerfile](docker\docker-images\Dockerfile) via 
    * right-click and `Build` (in the input section tag your Docker image as: augmentedfabricationlab/ros-abb-planner-fabtory:latest) or 
    * in the Terminal (cd to folder) via <br/> `docker build --rm -f Dockerfile -t augmentedfabricationlab/ros-abb-planner-fabtory .` 
    * (Building without cache: <br/> `docker build --no-cache --rm -f Dockerfile -t augmentedfabricationlab/ros-abb-planner-fabtory .`)

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