#pragma once
#include "../message.hpp"
#include <string>
#include <vector>
#include <map>

class Terminal{
    private:
    std::string buffer;
    std::map<std::string, id> users;
    //bool is_message_ready
    public:
    std::string get_buffer();
    message get_message();
};
