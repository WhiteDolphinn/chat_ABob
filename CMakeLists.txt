cmake_minimum_required(VERSION 3.2.7 FATAL_ERROR)
project(_gui)


#set(CMAKE_C_COMPILER   /mnt/c/Users/HP/Downloads/CodeBlocks/MinGW/bin/gcc.exe)
#set(CMAKE_CXX_COMPILER /mnt/c/Users/HP/Downloads/CodeBlocks/MinGW/bin/g++.exe)

#set(CMAKE_C_FLAGS -ggdb3)
set(CMAKE_CXX_FLAGS -fPIC)

set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_BUILD_TYPE RelWithDebInfo)

set(CMAKE_C_COMPILER   gcc)
set(CMAKE_CXX_COMPILER g++)

#link_directories(SFML-2.6.1/lib TGUI-1.1/lib)

#include_directories("GUI" "Link")
include_directories( ./Link ./tquic ./tquic/deps/boringssl/src/include/)


set(CMAKE_CXX_STANDARD 17)

#find_package(SFML COMPONENTS graphics audio system REQUIRED)
#find_package(TGUI REQUIRED)

add_library(_gui SHARED main.cpp
user.cpp
                        user.hpp
                        message.hpp
                        gui.cpp
                        gui.hpp
                        )
                        
set_target_properties(_gui PROPERTIES PREFIX "")

target_link_libraries(_gui sfml-graphics sfml-audio sfml-system sfml-window ssl ev tgui tquic python3.10 crypt dl m)
