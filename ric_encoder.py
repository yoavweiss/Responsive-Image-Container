#!/usr/bin/python

import pil
import iso_media

def ric_encode(org_image, encode_type, encode_options):
    if encode_type == "res_switch":
        image_layers = res_switch_encoder(org_image)
    output = write_header()
    output += write_layer_offsets(image_layers)
    output += wrwite_layers(image_layers)


