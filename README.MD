
# MPyCntrl

Control MicroPython with your own coding

## Drop in architecture with pttydev

can be used with minor changes with [pttydev](https://github.com/kr-g/pttydev)

***don't forget to use `ptty.waitready()` after `open()`***

pttydev sample code [sample_pttydev.py](https://github.com/kr-g/mpycntrl/blob/master/sample_pttydev.py)


## Code


sample code is in the github repo here [sample.py](https://github.com/kr-g/mpycntrl/blob/master/sample.py)

                

## cmd line


display all available cmd line options with `-h`


    usage: python3 -m mpycntrl [DEVICE-PARAMETER] [options]

    Control MicroPython via cmd line

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version info and exit
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
      -reconnect RECONNECT_AFTER
                            reconnect delay when connection breaks (default: 1)
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
      -get PATH [PATH ...]  get file from MicroPython
      -put PATH [PATH ...]  put file on MicroPhyton
      -hash FILE            get hash value for a file

    PTTY:
      websocket parameter

      -host IP, -ip IP      ip adress to use (default: None)
      -hostport PORT, -ipport PORT, -ipp PORT
                            ip port to use (default: 8266)
      -passwd PASSWD, -pass PASSWD, -pwd PASSWD
                            password to use (default: 123456)
      -ipdelay DELAY        delay for writing 255 byte blocks (default: 0.5)

    TTY:
      serial parameter

      -port PORT, -p PORT   port/device to use (default: /dev/ttyUSB0)
      -baud BAUD, -b BAUD   baud rate to use (default: 115200)
      -bytesize BYTESIZE, -cs BYTESIZE
                            bytesize to use (default: 8)
      -parity {N,E,O}       parity to use (default: N)
      -stopbits STOPBITS    stopbits to use (default: 1)


