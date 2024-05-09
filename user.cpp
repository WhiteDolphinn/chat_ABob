#include <iostream>
#include "user.hpp"

#define MAX_DATAGRAM_SIZE 1200

//#include <SFML/Network.hpp>

User::User(unsigned user_id_, std::string user_name_)
    : user_id(user_id_), user_name(user_name_)
{
    const char* host = "127.0.0.1";
    const char* port = "8000";
    create_socket(host, port);
    create_config();

    
};

int User::create_socket(const char* host, const char* port)
{

    const struct addrinfo hints = {.ai_family = PF_UNSPEC,
                                   .ai_socktype = SOCK_DGRAM,
                                   .ai_protocol = IPPROTO_UDP};
    
    
    if (getaddrinfo(host, port, &hints, &peer) != 0) {
        fprintf(stderr, "failed to resolve host\n");
        return -1;
    }
    sock = socket(peer->ai_family, SOCK_DGRAM, 0);
    if(sock < 0)
    {
        fprintf(stderr, "failed to create socket\n");
        return -1;
    }

    if(fcntl(sock, F_SETFL, O_NONBLOCK) != 0) {
        fprintf(stderr, "failed to make socket non-blocking\n");
        return -1;
    }

    local_addr_len = sizeof(local_addr);
    if(getsockname(sock, (struct sockaddr *)&local_addr,&local_addr_len) != 0) 
    {
        fprintf(stderr, "failed to get local address of socket\n");
        return -1;
    };
    return 0;
}

int User::create_config()
{
    config = quic_config_new();
    if (config == NULL)
    {
        fprintf(stderr, "failed to create config\n");
        return -1;
    }

    quic_config_set_max_idle_timeout(config, 5000);
    quic_config_set_recv_udp_payload_size(config, MAX_DATAGRAM_SIZE);
    return 0;
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
