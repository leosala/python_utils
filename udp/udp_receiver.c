#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// for uint64 printing
#include <inttypes.h>


#define BUFFER_LENGTH    1000

//Memory packing (see: https://msdn.microsoft.com/en-us/library/2e70t5y1.aspx)
#pragma pack(push)
#pragma pack(2)
struct packet_struct{
	uint64_t framenum;
	int16_t data[BUFFER_LENGTH];
};
struct packet_struct packet;
#pragma pack(pop)

//simple routine to get data from UDP socket
int get_message(int sd){
	ssize_t nbytes = recv(sd, &packet, sizeof(packet), MSG_DONTWAIT);
	if(nbytes >= 0){
		printf("%u\t", (uint)packet.framenum);
		printf("%hu\t", packet.data[0]);
		printf("%hu\t", packet.data[999]);
	}
	return nbytes;
}

/*
int main(){
	int ret;

	sd = socket(AF_INET, SOCK_DGRAM, 0);
	printf("SD: %d\n", sd);

	int   val=SOCKET_BUFFER_SIZE;
	setsockopt(sd, SOL_SOCKET, SO_RCVBUF, &val, sizeof(int));
	
	if (sd < 0){
	perror("socket() failed");
	return -1;
	}
	
	memset(&serveraddr, 0, sizeof(serveraddr));
	serveraddr.sin_family      = AF_INET;
	serveraddr.sin_port        = htons(SERVER_PORT);
	serveraddr.sin_addr.s_addr = inet_addr(SERVER_IP);
	
	rc = bind(sd, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
	printf("RC bind: %d\n", rc);
	//ret = setsockopt(socket, SOL_SOCKET, SO_RCVBUF, &val, sizeof(int));
	//printf("%d\n", ret);

	while(1)
		get_message(sd);
}
*/
