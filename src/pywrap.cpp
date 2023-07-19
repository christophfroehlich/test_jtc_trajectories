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
    // .def_readonly("v_data", &MyClass::v_data, byref)
    // .def_readonly("v_gamma", &MyClass::v_gamma, byref)
    ;
}