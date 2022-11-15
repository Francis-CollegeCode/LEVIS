cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 14)

PROJECT(cameracalib)

find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS})
ADD_EXECUTABLE(cameracalib main.cpp)
TARGET_LINK_LIBRARIES(cameracalib ${OpenCV_LIBS})