#include "gui.hpp"
#include <TGUI/TGUI.hpp>
#include <TGUI/Backend/SFML-Graphics.hpp>
//#include <SFML/Graphics.hpp>

void GUI::draw()
{
    tgui::Theme::setDefault("GUI/BabyBlue.txt");
    sf::RenderWindow window{sf::VideoMode(800, 600), "Alice-Bob chat"};
    tgui::Gui gui{window};

    tgui::Button::Ptr button = tgui::Button::create();
    auto edit_box = tgui::EditBox::create();
    auto chat_box = tgui::ChatBox::create();

    gui.add(chat_box, "Chat1");
    chat_box->setSize("100%", "85%");

    gui.add(edit_box, "MyWidgetName"    );
    edit_box->setPosition("25%", "90%");
    edit_box->setSize("50%", 50);

    gui.add(button);
    button->setPosition("75%", "90%");
    button->setSize(50, 50);
    button->onPress([=]{
        auto text = edit_box->getText();
        chat_box->addLine(text);
        edit_box->setText("");
        });


    gui.mainLoop();
}

