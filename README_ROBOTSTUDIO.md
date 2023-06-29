# ABB Fabtory RobotStudio Instructions

## Installation

* Download the newest [RobotStudio Version](https://new.abb.com/products/robotics/de/robotstudio/downloads) and install it
* Update RobotWare to 6.12.xx via **Add-Ins -> RobotApps -> Filter for RobotWare **IRC5** -> Choose the version in the drop-down menu to the right**

## Activation / License Server 

### RobotStudio Demo Version
* To access full licence to RobotStudio you need a TUM account, but the RobotStudio simulation will also work with the Demo version.

### Robot Studio TUM Version

#### OpenVPN Client

* Download the [VPN Client](data/openVPN) 
* Connect with the following credentials (Username: df, password: CRaBp!p$IwA9IuO%)
* If you encounter an installation error, copy and paste the configuration file manually:  C:\Users\AFAB\OpenVPN\config

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

This readme was created by [Julia Fleckenstein](julia.fleckenstein@tum.de) [@JuliaFleckenstein](https://github.com/JuliaFleckenstein) at [@augmentedfabricationlab](https://github.com/augmentedfabricationlab)
