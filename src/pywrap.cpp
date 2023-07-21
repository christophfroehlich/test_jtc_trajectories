// pywrap.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "test_jtc_trajectories/sample_trajectory.hpp"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;

PYBIND11_MODULE(TestJtc, m) {
    m.doc() = "optional module docstring";

    py::class_<SampleTrajectory>(m, "SampleTrajectory")
    .def(py::init<double, double, double, int>())  
    .def("add_trajectory", &SampleTrajectory::add_trajectory, py::call_guard<py::gil_scoped_release>())
    .def("sample", &SampleTrajectory::sample, py::call_guard<py::gil_scoped_release>())
    .def_readonly("time_sampled", &SampleTrajectory::time_sampled_, byref)
    .def_readonly("positions_sampled", &SampleTrajectory::positions_sampled_, byref)
    .def_readonly("accelerations_sampled", &SampleTrajectory::accelerations_sampled_, byref)
    .def_readonly("velocities_sampled", &SampleTrajectory::velocities_sampled_, byref)
    ;
}