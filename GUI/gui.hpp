#pragma once
//#include <SFML/Window.hpp>
#include "chat.hpp"
#include "window.hpp"


class GUI{
    private:
    Chat chat;
    window window;
    public:
    message get_message();
    void push_message(message message);
    void update();
};
