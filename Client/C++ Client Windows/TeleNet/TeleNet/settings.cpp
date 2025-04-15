#include "settings.h"
#include "utils.h"
#include <iostream>
#include <fstream>
#include <json.hpp>

using json = nlohmann::json;

std::string selectWeather() {
    std::string location;
    std::string choice;

    do {
        std::cout << "Enter nearest city for weather: ";
        std::getline(std::cin, location);

        std::cout << "Testing location..." << std::endl;
        std::string command = "curl wttr.in/" + location;
        system(command.c_str());

        std::cout << "Is this correct? (Y/N): ";
        std::getline(std::cin, choice);
    } while (choice != "Y" && choice != "y");

    return location;
}

void setup(Settings& settings) {
    clearScreen();
    std::cout << "[Setup Wizard]" << std::endl;

    settings.location = selectWeather();
    std::cout << "Enter default server IP (or leave blank): ";
    std::getline(std::cin, settings.defaultServer);
}

bool loadSettings(const std::string& filename, Settings& settings) {
    std::ifstream in(filename);
    if (!in.is_open()) return false;

    json j;
    in >> j;
    settings.location = j.value("location", "");
    settings.defaultServer = j.value("default_server", "");
    settings.autoReturn = j.value("auto_return", false);
    return true;
}

void saveSettings(const std::string& filename, const Settings& settings) {
    json j;
    j["location"] = settings.location;
    j["default_server"] = settings.defaultServer;
    j["auto_return"] = settings.autoReturn;

    std::ofstream out(filename);
    out << j.dump(4);
}