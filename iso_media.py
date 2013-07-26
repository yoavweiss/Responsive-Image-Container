import struct

INT32_LEN = 4

def read_int32(data):
    return struct.unpack(">I", data[0:4])[0]

def write_int32(num):
    return struct.pack(">I", num)

def read_int16(data):
    return struct.unpack(">H", data[0:4])[0]

def write_int16(num):
    return struct.pack(">H", num)

def read_box(data):
    length = read_int32(data)
    if length > len(data):
        print length, ">", len(data)
        raise Exception("Box length is larger than provided data")
    type = data[4:8]
    payload = data[8:length]
    return length, type, payload

def write_box(type, payload):
    if len(type) != INT32_LEN:
        raise Exception("Box type length is not 4")
    length = INT32_LEN + len(type) + len(payload)
    writeBuffer = write_int32(length)
    writeBuffer += type
    writeBuffer += payload
    return writeBuffer
