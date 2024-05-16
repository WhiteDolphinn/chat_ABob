#include <iostream>
#include <algorithm>
#include <thread>
#include "gui.hpp"
//#include <SFML/Graphics.hpp>

struct Gui Gui;

static PyMethodDef methods[] = 
{
    {"get_username", get_username, METH_NOARGS, "get_username"},
    {"push_chat", push_chat, METH_VARARGS, "push_chat"},
    {"push_message", push_message, METH_VARARGS, "push_message"},
    {"mainloop", mainloop, METH_NOARGS, "mainloop"},
    {"startup", startup, METH_VARARGS, "startup"},

    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = 
{
    PyModuleDef_HEAD_INIT, "_gui", "gui", -1, methods
};


PyMODINIT_FUNC
PyInit__gui(void)
{
    PyObject* mod = PyModule_Create(&module);

    return mod;
}

static PyObject* get_username(PyObject* self, PyObject* args)
{
    while(Gui.user.has_name == false)
        continue;

    std::cout << "\'" << Gui.user.name << "\'" << std::endl;
    
    return Py_BuildValue("s", Gui.user.name.c_str());
}

static PyObject* push_chat(PyObject* self, PyObject* args)
{
    char* name;
    PyArg_ParseTuple(args, "s", name);
    Chat chat = {.name = name};
    Gui.user.chats.push_back(chat);
    Py_RETURN_NONE;
}

static PyObject* push_message(PyObject* self, PyObject* args)
{
    char* chat_name;
    char* message;
    PyArg_ParseTuple(args, "ss", chat_name, message);
    
    for(auto& chat: Gui.user.chats)
    {
        if(chat.name.compare(chat_name)) 
            continue;

        chat.history.push_back(message);
        break;
    }

    Py_RETURN_NONE;
}

Gui::Gui()
: height(800), width(600), window(sf::VideoMode(height, width), "Alice-Bob chat"), gui(window)
{
    user.name = "";
    tgui::Theme::setDefault("GUI/BabyBlue.txt");
    
}

Gui::~Gui()
{
}

void Gui::draw()
{
    std::shared_ptr<tgui::EditBox> edit_box = tgui::EditBox::create();
    std::shared_ptr<tgui::ChatBox> chat_box = tgui::ChatBox::create();
    tgui::Button::Ptr button = tgui::Button::create();

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

    if(user.name.empty())
    {
        std::shared_ptr<tgui::MessageBox> message_box = tgui::MessageBox::create();
        message_box->setSize("50%", "50%");
        message_box->setPosition("30%", "0%");

        std::shared_ptr<tgui::EditBox> edit_message_box = tgui::EditBox::create();
        tgui::Button::Ptr message_button = tgui::Button::create();

        message_box->add(edit_message_box, "MyWidgetName");
        edit_message_box->setPosition("35%", "70%");
        edit_message_box->setSize("50%", 50);


        message_button->setPosition("85%", "90%");
        message_button->setSize(50, 50);
        message_box->add(message_button);


        message_button->onPress([=]{
        auto text = edit_message_box->getText();
        user.name = std::string(text);
        user.has_name = true;
        gui.remove(message_box);
        });

        gui.add(message_box);


    }

    gui.mainLoop();
}

static PyObject* mainloop(PyObject* self, PyObject* args)
{
    Gui.draw();

    Py_RETURN_NONE;
}

static PyObject* startup(PyObject* self, PyObject* args)
{
    std::thread thread([=](PyObject* args_)
    {
        char* code;
        PyArg_ParseTuple(args_, "s", &code);
        std::cout << "\'" << code << "\'" << std::endl;
        PyRun_SimpleString(code);   
    }, args);

    Gui.draw();

    thread.join();
    
    Py_RETURN_NONE;
}