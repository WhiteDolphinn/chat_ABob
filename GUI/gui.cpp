#include "gui.hpp"
#include <TGUI/TGUI.hpp>
#include <TGUI/Backend/SFML-Graphics.hpp>
//#include <SFML/Graphics.hpp>

void GUI::draw()
{
    sf::RenderWindow window{sf::VideoMode(800, 600), "Alice-Bob chat"};
    tgui::Gui gui{window};

    tgui::Button::Ptr button = tgui::Button::create();
    auto editBox = tgui::EditBox::create();

    gui.add(button);
    gui.add(editBox, "MyWidgetName");

    gui.mainLoop();
}
