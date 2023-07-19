#include "joint_trajectory_controller/trajectory.hpp"
#include "trajectory_msgs/msg/joint_trajectory.hpp"
#include "trajectory_msgs/msg/joint_trajectory_point.hpp"
#include "joint_trajectory_controller/interpolation_methods.hpp"

using TrajectoryPointIter = std::vector<trajectory_msgs::msg::JointTrajectoryPoint>::iterator;
using TrajectoryPointConstIter =
  std::vector<trajectory_msgs::msg::JointTrajectoryPoint>::const_iterator;

int main(int argc, char ** argv)
{
  (void) argc;
  (void) argv;  

  joint_trajectory_controller::interpolation_methods::InterpolationMethod interpolation_method_{
    joint_trajectory_controller::interpolation_methods::InterpolationMethod::VARIABLE_DEGREE_SPLINE};
  TrajectoryPointConstIter start_segment_itr, end_segment_itr;
  joint_trajectory_controller::Trajectory traj_;
  trajectory_msgs::msg::JointTrajectoryPoint state_sampled_;
  state_sampled_.positions.resize(1, 0.0);
  state_sampled_.velocities.resize(1, 0.0);
  state_sampled_.accelerations.resize(1, 0.0);

  // set initial point
  trajectory_msgs::msg::JointTrajectoryPoint state_desired_;
  state_desired_.positions.resize(1, 0.0);
  state_desired_.velocities.resize(1, 0.0);
  state_desired_.accelerations.resize(1, 0.0);
  traj_.set_point_before_trajectory_msg(rclcpp::Time(0), state_desired_);
  std::cout << "Initial point " << std::endl;
  std::cout << "Position: " << state_desired_.positions.at(0) << std::endl;
  std::cout << "Velocity: " << state_desired_.velocities.at(0) << std::endl;
  std::cout << "Accleration: " << state_desired_.accelerations.at(0) << std::endl;

  // set path
  trajectory_msgs::msg::JointTrajectory msg;
  trajectory_msgs::msg::JointTrajectoryPoint point;
  double dt = 0.5;
  point.positions.resize(1);
  point.velocities.resize(1);
  point.accelerations.resize(1);
  const auto delay = std::chrono::milliseconds(500);
  rclcpp::Duration duration_total{rclcpp::Duration(delay)};

  point.time_from_start = duration_total;
  point.accelerations.at(0) = 1.0;
  msg.points.push_back(point);
  duration_total += rclcpp::Duration(delay);

  point.time_from_start = duration_total;
  point.accelerations.at(0) = 0.5;
  msg.points.push_back(point);
  duration_total += rclcpp::Duration(delay);

  point.time_from_start = duration_total;
  point.accelerations.at(0) = -1.0;
  msg.points.push_back(point);
  duration_total += rclcpp::Duration(delay);

  point.time_from_start = duration_total;
  point.accelerations.at(0) = -0.5;
  msg.points.push_back(point);
  duration_total += rclcpp::Duration(delay);

  point.time_from_start = duration_total;
  point.accelerations.at(0) = 0.;
  msg.points.push_back(point);
  duration_total += rclcpp::Duration(delay);

  std::cout << std::endl << "Trajectory " << std::endl;
  size_t i = 0;
  msg.points.at(i).velocities.at(0) = state_desired_.velocities.at(0) + msg.points.at(i).accelerations.at(0) * dt;
  msg.points.at(i).positions.at(0) = state_desired_.positions.at(0) + msg.points.at(i).velocities.at(0) * dt;
  std::cout << "time: " << msg.points.at(i).time_from_start.sec + static_cast<double>(msg.points.at(i).time_from_start.nanosec)/1.e9 << std::endl;
  std::cout << "Position: " << msg.points.at(i).positions.at(0) << std::endl;
  std::cout << "Velocity: " << msg.points.at(i).velocities.at(0) << std::endl;
  std::cout << "Accleration: " << msg.points.at(i).accelerations.at(0) << std::endl;
  for (size_t i = 1; i < msg.points.size(); i++) {
    msg.points.at(i).velocities.at(0) = msg.points.at(i-1).velocities.at(0) + msg.points.at(i).accelerations.at(0) * dt;
    msg.points.at(i).positions.at(0) = msg.points.at(i-1).positions.at(0) + msg.points.at(i).velocities.at(0) * dt;
    std::cout << "time: " << msg.points.at(i).time_from_start.sec + static_cast<double>(msg.points.at(i).time_from_start.nanosec)/1.e9 << std::endl;
    std::cout << "Position: " << msg.points.at(i).positions.at(0) << std::endl;
    std::cout << "Velocity: " << msg.points.at(i).velocities.at(0) << std::endl;
    std::cout << "Accleration: " << msg.points.at(i).accelerations.at(0) << std::endl;
  }
  traj_.update(std::make_shared<trajectory_msgs::msg::JointTrajectory>(msg));

  std::cout << "# points: " << msg.points.size() << std::endl;


  std::cout << std::endl << "Start sampling" << std::endl;
  double interval_s = 0.1;
  for (int i = 0; i < duration_total.seconds()/interval_s; i++){
    rclcpp::Time time = rclcpp::Time(i*interval_s*1e9);

    const bool valid_point =
      traj_.sample(time, interpolation_method_, state_sampled_, start_segment_itr, end_segment_itr);

    std::cout << "time: " << time.seconds() << std::endl;
    std::cout << "valid_point: " << valid_point << std::endl;
    std::cout << "Position: " << state_sampled_.positions.at(0) << std::endl;
    std::cout << "Velocity: " << state_sampled_.velocities.at(0) << std::endl;
    std::cout << "Accleration: " << state_sampled_.accelerations.at(0) << std::endl;
    std::cout << std::endl;
  }

  return 0;
}
