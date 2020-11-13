#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep
from sys import stdout, version_info
from daqhats import mcc134, mcc152, mcc118, HatIDs, HatError, TcTypes, hat_list, DIOConfigItem, OptionFlags, \
    interrupt_callback_enable, HatCallback, interrupt_callback_disable
from daqhats_utils import select_hat_device, tc_type_to_string, enum_mask_to_string
from flask import Flask, request, jsonify
from ctypes import cdll

# Use a global variable for our board object so it is accessible from the
# interrupt callback
global HAT
HAT = None

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route('/myaddress')
def myaddress():

    mylist  = hat_list(filter_by_id=HatIDs.MCC_134)
    
    address = mylist[0].address
            
    return str(address)

@app.route('/TCtemps1')
def index():
    #address = select_hat_device(HatIDs.MCC_134)
    mylist = hat_list(filter_by_id=HatIDs.MCC_134)
    address = mylist[0].address
    
    
    hat = mcc134(address)
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 1  # Seconds
    channels = (0, 1, 2, 3)

    lib = cdll.LoadLibrary('/usr/local/lib/liblifepo4wered.so')

    for channel in channels:
        hat.tc_type_write(channel, tc_type)

    tempZero = str("{:.2f}".format((hat.t_in_read(0)*1.8)+32))
    tempOne = str("{:.2f}".format((hat.t_in_read(1)*1.8)+32))
    tempTwo = str("{:.2f}".format((hat.t_in_read(2)*1.8)+32))
    tempThree = str("{:.2f}".format((hat.t_in_read(3)*1.8)+32))
   # temp1 = float(tempZero)
   # temp2 = float(tempOne)
   # temp3 = float(tempTwo)
   # temp4 = float(tempThree)

   # tempDiff12 = str("{:.2f}".format(temp1 - temp2))
   # tempDiff13 = str("{:.2f}".format(temp1 - temp3))
   # tempDiff23 = str("{:.2f}".format(temp2 - temp3))
   # tempDiff24 = str("{:.2f}".format(temp2 - temp4))
   # tempDiff14 = str("{:.2f}".format(temp1 - temp4))
   # tempDiff34 = str("{:.2f}".format(temp3 - temp4))

    vbat = str(lib.read_lifepo4wered(10))

    temps = {
        'TC_Temps_1':[
        {'EAT': tempZero,},
        {'LAT': tempOne,},
        {'Clamp1': tempTwo,},
        {'Clamp2': tempThree,},
       # {'tempDiff12': tempDiff12,},
       # {'tempDiff13': tempDiff13,},
       # {'tempDiff23': tempDiff23,},
       # {'tempDiff24': tempDiff24,},
       # {'tempDiff14': tempDiff14,},
       # {'tempDiff34': tempDiff34,},
        {'vbat': vbat,}
        ]}

    return jsonify(temps)

@app.route('/TCtemps2')
def index2():
    #address = select_hat_device(HatIDs.MCC_134)
    mylist = hat_list(filter_by_id=HatIDs.MCC_134)
    address = mylist[1].address
    
    
    hat = mcc134(address)
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 1  # Seconds
    channels = (0, 1, 2, 3)

    lib = cdll.LoadLibrary('/usr/local/lib/liblifepo4wered.so')

    for channel in channels:
        hat.tc_type_write(channel, tc_type)

    tempZero = str("{:.2f}".format((hat.t_in_read(0)*1.8)+32))
    tempOne = str("{:.2f}".format((hat.t_in_read(1)*1.8)+32))
    tempTwo = str("{:.2f}".format((hat.t_in_read(2)*1.8)+32))
    tempThree = str("{:.2f}".format((hat.t_in_read(3)*1.8)+32))
    #temp1 = float(tempZero)
    #temp2 = float(tempOne)
    #temp3 = float(tempTwo)
    #temp4 = float(tempThree)

    #tempDiff12 = str("{:.2f}".format(temp1 - temp2))
    #tempDiff13 = str("{:.2f}".format(temp1 - temp3))
    #tempDiff23 = str("{:.2f}".format(temp2 - temp3))
    #tempDiff24 = str("{:.2f}".format(temp2 - temp4))
    #tempDiff14 = str("{:.2f}".format(temp1 - temp4))
    #tempDiff34 = str("{:.2f}".format(temp3 - temp4))

    vbat = str(lib.read_lifepo4wered(10))

    temps = {
        'TC_Temps_2':[
        {'Clamp3': tempZero,},
        {'Clamp4': tempOne,},
        {'Clamp5': tempTwo,},
        {'Clamp6': tempThree,},
        #{'tempDiff12': tempDiff12,},
        #{'tempDiff13': tempDiff13,},
        #{'tempDiff23': tempDiff23,},
        #{'tempDiff24': tempDiff24,},
        #{'tempDiff14': tempDiff14,},
        #{'tempDiff34': tempDiff34,},
        {'vbat': vbat,}
        ]}

    return jsonify(temps)


