#pragma once
#include "chat.hpp"
#include "message.hpp"
#include <string>
#include <vector>

class User
{
    private:
    unsigned user_id;
    std::string user_name;
    //link
    std::vector<Chat> chats;

    public:
    User(unsigned user_id_, std::string user_name_ = "Loshara")
    : user_id(user_id_), user_name(user_name_)
    {
    };

    ~User()
    {
    };

    unsigned get_user_id();
    std::string get_user_name();
    const std::vector<Chat>& get_chats();
    void give_message(message message_);
};
