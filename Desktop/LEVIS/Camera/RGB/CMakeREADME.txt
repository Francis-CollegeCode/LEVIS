****Tutorial for Understanding CMake

CMake uses two dependencies within the project file:
* Source
* 

------------
1) Place the program that you want to run in an arbitrary dir
2) Make a CMakeLists.txt file inside that dir 

the CmakeLists.txt file will look like: 

cmake_minimum_required(VERSION 3.0)
project(test)

set(CMAKE_CXX_STANDARD_17)
find_package (OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(test filename.cpp)
target_link_libraries(test ${OpenCV_LIBS})

3) Make a build folder inside that dir
4) Go to the command line and go inside the build folder dir
5) In the cmd type "CMake .."
6) Then type "make"
7) Run the file you make by typing in the cmd "./test" (test will replace whatever you called the exe)