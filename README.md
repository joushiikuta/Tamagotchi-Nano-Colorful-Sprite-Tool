# Tamagotchi-Nano-Colorful-Sprite-Tool

Extract and reimport sprites for Tamagotchi Nano Colorful using Python.

## Usage

### Export sprites
```
python bin2gfx.py <romPath> <outDir>
```
- `romPath`: Path to the ROM file
- `outDir`: The directory to export into

Files are exported as PNG files and BMP files into `outDir`.

e.g. python bin2gfx.py FANTASYTCHI.bin FANTASYTCHI

### Import sprites
```
python bmp2bin.py <inDir> <romPath> <outFile>
```
- `inDir`: The folder that contains BMP files to import
- `romPath`: Path to the ROM file
- `outFile`: Path to the repacked ROM file

e.g. python bmp2bin.py FANTASYTCHI_MOD/bmp FANTASYTCHI.bin FANTASYTCHI_MOD.bin
