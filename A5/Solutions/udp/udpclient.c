/* This code is public domain
   
   Author: XX, 2018
   xx@xx.xx
 */

#include <stdio.h>      /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), bind(), and connect() */
#include <arpa/inet.h>  /* for sockaddr_in and inet_ntoa() */
#include <stdlib.h>     /* for atoi() and exit() */
#include <string.h>     /* for memset() */
#include <unistd.h>     /* for close() */
#include <netdb.h>

#include <stdlib.h> // atoi, atof
#include <sys/time.h> // gettimeofday

#include<signal.h>
#include<errno.h>

#define TEN_TO_6 1000000
#define MAX_PACKET_SIZE 1000

int continue_sending = 1;

static void catch_function(int signal){
  (void)signal; // to suppress the warning about unused variable
  continue_sending = 0;
}

double get_time() {
  struct timeval t;
  gettimeofday(&t, 0);
  return t.tv_sec + (double) t.tv_usec / TEN_TO_6;
}


int main(int argc, char **argv) {
  signal(SIGINT, catch_function);
  
  struct hostent *dst_ptr;
  struct sockaddr_in dst_addr; 
  int sockfd, i, slen=sizeof(dst_addr);
  
  char * dst_name; short port; 
  
  char data_buf[MAX_PACKET_SIZE]; for (i=0;i<MAX_PACKET_SIZE;i++) data_buf[i]=1; 
  
  // We will try to send packets of size "packet_size" every "waiting_time" milliseconds
  double rate = 100;  // default = 100 kb/s.
  int packet_size; // in Bytes
  double waiting_time; // in milliseconds
  
  if (argc < 3) {
    fprintf(stderr, "Usage: %s <dst ip> <port> [rate kb/s]\n", argv[0]);
    exit(1);
  } 
  else {
    dst_name = argv[1];
    port = atoi(argv[2]);
    if (argc >= 4){
      rate = atof(argv[3]);
    }
  }

  // We now set the packet_size and the waiting_time time as a function of the rate. 
  // if the rate<50kbps, we use packets of size 125B = 1000b.
  // otherwise, packets of size 1000B=8000b. 
  if (rate < 50) {
    packet_size = 125; 
  }
  else {
    packet_size = 1000;
  }
  waiting_time = 8*packet_size/(1000*rate);
    
  /* create socket */
  if ((sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
    perror ("socket");
    exit(1);
  }

  if ((dst_ptr = gethostbyname(dst_name)) == 0) {
    perror ("gethostbyname");
    exit(1);
  }
  bcopy(dst_ptr->h_addr, (char *)&dst_addr.sin_addr, dst_ptr->h_length);
  dst_addr.sin_family = AF_INET ;
  dst_addr.sin_port = htons(port) ;

  /* memset( &dst_addr, 0 , sizeof(dst_addr) ); */
  /* dst_addr.sin_family = AF_INET ; */
  /* dst_addr.sin_port = htons(port) ; */
  /* if ( inet_aton(dst_name, &dst_addr.sin_addr) == 0){ */
  /*   perror("inet_aton failed\n"); */
  /*   exit(1); */
  /* } */
  
  double start_time = get_time();
  double last_print_time = start_time;
  double next_time = start_time+waiting_time;
  int nb_packets = 0, bytes_sent=0;
  int sent_len, recv_len; 
  
  
  /* Now, we try to send one packet every "waitine_time" */
  while(continue_sending)
    {
      // First, we send a packet
      sprintf(data_buf,"%d\n",nb_packets+1); // we send the packet number in the data
      if( (sent_len = sendto(sockfd,data_buf,packet_size,0,
			     (const struct sockaddr*) &dst_addr, slen)) == -1) {
	perror("sendto"); 
	exit(1);
      }
      bytes_sent += sent_len; 
      nb_packets ++;
      
      // Every second, we print how many packets were sent
      if (get_time() >= last_print_time+1){
	printf("%5.1fs - sent:%6d pkts, %6.1f kbits/s\n", get_time()-start_time, nb_packets, bytes_sent*8/ (get_time()-last_print_time) / 1000);
	bytes_sent= 0;
	last_print_time = get_time();
      }
      
      // Then, we add a wait to send a packet every x ms. 
      double time_to_wait = next_time-get_time();
      if (time_to_wait > 0 ) usleep(TEN_TO_6 *time_to_wait);
      next_time +=waiting_time;	
    }
  
  /* When we receive ^C, we stop sending at full rate.
     We send messages that start with 0 every 0.1s to notify the server. 
     until we receive an ack from the server (or another ^C) */
  
  // First, we set the timeout to 0.1 second. 
  struct timeval tv; tv.tv_sec=0; tv.tv_usec = 0.1*TEN_TO_6; 
  setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char*)&tv, sizeof(tv) );	
  
  // Now, we keep sending until we receive an ack or another ^C
  continue_sending = 1; 
  while( continue_sending) {
    data_buf[0]=0; 
    if( sendto(sockfd,data_buf,packet_size,0,(const struct sockaddr*) &dst_addr, slen) == -1) {
      perror("sendto"); 
      exit(1);
    }
    if ( (recv_len = continue_sending = recv(sockfd,data_buf,MAX_PACKET_SIZE,0)) < 0  ){
      if (!(errno == EWOULDBLOCK) ) { // if error is not caused by TIMEOUT, we die.
	perror("recv"); 
	exit(1); 
      }
    }
    else { // if we received an ack, we stop sending
      continue_sending = 0;
    }
  }
  printf("packets sent = %d, avg rate=%6.1fkbps\n", nb_packets, 8*packet_size*nb_packets/(get_time()-start_time)/1000);
  close (sockfd);
  return 0;
}



 





