#!/usr/bin/python

import iso_media
import res_switch
from PIL import Image
from StringIO import StringIO
import sys

codecs = {
        "res_switch": res_switch.ResSwitch,
        }
def ric_encode(imgbuf, codec_type, encode_options):
    codec = codecs[codec_type]
    img = Image.open(StringIO(imgbuf))
    encoder = codec.Algo.Encoder(img, encode_options)
    layers = encoder.encode()
    wrapped_layers, offsetTable = codec.Wrapper().wrapLayers(layers)
    output = ""
    output += iso_media.write_box("FTYP", "RIC ")
    output += iso_media.write_box("ILOT", write_layer_offsets(offsetTable))
    output += wrapped_layers
    return output

def ric_decode(imgbuf, codec_type, encode_options):
    codec = codecs[codec_type]
    offset = 0
    boxType = None
    boxLen, boxType, payload = iso_media.read_box(imgbuf[offset:])
    if boxType != "FTYP" or payload != "RIC ":
        print >> sys.stderr, "Fishy file type!!!", boxType, payload
        return None
    offset += boxLen
    boxLen, boxType, payload = iso_media.read_box(imgbuf[offset:])
    if boxType != "ILOT":
        print >> sys.stderr, "No offset table???", boxType
        return None
    offset += boxLen
    layers = codec.Wrapper().unwrapLayers(imgbuf[offset:])
    outputImg = codec.Algo.Decoder(layers).decode()
    output = StringIO()
    outputImg.save(output, "JPEG", quality = 90);
    return output.getvalue()


def write_layer_offsets(offsetTable):
    buf = ""
    for offset, res in offsetTable:
        buf += iso_media.write_int16(res)
        buf += iso_media.write_int32(offset)
    return buf

commands = {
        "decode": ric_decode,
        "encode": ric_encode,
        }

def read_cli_args():
    if len(sys.argv) < 4:
        print >>sys.stderr, "Usage:", sys.argv[0], "<input file> <output file> <resolution 1> <resolution 2> ...."
        return None
    commandStr = sys.argv[1]
    if not commands.has_key(commandStr):
        print >> sys.stderr, "Command can be only one of", commands.keys()
        return None
    command = commands[commandStr]
    input_filename = sys.argv[2]
    output_filename = sys.argv[3]
    resolutions = []
    prev_res = 0
    res = 0
    for i in range(4, len(sys.argv)):
        res = sys.argv[i]
        if res < prev_res:
            print >> sys.stderr, "Resolutions must be in incremental order"
            return None
        resolutions.append(int(sys.argv[i]))
    return command, input_filename, output_filename, resolutions

def apply(command, input_filename, output_filename, resolutions):
    input = open(input_filename, "rb").read()
    output = command(input, "res_switch", {'resolutions': resolutions})
    if output:
        open(output_filename, "wb").write(output)

def main():
    args = read_cli_args()
    if args:
        apply(*args)

if __name__ == "__main__":
    main()


