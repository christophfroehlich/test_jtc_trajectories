cmake_minimum_required(VERSION 3.10)
project(test_jtc_trajectories)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
set(CMAKE_CXX_STANDARD 20)
set(PYBIND11_PYTHON_VERSION 3.6)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(joint_trajectory_controller REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

add_executable(sample_trajectory src/sample_trajectory.cpp)
target_include_directories(sample_trajectory PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(sample_trajectory PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  sample_trajectory
  "joint_trajectory_controller"
)

pybind11_add_module(TestJtc src/pywrap.cpp)
target_compile_definitions(TestJtc PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
target_include_directories(TestJtc PRIVATE ${PYBIND11_INCLUDE_DIRS})
target_include_directories(TestJtc PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(
  TestJtc PUBLIC
  "joint_trajectory_controller"
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()


install(TARGETS sample_trajectory
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS TestJtc
  DESTINATION lib/${PROJECT_NAME})

ament_package()
