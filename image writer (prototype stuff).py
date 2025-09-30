#https://en.wikipedia.org/wiki/Portable_Network_Graphics#%22Chunks%22_within_the_file
#https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/PNG-Gradient_hex.png/784px-PNG-Gradient_hex.png
#https://cdn-images-1.medium.com/max/1600/1*t3TpfBRDZECoO_hRklG33A.png
#http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
'''
"Chunks" within the file

After the header, comes a series of chunks, each of which conveys certain information about the image. Chunks declare themselves as critical or ancillary, and a program encountering an ancillary chunk that it does not understand can safely ignore it. This chunk-based storage layer structure, similar in concept to a container format or to Amiga's IFF, is designed to allow the PNG format to be extended while maintaining compatibility with older versions—it provides forward compatibility, and this same file structure (with different signature and chunks) is used in the associated MNG, JNG, and APNG formats.

A chunk consists of four parts: length (4 bytes, big-endian), chunk type/name (4 bytes), chunk data (length bytes) and CRC (cyclic redundancy code/checksum; 4 bytes). The CRC is a network-byte-order CRC-32 computed over the chunk type and chunk data, but not the length.
Length 	Chunk type 	Chunk data 	CRC
4 bytes 	4 bytes 	Length bytes 	4 bytes

Chunk types are given a four-letter case sensitive ASCII type/name; compare FourCC. The case of the different letters in the name (bit 5 of the numeric value of the character) is a bit field that provides the decoder with some information on the nature of chunks it does not recognize.
The case of the first letter indicates whether the chunk is critical or not. If the first letter is uppercase, the chunk is critical; if not, the chunk is ancillary. Critical chunks contain information that is necessary to read the file. If a decoder encounters a critical chunk it does not recognize, it must abort reading the file or supply the user with an appropriate warning.
The case of the second letter indicates whether the chunk is "public" (either in the specification or the registry of special-purpose public chunks) or "private" (not standardised). Uppercase is public and lowercase is private. This ensures that public and private chunk names can never conflict with each other (although two private chunk names could conflict).
The third letter must be uppercase to conform to the PNG specification. It is reserved for future expansion. Decoders should treat a chunk with a lower case third letter the same as any other unrecognised chunk.
The case of the fourth letter indicates whether the chunk is safe to copy by editors that do not recognize it. If lowercase, the chunk may be safely copied regardless of the extent of modifications to the file. If uppercase, it may only be copied if the modifications have not touched any critical chunks. 


Critical chunks

A decoder must be able to interpret critical chunks to read and render a PNG file.

#   IHDR must be the first chunk; it contains (in this order) the image's width (4 bytes); height (4 bytes); bit depth (1 byte, values 1, 2, 4, 8, or 16); color type (1 byte, values 0, 2, 3, 4, or 6); compression method (1 byte, value 0); filter method (1 byte, value 0); and interlace method (1 byte, values 0 "no interlace" or 1 "Adam7 interlace") (13 data bytes total). As stated in the World Wide Web Consortium, bit depth is defined as "the number of bits per sample or per palette index (not per pixel)".
    PLTE contains the palette: a list of colors.
#   IDAT contains the image, which may be split among multiple IDAT chunks. Such splitting increases filesize slightly, but makes it possible to generate a PNG in a streaming manner. The IDAT chunk contains the actual image data, which is the output stream of the compression algorithm.
#   IEND marks the image end; the data field of the IEND chunk has 0 bytes/is empty.

The PLTE chunk is essential for color type 3 (indexed color). It is optional for color types 2 and 6 (truecolor and truecolor with alpha) and it must not appear for color types 0 and 4 (grayscale and grayscale with alpha).


Ancillary chunks

Other image attributes that can be stored in PNG files include gamma values, background color, and textual metadata information. PNG also supports color management through the inclusion of ICC color space profiles.

    bKGD gives the default background color. It is intended for use when there is no better choice available, such as in standalone image viewers (but not web browsers; see below for more details).
    cHRM gives the chromaticity coordinates of the display primaries and white point.
    dSIG is for storing digital signatures.
    eXIf stores Exif metadata.
    gAMA specifies gamma. The gAMA chunk contains only 4 bytes, and its value represents the gamma value multiplied by 100,000; for example, the gamma value 1/3.4 calculates to 29411.7647059 ((1/3.4)*(100,000)) and is converted to an integer (29412) for storage.
    hIST can store the histogram, or total amount of each color in the image.
    iCCP is an ICC color profile.
    iTXt contains a keyword and UTF-8 text, with encodings for possible compression and translations marked with language tag. The Extensible Metadata Platform (XMP) uses this chunk with a keyword 'XML:com.adobe.xmp'
    pHYs holds the intended pixel size (or pixel aspect ratio); the pHYs contains "Pixels per unit, X axis" (4 bytes), "Pixels per unit, Y axis" (4 bytes), and "Unit specifier" (1 byte) for a total of 9 bytes.
    sBIT (significant bits) indicates the color-accuracy of the source data; this chunk contains a total of between 1 and 13 bytes.
    sPLT suggests a palette to use if the full range of colors is unavailable.
    sRGB indicates that the standard sRGB color space is used; the sRGB chunk contains only 1 byte, which is used for "rendering intent" (4 values—0, 1, 2, and 3—are defined for rendering intent).
    sTER stereo-image indicator chunk for stereoscopic images.
    tEXt can store text that can be represented in ISO/IEC 8859-1, with one key-value pair for each chunk. The "key" must be between 1 and 79 characters long. Separator is a null character. The "value" can be any length, including zero up to the maximum permissible chunk size minus the length of the keyword and separator. Neither "key" nor "value" can contain null character. Leading or trailing spaces are also disallowed.
    tIME stores the time that the image was last changed.
    tRNS contains transparency information. For indexed images, it stores alpha channel values for one or more palette entries. For truecolor and grayscale images, it stores a single pixel value that is to be regarded as fully transparent.
    zTXt contains compressed text (and a compression method marker) with the same limits as tEXt.

The lowercase first letter in these chunks indicates that they are not needed for the PNG specification. The lowercase last letter in some chunks indicates that they are safe to copy, even if the application concerned does not understand them. 
'''
#https://gist.github.com/Chr1sDev/ce8630ed8f7a50a401d493f2fae70dc8

