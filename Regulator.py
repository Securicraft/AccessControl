#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
'''
First two lines MUST add on top in python script that run on RaspberryOS/raspbian
1st. line, tell system where is python interpreter
2nd. line, tell system use utf-8 unicode
'''
def PrintException(args):
    '''Correct all error to text file'''
    import linecache;
    exc_type, exc_obj, tb = sys.exc_info();
    frame       = tb.tb_frame;
    lineno      = tb.tb_lineno;
    filename    = frame.f_code.co_filename;
    linecache.checkcache(filename);
    fileline    = linecache.getline(filename, lineno, frame.f_globals);
    logfilename = time.strftime("%Y%m%d")+'.errlog';
    logfileopen = open(logfilename,'a');
    if args is None:        #debug script with argrument None is tracing error line in script
        logfileopen.write('Exception in ({}, Line {} "{}"): {}'.format(filename, lineno, fileline.strip(), exc_obj)+"\n"+time.strftime("%Y-%m-%d <> %H:%M")+"\n");        
    else:
        logfileopen.write(str(args)+ " : " +datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"+"\n"));
        logfileopen.write('Exception in ({}, Line {} "{}"): {}'.format(filename, lineno, fileline.strip(), exc_obj)+"\n"+time.strftime("%Y-%m-%d <> %H:%M")+"\n");                
    logfileopen.close();
    del linecache, frame, fileline, lineno, filename, logfilename, logfileopen;
    return;

def CreateList():
    file = open("ip.c", "w");
    file.write("//From https://man7.org/linux/man-pages/man3/getifaddrs.3.html\n");
    file.write("#define _GNU_SOURCE \n");
    file.write("#include <arpa/inet.h>\n");
    file.write("#include <sys/socket.h>\n");
    file.write("#include <netdb.h>\n");
    file.write("#include <ifaddrs.h>\n");
    file.write("#include <stdio.h>\n");
    file.write("#include <stdlib.h>\n");
    file.write("#include <unistd.h>\n");
    file.write("#include <string.h>\n");
    file.write("#define LSIZ 128 \n");
    file.write("#define RSIZ 10 \n");
    file.write("int main(int argc, char *argv[])\n");
    file.write("{\n");
    file.write("struct ifaddrs *ifaddr;\n");
    file.write("int family, s;\n");
    file.write("char host[NI_MAXHOST];\n");
    file.write("FILE *fptr;\n");
    file.write('fptr = fopen("ip.txt", "w");\n');
    file.write("if (getifaddrs(&ifaddr) == -1)\n");
    file.write("{\n");           
    file.write("perror('getifaddrs');\n");
    file.write("exit(EXIT_FAILURE);\n");
    file.write("}\n");
    file.write("for (struct ifaddrs *ifa = ifaddr; ifa != NULL;\n");
    file.write("ifa = ifa->ifa_next)\n");
    file.write("{\n");
    file.write("if (ifa->ifa_addr == NULL)\n");
    file.write("continue;\n");
    file.write("family = ifa->ifa_addr->sa_family;\n");
    file.write("if (family == AF_INET || family == AF_INET6) {\n");
    file.write("s = getnameinfo(ifa->ifa_addr,(family == AF_INET) ? sizeof(struct sockaddr_in) : sizeof(struct sockaddr_in6), host, NI_MAXHOST, NULL, 0, NI_NUMERICHOST);\n");
    file.write("if (s != 0) {\n");
    file.write('printf("getnameinfo() failed: %s ", gai_strerror(s));\n');
    file.write("exit(EXIT_FAILURE);\n");
    file.write("}\n");
    word = R'fprintf(fptr, "%s\n", host);'
    file.write(word+"\n");   #save result to file
    file.write("}\n");        
    file.write("else if (family == AF_PACKET && ifa->ifa_data != NULL) {\n");
    file.write("struct rtnl_link_stats *stats = ifa->ifa_data;\n");
    file.write("}\n");
    file.write("}\n");
    file.write("fclose(fptr);\n");
    file.write("freeifaddrs(ifaddr);\n");
    
    file.write("char line[RSIZ][LSIZ];\n");
    file.write('FILE *fp = fopen("ip.txt", "r");\n');
    file.write("int i = 0;\n");
    file.write("while(fgets(line[i], LSIZ, fp))\n");
    file.write("{\n");    
    file.write("line[i][strlen(line[i]) - 1] = '\0';\n");
    file.write("i++;\n");
    file.write("}\n");
    file.write("return (line[1], line[4]);\n");
    file.write("}\n");
    file.close();
    del file;
    return;
def IpAndMac():
    CreateList();
    p = subprocess.run(["gcc","-w", "ip.c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        print(p.stderr);
        raise SystemExit;
    subprocess.call(["sudo", "./a.out"])
    subprocess.call(["sudo", "rm", "a.out"])
    subprocess.call(["sudo", "rm", "ip.c"])
    file = open("ip.txt", "r", encoding='UTF-8');
    lines = file.readlines();
    file.close();
    subprocess.call(["sudo", "rm", "ip.txt"])
    if len(lines) >= 5:                         #eth0 With wlan0
        x = re.search("%", lines[4].strip());
        mac = lines[4][0:x.span()[0]];             #Cut "%eth0"
        return (lines[1].strip(), mac);
    elif len(lines) >= 3:                       #eth0 or wlan0        
        x = re.search("%", lines[3].strip());
        mac = lines[3][0:x.span()[0]]           #Cut "%eth0 or %wlan0"
        return (lines[1].strip(), mac);
    else:
        print("NOT detect ethernet network!\n  Consult your admin\n  Application will sutdown");
        raise SystemExit;
    del file, p, lines,x
    
'''Main script start here'''
DB = "";
try:
    import time, sys, subprocess;
    print("Load Standard Library :os, sys, time, datetime, platform, re, csv");
    import os, sys, time, datetime, shutil, platform, re, csv;
    import datetime as datetime;
    from time import gmtime, strftime;
    import os.path;
    print("Load Library :subprocess, socket");
    import subprocess;
    import socket;
    print("Load Library :configparser, collections");
    import configparser, collections;
    print("Load Library :requests");
    print("Load Library :threading");
    import threading, queue;
    from threading import Thread;
    try:
        import mysql.connector as DB;
        #import MySQLdb as DB
        #import MySQLdb.cursors as cursors
        
    except Exception as err:
        PrintException(err);
        print("Must install dependencied library before use");
        print("sudo pip3 install MySQL-python");
        print("system will use userinfo.txt, If it exist please wait...");
        from os import path
        if path.isfile("userinfo.txt"):
            pass;
        else:
            print("Sorry! not has user information");
            print("System will exit");
            raise SystemExit;
    print("Load Library complete");
except Exception as err:
    PrintException(None);
    print(err);
    raise SystemExit;

MyDir = os.getcwd();
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
del glob, filelist;
print("Load necessary variables")

#Default value
UserInfo    = 'userinfo.txt';
ConfigFile  = 'reader.conf';
EventFile   = 'event.txt';

DOORTYPE = 0;                       #Type of access, 0=ENTER and 1=EXIT, default = 0
DOORDELAY   = 5;                    ###Delay times(sec.) for door open
DOWNLOADTIME= 5;                    ###iNTERVAL TIME FOR CHECK USER INFORM.(Min.)

SQLHOST     = '192.168.1.133';                ###MySQL or MSSQL Server
SQLUSER     = 'root';
SQLPASS     = 'm6045001';
DATABASE    = 'userinfo';
SQLPORT     = 3306;

LOCALHOST     = '127.0.0.1';            ###FTP Server
LOCALUSER     = 'admin';                 ###User name on target server
LOCALPASS     = 'm6045001';                    ###Password
LOCALPORT     = 3306;                        ###Default SFTP port

blist = [];                             ###manisfest list name 'blist' that will store userinfo.txt along this script
DirList     = os.listdir(os.getcwd());  ###file name list in current directory

print("Load necessary variables complete")
print("Load configuration ...");
for line in DirList:
    if(re.match(UserInfo, line)):
        UserInfo = (line.rstrip()).lstrip();
    if(re.match(EventFile, line)):
        EventFile = (line.rstrip()).lstrip();

    config   = configparser.ConfigParser();
    if ConfigFile in DirList:                   ###reader.conf is exist
        config.read(ConfigFile);
        
        SQLHOST  = config['SQLServer']['sqlhost'];
        SQLUSER  = config['SQLServer']['sqluser'];
        SQLPASS  = config['SQLServer']['sqlpass'];
        DATABASE = config['SQLServer']['database'];
        SQLPORT  = config['SQLServer']['sqlport'];
        
        LOCALHOST  = config['LOCALServer']['LOCALhost'];
        LOCALUSER  = config['LOCALServer']['LOCALuser'];
        LOCALPASS  = config['LOCALServer']['LOCALpass'];
        LOCALPORT  = int(config['LOCALServer']['LOCALport']);
        
        UserInfo  = config['DEFAULT']['userinfo'];
        EventFile = config['DEFAULT']['EventFile'];
        DOORTYPE  = config['DEFAULT']['DOORTYPE'];
        DOORDELAY = int(config['DEFAULT']['DOORDELAY']);
        DOWNLOADTIME = int(config['DEFAULT']['DOWNLOADTIME']);
        
        IPAddr    = config['NETWORK']['ipaddress'];
        HostName  = config['NETWORK']['hostname'];
        NodeID    = config['NETWORK']['nodeid'];
        
    else:                                       ###reader.conf is not exist
        i = IpAndMac();
        from subprocess import check_output
        print('Configuration file does not exist, System will create default');

        config['DEFAULT'] ={'UserInfo': UserInfo,
                            'EventFile': EventFile,
                            'DOORTYPE' : DOORTYPE,
                            '#DOORTYPE': "Type of access, 0=ENTER and 1=EXIT, default = 0",
                            'DOORDELAY' : DOORDELAY,
                            '#DOORRELAY': "Delay times(sec.) for door open then, close it., default = 5",
                            'DOWNLOADTIME': DOWNLOADTIME
                             };        
    
        config['SQLServer'] = {'SQLHOST':SQLHOST,
                         'SQLUSER':SQLUSER,
                         'SQLPASS':SQLPASS,
                         'DATABASE':DATABASE,
                         'SQLPORT':SQLPORT
                         };
        config['LOCALServer'] = {'LOCALHOST':LOCALHOST,
                 'LOCALUSER': LOCALUSER,
                 'LOCALPASS': LOCALPASS,
                 'LOCALPORT': LOCALPORT
                 };
        config['NETWORK'] ={
            'ipaddress': i[0],
            '#IPAddress': "IP Address of this device.",
            'HostName': check_output(['hostname']).decode("utf-8").rstrip(),
            '#HostName': "Name of this device.",
            'NodeID' : i[1],
            '#NodeID': "UUID of this device in 16bitBase.",
            };
        del check_output;
        with open('reader.conf', 'w') as configfile:
            config.write(configfile);
            configfile.close();
        config.read(ConfigFile);
        SQLHOST  = config['SQLServer']['sqlhost'];
        SQLUSER  = config['SQLServer']['sqluser'];
        SQLPASS  = config['SQLServer']['sqlpass'];
        DATABASE = config['SQLServer']['database'];
        SQLPORT  = config['SQLServer']['sqlport'];
        LOCALHOST  = config['LOCALServer']['LOCALhost'];
        LOCALUSER  = config['LOCALServer']['LOCALuser'];
        LOCALPASS  = config['LOCALServer']['LOCALpass'];
        LOCALPORT  = int(config['LOCALServer']['LOCALport']);
        UserInfo  = config['DEFAULT']['userinfo'];
        EventFile = config['DEFAULT']['EventFile'];
        DOORDELAY = int(config['DEFAULT']['DOORDELAY']);
        DOWNLOADTIME = int(config['DEFAULT']['DOWNLOADTIME']);
        IPAddr    = config['NETWORK']['ipaddress'];
        HostName  = config['NETWORK']['hostname'];
        NodeID    = config['NETWORK']['nodeid'];
        break;
del line, DirList

print("Load configuration complete");
# Propose:-   for syncronized data between DatabaseServer and localServer
# Work on event:-
# 1. @time in cycle loop (time.sleep);
# 2. When found new DeviceID in Devices, Priviledge tables
# 3. When found event in log table
while True:
    #Case #1 ====================================================================
    cnx = DB.connect( user = SQLUSER,
                      password= SQLPASS,
                      host    = SQLHOST,
                      port    = int(SQLPORT),
                      database= DATABASE)
    curs   = cnx.cursor();
    #==================================================
    '''
    SQLList = ["SELECT `users`.`SSN` AS `ssn`,CONVERT(CAST(`users`.`fname` as BINARY) USING utf8) as `name`,`users`.`RFID` AS `rfid`,`users`.`date_update` AS `updates`,`devices`.`nodeID` AS `nodeID`",
                " FROM users, devices, privilege",
                " WHERE privilege.userID LIKE users.ID",
                " AND devices.active = 1 ",
                " AND users.status = 1",
                " AND devices.nodeID = %s;"
                ];
    '''
    SQLList = ["SELECT ssn, name, rfid, updates, nodeID FROM userinfo where nodeID = %s;"];
    #SQLList = ["SELECT * FROM userinfo WHERE userinfo.nodeID = %s;"];
    start = float(datetime.datetime.utcnow().timestamp());
    #curs.execute(SQLList[0]+SQLList[1]+SQLList[2]+SQLList[3]+SQLList[4]+SQLList[5], (str(NodeID),));
    curs.execute(SQLList[0], (str(NodeID),));
    #===================================================
    end = float(datetime.datetime.utcnow().timestamp());
    print("time in SQL SELECT from DataServer is ", "{:.2f}".format( (end - start)) );
    if curs:
        conn = DB.connect( user     = LOCALUSER,
                           password = LOCALPASS,
                           host     = LOCALHOST,
                           port     = int(LOCALPORT),
                           database = DATABASE)
        #create table
        sql00 = "SELECT GET_LOCK('userinfo',-1)";       #lock table before DROP/CREATE infinite timeout
        sql01 = "SELECT RELEASE_LOCK('userinfo')";      #Unlock table  
        sql1 = "DROP TABLE if EXISTS userinfo;";
        #===============================================
        sql2 = "CREATE TABLE userinfo (ssn varchar(20), name varchar(255), rfid varchar(255), updates varchar(255), nodeID varchar(255) );";
        sql3 = "INSERT INTO userinfo (ssn, name, rfid, updates, nodeID) VALUES (%s, %s, %s, %s, %s);"
        #===============================================        
        start = float(datetime.datetime.utcnow().timestamp())
        
        cur = conn.cursor();        
        cur.execute(sql00);                             #Lock table userinfo
        cur.fetchall()
            
        cur = conn.cursor();
        cur.execute(sql1);
        cur.close();
        conn.commit();

        cur = conn.cursor();
        cur.execute(sql2);
        cur.close();
        conn.commit();
            
        cur = conn.cursor();        
        cur.execute(sql01);                             #Unlock table userinfo
        cur.fetchall()
            
        #INSERT INTO userinfo ON localserver from dataserver line by line
        for row in curs:
            cur = conn.cursor();
            cur.execute(sql3, row)
            cur.fetchone()
            cur.close();
        conn.commit()
        conn.close();
        curs.close();
        cnx.commit();
        cnx.close();
        #================
        print(row)
        #================
        end = float(datetime.datetime.utcnow().timestamp())
    print("time in SQL INSERT to LocalServer is ", "{:.2f}".format((end - start)) )
    
    #End case #1 ================================================================
        
    #Case #2 ====================================================================
    InsertID = False;                   #Logic for check this reader is registed in DataServer ready?
    PsudouserID = 1;
    PsudonodeID = "PsudonodeID";
    cnx = DB.connect( user = SQLUSER,
                      password= SQLPASS,
                      host    = SQLHOST,
                      port    = int(SQLPORT),
                      database= DATABASE)
    curs   = cnx.cursor();
    SQLList = ["SELECT nodeID FROM devices;"];
    curs.execute(SQLList[0]);
    if curs:
        for line in curs:
            if (line[0] == NodeID):     #If "line[0] == NodeID is True" means this reader HAVE been registed in DatabaseServer
                InsertID = True;
    curs.close();
    cnx.close();        
    if InsertID != True:                #This reader NEVER been registed on DatabaseServer        
        curs.close();
        cnx.close();        
        cnx = DB.connect( user     = SQLUSER,
                          password = SQLPASS,
                          host     = SQLHOST,
                          port     = int(SQLPORT),
                          database = DATABASE)
        curs = cnx.cursor();
        SQLList = ["INSERT INTO devices (nodeID, active) VALUES (%s, %s)"];
        curs.execute( SQLList[0], (str(NodeID), 1) );
        curs.close();
        cnx.commit();
        '''
        #search is priviledge exist?
        curs = cnx.cursor();
        SQLList = ["SELECT nodeID FROM privilege WHERE privilege.nodeID = %s"];
        curs.execute( SQLList[0], (str(NodeID),) );
        curs.fetchall();
        if curs.rowcount <= 0:   #This privilege NOT EXIST
            curs = cnx.cursor();
            SQLList = ["SELECT userID FROM privilege ORDER BY userID DESC LIMIT 1;"];
            curs.execute(SQLList[0]);
            if curs:
                for line in curs:pass;PsudouserID = line[0]+1   # Step-up 1 to last userID (by @Naihin algoritm)
            #PsudonodeID = 2;                                   # Default value (by @Naihin algoritm)
            SQLList = ["INSERT INTO privilege (userID, nodeID) VALUES (%s, %s)"];
            #curs.execute( SQLList[0], (PsudouserID, PsudonodeID) );
            curs.execute( SQLList[0], (PsudouserID, NodeID) );
            cnx.commit();
        '''
    curs.close();
    cnx.close();
    #End case #2 ================================================================
    
    #Case #3 ====================================================================
    conn = DB.connect(user     = LOCALUSER,
                      password = LOCALPASS,
                      host     = LOCALHOST,
                      port     = int(LOCALPORT),
                      database = DATABASE)
    SQLList = ["SELECT * FROM log"];
    cur     = conn.cursor();
    cur.execute(SQLList[0]);
    if cur:
        #INSERT log into DataServer
        if 'pymssql'.lower() in str(DB):
            SQLPORT = 1433;
        elif 'mysql'.lower() in str(DB):
            SQLPORT = 3306;
        cnx = DB.connect(user    = SQLUSER,
                         password= SQLPASS,
                         host    = SQLHOST,
                         port    = SQLPORT,
                         database= DATABASE)
        sql00 = "SELECT GET_LOCK('log',-1)";        #lock table before DROP/CREATE/DELETE/INSERT infinite timeout
        sql01 = "SELECT RELEASE_LOCK('log')";       #Unlock table
        SQLList = "INSERT INTO log(ssn, devices, status, checktype) VALUES (%s, %s, %s, %s)";
        start = float(datetime.datetime.utcnow().timestamp());        
        curs = cnx.cursor();        
        curs.execute(sql00);                        #Lock table log
        curs.fetchall()
        curs.close();
        for line in cur:
            curs = cnx.cursor();
            curs.execute(SQLList, (line[1], line[2], line[3], line[4]));
            cnx.commit();            
            curs.close();
        curs = cnx.cursor();        
        curs.execute(sql01);                        #Unlock table log
        curs.fetchall();
        curs.close();
        cnx.close();
        end = float(datetime.datetime.utcnow().timestamp());
        print("time in SQL INSERT log table to DataServer is ", "{:.2f}".format((end - start)) );
        cur.close();
        #Delete ALL logs from localServer
        conn = DB.connect(user     = LOCALUSER,
                          password = LOCALPASS,
                          host     = LOCALHOST,
                          port     = int(LOCALPORT),
                          database = DATABASE)
        SQLList = "TRUNCATE TABLE log";
        cur     = conn.cursor();
        cur.execute(SQLList);
        cur.close();
        conn.close();
    #End case #3 ================================================================
    print("Ready to start controller")
    time.sleep(30*60);           #wait 0.10mins.(600secs.) then, repeat sync.
