#include <stdio.h>    	// Used for printf() statements
#include <wiringPi.h> 	// Include WiringPi library!
// Pin number declarations. We're using the Broadcom chip pin numbers.
// Compile with "gcc -o Pigpio Pigpio.c -l wiringPi"
// Compile on Raspberry pi Zero w
const int PinOut1 = 21;      //physical is 40, main relay
const int PinOut2 = 17;      //physical is 11, GATEOPEN relay
const int PinOut3 = 27;      //physical is 13, limit switch #1 relay
const int PinOut4 = 22;      //physical is 15, light sensor relay
const int PinOut5 = 23;      //physical is 16, limit switch #2 relay
const int PinOut6 = 24;      //physical is 18, GATECLOSE relay

const int PinIn1 = 5;        //physical is 29, main input for iVMS/wiegand signal
const int PinIn2 = 6;        //physical is 31, input for limit switch #1 signal
const int PinIn3 = 13;       //physical is 33, input for light switch signal
const int PinIn4 = 19;       //physical is 35, input for limit switch #2 signal

const int OpenGate = 1;      //Define input 12v. from iVMS or Wiegand board
int read;                    //Define reciever 12v. from iVMS or Wiegand board
int main(void)
{    
    wiringPiSetup();         //Initializes wiringPi using wiringPi's simlified number system.
    wiringPiSetupGpio();     //Initializes wiringPi using the Broadcom GPIO pin numbers.

    pinMode(PinOut1, OUTPUT);
    pinMode(PinOut2, OUTPUT);
    pinMode(PinOut3, OUTPUT);
    pinMode(PinOut4, OUTPUT);
    pinMode(PinOut5, OUTPUT);
    pinMode(PinOut6, OUTPUT);

    pinMode(PinIn1, INPUT);             //define input for patrol loop
    pinMode(PinIn2, INPUT);             //define input for limit switch#1
    pinMode(PinIn3, INPUT);             //define input for light sensor
    pinMode(PinIn4, INPUT);             //define input for limit switch#2
    pullUpDnControl(PinIn1, PUD_DOWN);      //Enable pull-down resistor on PinIn1
    pullUpDnControl(PinIn2, PUD_DOWN);      //Enable pull-down resistor on PinIn2
    pullUpDnControl(PinIn3, PUD_DOWN);      //Enable pull-down resistor on PinIn3
    pullUpDnControl(PinIn4, PUD_DOWN);      //Enable pull-down resistor on PinIn4

    digitalWrite(PinOut1, LOW);
    digitalWrite(PinOut2, LOW);
    digitalWrite(PinOut3, LOW);
    digitalWrite(PinOut4, LOW);  
    //check barrier is OPEN or CLOSE?
    digitalWrite(PinOut5, HIGH);
    read = digitalRead(PinIn4);
    if(read!=OpenGate)                      //GATECLOSE is OPEN 
    {
        digitalWrite(PinOut6, HIGH);
        while(read != OpenGate)            //limit switch #2 loop
        {
            read = digitalRead(PinIn4);
            delay(500);
            }
        }
    read = 0;
    printf("It's all OK!\n");
    digitalWrite(PinOut5, LOW);
    digitalWrite(PinOut6, LOW);   
    while(1)
    {
        digitalWrite(PinOut1, HIGH);
        read = 0;
        printf("read=%d\n", read);
        while(read != OpenGate)
        {
            read = digitalRead(PinIn1);       //Detect signal from iVMS or wiegand then, OPEN gate relay loop (main loop)
            delay(500);
            }
        printf("read=%d, OpenGate=%d\n", read, OpenGate);
        read = 0;
        printf("Open Gate Barrier\n");                              
        digitalWrite(PinOut2, HIGH);        //send signal ON to GATEOPEN (set relay to NO)
        delay(1000);                        //time delay for wait barrier up (wait 100ms.)
        digitalWrite(PinOut3, HIGH);
        printf("Open limit switch#1\n"); 
        printf("limit switch#1 = %d\n", read);
        while(read != OpenGate)            //limit switch#1 loop
        {
            read = digitalRead(PinIn2);
            delay(500);
            }
        printf("limit switch#1 = %d\n", read);
        read = 0;
        digitalWrite(PinOut3, LOW);         //send signal OFF to limit switch #1
        printf("Close limit switch#1 \n");
        digitalWrite(PinOut2, LOW);         //send signal OFF to GATEOPEN (set relay to NC)
        printf("CLOSE circuit GATE OPEN\nAnd wait for car/Truck pass 6sec.\n");
        //#====================
        delay(6000);                        //wait for car/truck pass six seconds (wait 6000ms.).
        //#====================
        printf("Open light sensor\n");
        printf("Light switch= %d\n", read);
        while(read != OpenGate)            //light switch loop
        {
            digitalWrite(PinOut4, HIGH);   //Send signal OPEN to light sensor
            delay(20);
            read = digitalRead(PinIn3);
            digitalWrite(PinOut4, LOW);
            delay(5000);
            }
        printf("Light switch= % d\n", read);
        read = 0;
        digitalWrite(PinOut4, LOW);         //send signal CLOSE to light sensor
        printf("Close light switch\n");
        digitalWrite(PinOut5, HIGH);        //send signal ON to limit switch #2   
        printf("Open limit switch#2\n");   
        digitalWrite(PinOut6, HIGH);        //send signal ON to GATECLOSE (set relay to NO)
        printf("Open circuit GATE CLOSE\n");
        printf("Limit switch#2= %d\n", read);
        while(read != OpenGate)            //limit switch #2 loop
        {
            read = digitalRead(PinIn4);
            delay(500);
            }
        printf("Limit switch#2= %d\n", read);
        read = 0;
        digitalWrite(PinOut5, LOW);         //send signal OFF to limit switch #2
        printf("Close limit switch#2\n");
        digitalWrite(PinOut6, LOW);         //send signal OFF to GATE CLOSE
        printf("Close circuit GATE CLOSE\n");
        delay(1000);
        printf("Close gate barrier completely\n");
        digitalWrite(PinOut1, LOW); 
    }
    return 0;
}
