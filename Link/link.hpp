#pragma once
#include <string.h>
#include "message.hpp"


namespace Link{


enum class State{
    N0_MESSAGE, 
    NEW_MESSAGE, 
    CONNECTION_ERROR,
    PROGRAM_ERROR,
    DEFAULT
};


typedef int64_t server_id;


class Link{
    private:
        State state = State::DEFAULT;
        server_id link_id;


    public:
        Link(const server_id& id): link_id(id){
            
        }

        ~Link(){}

        
        State& send_message(const message message);

        State& get_message(message& message);
};

}