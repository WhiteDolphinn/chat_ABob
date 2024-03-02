#pragma once
#include <vector>
#include <string>
#include <cstdint>

typedef unsigned id;
//typedef uint64_t time;

struct message{
    id sender;
    std::vector<id> receivers;
    std::string text;
    //time time;
    std::string name;
};
