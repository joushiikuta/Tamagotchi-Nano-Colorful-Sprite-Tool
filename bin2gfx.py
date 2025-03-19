# -*- coding= utf-8 -*-

import os
import sys
import numpy as np
from PIL import Image

# source_bin = "FANTASYTCHI.bin"
# output_folder = "FANTASYTCHI"
source_bin = sys.argv[1]
output_folder = sys.argv[2]

address = 0x80000

png_output_folder = "{}/png".format(output_folder)
bmp_output_folder = "{}/bmp".format(output_folder)
os.makedirs(png_output_folder, exist_ok = True)
os.makedirs(bmp_output_folder, exist_ok = True)

def getInfo(addr):
    info = []
    for i in range(int(data_list[addr]/2)):
        info.append(data_list[addr+i*2]+(data_list[addr+i*2+1]<<8))
    return info

def getPalette(info):
    global data_list
    palette = []
    p = info[-1*info[3]:]
    for i in range(len(p)):
        rgb565 = p[i]
        MASK5 = 0b011111
        MASK6 = 0b111111
        R = ((rgb565 >> 11) & MASK5) << 3
        G = ((rgb565 >> 5) & MASK6) << 2
        B = (rgb565 & MASK5) << 3
        palette.append(R)
        palette.append(G)
        palette.append(B)
    return palette

def saveGFX(addr, n):
    info = getInfo(addr)
    gfx_addr = addr + info[0]
    width = info[1]
    height = info[2]
    data_list_2D = np.reshape(data_list[gfx_addr:gfx_addr+width*height], (height,width))
    gfx_original = Image.fromarray(np.uint8(data_list_2D))
    gfx_palette = Image.new('P', gfx_original.size)
    gfx_palette.putpalette(getPalette(info))
    gfx_palette.paste(gfx_original, (0, 0))
    gfx_converted = gfx_palette.convert("RGBA")
    gfx_new = []
    for i in gfx_converted.getdata():
        if i == (0, 252, 0, 255):
            gfx_new.append((0, 255, 0, 0))
        else:
            gfx_new.append(i)
    gfx_converted.putdata(gfx_new)
    print("{:0>3d}".format(n))
    gfx_converted.save("{}/{:0>3d}.png".format(png_output_folder,n))
    gfx_converted.convert("RGB").save("{}/{:0>3d}.bmp".format(bmp_output_folder,n))

def main():
    global data_list
    with open(source_bin,"rb") as f:
        data_list = list(f.read())
    gfx_num = int((data_list[address]+(data_list[address+1]<<8))/4)
    for i in range(gfx_num):
        addr = address+(data_list[address+i*4])+(data_list[address+i*4+1]<<8)+(data_list[address+i*4+2]<<16)+(data_list[address+i*4+3]<<24)
        saveGFX(addr, i)
    print("-")
    print("Done.")

if __name__ == '__main__':
    main()