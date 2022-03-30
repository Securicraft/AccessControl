#!/usr/bin/python3.7                             ###use this line when run on raspbian platform
# -*- coding: utf-8 -*-
'''
fixed and update
1. 
'''

import time, sys;
def CheckIPaddress():
    result = [];
    try:
        checkf = open('rfile.txt','w');
        subprocess.call(['hostname'], stdout=checkf);
        checkf.close();
        checkf = open('rfile.txt','a');
        if platform.system() == 'Linux':
            subprocess.call(["sudo", "ifconfig"], stdout=checkf);
        else:
            subprocess.call(["ipconfig"], stdout=checkf);            
        checkf.close();
        checkf = open('rfile.txt','r');
        result.append( re.sub('[\n]', '', checkf.readline()));
        if platform.system() == 'Linux':
            inet  = 'inet';
            inet6 = 'inet6';
        else:
            inet  = 'IPv4 Address';
            inet6 = 'IPv6 Address';
        checkf.close();
        checkf = open('rfile.txt','r');
        for string in checkf:
            if platform.system() == 'Linux':
                if string.find(inet6) > 0:
                    pass;
                if string.find(inet) > 0:
                    if string.strip()[5:-47] != '127.0.0.1':
                        result.append(string.strip()[5:-47]);
            else:
                if string.find(inet6) > 0:
                    pass;
                if string.find(inet) > 0:
                    result.append(string[39:-1]);
        checkf.close();
        checkfile = "rfile.txt";
        if platform.system() == 'Linux':
            subprocess.call(["sudo","rm", "-r", checkfile], );
        else:
            os.remove(checkfile);
    except Exception:
        PrintException(None);
    del checkf, checkfile;
    return result;


def PrintException(args):
    logfilename = time.strftime("%Y%m%d")+'.log';
    logfileopen = open(logfilename,'a',encoding='utf-8');
    if args is None:
        import linecache;
        exc_type, exc_obj, tb = sys.exc_info();
        frame      = tb.tb_frame;
        lineno     = tb.tb_lineno;
        filename   = frame.f_code.co_filename;
        linecache.checkcache(filename);
        fileline   = linecache.getline(filename, lineno, frame.f_globals);
        logfileopen.write('Exception in ({}, Line {} "{}"): {}'.format(filename, lineno, fileline.strip(), exc_obj)+"\n"+time.strftime("%Y-%m-%d <> %H:%M")+"\n");        
        del linecache, frame, fileline, lineno, filename;
    else:
        logfileopen.write(args+"\n");
    logfileopen.close();
    del logfilename, logfileopen;
    return;


try:
    print("Load Standard Library :os, sys, time, datetime, platform, re");
    import io, os, sys, time, datetime, shutil, platform, re, csv;
    import datetime as datetime;
    from time import gmtime, strftime;
    #print("Load Library: stat, fstat, lstat");
    #import stat;
    print("Load Library :subprocess, socket");
    import subprocess;
    import socket;
    print("Load Library :urllib.parse");
    import urllib.parse;
    print("Load Library :configparser, collections");
    import configparser, collections;
    print("Load Library :serial, RPi.GPIO");
    import serial;
    import RPi.GPIO as IO;
    print("Load Library :picamera");
    import picamera
    print("Load Library :socketserver");
    import socketserver
    print("Load Library :threading");
    from threading import Condition
    print("Load Library :HTTPServer");    
    from http import server
    print("Load Library :logging");    
    import logging
    print("Load Library :ssl");    
    import ssl
    
except Exception as err:
    PrintException(None);
    print(err);
    raise SystemExit;
MyDir = os.getcwd();
print("Load Library complete"); 
print("Now working at directory : "+MyDir);

import glob;
filelist = glob.glob('*.csv');
filelist.sort();
if len(filelist) > 0:
    for file in filelist:
        if file == time.strftime("%Y%m%d")+'.csv':
            break;
        else:
            if platform.system() == 'Linux':
                subprocess.call(['sudo', 'rm', '-v', file], );
            else:
                os.remove(file);