# EXAMPLE / TEST IMAGES
#----------------------------------------------------------------------------------------------------------------------------------------
#img = [[[0,]*3 for y in range(200)] for x in range(200)]
#for x in range(20):
#    for y in range(20):
#        img[x+80][y+80] = [255,]*3

#img = [[[255,255,255] ,[0,255,0] ,[0,0,255] ,[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,0]],
#       [[255,0,0] ,[255,255,255] ,[0,255,0] ,[0,0,255] ,[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,0]],
#       [[0,0,255] ,[255,0,0] ,[255,255,255] ,[0,255,0] ,[0,0,255] ,[0,0,0] ,[0,0,0] ,[0,0,0]],
#       [[0,0,0] ,[0,0,255] ,[255,0,0] ,[255,255,255] ,[0,255,0] ,[0,0,255] ,[0,0,0] ,[0,0,0]],
#       [[0,0,0] ,[0,0,0] ,[0,0,255] ,[255,0,0] ,[255,255,255] ,[0,255,0] ,[0,0,255] ,[0,0,0]],
#       [[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,255] ,[255,0,0] ,[255,255,255] ,[0,255,0] ,[0,0,255]],
#       [[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,255] ,[255,0,0] ,[255,255,255] ,[0,255,0]],
#       [[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,0] ,[0,0,255] ,[255,0,0] ,[255,255,255]]]
#img = [[x+[255,] for x in y] for y in img]

#img = [[((x*1.5)/10 ,y/5 ,y/10 ,255) for x in range(2000)] for y in range(2000)]
#img = [[(x/10 ,y/10 ,((y/10)*(x/10))**.75 ,255) for x in range(2000)] for y in range(2000)]
#img = [[(x/4 ,0 ,y/4) for x in range(1000)] for y in range(2005)]


'''
from random import randint as rand

img = [[(0 ,)*3 for x in range(500)] for y in range(500)]
#voronoi tesselation
num = rand(75 ,125)
coords = []
for n in range(num):
    select = True
    while select:
        c = rand(0 ,len(img)-1) ,rand(0 ,len(img[0])-1)
        if not (c in coords):
            coords.append(c)
            select = False
for y in range(len(img)):
    for x in range(len(img[0])):
        d = 100000000000
        for p in coords:
            d = min(d ,((p[0]-x)**2 + (p[1]-y)**2)**.5)
        img[y][x] = (d ,)*3
'''
#img = [[[255 ,1 ,1] ,[255 ,1 ,1]] ,
#       [[255 ,1 ,1] ,[255 ,1 ,1]]]

