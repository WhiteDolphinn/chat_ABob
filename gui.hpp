#pragma once
#include <iostream>
#include <vector>
#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>
#include <python3.10/structmember.h>
#include <TGUI/TGUI.hpp>
#include <TGUI/Backend/SFML-Graphics.hpp>

static PyObject* get_username(PyObject* self, PyObject* args);
static PyObject* push_chat(PyObject* self, PyObject* args);
static PyObject* push_message(PyObject* self, PyObject* args);
static PyObject* mainloop(PyObject* self, PyObject* args);
static PyObject* startup(PyObject* self, PyObject* args);

struct Chat
{
    std::string name;
    std::vector<std::string> history;
};

struct User
{
    std::string name;
    bool has_name = false;
    std::vector<Chat> chats;
};

class Gui
{
    public:
    // std::shared_ptr<tgui::EditBox> edit_box;
    // std::shared_ptr<tgui::ChatBox> chat_box;
    // tgui::Button::Ptr button;


    unsigned height;
    unsigned width;
    User user;
    sf::RenderWindow window;


    tgui::Gui gui;

    Gui();
    ~Gui();

    void draw();

    //PyObject_HEAD
};

extern struct Gui Gui;
