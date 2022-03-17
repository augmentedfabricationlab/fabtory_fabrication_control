# ABB Fabtory RobotStudio Instructions

## Installation

* Download the newest [RobotStudio Version](https://new.abb.com/products/robotics/de/robotstudio/downloads) and install it
* Update RobotWare to 6.12.xx via **Add-Ins -> RobotApps -> Filter for RobotWare **IRC5** -> Choose the version in the drop-down menu to the right**

## Activation / License Server 

### RobotStudio Demo Version
* To access full licence to RobotStudio you need a TUM account, but the RobotStudio simulation will also work with the Demo version.

### Robot Studio TUM Version

#### Sophos VPN Client

* Go to Sophos [VPN Client](https://firewall.ai.ar.tum.de/) and log in with your TUM credentials. 
* Download the installation package and install it
* Start Sophos VPN and log in with your TUM credentials

#### Activation in RobotStudio

* Start RobotStudio
* To get full access go to **File -> Options -> Licensing -> Activation Wizard -> Network Licence to manage your server licence**   
* Enter the licence server key 10.162.157.47 and shut down the program
* Then restart the program
* To check if your License Server is online, go back once more to your Licence Server and check the availability

## Loading Fabtory Station

* Download the RobotStudio [Pack&Go File](https://drive.google.com/drive/folders/1p_he4GqPH-pw7OSO1jV9Rtm2k0KBjeF4?usp=sharing) of the fabtory setup
* In RobotStudio, load the file via **File -> Share -> Unpack&Work**
* Select the Pack&Go File, and store your target file in the your own RobotStudio directory **C:\Users\username\Documents\RobotStudio\Solutions**

Have fun!

## Setting up a new tool for the end effector

### Set up your geometry in RobotStudio

* Start RobotStudio
* Import geometry **Home -> Import Geometry -> Browse for Geometry** and select a solid model
* In the layout window rename your tool: t_xx
* Position your model in world0 with right click on the tool in your layout window **Position -> Place -> OnePoint**, if you need to rotate your geometry use **Rotate** till the geometry is oriented the same as in your grasshopper environment

### Set the tcf

* Create your tcf with **Home -> Frame -> Create Frame** and activate your snap
* Set your frame with right click on the frame in the layout window normal to the tcf surface **-> Set normal to surface and select the surface**

### Create tool

* Create your tool in **Modeling -> Create Tool**. A new window will guide you through.
* Rename your tool: t_xx
* Activate **use existing** and select your tcf as your target frame

### Safe your tool in the library

* Click right on your created tool **-> save as library** 
* Safe your current tool to the fabtory_fabrication_control workspace in **data -> robot_description -> abb_end_effectors**

### Update Robot with the new tool

* Drag your tool on your robot and update the robot position to snap
* In the Path&Target window you find the ToolData with your new tool
* To test your tool, select your robot geometry and select **Jogging**, your tool will now move while jogging
