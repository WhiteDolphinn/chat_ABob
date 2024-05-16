#pragma once
#include <TGUI/TGUI.hpp>
#include <TGUI/Backend/SFML-Graphics.hpp>
//#include "../user.hpp"


class GUI{
    private:
    User& user;
    sf::RenderWindow window;
    tgui::Gui gui;

    std::shared_ptr<tgui::EditBox> edit_box;
    std::shared_ptr<tgui::ChatBox> chat_box;
    tgui::Button::Ptr button;

    public:
    GUI(User& user_);

    void draw();
};
