#pragma once
#include "terminal.hpp"
#include "../message.hpp"
#include <vector>

class Chat{
    private:
    std::vector<message> history;
    Terminal terminal;
    public:
    message get_message();
    void push_message(message message);
    const std::vector<message>& get_history();

    std::string get_terminal_buffer();

};
