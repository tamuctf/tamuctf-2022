#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define xstr(s) str(s)
#define str(s) #s

// modified from: https://github.com/nikhilroxtomar/Multiple-Client-Server-Program-in-C-using-fork

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    int sockfd, ret;
    struct sockaddr_in serverAddr;

    int newSocket;
    struct sockaddr_in newAddr;

    socklen_t addr_size;

    pid_t childpid;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        fprintf(stderr, "[-]Error in connection.\n");
        exit(1);
    }
    printf("[+]Server Socket is created.\n");

    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = inet_addr("0.0.0.0");

    ret = bind(sockfd, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
    if (ret < 0) {
        fprintf(stderr, "[-]Error in binding.\n");
        exit(1);
    }
    printf("[+]Bind to port %d\n", PORT);

    if (listen(sockfd, 1024) == 0) {
        printf("[+]Listening....\n");
    } else {
        fprintf(stderr, "[-]Error in listening.\n");
        exit(1);
    }


    while (1) {
        newSocket = accept(sockfd, (struct sockaddr *) &newAddr, &addr_size);
        if (newSocket < 0) {
            fprintf(stderr, "[-]Error in accepting.\n");
            exit(1);
        }
        printf("Connection accepted from %s:%d\n", inet_ntoa(newAddr.sin_addr), ntohs(newAddr.sin_port));

        childpid = fork();
        if (childpid == -1) {
            fprintf(stderr, "[-]Error in binding.\n");
            exit(1);
        } else if (childpid == 0) {
            close(sockfd);
            dup2(newSocket, STDIN_FILENO);
            dup2(newSocket, STDOUT_FILENO);
            dup2(newSocket, STDERR_FILENO);
            setvbuf(stdout, NULL, _IONBF, 0);
            setvbuf(stdin, NULL, _IONBF, 0);
            setvbuf(stderr, NULL, _IONBF, 0);
            close(newSocket);
            char binary[128];
            snprintf(binary, sizeof(binary), "/pwn/%s", xstr(NAME));
            char * const argv[] = {binary, NULL};
            char * const envp[] = {NULL};
            execve(binary, argv, envp);
        } else {
            printf("Spawned %d for %s:%d\n", childpid, inet_ntoa(newAddr.sin_addr), ntohs(newAddr.sin_port));
        }
    }
}
