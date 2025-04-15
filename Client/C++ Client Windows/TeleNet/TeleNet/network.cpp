#include "network.h"
#include <winsock2.h>
#include <iostream>

#pragma comment(lib, "ws2_32.lib")

void connectToServer(const char* ip, int port) {
    WSADATA wsa;
    SOCKET s;
    struct sockaddr_in server;

    std::cout << "Initializing Winsock..." << std::endl;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cout << "Failed: " << WSAGetLastError() << std::endl;
        return;
    }

    if ((s = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        std::cout << "Socket creation failed: " << WSAGetLastError() << std::endl;
        return;
    }

    server.sin_addr.s_addr = inet_addr(ip);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    std::cout << "Connecting to " << ip << ":" << port << "..." << std::endl;
    if (connect(s, (struct sockaddr*)&server, sizeof(server)) < 0) {
        std::cout << "Connection failed." << std::endl;
        closesocket(s);
        WSACleanup();
        return;
    }

    std::cout << "Connected to server!" << std::endl;

    char serverReply[2000];
    int recv_size = recv(s, serverReply, 2000, 0);
    if (recv_size > 0) {
        serverReply[recv_size] = '\0';
        std::cout << "Server says: " << serverReply << std::endl;
    }

    closesocket(s);
    WSACleanup();
}
