
import serial # its pyserial 
from mpycntrl import *

##
##def get_pttyopen():
##
##    port = '/dev/ttyUSB0'
##    baudrate = 115200
##    bytesize = 8
##    parity = 'N'
##    stopbits = 1
##    timeout = 0.25
##
##    return pttyopen(port=port, baudrate=baudrate,
##                    bytesize=bytesize, parity=parity, stopbits=stopbits,
##                    timeout=timeout)
##


from websocket import *
import socket


class pttyws():
    
    def __init__(self,timeout=0):
        self.ws = None
        self.timeout = timeout
        self.buf = bytearray()

    def open(self,url,password):
        
        self.ws = create_connection(url,
                                    timeout=self.timeout,
                                    sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),)
                                    )

        #ws.sock.setblocking(0)
        
        r =  self.ws.recv()
        print("dev got", r )
        if r.find("Password:")>=0:
            self.ws.send(password+"\n")
        r = self.ws.recv()
        print("dev got", r )
        if r.find("WebREPL connected")>=0:
            return self
        
        raise Exception( "wrong password, additional information", r)

    def read(self,size=1):
        while True:
            #self.print("read", "waiting" )
            if size==-1:
                pos = self.buf.find(ord("\r"))
                #print("crlf",pos)
                if pos>=0:
                    if self.buf[pos+1]==ord("\n"):
                        size = pos+2
            l = len(self.buf)
            if l>=size and size!=-1:
                #print(len(self.buf),size)
                r = self.buf[:size]
                self.buf = self.buf[size:]
                self.print("read", r)
                return r
            try:
                r = self.ws.recv()
                if r!=None:
                    r = r.encode()
                    self.buf.extend(r)
                    self.print("got", r, self.buf )
            except WebSocketTimeoutException:
                return None
            
    def readline(self):
        self.print("readlines", "waiting" )
        r = self.read(-1)
        self.print("readlines", r )
        if r != None:
            return r
        return None

    def readlines(self):
        lines = []
        stop = time.time() + 3;
        while time.time()<stop:
            l = self.readline()
            if l is None:
                break
            lines.append(l)
        return lines

    def write(self,buf):
        self.print("write", buf )
        return self.ws.send(buf)
    
    def flush(self):
        self.print("flush" )
        pass
    
    def reset_input_buffer(self):
        self.print("reset buffer" )
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self,t,v,tb):
        pass
    
    def print(self,*args):
        print("ptty", *args )
        
    
def sample():
    
    debug = True # display more information 
    trace = False # display no detail trace information 

    tty = pttyws().open("ws://192.168.178.20:8266","123456")
    print(tty)

    with tty as octx:
        
##        while True:
##            r = octx.readline()
##            print( r )
       
        mpyc = MPyControl(octx,debug=debug,trace=trace)
        
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

def get_repl():
    while True:
        r = ws.recv().encode()
        print("repl got",r)
        if r == b'OK':
            continue
        if r == b'\x04':
            continue
        if r == b'>':
            break
        if r == b'\r':
            continue
        if r == b'\r\n':
            continue
        break
    
    return r     
   
def enter_rawrepl():   
    ws.send([0x03])
    ws.send([0x01])
    
    r = get_repl()
    print(r)
    if r != b'raw REPL; CTRL-B to exit\r\n':
        raise Exception("could not enter raw-repl")
    r = ws.recv().encode()
    print(r)
    if r != b'>':
        raise Exception("could not enter raw-repl")

 

def send_cmd(cmd):
  
    print("cmd", cmd )

    ws.send(cmd+"\r\n")
    ws.send([0x04])
    resp = get_repl()
    print("resp",resp)

    return resp

url = "ws://192.168.178.21:8266"
ws = create_connection(url,
                            #timeout=5,
                            sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 0),)
                            )
time.sleep(.1)
r = ws.recv()
print(r)
r = ws.send("123456\r\n")
print(r)
r = ws.recv()
print(r)

print("established")

enter_rawrepl()

r = send_cmd("print('hallo')")
print(r)
r = get_repl()
print(r)

r = send_cmd("print('welt')")
print(r)
r = get_repl()
print(r)

cmd = """
import uos, json
_tocreate = '%s'.split('/')
_path = ""
_sep = ""
_add = []
for _p in _tocreate:
    if len(_p.strip()) == 0:
        continue
    _path = _path + _sep + _p
    _sep='/'
    try:
        uos.mkdir( _path )\r\n
        _add.append( (True, _path) )
        #print("create", _path)
    except:
        _add.append( (False, _path) )
        #print("already exists", _path)
print( json.dumps( _add ) )
"""
cmd = cmd  % "others/www"
#print(cmd)
r = send_cmd( cmd )
print(r)

r = get_repl()
print(r)


