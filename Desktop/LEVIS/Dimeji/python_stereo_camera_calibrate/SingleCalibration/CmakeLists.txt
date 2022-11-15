cmake_minimum_required(VERSION 3.0)
project( Single_Camera_Calibration )
find_package( OpenCV REQUIRED )
add_executable( CalibrateCamera Single_Camera_Calibration.cpp )
target_link_libraries( CalibrateCamera ${OpenCV_LIBS} )

