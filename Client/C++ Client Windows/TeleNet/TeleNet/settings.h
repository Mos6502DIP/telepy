#ifndef SETTINGS_H
#define SETTINGS_H

#include <string>

struct Settings {
    std::string location;
    std::string defaultServer;
    bool autoReturn = false;
};

bool loadSettings(const std::string& filename, Settings& settings);
void saveSettings(const std::string& filename, const Settings& settings);
void setup(Settings& settings);

#endif