del glob;
print("Load necessary variables")

#DEFAULT Section
ConfigFile = 'home.ini';
button1pin = 33;
button2pin = 35;
button3pin = 36;
button4pin = 37;
button5pin = 38;
button6pin = 40;

#ButtonValue Section
button1val = "Switch#1"
button2val = "Switch#2"
button3val = "Switch#3"
button4val = "Switch#4"
button5val = "Switch#5"
button6val = "Switch#6"

#ButtonPosition Section
button1top = 10
button1left = 10

button2top = 10
button2left = 90

button3top = 10
button3left = 170

button4top = 10
button4left = 250

button5top = 10
button5left = 330

button6top = 10
button6left = 410

#FTP Section
ftphost = "192.168.1.33"
ftpuser = "ftpuser"
ftppass = "1234"
ftpport = 21

#NETWORK Section
ipaddress = "192.168.1.33"
hostname = "Securicraft"
nodeid = 247232638966470

'''
Raspi assign 16 pins for INPUT/OUTPUT:
 7, 11, 13, 15
16, 18, 22, 29
31, 32, 33, 35
36, 37, 38, 40
Other pins for 3.3VDC./5.1VDC Supply, Ground, SEND/RECIEVE signal(SPI, I2C, OneWire, Rx/Tx etc.)
'''

IO.setmode(IO.BOARD);
IO.setwarnings(False);

IO.setup(button1pin,IO.OUT);
IO.setup(button2pin,IO.OUT);
IO.setup(button3pin,IO.OUT);
IO.setup(button4pin,IO.OUT);
IO.setup(button5pin,IO.OUT);
IO.setup(button6pin,IO.OUT);

IO.output(button1pin, IO.LOW);
IO.output(button2pin, IO.LOW);
IO.output(button3pin, IO.LOW);
IO.output(button4pin, IO.LOW);
IO.output(button5pin, IO.LOW);
IO.output(button6pin, IO.LOW);
print("Load necessary variables complete")
print("Load configuration from: ", MyDir.strip()+"/"+ConfigFile);

