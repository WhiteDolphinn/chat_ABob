cmake_minimum_required(VERSION 3.2.7)
project(chat_ABob)

set(CMAKE_CXX_STANDARD 11)

find_package(SFML 2.5 COMPONENTS graphics audio REQUIRED)

add_executable(chat_ABob main.cpp)

target_link_libraries(chat_ABob sfml-graphics sfml-audio)
