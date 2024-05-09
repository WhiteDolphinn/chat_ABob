#pragma once
//#include <TGUI/Backend/SFML-Network.hpp>
//#include <SFML/Network.hpp>
#include <string>
#include <vector>
#include "message.hpp"
//#include "chat.hpp"
//#include <errno.h>
#include <ev.h>
#include <fcntl.h>
//#include <inttypes.h>
#include <netdb.h>
//#include <stdbool.h>
//#include <stdint.h>
//#include <stdio.h>
//#include <stdlib.h>
//#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
//#include <unistd.h>
    
#include "include/tquic.h"


class User
{
    private:
    quic_endpoint_t *quic_endpoint = NULL;
    ev_timer timer;
    int sock;
    struct sockaddr_storage local_addr;
    socklen_t local_addr_len;
    SSL_CTX *ssl_ctx = NULL;
    struct quic_tls_config_t *tls_config;
    struct quic_conn_t *conn = NULL;
    struct ev_loop *loop = NULL;

    quic_config_t *config = NULL;
    struct addrinfo *peer = NULL;

    unsigned user_id;
    std::string user_name;
    //link
   // std::vector<Chat> chats;

   // sf::UdpSocket socket;
    int create_socket(const char* host, const char* port);
    int create_config();

    public:
    User(unsigned user_id_, std::string user_name_ = "Loshara");

    ~User()
    {
        close(sock);
        freeaddrinfo(peer);
        SSL_CTX_free(ssl_ctx);
        quic_tls_config_free(tls_config);
        quic_endpoint_free(quic_endpoint);
        ev_loop_destroy(loop);
        quic_config_free(config);
    };


    void mainloop();

    unsigned get_user_id();
    std::string get_user_name();
    //const std::vector<Chat>& get_chats();
    void give_message(message message_);
};