DirList     = os.listdir(os.getcwd());  #file name list in current directory
for line in DirList:                    #Locate to home.ini
    if ConfigFile in DirList:           ###home.ini is exist
        config   = configparser.ConfigParser();
        config.read(ConfigFile);
        button1pin = config['DEFAULT']['button1pin'];
        button2pin = config['DEFAULT']['button2pin'];
        button3pin = config['DEFAULT']['button3pin'];
        button4pin = config['DEFAULT']['button4pin'];
        button5pin = config['DEFAULT']['button5pin'];
        button6pin = config['DEFAULT']['button6pin'];

        button1val = config['ButtonValue']['button1val'];
        button2val = config['ButtonValue']['button2val'];
        button3val = config['ButtonValue']['button3val'];
        button4val = config['ButtonValue']['button4val'];
        button5val = config['ButtonValue']['button5val'];
        button6val = config['ButtonValue']['button6val'];

        ftphost = config['FTP']['ftphost'];
        ftpuser = config['FTP']['ftpuser'];
        ftppass = config['FTP']['ftppass'];
        ftpport = config['FTP']['ftpport'];
       
        IPAddr    = config['NETWORK']['IPAddress'];
        HostName  = config['NETWORK']['hostname'];
        NodeID    = config['NETWORK']['NodeID'];
        MacAddr   = config['NETWORK']['MacAddr'];
        if IPAddr == '':
            from uuid import getnode;
            alist    = CheckIPaddress();
            HostName = alist[0];
            if alist[1] != '':
                IPAddr   = alist[1].strip();
            else:
                IPAddr   = alist[2].strip();            
            NodeID   = getnode();           #Get the hardware address as a 48-bit positive integer <recommended in RFC 4122>
            MacAddr  = hex(NodeID);
            del alist, getnode;
    else:                                   #home.ini not exist
        from uuid import getnode;
        alist    = CheckIPaddress();
        HostName = alist[0];
        if alist[1] != '':
            IPAddr   = alist[1].strip();
        else:
            IPAddr   = alist[2].strip();            
        NodeID   = getnode();               #Get the hardware address as a 48-bit positive integer <recommended in RFC 4122>
        MacAddr  = hex(NodeID);
        del alist, getnode;
        print('Configuration file does not exist, System will create default');
        config   = configparser.ConfigParser(allow_no_value=True);
        config.optionxform = str;
        config['DEFAULT'] = {
            'button1pin': button1pin,
            'button2pin': button2pin,
            'button3pin': button3pin,
            'button4pin': button4pin,
            'button5pin': button5pin,
            'button6pin': button6pin            
            };
        
        config['ButtonValue'] = {
            'button1val': button1val,
            'button2val': button2val,
            'button3val': button3val,
            'button4val': button4val,
            'button5val': button5val,
            'button6val': button6val
            };
        config['ButtonPosition'] = {
            'button1left': button1left,
            'button1top': button1top,
            'button2left': button2left,
            'button2top': button2top,
            'button3left': button3left,
            'button3top': button3top,
            'button4left': button4left,
            'button4top': button4top,
            'button5left': button5left,
            'button5top': button5top,
            'button6left': button6left,
            'button6top': button6top
            };
        config['FTP'] = {
            'ftphost': ftphost,
            'ftpuser': ftpuser,
            'ftppass': ftppass,
            'ftpport': ftpport
            };
        config['NETWORK']   = {
            'IPAddress': IPAddr,
            'HostName': HostName,
            'NodeID' : NodeID,
            'MacAddr' : MacAddr
            };
        for section in config._sections:
            config._sections[section] = collections.OrderedDict(sorted(config._sections[section].items(), key=lambda t: t[0]))
        config._sections = collections.OrderedDict(sorted(config._sections.items(), key=lambda t: t[0] ))
        with open(ConfigFile, 'w') as configfile:
            config.write(configfile);
            configfile.close();
            break;
#------------------------------------------------Create WEB page and all structures.--------------------------------------------

