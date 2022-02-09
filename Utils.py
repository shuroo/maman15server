class Utils:

    @staticmethod
    def strFiller(content,sze):
        message = content
        fill = ' '
        align = '<'
        width = sze
        f'{message:{fill}{align}{width}}'

    @staticmethod
    def strToBytes(content):
       return bytes(content, 'UTF-8');

# UTF-16LE: A character encoding that maps code points of Unicode character set to a sequence of 2 bytes (16 bits).
# UTF-16LE stands for Unicode Transformation Format - 16-bit Little Endian.