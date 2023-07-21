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

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "test_jtc_trajectories/sample_trajectory.hpp"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;

PYBIND11_MODULE(TestJtc, m)
{
  m.doc() = "optional module docstring";

  py::class_<SampleTrajectory>(m, "SampleTrajectory")
    .def(py::init<double, double, double, int>())
    .def(
      "add_trajectory", &SampleTrajectory::add_trajectory, py::call_guard<py::gil_scoped_release>())
    .def("sample", &SampleTrajectory::sample, py::call_guard<py::gil_scoped_release>())
    .def_readonly("time_sampled", &SampleTrajectory::time_sampled_, byref)
    .def_readonly("positions_sampled", &SampleTrajectory::positions_sampled_, byref)
    .def_readonly("accelerations_sampled", &SampleTrajectory::accelerations_sampled_, byref)
    .def_readonly("velocities_sampled", &SampleTrajectory::velocities_sampled_, byref);
}
