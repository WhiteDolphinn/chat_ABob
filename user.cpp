#include "user.hpp"
#include <iostream>

unsigned User::get_user_id()
{
    return user_id;
}

std::string User::get_user_name()
{
    return user_name;
}

const std::vector<Chat>& User::get_chats()
{
    return chats;
}

void User::give_message(message message_)
{
    std::cout << "I got message!(User)" << std::endl;
}
