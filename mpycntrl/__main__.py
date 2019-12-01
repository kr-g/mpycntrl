
from . mpycntrl import *

def print_tr( tr, l, head="received", debug=True ):
    if tr:
        try:
            if debug:
                print( head, l.decode().rstrip() )
            else:
                print( l.decode().rstrip() )
            return
        except:
            pass
    if debug:
        print( head, l )
    else:
        print( l )
        

def main():
    
    show_time = False
    maxretry = 3
    follow = False
    debug = False
    
    port = '/dev/ttyUSB0'
    baud = 115200
    bytesize = 8
    parity = 'N'
    stopbits = 1
    timeout = .35

    import argparse
    parser = argparse.ArgumentParser(description='Control MicroPython via cmd line')
    parser.add_argument("-v", "--version", dest='show_version', action="store_true",
                        help="show version info and exit", default=False )
    
    parser.add_argument("-port", "-p", type=str, dest='port', action="store",
                        help="port/device to use (default: %(default)s)", default=port )
    parser.add_argument("-baud", "-b", type=int, dest='baud', action="store",
                        help="baud rate to use (default: %(default)s)", default=baud )
    parser.add_argument("-bytesize", "-cs", type=int, dest='bytesize', action="store",
                        help="bytesize to use (default: %(default)s)", default=bytesize )
    parser.add_argument("-parity", type=str, dest='parity', action="store",
                        help="parity to use (default: %(default)s)", default=parity, choices=['N', 'E', 'O'] )
    parser.add_argument("-stopbits", type=int, dest='stopbits', action="store",
                        help="stopbits to use (default: %(default)s)", default=stopbits )
    parser.add_argument("-timeout", "-to", type=float, dest='timeout', action="store",
                        help="timeout in sec to use (default: %(default)s)", default=timeout )
    parser.add_argument("-debug", "-d", dest='debug', action="store_true",
                        help="display debug info (default: %(default)s)", default=debug )
    parser.add_argument("-showtime", dest='show_time', action="store_true",
                        help="display execution time (default: %(default)s)", default=show_time )
    parser.add_argument("-follow", "-f", dest='follow', action="store_true",
                        help="don't exit, keep following the output of MicroPython (default: %(default)s)", default=follow )
    parser.add_argument("-maxretry", "-max", type=int, dest='maxretry', action="store",
                        help="max number of retries to connect (default: %(default)s)", default=maxretry )

    parser.add_argument("-blocksize", "-bs", type=int, dest='blocksize', action="store",
                        help="blocksize during file transfer (default: %(default)s)", default=512 )

    parser.add_argument("-translate", "-tr", dest='translate', action="store_true",
                        help="translate response as string where possible (default: %(default)s)", default=False )

    group = parser.add_mutually_exclusive_group()
    group.add_argument( "-eval", "-exe", "-run", "-e", type=str, dest='eval', action="store",
                        help="send source code to MicroPython and execute", default="" )
    group.add_argument("-reset", "-r", dest='reset', action="store_true",
                        help="reset MicroPython by sending cntrl + D, soft restart", default=False )
    group.add_argument("-hardreset", "-R", dest='hardreset', action="store_true",
                        help="hard reset MicroPython", default=False )
    group.add_argument("-cntrlc", "-c", dest='cntrl_c', action="store_true",
                        help="send break cntrl + C", default=False )
    group.add_argument("-meminfo", "-i", dest='meminfo', action="store_true",
                        help="get memory info", default=False )

    group.add_argument( "-ls", dest="ls_path", metavar="PATH", type=str, action="store", help="list directory", nargs="?", const="." )
    group.add_argument( "-ll", dest="ll_path", metavar="PATH", type=str, action="store",
                        help="long list directory as json with stat_result. refer to os.stat() for more details", nargs="?", const="." )
    group.add_argument( "-rm", dest="rm_path", metavar="PATH", type=str, action="store", help="remove file", nargs=1 )
    group.add_argument( "-mkdir", "-mk", dest="mk_path", metavar="PATH", type=str, action="store",
                        help="create folders including sub folders, returns array of tupels which dirs where created. "
                        "returns false if directory is already existing", nargs=1 )
    group.add_argument( "-rmdir", "-rd", dest="rm_r_path", metavar="PATH", type=str, action="store",
                        help="remove folder and all containing files and sub folders", nargs=1 )
    group.add_argument( "-get", dest="get_path", metavar="PATH", type=str, action="store",
                        help="get file from MicroPython", nargs=2 )
    group.add_argument( "-put", dest="put_path", metavar="PATH", type=str, action="store",
                        help="put file on MicroPhyton", nargs="+" )

    args = parser.parse_args()
    
    if args.debug:
        print( "arguments", args )
    
    if args.show_version:
        print( "Version:", MPyControl.VERSION )
        return

    start_time = time.time()

    with serial.Serial(port=args.port, baudrate=args.baud,
                       bytesize=args.bytesize, parity=args.parity, stopbits=args.stopbits,
                       timeout=args.timeout) as ser:

        mpyc = MPyControl(ser,debug=args.debug)
        
        r = None
        
        if args.reset:
            r = mpyc.send_reset( )
 
        if args.hardreset:
            r = mpyc.send_hardreset( )

        if args.cntrl_c:
            for retry in range( 0, args.maxretry ):
                try:
                    r = mpyc.send_cntrl_c( )
                    print_tr( args.translate, r, head="connected", debug=args.debug )
                    break
                except:
                    pass
                
        if args.meminfo:
            r = mpyc.send_machine_info( )

        if args.eval != "":
            r = mpyc.sendcmd( bytes(args.eval, "utf-8").decode("unicode_escape") )

        if args.ll_path:
            path = args.ll_path[0] if isinstance( args.ll_path, list ) else args.ll_path
            r = mpyc.cmd_ls( path )
        if args.ls_path:
            path = args.ls_path[0] if isinstance( args.ls_path, list ) else args.ls_path
            r = mpyc.cmd_ls( path )
            r = list( r.keys() )
            
        if args.rm_path:
            r = mpyc.cmd_rm( args.rm_path[0] )
        if args.mk_path:
            r = mpyc.cmd_mkdirs( args.mk_path[0] )
        if args.rm_r_path:
            r = mpyc.cmd_rm_r( args.rm_r_path[0] )
        if args.put_path:
            if len(args.put_path)>2:
                raise Exception( "wrong argument" )
            fnam = args.put_path[0]
            dest = fnam if len(args.put_path)==1 else args.put_path[1]
            r = mpyc.cmd_put( fnam, dest=dest, blk_size=args.blocksize )
        if args.get_path:
            if len(args.get_path)>2:
                raise Exception( "wrong argument" )
            fnam = args.get_path[0]
            dest = fnam if len(args.get_path)==1 else args.get_path[1]
            r = mpyc.cmd_get( fnam, dest=dest, blk_size=args.blocksize )

        if r:
            if isinstance(r, list):
                for l in r:
                    print_tr( args.translate, l, debug=args.debug )       
            else:
                print_tr( args.translate, r, debug=args.debug )       

        while args.follow:
            r = ser.readlines()        
            for l in r:
                print_tr( args.translate, l, debug=args.debug )
            
    stop_time = time.time()
    if args.show_time:
        print( "total time:", stop_time - start_time )
        
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print( "error", ex )


