# -*- coding= utf-8 -*-

import os
import sys
import numpy as np
from PIL import Image

# bmp_folder = "FANTASYTCHI/bmp"
# source_bin = "FANTASYTCHI.bin"
# output_bin = "FANTASYTCHI_MOD.bin"
bmp_folder = sys.argv[1]
source_bin = sys.argv[2]
output_bin = sys.argv[3]

address = 0x80000
new_gfx = []
new_gfx_address =[]

def gfx2data(flie):
    data = []
    gfx = []
    palette = []
    print("{}".format(flie))
    im = Image.open(flie).convert("RGB")
    width = im.width
    height = im.height
    for h in range(height):
        for w in range(width):
            color = im.getpixel((w,h))
            R = color[0]>>3
            G = color[1]>>2
            B = color[2]>>3
            rgb565 = (R<<11)|(G<<5)|B
            if rgb565 in palette:
                pass
            else:
                palette.append(rgb565)
            gfx.append(palette.index(rgb565))
    palette_length = len(palette)
    if palette_length > 256:
        print("-")
        print("Error!")
        print("Palette length:{:>3d}".format(len(palette)))
        print("BMP files support up to 256 different colors.")
        print("Please reduce the colors you use.")
        sys.exit()
    info_size = palette_length * 2 + 8
    data.append(info_size & 0xFF)
    data.append(info_size >> 8)
    data.append(width & 0xFF)
    data.append(width >> 8)
    data.append(height & 0xFF)
    data.append(height >> 8)
    data.append(palette_length & 0xFF)
    data.append(palette_length >> 8)
    for i in range(palette_length):
        data.append(palette[i] & 0xFF)
        data.append(palette[i] >> 8)
    data.extend(gfx)
    return data

def main():
    with open(source_bin,"rb") as f:
        data_list = list(f.read())
    gfx_address = int(data_list[address]+(data_list[address+1]<<8))
    gfx_num = int(gfx_address/4)
    bmps = os.listdir("{}".format(bmp_folder))
    for i in range(gfx_num):
        new_gfx_address.append((gfx_address>>0)&0xFF)
        new_gfx_address.append((gfx_address>>8)&0xFF)
        new_gfx_address.append((gfx_address>>16)&0xFF)
        new_gfx_address.append((gfx_address>>32)&0xFF)
        data = gfx2data("{}/{}".format(bmp_folder, bmps[i]))
        new_gfx.extend(data)
        gfx_address = gfx_address + len(data)
    with open("{}".format(output_bin), 'wb') as f:
        for x in data_list[:address]:
            f.write(bytes.fromhex("%02x"%x))
        for x in new_gfx_address:
            f.write(bytes.fromhex("%02x"%x))
        for x in new_gfx:
            f.write(bytes.fromhex("%02x"%x))
        for x in data_list[address+len(new_gfx_address)+len(new_gfx):]:
            f.write(bytes.fromhex("%02x"%x))
    print("-")
    print("Done.")

if __name__ == '__main__':
    main()