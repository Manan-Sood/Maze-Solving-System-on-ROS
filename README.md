# Maze-Solving-System-on-ROS
 A maze solving system on ROS that can be used in a micro-mouse competition.

## Folders

### maps

This folder contains the maps for testing the algorithm.

Each map file has the following format -

```bash
map_width map_height
start_coord_x start_coord_y end_coord_x end_coord_y
< array representing map walls >
```

### msg

This folder contains the custom msgs which are to be used for communication among the ROS nodes provided.

### scripts

This folder contains the various scripts in which the ROS nodes are running.

 - ##### MapClass.py

    This file contains the data structure used for the map of the maze.

    The map is represented as an array of integers. Each integer is a number from 0-15 and represents the walls adjacent to that cell in Top-Left-Right-Bottom convention with values as 8-4-2-1

    Basically a square with say top and bottom walls only will have value = 8(top) + 1(bottom) = 9

- ##### MapNode.py

   This file initializes the ROS node and provides a graphic interface using the map.

   The script starts a ROS Node named map-node which has one publisher and one subscriber.

   The subscriber subscribes to the /direction topic and on receiving the direction of movement, it moves the robot in that direction. Right after the movement is done, the publisher is called to inform the bot of the walls of the new cell.

   The publisher publishes to the /walls topic and publishes data about the walls on the current position of the robot. This is done to emulate the real world maze, where the robot can only see the walls of the position it is on currently.

- ##### PlannerNode.py

  A path-planning algorithm has been implemented which will decide the direction of movement of the robot and publish it to the /direction topic, whenever it receives information about the walls of the current cell from the /walls topic.

  Some points -

  - It is guaranteed that the bottom direction will be the first step the robot has to take.
  - We cannot access the map directly. Only the data from the /walls topic is accessible to us and the algorithm is based on that.
  
