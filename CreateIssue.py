import datetime 
import time
import argparse
import sys


__version__ = "0.1"


    
def main(argv):
    
    
    parser = argparse.ArgumentParser(usage="""
    {1}    Version:{0}
    


 EXAMPLE: python script.py  -t some_txt

    """.format(__version__,sys.argv[0]))

    parser.add_argument('-t','--target', help='<Print something>')
    parser.add_argument('-v','--version', help='<Version>', action='store_true')
    
    args = parser.parse_args()
        
    
    if args.version:
        print 'Tool version: %s'  % __version__
        print "DEMO FIRDAY" 
        sys.exit(2)    
         
    tparam = args.target or ''

  
    # quick old-school way to check needed parameters
    if (tparam == ""):
        parser.print_help()
        sys.exit(2)
    
    print "---------------------------------------------------------"
    print "Parameter was: {0}".format(tparam)
    print "---------------------------------------------------------"
    
    
if __name__ == "__main__":
        main(sys.argv[1:])