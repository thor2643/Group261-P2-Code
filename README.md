# P2-Project code for Group 261
<a href="#sec_contributors"><img src="https://img.shields.io/badge/Authors-Group_261-blue.svg"></a> ![](https://img.shields.io/badge/C++-11-brightgreen.svg) [![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

This repository contains the codebase for the 2nd semester project by Group 261. The semester focused on robot manipulators and specifically the UR5 for the respective project. 
The ambition of the project was to reduce the environmental footprint of the robot. The idea was to assemble a dummy phone with minimum stops to decrease required accelerations and decelerations, which was found to
cause big energy spikes. Therefore a gripper consisting of four individual grippers for each component of the dummy phone was created. The individual grippers was assembled in a circular shape with equal distance
to the center. This allowed the robot to pick up all the components in a continous rolling motion, which indeed was a very satisfying thing to watch!
Although the effect on the environmental footprint were minimal, the continous flow in the pick showed great potential in regard to throughput. However, this would require some tweaking and improvements to the
current robot trajectory as it currently is only as fast as the "classical" approach. Nevertheless, we urge you to take a look at the video "20 phones assembled 100 % success" in the YouTube playlist found by
following the link [P2-Playlist](https://www.youtube.com/playlist?list=PLvF0YaCHe3KkmQyWYJX_KTgWdvqXj8dY-).

<img src="Images/FrontPage.png" width="640">

## Code overview
The code setup consist primarily of the 4 parts:
1.  **Customer GUI** 
2.  **Operator GUI**
3.  **Central Hub**
4.  **Dispenser Code**

The central hub functions as the link between the robot, the dispensers, the customer GUI and the operator GUI. It takes orders from the customer GUI through a TCP connection and sends the respective order to the arduino controlling
the dispensers over a serial connection. When receiving an acknowledgement from the arduino the central hub starts an appropriate program on the UR5 also through a TCP connection through RoboDK. Lastly, component
lists are updated, which the operator GUI uses to alert the operator if the cell is running out of components. The GUI's has also been shown in the [P2-Playlist](https://www.youtube.com/playlist?list=PLvF0YaCHe3KkmQyWYJX_KTgWdvqXj8dY-). 

Beside the physical cell, a digital twin of the cell has been set up in RoboDK to allow for offline development and testing ideas before running them on the actual robot cell. Together, with a range of helper scripts
the programs could be generated automatically based on the kinematics learned thorughout the semester. 
<img src="Images/Robot cell in RoboDK.png" width="640">

## Contributors
This project was developed by group 261 on Aalborg University, Robot Technology at 2nd semester.

<section id="sec_contributors">
<table>
  <tr> 
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/signeskuldbol"><img src="https://avatars.githubusercontent.com/u/117270262?v=4" width="100px;" alt=""/><br/><sub><b>Signe Møller-Skuldbøl</b></sub></a></br><a href="gttps://github.com/signeskuldbol" title="">👧</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/thor2643"><img src="https://avatars.githubusercontent.com/u/66319719?v=4" width="100px;" alt=""/><br/><sub><b>Thor Iversen</b></sub></a></br><a href="gttps://github.com/thor2643" title="">👨‍🌾</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/silasjensen2001"><img src="https://avatars.githubusercontent.com/u/54105795?v=4" width="100px;" alt=""/><br/><sub><b>Silas Jensen</b></sub></a></br><a href="gttps://github.com/silasjensen2001" title="">🤠</a></td>
  <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/Magnusdar"><img src="https://avatars.githubusercontent.com/u/74591165?v=4" width="100px;" alt=""/><br/><sub><b>Magnus Darø</b></sub></a></br><a href="gttps://github.com/Magnusdar" title="">🐻</a></td>
  <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/TheRobotSkier"><img src="https://avatars.githubusercontent.com/u/121627019?v=4" width="100px;" alt=""/><br/><sub><b>Emil Hausberger</b></sub></a></br><a href="gttps://github.com/TheRobotSkier" title="">😎</a></td>
  <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/bordlampe123"><img src="https://avatars.githubusercontent.com/u/104758251?v=4" width="100px;" alt=""/><br/><sub><b>Benjamin Jørgensen</b></sub></a></br><a href="gttps://github.com/bordlampe123" title="">😎</a></td>

  </tr>
</table>