@app.route('/Battery', methods=['GET'])
def Battery():
     
    lib = cdll.LoadLibrary('/usr/local/lib/liblifepo4wered.so')
    
    BattInfo = {
        'battinfo':[
        {'Iout': str(lib.read_lifepo4wered(12)),},
        {'VBat':str(lib.read_lifepo4wered(10)),},
        {'PiVin': str(lib.read_lifepo4wered(9)),}
        ]}
    
    return jsonify(BattInfo)        
        
@app.route('/DigOutWrite', methods=['GET'])
def api_id():

    
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error detected" 
           
    #get MCC152 board address
    boardAddr = select_hat_device(HatIDs.MCC_152) 
    board = mcc152(boardAddr)
    bit = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    
    board.dio_config_write_port(DIOConfigItem.DIRECTION, 0x00)
   
    board.dio_output_write_port(id)

    bit0 = str(board.dio_input_read_bit(0))
    bit1 = str(board.dio_input_read_bit(1))
    bit2 = str(board.dio_input_read_bit(2))
    bit3 = str(board.dio_input_read_bit(3))
    bit4 = str(board.dio_input_read_bit(4))
    bit5 = str(board.dio_input_read_bit(5))
    bit6 = str(board.dio_input_read_bit(6))
    bit7 = str(board.dio_input_read_bit(7))    
        
    myDIO = [
        {'bit': 0,
        'value': bit0,},
        {'bit': 1,
        'value': bit1,},
        {'bit': 2,
        'value': bit2,},
        {'bit': 3,
        'value': bit3,},
        {'bit': 4,
        'value': bit4,},
        {'bit': 5,
        'value': bit5,},
        {'bit': 6,
        'value': bit7,},
        {'bit': 7,
        'value': bit7,} 
        ]

    return jsonify(myDIO)


@app.route('/AnalogOut0', methods=['GET'])
def AnaOut0():

    if 'id' in request.args:
        id = float(request.args['id'])
    else:
        return "Error detected"
    
    options = OptionFlags.DEFAULT
    boardAddr = select_hat_device(HatIDs.MCC_152) 
    board = mcc152(boardAddr)
            
    board.a_out_write(channel=0, value=id, options=options)
    return "SUCCESS"

@app.route('/AnalogOut1', methods=['GET'])
def AnaOut1():

    if 'id' in request.args:
        id = float(request.args['id'])
    else:
        return "Error detected"
    
    options = OptionFlags.DEFAULT
    boardAddr = select_hat_device(HatIDs.MCC_152) 
    board = mcc152(boardAddr)
    board.dio_reset()
        
    board.a_out_write(channel=1, value=id, options=options)
    return jsonify("SUCCESS")


@app.route('/AnalogInChan', methods=['GET'])
def AnaIN():

    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error detected"
        
    options = OptionFlags.DEFAULT
    boardAddr = select_hat_device(HatIDs.MCC_118) 
    board = mcc118(boardAddr)
    
    value = board.a_in_read(id, options)
    #value = value * 2
    #value = "{:.2f}".format(value)    
    
    myAnalogIn = [
        {'chan': id,
        'value': value,}
        ]

    return jsonify(myAnalogIn)


