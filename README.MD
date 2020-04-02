
# MPyCntrl

Control MicroPython with your own coding

## Drop in architecture with pttydev

can be used with minor changes with [pttydev](https://github.com/kr-g/pttydev)

***don't forget to use `ptty.waitready()` after `open()`***

pttydev sample code [sample_pttydev.py](https://github.com/kr-g/mpycntrl/blob/master/sample_pttydev.py)


## Code


sample code is in the github repo here [sample.py](https://github.com/kr-g/mpycntrl/blob/master/sample.py)

                

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

