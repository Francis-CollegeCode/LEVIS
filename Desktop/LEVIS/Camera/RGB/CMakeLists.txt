cmake_minimum_required(VERSION 3.0)
project(test)

set(CMAKE_CXX_STANDARD_17)
find_package (OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(test RGBCamera.cpp)
target_link_libraries(test ${OpenCV_LIBS})