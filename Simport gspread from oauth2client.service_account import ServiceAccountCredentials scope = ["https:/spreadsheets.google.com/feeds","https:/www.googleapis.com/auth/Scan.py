import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [ "https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive" ]
creds = ServiceAccountCredentials.from_json_keyfile_name( "creds.json" , scope )
client = gspread.authorize( creds )
spreadName = "testsheet"
spreadsheet = client.open( spreadName )
import datetime
import time
from datetime import date

class Spreadsheet:

  def __init__( self ):
    self.start = 0
    self.sheet = spreadsheet.get_worksheet( self.start )
    self.sheet.update_cell( 1, 1, 'absences' )
    self.sheet.update_cell( 1, 2, 'tardy' )
    self.sheet.update_cell( 1, 4, 'Present' )
    self.sheet.update_cell( 1, 5, 'Check In' )
    self.sheet.update_cell( 1, 6, 'Check Out' )


  def newTab( self, name ):
    spreadsheet.add_worksheet( name, 100, 100)
    self.start=self.start + 1
    self.sheet = spreadsheet.get_worksheet( self.start )
    self.sheet.update_cell( 1, 1, 'absences' )
    self.sheet.update_cell( 1, 2, 'tardy' )
    self.sheet.update_cell( 1, 4, 'Present' )
    self.sheet.update_cell( 1, 5, 'Check In' )
    self.sheet.update_cell( 1, 6, 'Check Out' )


  def addTardy( self, tardyList ):
    countT = 2
    for t in tardyList:
      self.sheet.update_cell( countT, 2, t)
      countT = countT + 1

  def addAbsent( self, absentList ):
    countA = 2
    for a in absentList:
      self.sheet.update_cell( countA, 1, a )
 
  def addCheckIn( self, checkInDict ):
    countIn = 2
    for I in checkInDict:
      self.sheet.update_cell( countIn, 4, I)
      self.sheet.update_cell( countIn, 5, checkInDict[ I ])
      countIn = countIn + 1


  def addCheckOut( self , checkOutDict ):
    countOut = 2
    for O in checkOutDict:
      self.sheet.update_cell( countOut, 4, O )
      self.sheet.update_cell( countOut, 6 , checkOutDict[ O ] )
      countOut = countOut + 1


class Controller:
#to do: rename data to student map and scan map
  def __init__( self, sheet ):
    self.studentMap = self.regRead( "Data.txt" )
    self.sheet = sheet
    self.scanMap = self.readData( "foo.txt" )
    self.tardyList = [ ]
    self.absentList = [ ]
    self.checkInDict = { }
    self.checkOutDict={ }
    self.today = datetime.datetime.today( )
    self.year = self.today.year
    self.month = self.today.month
    self.day = self.today.day

  def readData( self, name ):
    temp=' '
    dataTemp={ }
    data = open(name,"r")
    lines = data.readlines()
    for line in lines:
       listTemp = [ ]
       temp = line.split( "," )
       if temp[ 0 ] in dataTemp :
         listTemp = dataTemp[ temp[ 0 ] ]
       listTemp.append(temp[ 1 ].strip( '\n' ) )
       dataTemp[ temp[ 0 ] ] = listTemp

    for key in dataTemp:
      listTemp=[ ]
      if len( dataTemp[ key ] ) >= 2:
        listTemp.append( dataTemp[ key ][ 0 ] )
        listTemp.append( dataTemp[ key ][ len( dataTemp[ key ] )-1 ] )
        dataTemp[ key ] = listTemp
    return dataTemp

  def regRead( self , name ):
    temp=' '
    dataTemp={ }
    data = open( name , "r" )
    lines = data.readlines( )
    for line in lines:
       temp = line.split( "," )
       dataTemp[ temp[ 0 ] ] = temp[ 1 ].strip( '\n' )
    return dataTemp

  def makeTardy( self ):
    for key in self.scanMap:
      if len( self.scanMap[ key ]) == 1:
        lowBound = float( datetime.datetime( self.year, self.month, self.day, 15,40 ).strftime( '%s' ) )
        highBound = float( datetime.datetime( self.year,self.month , self.day, 15, 50 ).strftime( '%s' ) )
        if float( self.scanMap[ key ][ 0 ]) >= lowBound and float(self.scanMap[ key ][ 0 ]) < highBound:
          for num in self.studentMap:
            if key == num:
              self.tardyList.append( self.studentMap[ num ] )

    self.sheet.addTardy( self.tardyList )
    print( self.tardyList )

  def makeAbsent( self ):

    for num in self.studentMap:
      if not num in self.scanMap:
         self.absentList.append( self.studentMap[ num ] )

    for key in self.scanMap:
      if len( self.scanMap[ key ]) == 1:
        lowBound = float( datetime.datetime( self.year, self.month, self.day, 15, 30 ).strftime( '%s' ) )
        highBound = float( datetime.datetime( self.year,self.month, self.day, 15, 40 ).strftime( '%s' ) )
        if float( self.scanMap[ key ][ 0 ] ) >= lowBound and float( self.scanMap[ key ][ 0 ] ) < highBound:
          for num in self.studentMap:
           if key == num:
             self.absentList.append( self.studentMap[ num ] )

    self.sheet.addAbsent( self.absentList )
    print( self.absentList )

  def makePresent( self ):
    lowBound1 = float( datetime.datetime( self.year, self.month, self.day , 15 , 30 ).strftime('%s' ) )
    lowBound2 = float( datetime.datetime( self.year, self.month, self.day, 15, 40 ).strftime( '%s' ) )
    highBound1 = float( datetime.datetime( self.year, self.month, self.day, 15, 40 ).strftime( '%s ') )
    highBound2 = float( datetime.datetime( self.year,self.month , self.day, 15, 50 ).strftime( '%s' ) )
    for key in self.scanMap:
      if len( self.scanMap[ key ] ) == 2:
        if float( self.scanMap[ key ][ 0 ]) >= lowBound1 and float( self.scanMap[ key ][ 0 ]) < highBound1:
          if float( self.scanMap[ key ][ 1 ] )>= lowBound2 and float( self.scanMap[ key ][ 1 ] )< highBound2:
            for num in self.studentMap:
              if key == num:
                self.checkInDict[ self.studentMap[ num ] ] = datetime.datetime.fromtimestamp( float( self.scanMap[ key ][ 0 ] ) ).strftime( '%c' )
                self.checkOutDict[ self.studentMap[ num ] ] = datetime.datetime.fromtimestamp( float( self.scanMap[ key ][ 1 ] ) ).strftime( '%c' )

    self.sheet.addCheckIn( self.checkInDict )
    self.sheet.addCheckOut( self.checkOutDict )
    print( self.checkInDict )
    print( self.checkOutDict )

  def newTabTime( self ):
    self.sheet.newTab( str( datetime.date.today() + datetime.timedelta( days = 1 ) ) )

val=Spreadsheet()
c=Controller(val)
c.makeTardy()
c.makeAbsent()
c.makePresent()
c.newTabTime()




