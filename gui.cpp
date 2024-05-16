#include <iostream>
#include <algorithm>
#include <thread>
#include "gui.hpp"
//#include <SFML/Graphics.hpp>

#define MAX_COUNT_OF_CHATS 5

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
    /*while(Gui.user.has_name == false)
        continue;*/

    std::cout << "\'" << Gui.user.has_name << "\'" << std::endl;
    std::cout << "\'" << Gui.user.name << "\'" << std::endl;
    
    return Py_BuildValue("s", Gui.user.name.c_str());
}

static PyObject* push_chat(PyObject* self, PyObject* args)
{
    Gui.mutex.lock();
    char* name;
    PyArg_ParseTuple(args, "s", &name);

    for(auto& chat: Gui.user.chats)
    {
        if(!chat.name.compare(std::string(name)))
        {
            Gui.mutex.unlock();
            Py_RETURN_NONE;
        }
    }

    if(Gui.user.chats.size() >= MAX_COUNT_OF_CHATS)
    {
        Gui.mutex.unlock();
        Py_RETURN_NONE;
    }

    Chat chat = {.name = name};
    Gui.user.chats.push_back(chat);

    Gui.add_chat(name);

    Gui.mutex.unlock();
    Py_RETURN_NONE;
}

static PyObject* push_message(PyObject* self, PyObject* args)
{
    Gui.mutex.lock();
    char* chat_name;
    char* message;
    PyArg_ParseTuple(args, "ss", &chat_name, &message);
    
    for(auto& chat: Gui.user.chats)
    {
        if(chat.name.compare(chat_name)) 
            continue;

        chat.history.push_back(message);
        if(!std::string(chat_name).compare(Gui.current_chat_name))
            Gui.add_message(message);

        break;
    }

    Gui.mutex.unlock();
    Py_RETURN_NONE;
}

Gui::Gui()
: height(800), width(600), window(sf::VideoMode(height, width), "Alice-Bob chat"), gui(window)
{
    user.name = "";
    current_chat_name = "";
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
    button->onPress([=]
    {
        std::cout << current_chat_name << std::endl;
        for(auto& chat: user.chats)
        {
                std::cout << chat.name << std::endl;
        }

        mutex.lock();
        auto text = edit_box->getText();
        if(text.empty())
        {
            mutex.unlock();
            return;
        }

        //std::string m = "print(\"hello\")";
        std::string m = R"(import sys
sys.path.append('.')
import proxy
proxy.push_message(")";
        m += std::string(current_chat_name);
        m += "\", \"";
        m += std::string(text);
        m += "\")";
        PyRun_SimpleString(m.c_str());

        std::time_t end_time = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
 

        std::string mess = user.name;
        mess += ": ";
        mess += std::ctime(&end_time);
        *(mess.end() - 1) = ':';
        mess += " ";
        mess += std::string(text);
        chat_box->addLine(mess);
        edit_box->setText("");
        
        for(auto& chat: user.chats)
        {
            if(chat.name.compare(current_chat_name)) 
                continue;

            chat.history.push_back(std::string(mess));
            break;
        }

        mutex.unlock();
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


        message_button->setPosition("85%", "70%");
        message_button->setSize(50, 50);
        message_box->add(message_button);


        message_button->onPress([=]
        {
        auto text = edit_message_box->getText();
        if(text.empty())
            return;
        user.name = std::string(text);
        user.has_name = true;
        gui.remove(message_box);

        std::thread thread([=]()
        {
            PyRun_SimpleString(code);   
        });
        thread.detach();
        });

        gui.add(message_box);
    }

    tgui::Button::Ptr create_chat_button = tgui::Button::create();
    create_chat_button->setPosition("0%", "90%");
    create_chat_button->setSize("30%", "10%");
    gui.add(create_chat_button);

    std::shared_ptr<tgui::MessageBox> create_chat_box = tgui::MessageBox::create();
    create_chat_button->onPress([=]
    {
        if(user.chats.size() >= MAX_COUNT_OF_CHATS)
            return;

        create_chat_box->setSize("50%", "50%");
        create_chat_box->setPosition("30%", "0%");

        std::shared_ptr<tgui::EditBox> edit_create_chat_box = tgui::EditBox::create();
        tgui::Button::Ptr create_chat_button = tgui::Button::create();

        create_chat_box->add(edit_create_chat_box, "MyWidgetName");
        edit_create_chat_box->setPosition("35%", "70%");
        edit_create_chat_box->setSize("50%", 50);

        create_chat_button->setPosition("85%", "70%");
        create_chat_button->setSize(50, 50);
        create_chat_box->add(create_chat_button);

        create_chat_button->onPress([=]
        {
            auto text = edit_create_chat_box->getText();
            if(text.empty())
                return;

            
            gui.remove(create_chat_box);
            std::string m = R"(import sys
sys.path.append('.')
import proxy
proxy.create_chat(")";
        m += std::string(text);
        m += "\")";
        PyRun_SimpleString(m.c_str());

        Chat chat{.name = std::string(text).substr(0, std::string(text).find(":"))};
        std::cout << "\'" << chat.name << "\'" << std::endl;
        user.chats.push_back(chat);
        add_chat((char*)((user.chats.end()-1)->name).c_str());
        std::cout << "\'" << (user.chats.end()-1)->name  << "\'" << std::endl;
        
        });

        gui.add(create_chat_box);
    });


    std::vector<tgui::Button::Ptr> chat_buttons;

    add_chat = [this, &chat_buttons, &edit_box, &chat_box](char* chat_name)
    {
        auto chat_button = tgui::Button::create();
        chat_button->setText(chat_name);
        chat_button->setSize("30%", "10%");
        char percent[10];
        sprintf(percent, "%ld%%", chat_buttons.size()*10);
        chat_button->setPosition("0%", percent);

        chat_button->onPress([=]
        {
            edit_box->setText("");
            chat_box->removeAllLines();

            for(auto& chat: user.chats)
            {
                if(chat.name.compare(chat_name)) 
                    continue;

                for(auto& message: chat.history)
                {
                    chat_box->addLine(message);
                }
                current_chat_name = chat_name;
                break;
            }
        });

        chat_buttons.push_back(std::move(chat_button));
        gui.add(*(chat_buttons.end() - 1));
    };

    add_message = [&chat_box](char* message)
    {
        chat_box->addLine(message);
    };

    gui.mainLoop();
}

static PyObject* mainloop(PyObject* self, PyObject* args)
{
    Gui.draw();

    Py_RETURN_NONE;
}

static PyObject* startup(PyObject* self, PyObject* args)
{
        Py_Initialize();
        char* code;
        PyArg_ParseTuple(args, "s", &code);
        std::cout << "\'" << code << "\'" << std::endl;
        Gui.code = code;
    

    Gui.draw();

    
    Py_RETURN_NONE;
}