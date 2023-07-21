#include "joint_trajectory_controller/trajectory.hpp"
#include "trajectory_msgs/msg/joint_trajectory.hpp"
#include "trajectory_msgs/msg/joint_trajectory_point.hpp"
#include "joint_trajectory_controller/interpolation_methods.hpp"

using TrajectoryPointIter = std::vector<trajectory_msgs::msg::JointTrajectoryPoint>::iterator;
using TrajectoryPointConstIter =
  std::vector<trajectory_msgs::msg::JointTrajectoryPoint>::const_iterator;

class SampleTrajectory {
public:
  SampleTrajectory(double pos = 0.0, double vel = 0.0, double acc = 0.0, int interpolation_method = 0) {    

    trajectory_msgs::msg::JointTrajectoryPoint state_desired_;
    state_desired_.positions.resize(1, pos);
    state_desired_.velocities.resize(1, vel);
    state_desired_.accelerations.resize(1, acc);
    traj_.set_point_before_trajectory_msg(rclcpp::Time(0), state_desired_);
    std::cout << "Initial point " << std::endl;
    std::cout << "Position: " << state_desired_.positions.at(0) << std::endl;
    std::cout << "Velocity: " << state_desired_.velocities.at(0) << std::endl;
    std::cout << "Accleration: " << state_desired_.accelerations.at(0) << std::endl;

    std::cout << "Interpolation method: ";
    switch (interpolation_method)
    {
      case 1:
        interpolation_method_ = joint_trajectory_controller::interpolation_methods::InterpolationMethod::VARIABLE_DEGREE_SPLINE;
        std::cout << "Spline" << std::endl;
        break;
      default:
        interpolation_method_ = joint_trajectory_controller::interpolation_methods::InterpolationMethod::NONE;
        std::cout << "None" << std::endl;
    }
  }

  void add_trajectory(double dt, std::vector<double> positions, std::vector<double> velocities, std::vector<double> accelerations) {
    const auto delay = std::chrono::milliseconds(static_cast<int>(dt*1000));
    duration_total_ = rclcpp::Duration(0,0);

    has_position_ = positions.size() > 0;
    has_velocity_ = velocities.size() > 0;
    has_acceleration_ = accelerations.size() > 0;

    std::cout << std::endl << "Load trajectory " << std::endl;
    if ( (!has_position_ && !has_velocity_ && !has_acceleration_)
      || (has_position_ && !has_velocity_ && has_acceleration_)
      || (has_position_ && has_velocity_ && positions.size() != velocities.size())
      || (has_acceleration_ && has_velocity_ && velocities.size() != accelerations.size())
      )
    {
      std::cerr << "Invalid inputs" << std::endl;
      return;
    }

    trajectory_msgs::msg::JointTrajectory msg;
    trajectory_msgs::msg::JointTrajectoryPoint point;
    size_t num_points;
    if (has_position_) {
      num_points = positions.size();
      point.positions.resize(1);
    }
    if (has_velocity_) {
      num_points = velocities.size();
      point.velocities.resize(1);
    }
    if (has_acceleration_) {
      num_points = accelerations.size();
      point.accelerations.resize(1);
    }
    for (size_t i = 0; i < num_points; i++)
    {
      duration_total_ += rclcpp::Duration(delay);
      point.time_from_start = duration_total_;
      if (has_position_) {
        point.positions.at(0) = positions.at(i);
      }
      if (has_velocity_) {
        point.velocities.at(0) = velocities.at(i);
      }
      if (has_acceleration_) {
        point.accelerations.at(0) = accelerations.at(i);
      }
      msg.points.push_back(point);
    }  
    
    std::cout << "loaded # points: " << num_points << std::endl;
    traj_.update(std::make_shared<trajectory_msgs::msg::JointTrajectory>(msg));
  }

  void sample(double interval_s) 
  {
    std::cout << std::endl << "Start sampling" << std::endl;

    TrajectoryPointConstIter start_segment_itr, end_segment_itr;

    trajectory_msgs::msg::JointTrajectoryPoint state_sampled;
    state_sampled.positions.resize(1, 0.0);
    state_sampled.velocities.resize(1, 0.0);
    state_sampled.accelerations.resize(1, 0.0);

    rclcpp::Time time;
    for (int i = 0; i < 1 + duration_total_.seconds()/interval_s; i++){
      time = rclcpp::Time(i*interval_s*1e9);

      const bool valid_point =
        traj_.sample(time, interpolation_method_, state_sampled, start_segment_itr, end_segment_itr);

      std::cout << "time: " << time.seconds() << std::endl;
      time_sampled_.push_back(time.seconds());
      std::cout << "valid_point: " << valid_point << std::endl;
      if (has_position_ || has_velocity_ || has_acceleration_) {
        std::cout << "Position: " << state_sampled.positions.at(0) << std::endl;
        positions_sampled_.push_back(state_sampled.positions.at(0));
      }
      if (has_velocity_ || (has_acceleration_ && !has_position_)) {
        std::cout << "Velocity: " << state_sampled.velocities.at(0) << std::endl;
        velocities_sampled_.push_back(state_sampled.velocities.at(0));
      }
      if (has_acceleration_) {
        std::cout << "Acceleration: " << state_sampled.accelerations.at(0) << std::endl;
        accelerations_sampled_.push_back(state_sampled.accelerations.at(0));
      }
      std::cout << std::endl;
    }
  }
  std::vector<double> positions_sampled_, velocities_sampled_, accelerations_sampled_, time_sampled_;

private:
  joint_trajectory_controller::interpolation_methods::InterpolationMethod interpolation_method_{
    joint_trajectory_controller::interpolation_methods::DEFAULT_INTERPOLATION};
  joint_trajectory_controller::Trajectory traj_;
  rclcpp::Duration duration_total_ = rclcpp::Duration(0,0);
  bool has_position_ = false;
  bool has_velocity_ = false;
  bool has_acceleration_ = false;
};