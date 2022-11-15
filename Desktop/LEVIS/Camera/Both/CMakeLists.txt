cmake_minimum_required(VERSION 3.0)
project(ThreadBoth)

set(CMAKE_CXX_STANDARD_17)
find_package (OpenCV REQUIRED)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(ThreadBoth ThreadBoth.cpp)
target_link_libraries(ThreadBoth ${OpenCV_LIBS})