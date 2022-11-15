cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 14)

PROJECT(cameracalib)

find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS})

MACRO(cameracalib)
  ADD_EXECUTABLE(cameracalib main.c)
  TARGET_LINK_LIBRARIES($cameracalib ${OpenCV_LIBS})
ENDMACRO()