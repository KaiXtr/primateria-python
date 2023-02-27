#include <stdio.h>
#include <time.h>

int main () {
  printf("Hello World!");
  return 0;
}

int getCurrentTime () {
  time_t rawtime;
  struct tm * timeinfo;

  time ( &rawtime );
  timeinfo = localtime ( &rawtime );
  printf ( "Current local time and date: %s", asctime (timeinfo) );
  int r = hello(8);
  return (0);
}