@app.route('/ButtonSet', methods=['GET'])
def ButtonSet():
    
    # setup button
    options = OptionFlags.DEFAULT
    
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error detected"
         
    #print("MCC 152 digital input interrupt example.")
    #print("Enables interrupts on the inputs and displays their state when")
    #print("they change.")
    #print("   Functions / Methods demonstrated:")
    #print("      mcc152.dio_reset")
    #print("      mcc152.dio_config_write_port")
    #print("      mcc152.dio_input_read_port")
    #print("      mcc152.dio_int_status_read_port")
    #print("      mcc152.info")
    #print("      interrupt_callback_enable")
    #print("      interrupt_callback_disable")
    #print()

    # Get an instance of the selected HAT device object.
    address = select_hat_device(HatIDs.MCC_152)

    #print("\nUsing address {}.\n".format(address))

    global HAT  # pylint: disable=global-statement

    HAT = mcc152(address)

    # Reset the DIO to defaults (all channels input, pull-up resistors
    # enabled).
    HAT.dio_reset()

    # use bit 6 as status of button press and set to 0
    HAT.dio_config_write_bit(6, DIOConfigItem.DIRECTION, 0)
    HAT.dio_output_write_bit(6, 0)
    
    # set up Analog out 1 to supply 5VDC to button
    HAT.a_out_write(channel=1, value=.5, options=options)
        
    # Read the initial input values so we don't trigger an interrupt when
    # we enable them.
    value = HAT.dio_input_read_port()

    # Enable latched inputs so we know that a value changed even if it changes
    # back to the original value before the interrupt callback.
    HAT.dio_config_write_port(DIOConfigItem.INPUT_LATCH, 0xFF)

    # Unmask (enable) interrupts on all channels.
    HAT.dio_config_write_port(DIOConfigItem.INT_MASK, 0x00)

    #print("Current input values are 0x{:02X}".format(value))
    #print("Waiting for changes, enter any text to exit. ")

    # Create a HAT callback object for our function
    callback = HatCallback(interrupt_callback)

    # Enable the interrupt callback function. Provide a mutable value for
    # user_data that counts the number of interrupt occurrences.

    int_count = [0]
    interrupt_callback_enable(callback, int_count)

    # Wait for the user to enter anything, then exit.
    if version_info.major > 2:
        input("")
    else:
        raw_input("")

    # Return the digital I/O to default settings.
    HAT.dio_reset()

    # Disable the interrupt callback.
    interrupt_callback_disable()
        
    return jsonify("Button Complete")

def interrupt_callback(user_data):
    """
    This function is called when a DAQ HAT interrupt occurs.
    """
    options = OptionFlags.DEFAULT
    HAT.a_out_write(channel=1, value=1, options=options)
      
    print("Interrupt number {}".format(user_data[0]))
    user_data[0] += 1

    # An interrupt occurred, make sure this board was the source.
    status = HAT.dio_int_status_read_port()

    if status != 0:
        HAT.a_out_write(channel=1, value=5, options=options)
        # use bit 6 as status of button press and set to 0
      
        i = HAT.info().NUM_DIO_CHANNELS
        print("Input channels that changed: ", end="")
        for i in range(8):
            if (status & (1 << i)) != 0:
                print("{} ".format(i), end="")
                
        # Read the inputs to clear the active interrupt.
        value = HAT.dio_input_read_port()
        
        HAT.dio_config_write_bit(6, DIOConfigItem.DIRECTION, 0)
        HAT.dio_output_write_bit(6, 1)
        
        print("\nCurrent port value: 0x{:02X}".format(value))
        
    return    

@app.route('/BitSet', methods=['GET'])
def BitSet():

     boardAddr = select_hat_device(HatIDs.MCC_152)
     board = mcc152(boardAddr)
     board.dio_output_write_bit(6,1)
     return jsonify("Bit set")

@app.route('/BitStatus', methods=['GET'])
def BitStatus():

    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "error detected"
        
    boardAddr = select_hat_device(HatIDs.MCC_152)
    board = mcc152(boardAddr)
       
    bitValue = board.dio_input_read_bit(6)
    
    #buttonStatus = [
    #    {'bitStatus': id,
    #    'bitValue': bitValue}
    #    ]  
    
    return str(bitValue)

@app.route('/ButtonClear', methods=['GET'])
def ButtonClear():

    options = OptionFlags.DEFAULT
    
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return jsonify("Error detected clearing bit 6")  

    boardAddr = select_hat_device(HatIDs.MCC_152)
    board = mcc152(boardAddr)
    board.dio_output_write_bit(6,0)
    board.a_out_write(channel=1, value=0, options=options)
    
    buttonReset = [
        {'ButtonStatus': id,
        'value': board.dio_input_read_bit(6),}
        ]
    
    return jsonify(buttonReset)
    
@app.route('/ResetMcc152', methods=['GET'])
def ResetMcc152():
    
    boardAddr = select_hat_device(HatIDs.MCC_152) 
    board = mcc152(boardAddr)
    board.dio_reset()
    
         
    return jsonify("MCC152 RESET")




if __name__ == '__main__':  
    app.run(host="10.111.7.131", port="5000")
    
    
