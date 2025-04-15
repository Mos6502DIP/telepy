#include <iostream>
#include "settings.h"
#include "utils.h"
#include "network.h"

int main() {
    clearScreen();
    std::cout << "Welcome to Telepy (C++ Edition)!" << std::endl;

    Settings settings;
    if (!loadSettings("config.txt", settings)) {
        setup(settings);
        saveSettings("config.txt", settings);
    }

    std::cout << "Your weather location is set to: " << settings.location << std::endl;
    std::cout << "Default server: " << (settings.defaultServer.empty() ? "None" : settings.defaultServer) << std::endl;

    std::string ip;
    std::cout << "Enter server IP (or leave blank for default): ";
    std::getline(std::cin, ip);
    if (ip.empty()) ip = settings.defaultServer;

    if (ip.empty()) {
        std::cout << "No server provided. Exiting." << std::endl;
        return 1;
    }

    connectToServer(ip.c_str(), 1998);

    return 0;
}