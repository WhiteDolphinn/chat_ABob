#pragma once
#include <vector>
#include <string>

typedef unsigned id;
typedef unsigned int64_t time;

struct message{
    id sender;
    std::vector<id> receivers;
    std::string text;
    time time;
    std::string name;
};
