#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc134, mcc152, mcc118, HatIDs, HatError, TcTypes, hat_list, DIOConfigItem, OptionFlags
from daqhats_utils import select_hat_device, tc_type_to_string, enum_mask_to_string
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = False

@app.route('/TCtemps')
def index():
    address = select_hat_device(HatIDs.MCC_134)
    hat = mcc134(address)
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 1  # Seconds
    channels = (0, 1, 2, 3)
    
    for channel in channels:
        hat.tc_type_write(channel, tc_type)

    tempZero = str(hat.t_in_read(0))
    tempOne = str(hat.t_in_read(1))
    tempTwo = str(hat.t_in_read(2))
    tempThree = str(hat.t_in_read(3))
        
    temps = [
        {'chan': 0,
        'value': tempZero,},
        {'chan': 1,
        'value': tempOne,},
        {'chan': 2,
        'value': tempTwo,},
        {'chan': 3,
        'value': tempThree,} 
        ]
   
    return jsonify(temps)
            
        
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
    board.dio_reset()

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
    board.dio_reset()
        
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
    
    myAnalogIn = [
        {'chan': id,
        'value': value,}
        ]

    
    return jsonify(myAnalogIn)


        
if __name__ == '__main__':
    app.run(host="10.111.3.40", port="5000")