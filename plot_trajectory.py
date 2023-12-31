# Copyright 2023 Austrian Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(
    os.path.join(
        os.path.dirname(__file__), "../../install/test_jtc_trajectories/lib/test_jtc_trajectories/"
    )
)
from TestJtc import SampleTrajectory  # noqa: E402

show_figure = False

dt_sample = 0.01

style_init = "mo"
style_points = "xg"
style_none = "#e74c3c"
style_spline = "#2980b9"

if True:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)
    trajectory_sampler = SampleTrajectory(pos0, vel0, acc0, 0)

    positions = [0.0625, 0.28125, 0.5625, 0.71875, 0.75]
    velocities = []
    accelerations = []
    dt = 0.5
    time = np.arange(dt, dt * (len(positions) + 1), dt)

    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler.sample(dt_sample)
    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(2, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.plot(time, positions, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.positions_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.subplot(2, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.xlabel("time / s")
    plt.grid()
    plt.tight_layout()
    plt.savefig("spline_position.png")
    if show_figure:
        plt.show()

    # ---------------------
if True:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)

    velocities = [0.25, 0.625, 0.5, 0.125, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(velocities) + 1), dt)

    positions = []
    accelerations = []

    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()

    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.tight_layout()
    plt.savefig("spline_velocity.png")
    if show_figure:
        plt.show()

    print(time)
    print(positions)
    print(velocities)
    print(accelerations)

    # ---------------------
if True:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)
    trajectory_sampler = SampleTrajectory(pos0, vel0, acc0, 0)

    velocities = [0.25, 0.625, 0.5, 0.125, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(velocities) + 1), dt)

    # Heun's method (this is the integration strategy from trajectory class)
    positions = [pos0 + (vel0 + velocities[0]) * 0.5 * dt]
    for i in range(len(velocities) - 1):
        positions.append(positions[i] + (velocities[i] + velocities[i + 1]) * 0.5 * dt)
    print(positions)
    accelerations = []

    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)
    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.plot(time, positions, style_points, label="Trajectory points")
    plt.plot(
        trajectory_sampler.time_sampled,
        trajectory_sampler.positions_sampled,
        style_none,
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.plot(
        trajectory_sampler.time_sampled,
        trajectory_sampler.velocities_sampled,
        style_none,
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.xlabel("time / s")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()

    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.tight_layout()

    plt.savefig("spline_position_velocity.png")
    if show_figure:
        plt.show()

    print(time)
    print(positions)
    print(velocities)
    print(accelerations)

    # ---------------------
if True:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)
    trajectory_sampler = SampleTrajectory(pos0, vel0, acc0, 0)

    positions = [1.0, 0.5, -1.0, -0.5, 0.0]
    velocities = [1.0, 0.5, -1.0, -0.5, 0.0]
    accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(accelerations) + 1), dt)

    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler.sample(dt_sample)
    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.plot(time, positions, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.positions_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.velocities_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.plot(time, accelerations, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.accelerations_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()
    plt.savefig("spline_wrong_points.png")
    if show_figure:
        plt.show()

# ---------------------
if True:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)

    accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(accelerations) + 1), dt)

    velocities = []
    positions = []

    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.plot(time, accelerations, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()
    plt.savefig("spline_acceleration.png")
    if show_figure:
        plt.show()

    print(positions)
    print(velocities)
    print(accelerations)

    # ---------------------
if False:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)

    accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(accelerations) + 1), dt)

    # Heun's method (this is the integration strategy from trajectory class)
    velocities = [vel0 + (acc0 + accelerations[0]) * 0.5 * dt]
    for i in range(len(accelerations) - 1):
        velocities.append(velocities[i] + (accelerations[i] + accelerations[i + 1]) * 0.5 * dt)
    print(velocities)
    positions = []

    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)

    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    # plt.plot(trajectory_sampler.time_sampled, trajectory_sampler.positions_sampled, label='Sampled points')
    plt.ylabel("position")
    plt.legend()
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    # plt.plot(trajectory_sampler.time_sampled, trajectory_sampler.velocities_sampled, label='Sampled points')
    plt.ylabel("velocity")
    plt.legend()
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.plot(time, accelerations, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    # plt.plot(trajectory_sampler.time_sampled, trajectory_sampler.accelerations_sampled, label='Sampled points')
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.legend()
    plt.grid()
    if show_figure:
        plt.show()

    print(time)
    print(positions)
    print(velocities)
    print(accelerations)

    # ---------------------
    # position+velocity+acceleration

if True:
    pos0 = 0.0
    vel0 = 0.0
    acc0 = 0.0
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)
    trajectory_sampler = SampleTrajectory(pos0, vel0, acc0, 0)

    accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(accelerations) + 1), dt)

    # Heun's method (this is the integration strategy from trajectory class)
    velocities = [vel0 + (acc0 + accelerations[0]) * 0.5 * dt]
    positions = [pos0 + (vel0 + velocities[0]) * 0.5 * dt]
    for i in range(len(accelerations) - 1):
        velocities.append(velocities[i] + (accelerations[i] + accelerations[i + 1]) * 0.5 * dt)
    print(velocities)
    for i in range(len(velocities) - 1):
        positions.append(positions[i] + (velocities[i] + velocities[i + 1]) * 0.5 * dt)
    print(positions)

    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)
    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.plot(time, positions, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.positions_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.velocities_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.plot(time, accelerations, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.accelerations_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()
    plt.savefig("spline_position_velocity_acceleration.png")
    if show_figure:
        plt.show()

    print(time)
    print(positions)
    print(velocities)
    print(accelerations)

    # ---------------------
    # position+velocity+acceleration with nonzero start

if True:
    pos0 = -0.1
    vel0 = -0.1
    acc0 = -0.1
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)
    trajectory_sampler = SampleTrajectory(pos0, vel0, acc0, 0)

    accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]
    dt = 0.5
    time = np.arange(dt, dt * (len(accelerations) + 1), dt)

    # Heun's method (this is the integration strategy from trajectory class)
    pos0_traj = 0.0
    vel0_traj = 0.0
    acc0_traj = 0.0
    velocities = [vel0_traj + (acc0_traj + accelerations[0]) * 0.5 * dt]
    positions = [pos0_traj + (vel0_traj + velocities[0]) * 0.5 * dt]
    for i in range(len(accelerations) - 1):
        velocities.append(velocities[i] + (accelerations[i] + accelerations[i + 1]) * 0.5 * dt)
    print(velocities)
    for i in range(len(velocities) - 1):
        positions.append(positions[i] + (velocities[i] + velocities[i + 1]) * 0.5 * dt)
    print(positions)

    trajectory_sampler_spline.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)
    trajectory_sampler.add_trajectory(dt, dt, positions, velocities, accelerations)
    trajectory_sampler.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.plot(time, positions, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.positions_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.velocities_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.plot(time, accelerations, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.accelerations_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()
    plt.savefig("spline_position_velocity_acceleration_initialpoint.png")
    if show_figure:
        plt.show()

    print(time)
    print(positions)
    print(velocities)
    print(accelerations)

    # ---------------------
    # position+velocity+acceleration with nonzero start, no time

if True:
    pos0 = -0.1
    vel0 = -0.1
    acc0 = -0.1
    trajectory_sampler_spline = SampleTrajectory(pos0, vel0, acc0, 1)
    trajectory_sampler = SampleTrajectory(pos0, vel0, acc0, 0)

    accelerations = [1.0, 0.5, -1.0, -0.5, 0.0]
    dt = 0.5
    time = np.arange(0.0, dt * (len(accelerations)), dt)

    # Heun's method (this is the integration strategy from trajectory class)
    pos0_traj = 0.0
    vel0_traj = 0.0
    acc0_traj = 0.0
    velocities = [vel0_traj + (acc0_traj + accelerations[0]) * 0.5 * dt]
    positions = [pos0_traj + (vel0_traj + velocities[0]) * 0.5 * dt]
    for i in range(len(accelerations) - 1):
        velocities.append(velocities[i] + (accelerations[i] + accelerations[i + 1]) * 0.5 * dt)
    print(velocities)
    for i in range(len(velocities) - 1):
        positions.append(positions[i] + (velocities[i] + velocities[i + 1]) * 0.5 * dt)
    print(positions)

    trajectory_sampler_spline.add_trajectory(dt, 0.0, positions, velocities, accelerations)
    trajectory_sampler_spline.sample(dt_sample)
    trajectory_sampler.add_trajectory(dt, 0.0, positions, velocities, accelerations)
    trajectory_sampler.sample(dt_sample)

    plt.figure().set_figwidth(7.0)  # default 100dpi -> 700px
    plt.subplot(3, 1, 1)
    plt.plot(0.0, pos0, style_init, label="Initial point")
    plt.plot(time, positions, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.positions_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.positions_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("position")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(0.0, vel0, style_init, label="Initial point")
    plt.plot(time, velocities, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.velocities_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.velocities_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.ylabel("velocity")
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(0.0, acc0, style_init, label="Initial point")
    plt.plot(time, accelerations, style_points, label="Trajectory points")
    plt.step(
        trajectory_sampler.time_sampled,
        trajectory_sampler.accelerations_sampled,
        style_none,
        where="post",
        label="Sampled points `none`",
    )
    plt.step(
        trajectory_sampler_spline.time_sampled,
        trajectory_sampler_spline.accelerations_sampled,
        where="post",
        label="Sampled points `spline`",
    )
    plt.xlabel("time / s")
    plt.ylabel("acceleration")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()
    plt.savefig("spline_position_velocity_acceleration_initialpoint_notime.png")
    if show_figure:
        plt.show()

    print(time)
    print(positions)
    print(velocities)
    print(accelerations)
