import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
spreadName="testsheet"
spreadsheet=client.open(spreadName)

class Spreadsheet:

  def __init__(self):
    self.start=0
    self.sheet=spreadsheet.get_worksheet(self.start)
    self.tardyList=[]
    self.absentList=[]
    self.times={}
    self.sheet.update_cell(1,1,'absences')
    self.sheet.update_cell(1,2,'tardy')
    self.sheet.update_cell(1,4,'Present')
    self.sheet.update_cell(1,5,'Check In')
    self.sheet.update_cell(1,6,'Check Out')


  def newTab(self,name):
    spreadsheet.add_worksheet(name, 100, 100)
    self.start=self.start+1
    self.sheet=spreadsheet.get_worksheet(self.start)
    self.sheet.update_cell(1,1,'absences')
    self.sheet.update_cell(1,2,'tardy')
    self.sheet.update_cell(1,4,'Present')
    self.sheet.update_cell(1,5,'Check In')
    self.sheet.update_cell(1,6,'Check Out')


  def addTardy(self):
    countT=2
    for t in self.tardyList:
      self.sheet.update_cell(countT,2,t)
      countT=countT+1

  def addAbsent(self):
    countA=2
    for a in self.absentList:
      self.sheet.update_cell(countA,1,a)
      countA=countA+1


  def addCheckIn(self):
    countIn=2
    for I in self.checkInDict:
      self.sheet.update_cell(countIn,4,I)
      self.sheet.update_cell(countIn,5,self.checkInDict[I])
      countIn=countIn+1


  def addCheckOut(self):
    countOut=2
    for O in self.checkOutDict:
      self.sheet.update_cell(countOut,4,O)
      self.sheet.update_cell(countOut,6,self.checkOutDict[O])
      countOut=countOut+1
class Scanner:

  def __init__(self):
    self.DataID=self.readData("DataID.txt")

  def scan(self):

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

    fp = open( '/dev/hidraw0', 'rb' )

    done = False

    code = ""


    while not done:
      print( "reading 8 bytes .." )

      buffer = fp.read( 8 )

    for c in buffer:
      print( str( ord( c ) ) )
      if ord( c ) == 40:
         print ("DONE !!!")
         print( code )
         done = True
         break
      if ord( c ) in hid:
         code += hid[ ord( c ) ]

    fp.close()


  def readData(self,name):
    temp=[]
    dataTemp={}
    data= open(name,"r")
    lines=data.readlines()
    for line in lines:
       temp=line.split(",")
       dataTemp[temp[0]]=temp[1].strip('\n')
    return dataTemp





class Controller:

  def __init__(self,sheet):
    self.data=self.listData("Data.txt")

 self.sheet=sheet
    self.sheet.times=self.readData("Times.txt")


  def readData(self,name):
    temp=[]
    dataTemp={}
    data= open(name,"r")
    lines=data.readlines()
    for line in lines:
       temp=line.split(",")
       dataTemp[temp[0]]=temp[1].strip('\n')
    return dataTemp


  def listData(self,name):
    temp=[]
    data=open(name,"r")
    lines=data.readlines()
    for i in range(len(lines)):
      lines[i]=lines[i].strip('\n')
    return lines

  def makeLists(self):

    for name in self.data:
      countIn=0
      countOut=0
      for key in self.sheet.times:
        if self.sheet.times[key]==name:
          word=key.replace(":",'')
          num=int(word)
          if num>=245 and num<=305:
            countIn=countIn+1
          if num>=345 and num<=4:
            countOut=countOut+1
      if countIn>0 and not countOut>0:
        self.sheet.tardyList.append(name)
      if not countIn>0 and not countOut>0:
        self.sheet.absentList.append(name)
      if countIn>0 and not countOut>0:
        self.sheet.absentList.append(name)
    print(self.sheet.absentList)
    print(self.sheet.tardyList)

val=Spreadsheet()
sheetVal=Controller(val)
sheetVal.makeLists()

