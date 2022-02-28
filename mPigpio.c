#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/binary_info.h"

/*compile with
 * cd /home/pi/pico/pico-examples/Hongsa/build
 * export PICO_SDK_PATH=../../pico-sdk
 * cmake ..
 * make
 * Then, copy *.uf2 to the pico board when it is mounted as a USB drive
*/

const uint RunPin = 1;      //set var named RunPin = GP1 (physical is 2)

const uint PinOut1 = 2;      //set var named PinOut1 = GP2 (physical is 4, main relay)
const uint PinOut2 = 3;      //set var named PinOut2 = GP3 (physical is 5, gate OPEN relay)
const uint PinOut3 = 4;      //set var named PinOut3 = GP4 (physical is 6, limit switch #1 relay)
const uint PinOut4 = 5;      //set var named PinOut4 = GP5 (physical is 7, light sensor relay)
const uint PinOut5 = 6;      //set var named PinOut5 = GP6 (physical is 9, limit switch #2 relay)
const uint PinOut6 = 7;      //set var named PinOut6 = GP7 (physical is 10, gate CLOSE relay)

const uint PinIn1 = 10;      //set var named PinIn1 = GP10 (physical is 14, main input for iVMS/wiegand signal)
const uint PinIn2 = 11;      //set var named PinIn2 = GP11 (physical is 15, input for limit switch #1 signal)
const uint PinIn3 = 12;      //set var named PinIn3 = GP12 (physical is 16, input for light switch signal)
const uint PinIn4 = 13;      //set var named PinIn4 = GP13 (physical is 17, input for limit switch #2 signal)
const uint OpenGate = 1;     //Define input 12v. from iVMS or Wiegand board

