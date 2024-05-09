#include <iostream>
#include "user.hpp"

#define READ_BUF_SIZE 4096
#define MAX_DATAGRAM_SIZE 1200

//#include <SFML/Network.hpp>

User::User(unsigned user_id_, std::string user_name_)
    : user_id(user_id_), user_name(user_name_)
{
    const char* host = "127.0.0.1";
    const char* port = "8000";
    create_socket(host, port);
    create_config();

    int ret = quic_endpoint_connect(
        quic_endpoint, (struct sockaddr *)&local_addr,
        sizeof(local_addr), peer->ai_addr, peer->ai_addrlen,
        NULL /* server_name */, NULL /* session */, 0 /* session_len */,
        NULL /* token */, 0 /* token_len */, NULL /* config */,
        NULL /* index */);
    if (ret < 0)
    {
        fprintf(stderr, "failed to connect to client: %d\n", ret);
        ret = -1;
    }    
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
    loop = ev_default_loop(0);

    ev_init(&timer, timeout_callback);

    timer.data = this;
}

void User::timeout_callback(EV_P_ ev_timer *w, int revents)
{
    //struct simple_client *client = w->data;
    quic_endpoint_on_timeout(quic_endpoint);
    process_connections();
}

void User::process_connections()
{
    quic_endpoint_process_connections(quic_endpoint);
    double timeout = quic_endpoint_timeout(quic_endpoint) / 1000.0;
    if(timeout < 0.0001)
        timeout = 0.0001;

    timer.repeat = timeout;
    ev_timer_again(loop, &timer);
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

void User::conn_created(struct quic_conn_t *conn_)
{
    conn = conn_;
}

void User::conn_established(struct quic_conn_t *conn)
{
    const char *data = "GET /\r\n";
    quic_stream_write(conn, 0, (uint8_t *)data, strlen(data), true);
}

void User::conn_closed(struct quic_conn_t *conn)
{
    ev_break(loop, EVBREAK_ALL);
}

void User::stream_created(struct quic_conn_t *conn, uint64_t stream_id)
{

}

void User::stream_readable(struct quic_conn_t *conn, uint64_t stream_id) 
{
    static uint8_t buf[READ_BUF_SIZE];
    bool fin = false;
    ssize_t r = quic_stream_read(conn, stream_id, buf, READ_BUF_SIZE, &fin);
    if (r < 0) {
        fprintf(stderr, "stream[%ld] read error\n", stream_id);
        return;
    }

    printf("%.*s", (int)r, buf);

    if (fin) {
        const char *reason = "ok";
        quic_conn_close(conn, true, 0, (const uint8_t *)reason, strlen(reason));
    }
}

void User::stream_writable(struct quic_conn_t *conn, uint64_t stream_id)
{
    quic_stream_wantwrite(conn, stream_id, false);
}

void User::stream_closed(struct quic_conn_t *conn, uint64_t stream_id)
{

}

int User::packets_send(struct quic_packet_out_spec_t *pkts, unsigned int count)
{

    unsigned int sent_count = 0;
    int i, j = 0;
    for (i = 0; i < count; i++) {
        struct quic_packet_out_spec_t *pkt = pkts + i;
        for (j = 0; j < (*pkt).iovlen; j++) {
            const struct iovec *iov = pkt->iov + j;
            ssize_t sent =
                sendto(sock, iov->iov_base, iov->iov_len, 0,
                       (struct sockaddr *)pkt->dst_addr, pkt->dst_addr_len);

            if (sent != iov->iov_len) {
                if ((errno == EWOULDBLOCK) || (errno == EAGAIN)) {
                    fprintf(stderr, "send would block, already sent: %d\n",
                            sent_count);
                    return sent_count;
                }
                return -1;
            }
            sent_count++;
        }
    }

    return sent_count;
}
