
# MPyCntrl

Control MicroPython with your own coding

## Drop in architecture with pttydev

can be used with minor changes with [pttydev](https://github.com/kr-g/pttydev)

sample code [sample_pttydev.py](https://github.com/kr-g/mpycntrl/sample_pttydev.py)

the websocket device is __experimental__ and will fail when sending longer strings (commands) to MicroPython


## Code


    import serial # its pyserial 
    from mpycntrl import *

    def sample_code():
        
        debug = True # display more information 
        trace = False # display no detail trace information 

        port = '/dev/ttyUSB0'
        baud = 115200
        bytesize = 8
        parity = 'N'
        stopbits = 1
        timeout = .35

        with serial.Serial(port=port, baudrate=baud,
                           bytesize=bytesize, parity=parity, stopbits=stopbits,
                           timeout=timeout) as ser:

            mpyc = MPyControl(ser,debug=debug,trace=trace)
                
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
                
            # get some info from micropython
            r = mpyc.send_collect_ids()
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
                


                

## cmd line


display all available cmd line options with


    python3 -m mpycntrl -h

    usage: __main__.py [-h] [-v] [-port PORT] [-baud BAUD] [-bytesize BYTESIZE]
                       [-parity {N,E,O}] [-stopbits STOPBITS] [-timeout TIMEOUT]
                       [-trace] [-debug] [-showtime] [-follow]
                       [-maxretry MAXRETRY] [-blocksize BLOCKSIZE] [-translate]
                       [-eval EVAL | -reset | -hardreset | -cntrlc | -meminfo | -ls [PATH]
                       | -ll [PATH] | -rm PATH | -mkdir PATH | -rmdir PATH | -get
                       PATH PATH | -put PATH [PATH ...]]

    Control MicroPython via cmd line

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version info and exit
      -port PORT, -p PORT   port/device to use (default: /dev/ttyUSB0)
      -baud BAUD, -b BAUD   baud rate to use (default: 115200)
      -bytesize BYTESIZE, -cs BYTESIZE
                            bytesize to use (default: 8)
      -parity {N,E,O}       parity to use (default: N)
      -stopbits STOPBITS    stopbits to use (default: 1)
      -timeout TIMEOUT, -to TIMEOUT
                            timeout in sec to use (default: 0.35)
      -trace, -t            display trace info (default: False)
      -debug, -d            display debug info (default: False)
      -showtime             display execution time (default: False)
      -follow, -f           don't exit, keep following the output of MicroPython
                            (default: False)
      -maxretry MAXRETRY, -max MAXRETRY
                            max number of retries to connect (default: 3)
      -blocksize BLOCKSIZE, -bs BLOCKSIZE
                            blocksize during file transfer (default: 512)
      -translate, -tr       translate response as string where possible (default:
                            False)
      -eval EVAL, -exe EVAL, -run EVAL, -e EVAL
                            send source code to MicroPython and execute
      -reset, -r            reset MicroPython by sending cntrl + D, soft restart
      -hardreset, -R        hard reset MicroPython
      -cntrlc, -c           send break cntrl + C
      -meminfo, -i          get memory info
      -ls [PATH]            list directory
      -ll [PATH]            long list directory as json with stat_result. refer to
                            os.stat() for more details
      -rm PATH              remove file
      -mkdir PATH, -mk PATH
                            create folders including sub folders, returns array of
                            tupels which dirs where created. returns false if
                            directory is already existing
      -rmdir PATH, -rd PATH
                            remove folder and all containing files and sub folders
      -get PATH PATH        get file from MicroPython
      -put PATH [PATH ...]  put file on MicroPhyton

