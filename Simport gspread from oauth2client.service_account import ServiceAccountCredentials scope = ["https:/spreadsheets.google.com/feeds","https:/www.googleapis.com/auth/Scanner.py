from datetime import datetime, timedelta
from threading import Timer
from datetime import datetime
import time
import sys
class Scanner:

  def scan( self ):
    # hid converts hidraw0 text into ascII text in order to read scanner onto a file
    hid = { 30: '1',
        31: '2',
        32: '3',
        33: '4',
        34: '5',
        35: '6',
        36: '7',
        37: '8',
        38: '9',
        39: '0' }
    #This reads from the /dev/hidraw file made when scanning
    fp = open( '/dev/hidraw0', 'rb' )
    #Checks if all binary characters are scanned
    done = False
    #We add the new ascII characters to code in order to get ID
    code = ""
    while not done:
       buffer=fp.read( 8 )
       for c in buffer:
          #40 represents the last character in hidraw file. Once we reach the last character, we exit the loop as done=true
          if ord( c ) == 40:
             done = True
             break
          #Checks if a corresponding hidraw value is in our dictionary at a specific part of hidraw0
          if ord( c ) in hid:
            #the ascII value of that hidraw0 value is added to code
            code += hid[ ord( c )]

    #This obtains the time after epoch
    ts=time.time()
    #The %s tells the file that we are printing a string
    print( "%s %s" %( code, ts ) )
    #This method directly writes the print statement to a file by pushing buffer values
    sys.stdout.flush()
    fp.close()


  def contScan( self ):
      while True:
        self.scan()

s=Scanner()
s.contScan()




