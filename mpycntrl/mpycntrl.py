import io, os, sys, time
import binascii, json, textwrap
import serial # its pyserial

class _ChangeTimeout:
    
    """Context for securly changing and reverting the timeout for MPyControl"""
    
    def __init__(self, mpyc, timeout, debug=True):
        self.mpyc = mpyc
        self.newtimeout = timeout
        self.oldtimeout = mpyc.serial.timeout
        self.debug=debug
    
    def __enter__(self):
        self.mpyc.serial.timeout = self.newtimeout
        self.starttime = time.time()
        return self

    def __exit__( self, exception_type, exception_value, traceback ):
        self.mpyc.serial.timeout = self.oldtimeout
        
    def diff_time(self,set=False):
        """calculate the time for working with the context"""
        return time.time() - self.starttime
    

class MPyControl:
    
    """
        control micropython with your own code
    """

    VERSION = "0.0.4"

    def __init__(self, serial, debug=True, trace=False, tout=None):
        self.serial = serial
        self.debug = debug
        self.trace = trace
        self.tout = tout
        self.print("using",serial)
        self.reset_timer()
        
    def reset_timer(self):
        self.start_time = time.time()
        
    def diff_time(self):
        return time.time() - self.start_time

    def print( self, *args, **kwargs ):
        if self.debug:
            print( "(debug)", *args, **kwargs )
            
    def print_t( self, *args, **kwargs ):
        if self.trace:
            print( "(trace)", *args, **kwargs )
    
    def timeout(self, timeout ):
        """change the timeout securely in a with code block"""
        return _ChangeTimeout( self, timeout )
    
    def read(self,flen):
        r = self.serial.read( flen )
        return r        
    
    def write(self,bytes):
        self.print( "sending", bytes )
        self.serial.write( bytes )
        
    def write_t(self,bytes):
        self.print_t( "sending", bytes )
        self.serial.write( bytes )

    def flush(self):
        self.serial.flush()
    
    def readlines(self):
        r = self.serial.readlines()
        self.print( "received", r )
        return r
    
    def send_cntrl_c(self):
        """send cntrl + c to micropython"""
        self.write_t( [0x03] ) # cntrl c 
        self.flush()
        r = self.readlines()
        return r    

    def send_cntrl_a(self):
        """send cntrl + a to micropython"""
        self.write_t( [0x01] ) # cntrl a
        self.flush()
        r = self.readlines()
        return r    

    def get_ok(self):
        """get OK after entering raw-repl"""
        res = self.read(2)
        #print(res)
        return res.decode().lower() == "ok"

    def sendcmd( self, cmd ):        
        """send a command and wait for result"""
        cmd = textwrap.dedent( cmd ) # remove common leading withspace 
        r = self.send_cntrl_a()
        #print(r)
        
        self.write_t( cmd.encode() ) # encode for sending raw bytes
        
        self.write_t( [0x04] ) # cntrl d, leave raw-repl
        self.flush()
        r = self.get_ok()
        if not r:
            raise Exception("could not enter raw-repl")
        r = self.readlines()
        return r    

    def send_reset(self):
        """reset the board"""
        self.write_t( [0x03,0x04] ) # cntrl c + cntrl d, reset board
        self.flush()
        r = self.readlines()
        return r    

    def send_hardreset(self):
        """hard reset the board"""
        self.write_t( [0x03] ) # cntrl c
        self.flush()
        cmd = """
            import machine
            machine.reset()
            """
        r = self.sendcmd( cmd )
        return r

    def send_machine_info(self):
        """get memory info"""
        cmd = """
            import micropython
            micropython.mem_info(0)
            """
        r = self.sendcmd( cmd )
        return r

    def send_collect_ids(self):
        """collect several number/info/id's eg. machine.unique_id(), wlan mac etc"""
        cmd = """
            import machine, sys, network, ubinascii, json
            _ids = {}
            _ids["unique_id"] = ubinascii.hexlify( machine.unique_id() )
            _ids["platform"] = sys.platform
            _ids["version"] = sys.version
            _ids["byteorder"] = sys.byteorder
            _ids["wlan"] = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'))
            _ids["ap"] = ubinascii.hexlify(network.WLAN(network.AP_IF).config('mac'))
            print( json.dumps( _ids ) )
            """
        r = self.sendcmd( cmd )
        if len(r)==0:
            raise Exception("timeout during execution")
        all_ids = json.loads( r[0].decode() )
        return all_ids
        

    def cmd_ls(self,path="."):
        """get a directoty list from mpy board"""
        cmd = """
            import uos, json
            _path = '%s'
            _files = {}
            for _f in uos.listdir(_path):
                _file = "/".join( [_path, _f] ) if _path != "." else _f
                _files[_file] = uos.stat( _file )
            print( json.dumps( _files ) )
            """
        r = self.sendcmd( cmd % path )
        if len(r)==0:
            raise Exception("timeout during execution")
        files = json.loads( r[0].decode() )
        return files

    def cmd_rm(self,fnam):
        """remove a file on the mpy board"""
        cmd = """
            import uos
            _fnam = '%s'
            try:
                uos.remove( _fnam )
                print( "deleted", _fnam )
            except Exception as ex:
                print( "error", ex )
            """
        r = self.sendcmd( cmd % fnam )
        return r

    def cmd_rm_r(self,fnam):
        """remove complete folder and all files recursive on the mpy board"""
        cmd = """
            import uos, json
            _fnam = '%s'
            _del = []
            def _rm_r( path ):
                for _f in uos.listdir( path ):
                    _file = path + '/' + _f
                    _st = uos.stat( _file )
                    _isfolder = ( _st[0] & 0x8000 ) == 0
                    if _isfolder:
                        _rm_r( _file )
                        _del.append( _file )
                    else:
                        uos.remove( _file )
                        _del.append( _file )
                uos.rmdir( path )
                _del.append( path )
                
            _rm_r( _fnam )
            print( json.dumps( _del ) )
            """
        r = self.sendcmd( cmd % fnam )
        if len(r)==0:
            raise Exception("timeout during execution")
        #files = json.loads( r[0].decode() )
        return r

    def cmd_mkdirs(self,path):
        """create path recursive, including missing sub-direcories, on the mpy board"""
        cmd = """
            import uos
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
        r = self.sendcmd( cmd % path )
        return r

    def _get_part( self, r_data ):
        data = r_data.decode()
        o = json.loads( data )
        size = o["size"]
        if size == 0:
            return None
        hexdata = o["data"]
        bytes = binascii.unhexlify( hexdata )
        if size is not len(bytes):
            raise Exception("data corrupted" )
        o['data'] = bytes
        return o

    def cmd_get( self, fnam, dest=None, blk_size=256 ):
        """receive a file from mpy board"""
        content = bytearray()
        pos = 0
        while True:
            cmd = """
                import ubinascii, json, uos
                _fnam = '%s'
                _pos = %d
                _blk_size = %d
                _size = uos.stat(_fnam)[6]
                with open(_fnam,'rb') as _f:
                    _f.seek( _pos )
                    _cb = 0
                    if _blk_size <= 0:
                        _cb = _f.read()
                    else:
                        _cb = _f.read(_blk_size)
                    _data = { 'size' : len( _cb ), 'fsize' : _size, 'pos' : _pos, 'data' : ubinascii.hexlify( _cb ) }
                    print( json.dumps( _data ) )
                """
            r = self.sendcmd( cmd % (fnam,pos,blk_size) )
            self.print( "received", pos, blk_size )
            if len(r)==0:
                raise Exception("timeout during execution")
            part = self._get_part( r[0] )
            if part is None:
                break;
            content.extend( part["data"] )
            pos += blk_size
            if pos > part["fsize"]:
                break

        if dest:
            with open( dest, "wb" ) as f:
                f.write( content )

        return content

    def cmd_put( self, fnam, content=None, dest=None, blk_size=256, ACKN=b'\x04\x04>' ):
        """send a file to mpy board"""
        if dest is None:
            dest = fnam
        if content is None:
            with open( fnam, "rb" ) as f:
                content = f.read()
        conthex = binascii.hexlify(content)
        
        blks = int( len( conthex ) / blk_size )
        add = 0 if len( conthex ) % blk_size == 0 else 1
        loops = blks + add
        r =  None
        
        for l in range( 0 , loops ):
            cmd = """
                import ubinascii
                _fnam = '%s'
                _pos = %d
                _cb = %s
                with open(_fnam,'wb') as _f:
                    try:
                        if len(_cb):
                            _f.seek(_pos)
                            _f.write(ubinascii.unhexlify(_cb))                        
                    except Exception as ex:
                        print( "error:", ex )
                    """
            pos = l * blk_size
            part = conthex[pos:pos+blk_size]
            self.print( "sending", l, pos, len(part), part )
            r = self.sendcmd( cmd % (dest, pos / 2, part ) )
            if ACKN and len(r)>0:
                if r[0] != ACKN:
                    raise Exception( "send error", r )
            #self.print( "received", r )
            
        return r

