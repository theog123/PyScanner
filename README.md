# PyScanner
This program will scan barcodes and add specific information to a google spreadsheet. A user will be able to populate their own spreadsheet database using the Scanner, Controller, and Spreadsheet classes. A regular usb 2D scanner is need for this project to work. 

## Scanner


### Input: /dev/hidraw0
### Output: text file

The sscanner is abstracted by the file /dev/hidraw0.


## Controller

![Controller](https://user-images.githubusercontent.com/32689872/82836620-b3077d80-9e7b-11ea-9002-fe80c4c06676.png)

### Input: the textfile containing barcodes for given id numbers
### Output: a spreadsheet tabulating the attendance


There is separate attendance access outside of the controller making it easy to use another database in the future. Other data bases include SQL or Oracle.
