import machine;
import utime;
#Pin assign from GPIO not physical 
OpenGate = 1;                                   #Define value when recieve 12v. from iVMS or Wiegand board
read = 0;                                       #Define value to receive sinal from pinIn
PinOut1 = machine.Pin(2, machine.Pin.OUT);      #physical is 4, main relay      
PinOut2 = machine.Pin(3, machine.Pin.OUT);      #physical is 5, GATEOPEN relay
PinOut3 = machine.Pin(4, machine.Pin.OUT);      #physical is 6, limit switch #1 relay             
PinOut4 = machine.Pin(5, machine.Pin.OUT);      #physical is 7, light sensor relay
PinOut5 = machine.Pin(6, machine.Pin.OUT);      #physical is 9,limit switch #2 relay
PinOut6 = machine.Pin(7, machine.Pin.OUT);      #physical is 10, GATECLOSE relay

PinOut1.value(0);
PinOut2.value(0);
PinOut3.value(0);
PinOut4.value(0);
PinOut5.value(0);
PinOut6.value(0);

PinIn1 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN);       #physical is 14, main input for iVMS/wiegand signal
PinIn2 = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_DOWN);       #physical is 15, input for limit switch #1 signal
PinIn3 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN);       #physical is 16, input for light switch signal
PinIn4 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN);       #physical is 17, input for limit switch #2 signal

PinOut1.value(1);                               #innitiate value to PinOut1 for patrol
while True:
    print("Program start again...");
    read = PinIn1.value();
    if  read == OpenGate:              #Detect signal from iVMS or wiegand then, OPEN gate relay loop (main loop)
        PinOut1.value(0);                       #Disable value for encapsulate system
        print("Power ON gate OPEN");
        PinOut2.value(1);                       #send signal to ON GATEOPEN (set relay to OPEN)
        utime.sleep(0.5);                       #time delay for wait barrier start it up
        PinOut3.value(1);                       #send signal to OPEN limit switch #1
        print("Open limit switch #1"); 
        #wait for barrier OPEN ready (limit switch#1 close itself)
        read = PinIn2.value();
        while read != OpenGate:       #limit switch#1 loop
            read = PinIn2.value();
            print("limit swirch#1=", read)
            utime.sleep(0.5);
        read = 0;                               #reset read to default
        PinOut2.value(0);                       #send signal to OFF GATEOPEN (set relay to CLOSE)
        PinOut3.value(0);                       #send signal to CLOSE limit switch #1
        print("Power OFF gate OPEN");
        print("Close limit switch #1");
        utime.sleep(6);                         #Wait for truck or car come in area
        PinOut4.value(1);                       #send signal to OPEN light sensor
        print("Open light switch");
        #loop to check is light sensor detect car pass?
        #read = PinIn3.value();
        while read != OpenGate:       #light switch loop
            read = PinIn3.value();
            print("light switch=", read);
            utime.sleep(1);
        read = 0;                               #reset read to default
        PinOut4.value(0);                       #send signal to CLOSE light sensor
        print("Close light switch");
        print("Power ON gate CLOSE");
        PinOut5.value(1);                       #send signal to OPEN limit switch #2
        utime.sleep(0.5);
        PinOut6.value(1);                       #send signal to ON GATECLOSE (set relay to CLOSE)
        print("Open limit switch #2"); 
        #wait for barrier CLOSE ready (limit switch#1 close itself
        while read != OpenGate:       #limit switch loop
            read = PinIn4.value();
            print("limit switch#2=", read);
            utime.sleep(0.5);
        PinOut1.value(0);                       #set patrol state to OFF
        print("Close limit switch #2"); 
        PinOut5.value(0);                       #send signal to OFF gate CLOSE
        PinOut6.value(0);                       #send signal to CLOSE limit switch #2
        print("Power OFF gate CLOSE"); 
        print("Close gate barrier completely!");
        utime.sleep(1);
        PinOut1.value(1);
    else:
        try:
            utime.sleep(1);
            pass;
        except:
            PinOut1.value(0);
            PinOut2.value(0);
            PinOut3.value(0);
            PinOut4.value(0);
            PinOut5.value(0);
            PinOut6.value(0);
            break;