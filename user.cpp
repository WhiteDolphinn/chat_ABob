#include <iostream>
#include "user.hpp"


//#include <SFML/Network.hpp>

User::User(unsigned user_id_, std::string user_name_)
    : user_id(user_id_), user_name(user_name_)
{
    const char *host = "127.0.0.1";
    const char *port = "8000";
};

void User::create_socket(std::string host, std::string port)
{

}

void User::mainloop()
{

}

unsigned User::get_user_id()
{
    return user_id;
}

std::string User::get_user_name()
{
    return user_name;
}

/*const std::vector<Chat>& User::get_chats()
{
    return chats;
}*/

void User::give_message(message message_)
{
    std::cout << "I got message!(User)" << std::endl;
}
