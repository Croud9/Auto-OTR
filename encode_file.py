import os

def to_utf8(srcfile, trgfile):
    try:
        with open(srcfile, 'r') as f, open(trgfile, 'w', encoding="utf-8") as e:
            text = f.read() # for small files, for big use chunks
            e.write(text)
        os.remove(srcfile) # remove old encoding file
        os.rename(trgfile, srcfile) # rename new encoding
        print('to utf8 sucscs')
    except UnicodeDecodeError:
        print('Decode Error')
    except UnicodeEncodeError:
        print('Encode Error')