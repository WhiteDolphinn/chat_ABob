#pragma once
#include "../user.hpp"


class GUI{
    private:
    User& user;
    public:
    GUI(User& user_)
    : user(user_)
    {
    };
    void draw();
};
