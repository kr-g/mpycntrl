
import serial # its pyserial 
from mpycntrl import *

def sample_code():
    
    debug = True # display more information 

    port = '/dev/ttyUSB0'
    baud = 115200
    bytesize = 8
    parity = 'N'
    stopbits = 1
    timeout = .35

    with serial.Serial(port=port, baudrate=baud,
                       bytesize=bytesize, parity=parity, stopbits=stopbits,
                       timeout=timeout) as ser:

        mpyc = MPyControl(ser,debug=debug)
            
        # enter raw-repl mode
        r = mpyc.send_cntrl_c()
        print( "received", r )
        
        # get directory listing
        r = mpyc.cmd_ls()
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
            
sample_code()
