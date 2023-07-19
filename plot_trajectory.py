import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(__file__),
    "../../install/control_toolbox/lib/"))
sys.path.append(os.path.join(
    os.path.dirname(__file__),
    "../../install/test_jtc_trajectories/lib/test_jtc_trajectories/"))
from TestJtc import SampleTrajectory

trajectory_sampler = SampleTrajectory(0.0, 0.0, 0.0, 0)

positions = [1.0, 0.5, -1.0, -0.5, 0.0]
velocities = []
accelerations = []

trajectory_sampler.add_trajectory(0.5, positions, velocities, accelerations)
trajectory_sampler.sample(0.1)


trajectory_sampler = SampleTrajectory(0.0, 0.0, 0.0, 1)
positions = [1.0, 0.5, -1.0, -0.5, 0.0]
velocities = [1.0, 0.5, -1.0, -0.5, 0.0]
accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]

trajectory_sampler.add_trajectory(0.5, positions, velocities, accelerations)
trajectory_sampler.sample(0.1)