PAGE = """\
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">       
        <title>Home Automation</title>
    </head>
	<style>
	    .background
		{
                    position: absolute;
                    top: 6px;
                    left: 12px;
                    color: white;
		}

	    .btnpos1
		{
                    position: absolute;
		    top: 8px;
		    left: 16px;
		}
	    .btnpos2
		{
		    position: absolute;
		    top: 8px;
		    left: 80px;
		}
            .btnpos3
		{
		    position: absolute;
		    top: 8px;
		    left: 144px;
		}
            .btnpos4
		{
		    position: absolute;
		    top: 8px;
		    left: 208px;
		}
            .btnpos5
		{
		    position: absolute;
		    top: 8px;
		    left: 272px;
		}
            .btnpos6
		{
		    position: absolute;
		    top: 8px;
		    left: 336px;
		}		
	</style>
    <body>
	<p id="btnpos1"/p>
	<p id="btnpos2"/p>
	<p id="btnpos3"/p>
	<p id="btnpos4"/p>
	<p id="btnpos5"/p>
	<p id="btnpos6"/p>
	<div class="left background">
            <left>
		<img src="stream.mjpg" width="640" height="360">
	    /left>
	    <td>
                <input type="button" id="btnpos1" class="btnpos1" value="Switch1" onclick="window.location.href='out1.html'">
	    </td>
	    <td> 
		<input type="button" id="btnpos2" class="btnpos2" value="Switch2" onClick="window.location.href='out2.html'"> 
            </td>
            <td> 
            	<input type="button" id="btnpos3" class="btnpos3" value="Switch3" onClick="window.location.href='out3.html'"> 
            </td>
            <td> 
            	<input type="button" id="btnpos4" class="btnpos4" value="Switch4" onClick="window.location.href='out4.html'">  
            </td>
            <td> 
            	<input type="button" id="btnpos5" class="btnpos5" value="Switch5" onClick="window.location.href='out5.html'"> 
            </td>
            <td> 
            	<input type="button" id="btnpos6" class="btnpos6" value="Switch6" onClick="window.location.href='out6.html'"> 
            </td>
        </div>
    </body>
</html>
""";

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all clients it's available.
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
#-------------------------------------------------------------starting to monitor event ButtonClick------------------------------------------------
        #First 4 lines use to write pseudo web page. And tell Server "Just know, I am ready."
        elif self.path == '/out1.html':
            content = PAGE.encode('utf-8')
            self.send_response(205)
            self.end_headers();            
            self.wfile.write(content)
            if self.ButtonClick(button1pin) != True:
                print("Switch has Error to On/Off!");
        elif self.path == '/out2.html':
            content = PAGE.encode('utf-8')
            self.send_response(205)
            self.end_headers();            
            self.wfile.write(content)
            if self.ButtonClick(button2pin) != True:
                print("Switch has Error to On/Off!");
        elif self.path == '/out3.html':
            content = PAGE.encode('utf-8')
            self.send_response(205)
            self.end_headers();            
            self.wfile.write(content)
            if self.ButtonClick(button3pin) != True:
                print("Switch has Error to On/Off!");
        elif self.path == '/out4.html':
            content = PAGE.encode('utf-8')
            self.send_response(205)
            self.end_headers();            
            self.wfile.write(content)
            if self.ButtonClick(button4pin) != True:
                print("Switch has Error to On/Off!");
        elif self.path == '/out5.html':
            content = PAGE.encode('utf-8')
            self.send_response(205)
            self.end_headers();            
            self.wfile.write(content)
            if self.ButtonClick(button5pin) != True:
                print("Switch has Error to On/Off!");
        elif self.path == '/out6.html':
            content = PAGE.encode('utf-8')
            self.send_response(205)
            self.end_headers();            
            self.wfile.write(content)
            if self.ButtonClick(button6pin) != True:
                print("Switch has Error to On/Off!");
#-------------------------------------------------------------End of event----------------------------------------------------------------
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
    def ButtonClick(self, args):
        self.ref = False;                            #false to On/Off
        self.BStatus = IO.input(int(eval(args)));    #check status ON(1) or OFF(0)
        try:
            if self.BStatus == 0:
                IO.output(int(eval(args)), IO.HIGH);
            else:
                IO.output(int(eval(args)), IO.LOW);
            self.ref = True;                             #success to On/Off
        except Exception as err:
            PrintException(None);
            print(err);
        return self.ref;
        
            
#------------------------------------------------ End of creating --------------------------------------------------------------

print("Everything is up, Start to run script...");
#=======================================#
#=========programme start here==========#
#=======================================#
with picamera.PiCamera(resolution='640x360', framerate=24) as camera:
    camera.vflip = True;    
    output = StreamingOutput();
    camera.start_recording(output, format='mjpeg');
    try:
        address = ('', 8000);
        server = StreamingServer(address, StreamingHandler);
        #-------change HTTP to HTTPS by insert certificate and key .pem wraped to server------------------
        #Before run https MUST generate local SSL
        #By:
        
        #Option 1 use openssl library
        #openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

        #Option 2 use server.socket 
        #server.socket = ssl.wrap_socket(server.socket, server_side=True, certfile='server.pem', ssl_version=ssl.PROTOCOL_TLSv1);
        #ONLY 1 option for use this case
        #-------------------------------------------------------------------------------------------------
        server.serve_forever()
    finally:
        camera.stop_recording()
        IO.cleanup();
        print('Program ended.')                                                                
#=======================================#
#========= programme end here ==========#
#=======================================#

