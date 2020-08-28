# PythonPiDAQ
Python on a Pi using MCC152, MCC118 and MCC134 hats and Flask to return JSON data.  
Switched to PiZero WiFi and LiFePO4wered/Pi™ battery

MCC152 requires IC2 be enabled on Pi

I have MCC134 at address 0 and MCC152 at Address 1

Web Calls
**************************************************
GetThermocouple Temperatures
10.111.340:5000/TCtemps 
returns:

[
  {
    "chan": 0, 
    "value": "22.69143038839301"
  }, 
  {
    "chan": 1, 
    "value": "22.567366509066666"
  }, 
  {
    "chan": 2, 
    "value": "23.51341824419599"
  }, 
  {
    "chan": 3, 
    "value": "23.47018505035673"
  }
]
**************************************************
Set Digital Outputs
http://10.111.3.40:5000/DigOutWrite?id=7
use decimal to send
255 = all on:
0 = all off:
7 = 00000111:

[
  {
    "chan": 0, 
    "value": "1"
  }, 
  {
    "chan": 1, 
    "value": "1"
  }, 
  {
    "chan": 2, 
    "value": "1"
  }, 
  {
    "chan": 3, 
    "value": "0"
  }, 
  {
    "chan": 4, 
    "value": "0"
  }, 
  {
    "chan": 5, 
    "value": "0"
  }, 
  {
    "chan": 6, 
    "value": "0"
  }, 
  {
    "chan": 7, 
    "value": "0"
  }
]


**************************************************
Analog Out (2 Chan)
http://10.111.3.40:5000/AnalogOut1?id=1.69
Analog0?id=3.3 will send 3.3 to Analog Output 0
Analog1?id=1.69 will send 1.69 volts to Analog Output 1

SUCCESS will be returned if everythinhg is OK

**************************************************
Analog Input (8 Chan - 0 to 7)
http://10.111.3.40:5000/AnalogInChan?id=0
AnalogInChan?id=0 returns the voltage at chan 0:
[{"chan":0,"value":4.692157421477653}]