#https://hexed.it/

#img = [[[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128]],
#       [[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128]],
#       [[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128]],
#       [[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128] ,[0,255,128]]]

img = [[[0 ,0 ,0],[255 ,0 ,0],[0 ,255 ,0],[0 ,0 ,255]],
       [[0 ,0 ,255],[0 ,255 ,0],[255 ,0 ,0],[0 ,0 ,0]],]
'''
import raymarching
sphere = raymarching.Object(0 ,0 ,0 ,'sphere' ,raymarching.sdfs.sphere ,(0,)*3 ,{'radius':3} ,(0 ,255 ,128))
cube = raymarching.Object(0 ,0 ,0 ,'square' ,raymarching.sdfs.box ,(0,)*3 ,{'dimensions':(3,3,3)} ,(255 ,0 ,0))

mode = 'rgb'#'distance'#
#objects = [sphere ,cube]# ,plane]
objects = []
objects.append(cube)#sphere)

cam = raymarching.camera(0 ,0 ,0 ,1 ,1 ,1 ,objects)
F = cam.frame(mode ,(200,200))
if mode == 'distance':
    img = [[(x*10,)*3 for x in y] for y in F]
else:
    img = [[(x if type(x) == tuple or type(x) == list else (x,)*3) for x in y] for y in F]
'''
#----------------------------------------------------------------------------------------------------------------------------------------


name = 'img'
filepath = input('filepath : ')#r''
size = (len(img[0]) ,len(img) ,len(img[0][0]))
if (size[0] > 2**32 or size[1] > 2**32): raise AttributeError(f'image is too big to fit image height and width into 4 bytes! (image height and/or width needs to be less than 2^32 ({2**32})) image dimensions : \nheight : {size[0]}\nwidth : {size[1]}\n\nchannels : {size[2]}')


print('-- START --')
print(size)

import zlib ,struct
def dec2bytes32(dec):
    return [x for x in struct.pack('>I' ,dec)]

HEADER ,IEND = [137, 80, 78, 71, 13, 10, 26, 10] ,[0 ,0 ,0 ,0 ,73, 69, 78, 68 ,174, 66, 96, 130]

#dimbytes = (('0'*(32-len(bin(size[0])[2:])))+bin(size[0])[2:]) + (('0'*(32-len(bin(size[1])[2:])))+bin(size[1])[2:]) ---> [int('0b'+dimbytes[(x*8):(x*8)+7] ,2) for x in range(8)]
IHDR = [73, 72, 68, 82] + dec2bytes32(size[0]) + dec2bytes32(size[1]) + [8 ,(6 if size[2] == 4 else 2) ,0 ,0 ,0]#16 ,(6 if size[2] == 4 else 2) ,0 ,0 ,0]
crc = zlib.crc32(bytes(IHDR[4:]) ,zlib.crc32(b'IHDR'))
print(f'IHDR CRC : {crc}')
IHDR = dec2bytes32(len(IHDR)-4) + IHDR + dec2bytes32(crc)# + len(dec2bytes32(crc))

imgdat = []
for x in img:
    row = []
    for y in x:
        row += [((int(z) if int(z) < 256 else 255) if (int(z) if int(z) < 256 else 255) > -1 else 0) for z in y]
    imgdat += [0,] + row
IDAT = [73, 68, 65, 84] + [x for x in zlib.compress(bytes(imgdat))]# + [x for x in zlib.flush()]
crc = zlib.crc32(bytes(IDAT[4:]) ,zlib.crc32(b'IDAT'))
print(f'IDAT CRC : {crc}')
IDAT = dec2bytes32(len(IDAT)-4) + IDAT + dec2bytes32(crc)# + len(dec2bytes32(crc))



FINAL = HEADER + IHDR + IDAT + IEND
print(f'\n\n\n{FINAL}')
print(f'\n{bytes(FINAL)}')
with open(f'{filepath}{name}.png' ,'wb') as f:
    f.write(bytes(FINAL))
    f.close()


