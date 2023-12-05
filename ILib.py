import zlib ,struct ,math
def dec2bytes32(dec):
    return [x for x in struct.pack('>I' ,dec)]

HEADER ,IEND = [137, 80, 78, 71, 13, 10, 26, 10] ,[0 ,0 ,0 ,0 ,73, 69, 78, 68 ,174, 66, 96, 130]

def write(img ,filepath ,bKGD=None):
    size = (len(img[0]) ,len(img) ,len(img[0][0]))
    if (size[0] > 2**32 or size[1] > 2**32): raise AttributeError(f'image is too big to fit image height and width into 4 bytes! (image height and/or width needs to be less than 2^32 ({2**32})) image dimensions : \nheight : {size[0]}\nwidth : {size[1]}\n\nchannels : {size[2]}')
    
    IHDR = [73, 72, 68, 82] + dec2bytes32(size[0]) + dec2bytes32(size[1]) + [8 ,(6 if size[2] == 4 else 2) ,0 ,0 ,0]
    crc = zlib.crc32(bytes(IHDR[4:]) ,zlib.crc32(b'IHDR'))
    IHDR = dec2bytes32(len(IHDR)-4) + IHDR + dec2bytes32(crc)
    
    if bKGD != None:
        r = ('0'*(16-len(bin(bKGD[0])[2:]))+bin(bKGD[0])[2:])
        g = ('0'*(16-len(bin(bKGD[1])[2:]))+bin(bKGD[1])[2:])
        b = ('0'*(16-len(bin(bKGD[2])[2:]))+bin(bKGD[2])[2:])
        bKGD = [ord(x) for x in 'bKGD'] + [int(r[:8] ,2) ,int(r[8:16] ,2) ,int(g[:8] ,2) ,int(g[8:16] ,2) ,int(b[:8] ,2) ,int(b[8:16] ,2)]
    
    imgdat = []
    for x in img:
        row = []
        for y in x:
            y = [(z.real if type(z) == complex else z) for z in y]
            y = [(0 if math.isnan(z) else z) for z in y]
            y = [(0 if z == float('-inf') else z) for z in y]
            y = [(255 if z == float('inf') else z) for z in y]
            p = [((int(z) if int(z) < 256 else 255) if (int(z) if int(z) < 256 else 255) > -1 else 0) for z in y]
            row += p
        imgdat += [0,] + row
    IDAT = [73, 68, 65, 84] + [x for x in zlib.compress(bytes(imgdat))]
    crc = zlib.crc32(bytes(IDAT[4:]) ,zlib.crc32(b'IDAT'))
    IDAT = dec2bytes32(len(IDAT)-4) + IDAT + dec2bytes32(crc)
    
    if bKGD == None:
        FINAL = HEADER + IHDR + IDAT + IEND
    else:
        FINAL = HEADER + IHDR + bKGD + IDAT + IEND
    with open(f'{filepath}.png' ,'wb') as f:
        f.write(bytes(FINAL))
        f.close()

def read(filepath ,debug=False):
    DATA = open(f'{filepath}.png' ,'rb').read()
    
    DAT = DATA[8:]
    i = 0
    chunks = {}
    done = False
    while not done:
        L ,name = struct.unpack('>I' ,DAT[i:i+4])[0] ,bytes(DAT[i+4:i+8])
        if name == b'IEND':
            done = True
            data  = []
        i += 8
        c ,data = 0 ,[]
        while c != L:
            data.append(DAT[i])
            i += 1
            c += 1
        crc = struct.unpack('>I' ,DAT[i:i+4])[0]
        i += 4
        if name == b'IEND':
            crc = 2923585666
        Ecrc = zlib.crc32(bytes(data), zlib.crc32(name))
        if crc != Ecrc:
            if name in (b'IHDR' ,b'PLTE' ,b'IDAT' ,b'IEND'):
                raise Exception(f'critical chunk crc error! {"".join([chr(x) for x in name])} chunk! chunk listed crc as [{crc}] but the computed crc of the chunk was : [{Ecrc}]')
            else:
                continue
        else:
            chunks[name] = {'data':bytes(data) ,'crc':crc}
    
    IHDR_data ,IDAT_data = chunks[b'IHDR']['data'] ,chunks[b'IDAT']['data']
    
    width ,height ,colour_depth ,colour_type = struct.unpack('>I' ,IHDR_data[0:4])[0] ,struct.unpack('>I' ,IHDR_data[4:8])[0] ,int(IHDR_data[8]) ,int(IHDR_data[9])
    compression_mode ,filter_mode ,interlace = int(IHDR_data[10]) ,int(IHDR_data[11]) ,int(IHDR_data[12])
    if debug:
        print(f'\n{"-"*50}\n\nimage data (from IHDR) : [{width}x{height}] ,colour depth : {colour_depth} ,colour type : {("RGB" if colour_type == 2 else ("RGBA" if colour_type == 6 else "currently unsupported colour type!"))}\ncompression type : {compression_mode} ,filter type : {filter_mode} ,interlacing? : {interlace == 1}\n\n\n')
    
    #
    # FILTER APPLICATION CODE
    #
    
    IDAT_data = zlib.decompress(IDAT_data)
    data2 = [x for x in IDAT_data][1:]
    
    data ,img = [] ,[]
    counter ,channels = 0 ,(3 if colour_type == 2 else 4)
    for y in range(height):
        row = []
        for x in range(width):
            pixel = []
            for c in range(channels):
                pixel.append(data2[counter])
                counter += 1
            row.append(pixel)
        img.append(row)
        counter += 1
    
    if debug:
        return img ,chunks
    else:
        return img
