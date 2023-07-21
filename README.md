# test_jtc_trajectories

Wrapper class for `joint_trajectory_controller::Trajectory` class, which is exported as Python module using pybind11.

## install and run
* has to be inside src/ folder of a ROS 2 workspace.
* Build with colcon
* source your ROS2 workspace
* Run from any folder with `python3 <path/to>/test_jtc_trajectories/plot_trajectory.py`

## resources
I followed the tutorial from https://www.matecdev.com/posts/cpp-call-from-python.html

One could also use the ROS data structures inside python, e.g. with
https://gist.github.com/kervel/75d81b8c34e45a19706c661b90d02548.
But as it is now, the python script does not need any other ROS dependencies.
