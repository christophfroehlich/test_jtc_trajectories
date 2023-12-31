// Copyright 2023 Austrian Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "test_jtc_trajectories/sample_trajectory.hpp"

using TrajectoryPointIter = std::vector<trajectory_msgs::msg::JointTrajectoryPoint>::iterator;
using TrajectoryPointConstIter =
  std::vector<trajectory_msgs::msg::JointTrajectoryPoint>::const_iterator;

int main(int argc, char ** argv)
{
  (void)argc;
  (void)argv;

  // set initial point
  double pos = 0.0;
  double vel = 0.0;
  double acc = 0.0;

  // #################
  {
    double dt = 0.5;
    SampleTrajectory trajectory_sampler(pos, vel, acc, 0);

    std::cout << std::endl << "Create Trajectory " << std::endl;
    std::vector<double> positions;
    positions.resize(5);
    std::vector<double> velocities;
    velocities.resize(5);
    std::vector<double> accelerations = {1.0, 0.5, -1.0, -0.5, 0.0};
    size_t i = 0;
    velocities.at(i) = vel + accelerations.at(i) * dt;
    positions.at(i) = pos + velocities.at(i) * dt;
    std::cout << "time: " << dt * (i + 1) << std::endl;
    std::cout << "Position: " << positions.at(i) << std::endl;
    std::cout << "Velocity: " << velocities.at(i) << std::endl;
    std::cout << "Acceleration: " << accelerations.at(i) << std::endl;
    for (size_t i = 1; i < accelerations.size(); i++)
    {
      velocities.at(i) = velocities.at(i - 1) + accelerations.at(i) * dt;
      positions.at(i) = positions.at(i - 1) + velocities.at(i) * dt;
      std::cout << "time: " << dt * (i + 1) << std::endl;
      std::cout << "Position: " << positions.at(i) << std::endl;
      std::cout << "Velocity: " << velocities.at(i) << std::endl;
      std::cout << "Acceleration: " << accelerations.at(i) << std::endl;
    }

    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations);
    trajectory_sampler.sample(0.1);
  }

  // #################
  {
    double dt = 0.5;
    SampleTrajectory trajectory_sampler(pos, vel, acc, 0);

    std::cout << std::endl << "Create Trajectory " << std::endl;
    std::vector<double> positions;
    positions.resize(5);
    std::vector<double> velocities = {1.0, 0.5, -1.0, -0.5, 0.0};
    std::vector<double> accelerations;
    size_t i = 0;
    positions.at(i) = pos + velocities.at(i) * dt;
    std::cout << "time: " << dt * (i + 1) << std::endl;
    std::cout << "Position: " << positions.at(i) << std::endl;
    std::cout << "Velocity: " << velocities.at(i) << std::endl;
    for (size_t i = 1; i < velocities.size(); i++)
    {
      positions.at(i) = positions.at(i - 1) + velocities.at(i) * dt;
      std::cout << "time: " << dt * (i + 1) << std::endl;
      std::cout << "Position: " << positions.at(i) << std::endl;
      std::cout << "Velocity: " << velocities.at(i) << std::endl;
    }

    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations);
    trajectory_sampler.sample(0.1);
  }

  // #################
  {
    double dt = 0.5;
    SampleTrajectory trajectory_sampler(pos, vel, acc, 0);

    std::cout << std::endl << "Create Trajectory " << std::endl;
    std::vector<double> positions = {1.0, 0.5, -1.0, -0.5, 0.0};
    std::vector<double> velocities;
    std::vector<double> accelerations;

    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations);
    trajectory_sampler.sample(0.1);
  }

  return 0;
}
