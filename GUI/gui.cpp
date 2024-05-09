#include <iostream>

#include "gui.hpp"
//#include <SFML/Graphics.hpp>

GUI::GUI(User& user_)
: user(user_), window(sf::VideoMode(800, 600), "Alice-Bob chat"), gui(window)
{
    tgui::Theme::setDefault("GUI/BabyBlue.txt");
    
    edit_box = tgui::EditBox::create();
    chat_box = tgui::ChatBox::create();
    button = tgui::Button::create();

};

void GUI::draw()
{
    gui.add(chat_box, "Chat1");
    chat_box->setPosition("30%", "0%");
    chat_box->setSize("70%", "85%");


    gui.add(edit_box, "MyWidgetName"    );
    edit_box->setPosition("35%", "90%");
    edit_box->setSize("50%", 50);

    gui.add(button);
    button->setPosition("85%", "90%");
    button->setSize(50, 50);
    //button->setText("zhopa");
    button->onPress([=]{
        auto text = edit_box->getText();
        chat_box->addLine(text);
        edit_box->setText("");
        });


    gui.mainLoop();
}

