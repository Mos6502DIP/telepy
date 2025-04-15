#include "utils.h"
#include <iostream>
#include <conio.h>
#include <windows.h>

void clearScreen() {
    system("cls");
}

std::string getPassword() {
    std::string pwd;
    char ch;
    while ((ch = _getch()) != '\r') {
        if (ch == '\b') {
            if (!pwd.empty()) {
                pwd.pop_back();
                std::cout << "\b \b";
            }
        }
        else {
            pwd.push_back(ch);
            std::cout << '*';
        }
    }
    std::cout << "\n";
    return pwd;
}

void setConsoleColor(int fg, int bg) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), (bg << 4) | fg);
}