int read;                    //Define reciever 12v. from iVMS or Wiegand board
char message[10];
int main() 
{
	bi_decl(bi_program_description("RFID board interchangable"));
	//bi_decl(bi_1pin_with_name(RunPin, "LED on GP17"));
	//Initial standard input/output
	stdio_init_all();        
	//Initial All output pin
	gpio_init(RunPin);		
	gpio_init(PinOut1);
	gpio_init(PinOut2);
	gpio_init(PinOut3);
	gpio_init(PinOut4);
	gpio_init(PinOut5);
	gpio_init(PinOut6);
	//Initial All input pin
	gpio_init(PinIn1);
	gpio_init(PinIn2);
	gpio_init(PinIn3);
	gpio_init(PinIn4);
	//set PinOut to output
	gpio_set_dir(RunPin, GPIO_OUT);
	gpio_set_dir(PinOut1, GPIO_OUT);
	gpio_set_dir(PinOut2, GPIO_OUT);
	gpio_set_dir(PinOut3, GPIO_OUT);
	gpio_set_dir(PinOut4, GPIO_OUT);
	gpio_set_dir(PinOut5, GPIO_OUT);
	gpio_set_dir(PinOut6, GPIO_OUT);
	//set PinIn to input
	gpio_set_dir(PinIn1, GPIO_IN);
	gpio_set_dir(PinIn2, GPIO_IN);
	gpio_set_dir(PinIn3, GPIO_IN);
	gpio_set_dir(PinIn4, GPIO_IN);
	//enable pulldown resistor on ALL PinIn
	gpio_pull_down(PinIn1);
	gpio_pull_down(PinIn2);
	gpio_pull_down(PinIn3);
	gpio_pull_down(PinIn4);
	//define value OFF to ALL PinOut
	gpio_put(PinOut1, 0);
	gpio_put(PinOut2, 0);
	gpio_put(PinOut3, 0);
	gpio_put(PinOut4, 0);
	gpio_put(PinOut5, 0);
	gpio_put(PinOut6, 0);
	//Everything readey to run program
	gpio_put(RunPin, 1);
	puts("Readey to run rpogram\n");
	//check barrier is OPEN or CLOSE?
    gpio_put(PinOut5, 1);
    read = gpio_get(PinIn4);
    if(read!=OpenGate)                      //GATECLOSE is OPEN 
    {
		gpio_put(PinOut6, 1);				//define value to ON 3.3vdc to PinOut6
		while (read != OpenGate)            //limit switch #2 loop
        {
            read = gpio_get(PinIn4);		//read value from limit switch#2
            puts("GATECLOSE is OPEN\n");
            sleep_ms(500);					//delay for 500ms.
        }
        puts("GATECLOSE is CLOSE\n");
        gpio_put(PinOut5, 0);				//define value to OFF 3.3vdc to PinOut5
        gpio_put(PinOut6, 0);				//define value to OFF 3.3vdc to PinOut6
	}
    puts("It's all OK!\n");					//everything OK. ready to run normally
	while (1) 								//main loop
	{
		read = 0;
		gpio_put(PinOut1, 1);		
        while (read != OpenGate)
        {
			read = gpio_get(PinIn1);		//Detect signal from iVMS or wiegand then, OPEN gate relay loop (main loop)
			puts("wait for incoming signal...");
            sleep_ms(500);					//delay for 500ms.
            
        }
		read = 0;
		puts("Detect signal from PinIn1\n");
		gpio_put(PinOut2, 1);				//send signal ON to GATE OPEN (set relay to NO)    
		puts("Open GATE OPEN\n");  
        sleep_ms(1000);                     //time delay for wait barrier up (wait 1 sec.)
        gpio_put(PinOut3, 1);				//send signal ON to limit switch#1 (set relay to NO) 
        puts("wait for signal from limit switch#1\n"); 

		while (read != OpenGate)            //limit switch#1 loop
        {
            read = gpio_get(PinIn2);
            sleep_ms(500);
        }
        read = 0;
        puts("Open GATE OPEN complete\n");
        gpio_put(PinOut2, 0);			//send signal OFF to GATE OPEN
        gpio_put(PinOut3, 0);         	//send signal OFF to limit switch#1
        puts("Close limit switch#1 \n"); 
        puts("CLOSE circuit GATE OPEN\nAnd wait for car/Truck pass 6 sec.\n");
        //#====================
        sleep_ms(6000);                 //wait for car/truck pass six seconds (wait 6 sec.)
        //#====================
        puts("Open light switch\n");
        
        while(read != OpenGate)         //light switch loop
        {
			puts("wait for signal from light switch\n");
            gpio_put(PinOut4, 1);		//Send signal enable to light sensor
            sleep_ms(20);				//delay short time before read again
            read = gpio_get(PinIn3);	//read signal from light sensor
            gpio_put(PinOut4, 0);		//temporary disable light sensor
            sleep_ms(5000);				//wait 5 sec. for obstruction(car/truck) run past
        }
        read = 0;						//restore default value of read
        gpio_put(PinOut4, 0);         	//send signal CLOSE to light sensor
        puts("Close light switch\n");
        sleep_ms(1000);					//wait for GATE CLOSE comedown
        gpio_put(PinOut6, 1);        	//send signal ON to GATE CLOSE (set relay to NO)
        puts("Close GATE CLOSE\n");
        gpio_put(PinOut5, 1);        	//send signal ON to limit switch#2 
        puts("wait for signal from limit switch#2");
        while(read != OpenGate)         //limit switch#2 loop
        {
            read = gpio_get(PinIn4);	
            sleep_ms(500);
        }
        read = 0;								//restore default value of read
        gpio_put(PinOut5, 0);        			//send signal OFF to limit switch#2 
        printf("Close limit switch#2\n");
        gpio_put(PinOut6, 0);           		//send signal OFF to GATE CLOSE
        puts("Close circuit GATE CLOSE\n");
        gpio_put(PinOut1, 0); 					//clear buffer
        sleep_ms(1000);
        puts("Close gate barrier completely\n");
        
        while (read <= 3)
        {													
			gpio_put(RunPin, 0);
			sleep_ms(500);
			gpio_put(RunPin, 1);
			sleep_ms(500);
			read++;
		}
		read = 0;
	}
	
}
