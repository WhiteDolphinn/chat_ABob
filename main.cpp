#include <iostream>
#include "user.hpp"
#include "GUI/gui.hpp"

int main()
{
    User user(4, "Belarusian");
    GUI gui(user);
    gui.draw();
    //std::cout << "worked\n";
    return 0;
}
