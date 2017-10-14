//Data Logging Program, with DHT22, PM2001

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
#include <wiringPi.h>
#include <wiringSerial.h>

//DHT22 설정에 필요한 변수값
#define MAX_TIMINGS    85
#define DHT_PIN        3    /* GPIO-22 */

typedef enum {false, true} bool;

int data[5] = { 0, 0, 0, 0, 0 };
char fileD[] = "tempD.csv";


void make_file()
{
	FILE* fp = fopen(fileD, "a");
        fclose(fp);

}

//DHT22
void read_dht_data()
{   int remeasuretime = 0;
    bool measurestate = true;
    while ( measurestate )
    {
	uint8_t laststate    = HIGH;
	uint8_t counter      = 0;
 	uint8_t j            = 0, i;
 
	data[0] = data[1] = data[2] = data[3] = data[4] = 0;
 
	/* pull pin down for 18 milliseconds */
	pinMode( DHT_PIN, OUTPUT );
	digitalWrite( DHT_PIN, LOW );
	delay( 18 );
 
	/* prepare to read the pin */
	pinMode( DHT_PIN, INPUT );
 
	/* detect change and read data */
	for ( i = 0; i < MAX_TIMINGS; i++ )
	{
		counter = 0;
		while ( digitalRead( DHT_PIN ) == laststate )
 		{
			counter++;
           		delayMicroseconds( 1 );
            		
			if ( counter == 255 )
            		{
                		break;
            		}
        	}
		laststate = digitalRead( DHT_PIN );
 
		if ( counter == 255 )
		break;
 
		/* ignore first 3 transitions */
		if ( (i >= 4) && (i % 2 == 0) )
		{
			/* shove each bit into the storage bytes */
			data[j / 8] <<= 1;
			if ( counter > 16 )
			data[j / 8] |= 1;
			j++;
  		}
	}
 
	/* check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
	* print it out if data is good*/
	if ( (j >= 40) && (data[4] == ( (data[0] + data[1] + data[2] + data[3]) & 0xFF) ) )
	{
		float h = (float)((data[0] << 8) + data[1]) / 10;
		float c = (float)(((data[2] & 0x7F) << 8) + data[3]) / 10;

		if ( data[2] & 0x80 )
		{
			c = -c;
		}
 		printf( "Humidity = %.1f %% Temperature = %.1f *C Remeasured %d times\n", h, c, remeasuretime);
                //시간측정
                time_t timer;
                struct tm *t;
                timer = time(NULL);     //현재 시간 읽기
                t = localtime(&timer);  //분리하여 구조체에 넣기

                //DATA.csv파일 쓰기
                FILE* fp = fopen(fileD,"a");
                fprintf(fp,"%d-%d-%d %d:%d,%.1f,%.1f,%d\n",t->tm_year + 1900,t->tm_mon +1, t->tm_mday, t->tm_hour, t->tm_min,c,h,remeasuretime);
                fclose(fp);
        measurestate = false;
        
        if(h>150||c>150){
            measurestate = true;
            delay(2500);
        }
    }
	else 
    {
        measurestate = true;
        delay(2500);
        remeasuretime++;
	}
}
}

//PM2007
void read_pm_data()
{	
		//PM2007이용
		int dustPCS=0;					//PCS값을 저장
		float dustValue=0;				//농도값을 저장
		float dustValue10 = 0;
		int fd=serialOpen("/dev/ttyAMA0",9600);		//UART 통신을 열어줌
		char send[]={0x11, 0x02, 0x0B, 0x01, 0xE1};	//Read particle measuring
		char send_open[] = {0x11, 0x03, 0x0C, 0x02, 0x1E, 0xC0};
		char send_close[] = {0x11, 0x03, 0x0C, 0x01, 0x1E, 0xC1};
		
		char respone[20];
		char respone_open[5];
		char respone_close[5];

		int readbyte = 20;

		unsigned char i;
		
//		printf("Serial Initialized_%d",fd);
		for(i=0; i<5; i++)
		{
			serialPutchar(fd, send[i]);
			delay(1);      // Don't delete this line !!
		}

		unsigned char recv_cnt = 0;
  		while(1)
		{
			if(serialDataAvail(fd))
			{
				respone[recv_cnt++] = serialGetchar(fd);
				if(recv_cnt ==20){recv_cnt = 0; break;}
			}
		}
		
		printf("DUST RAW DATA ");
		unsigned char checksum = 0;
		unsigned char count = 0;
		for (count = 0; count < 19; count++)
		{
			checksum += respone[count];
			printf(" %X",respone[count]);
		}
		checksum = 0x100-checksum;
		printf(" %X \nChesksum %X / Correction %d \n", respone[count], checksum, checksum == respone[count]);


		if(checksum==respone[count])		//측정성공
		{
			dustValue=respone[3]*256*256*256 + respone[4]*256*256 + respone[5]*256 + respone[6]; //PM2.5(0.3um ~ 2.5um) measured data (ug/m3)
			dustValue10 = respone[7]*256*256*256 + respone[8]*256*256 + respone[9]*256 + respone[10];

			printf("Dust PM2.5 : %.0f ug/m3  Dust PM10 : %.0f ug/m3  \n", dustValue, dustValue10);	//측정값 출력(ug/m3)

	                //DATA.csv파일 쓰기
        	        FILE* fp = fopen(fileD,"a");
               		fprintf(fp,",%.0f,%.0f",dustValue,dustValue10);

			fclose(fp);
		}
		else		//측정실패
		{
			FILE* fp = fopen(fileD,"a");
			printf("Fail to Receive");
			fprintf(fp,",,\n");
			fclose(fp);
		}

		serialClose(fd);		//시리얼 포트를 닫음
}

int main( void )
{
	if ( wiringPiSetup() == -1 )
	exit( 1 );
 
	make_file();
		printf("\n");

 
	return(0);
}
