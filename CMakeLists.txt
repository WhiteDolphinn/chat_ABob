cmake_minimum_required(VERSION 3.2.7 FATAL_ERROR)
project(chat_ABob)

#set(CMAKE_C_COMPILER   /mnt/c/Users/HP/Downloads/CodeBlocks/MinGW/bin/gcc.exe)
#set(CMAKE_CXX_COMPILER /mnt/c/Users/HP/Downloads/CodeBlocks/MinGW/bin/g++.exe)


set(CMAKE_C_COMPILER   gcc)
set(CMAKE_CXX_COMPILER g++)

#link_directories(SFML-2.6.1/lib TGUI-1.1/lib)

#include_directories("GUI" "Link")
include_directories(./GUI ./Link)


set(CMAKE_CXX_STANDARD 17)

#find_package(SFML COMPONENTS graphics audio system REQUIRED)
#find_package(TGUI REQUIRED)

add_executable(chat_ABob main.cpp
                         user.cpp
                         user.hpp
                         message.hpp
                         GUI/chat.cpp
                         GUI/chat.hpp
                         GUI/gui.cpp
                         GUI/gui.hpp
                         GUI/terminal.cpp
                         GUI/terminal.hpp)

target_link_libraries(chat_ABob sfml-graphics sfml-audio sfml-system sfml-window tgui)
