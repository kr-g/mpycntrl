
import serial # its pyserial 
from mpycntrl import *

#
# pttydev must installed manually before!!!
#
from pttydev import *


def get_pttyopen():

    port = '/dev/ttyUSB0'
    baudrate = 115200
    bytesize = 8
    parity = 'N'
    stopbits = 1
    timeout = 0.25

    return pttyopen(port=port, baudrate=baudrate,
                    bytesize=bytesize, parity=parity, stopbits=stopbits,
                    timeout=timeout)

# put here the board IP adr
IP_ADR = "192.168.178.30"
IP_ADR = "192.168.178.26"

IP_PORT = 8266
IP_PASS = "123456"


def get_pttywsopen():
    # check this !!!
    # ESP32 delay 0.3-0.5
    # ESP8266 delay 0.01
    delay = 0.5
    return pttywsopen( f"ws://{IP_ADR}:{IP_PORT}", IP_PASS, write_delay=delay )

    
def sample():
    
    debug = True # display more information 
    trace = False # display no detail trace information 

    tty = PseudoTTY(
                    # uncomment the part you want to test
                    get_pttyopen,
                    #get_pttywsopen,
                    
                    #thrd_reader=_the_thread_reader,
                    
                    timeout=0.35,
                    block_size=512,
                    reconnect_delay=1,
                    
                    debug=True,
                    #trace_on=True,                    
                    thrd_debug=True,
                    thrd_trace_on=True
                    )

    with tty.open() as octx:
        
        octx.waitready()
        
        mpyc = MPyControl(octx,debug=debug,trace=trace)
        
        # enter raw-repl mode
        r = mpyc.send_cntrl_c()
        print( "received", r )
        
        # get directory listing
        r = mpyc.cmd_ls()
        print( "received", r )
        # get directory listing
        r = mpyc.cmd_ls()
        print( "received", r )
        # get directory listing
        r = mpyc.cmd_ls()
        print( "received", r )

        # get a hash for boot.py
        r = mpyc.cmd_hash("boot.py")
        print( "received", r )

        # create folders
        r = mpyc.cmd_mkdirs("www/others")
        print( "received", r )

        # create folders again, check result !
        r = mpyc.cmd_mkdirs("www/others")
        print( "received", r )

        # create a file 
        r = mpyc.cmd_put( "www/test.txt", content = b"read this!!!\n" )
        print( "received", r )

        # get and print the former created file
        r = mpyc.cmd_get( "www/test.txt" )
        print( "received", r )

        # create a second file
        r = mpyc.cmd_put( "www/test2.txt", content = b"read this too!!!\n" )
        print( "received", r )

        # get a directory listing
        r = mpyc.cmd_ls("www")
        print( "received", r )
        # print file and size and type
        for f,stat in r.items():
            type = "file" if stat[0] & 0x8000 != 0 else "dir"
            print( type, stat[6], f)

        # remove second file
        r = mpyc.cmd_rm( "www/test2.txt" )
        print( "received", r )

        # get a directory listing
        r = mpyc.cmd_ls("www")
        print( "received", r )

        # remove all created files and folders 
        # increase timeout due to longer running task 
        with mpyc.timeout( 1 ) as to:
            r = mpyc.cmd_rm_r("www")
            print( "received", r )
            print( "execution time:", to.diff_time() )
            
        # get some info from micropython
        r = mpyc.send_collect_ids()
        print( "received", r )

        # get a hash for boot.py
        r = mpyc.cmd_hash("boot.py")
        print( "received", r )

        # hard reset the micropython board
        r = mpyc.send_hardreset()
        print( "received", r )
        
        # follow the output
        # loop until users breaks with cntrl+c
        while True:
            r = mpyc.readlines()        
            for l in r:
                print( r )
            
            
if __name__=='__main__':
    sample()

