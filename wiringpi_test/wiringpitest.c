#include <wiringPi.h>
#include <stdio.h>

int sp;
int pin = 1;
int count = 0;

void blink(void)
{
	pinMode(pin, OUTPUT);
	for(count = 0; count < 18; count++)
	{
		printf("%d\n",count);
		digitalWrite(pin,HIGH);
		delay(500);
		digitalWrite(pin,LOW);
		delay(500);
	}
return;
}


int main()
{
	printf("SETUP\n");
	sp = wiringPiSetup();
	printf("SETUPED\n");
	printf("%d\n",sp);
	blink();
	return 0;
}

