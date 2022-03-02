class Utils:

    @staticmethod
    def strFillerWithSpaces(content, sze):
        message = content
        fill = ' '
        align = '<'
        width = sze
        return f'{message:{fill}{align}{width}}'

    @staticmethod
    def strFillerWithNulls(content, sze):
        message = content
        fill = '\0'
        align = '<'
        width = sze
        return f'{message:{fill}{align}{width}}'

    @staticmethod
    def strFillerWithTrailingZeros(content, sze):
        number_str = str(content)
        zero_filled_number = number_str.zfill((sze - len(number_str)))
        return Utils.strToBytes(zero_filled_number)

    @staticmethod
    def addNullTerminator(content):
        return Utils.strFillerWithNulls(content,len(content)+1)

    @staticmethod
    def strToBytes(content):
       return bytes(content, 'UTF-8');

    @staticmethod
    def uncodeIntAsString(integer):
        str_int = Utils.strToBytes(Utils.addNullTerminator(str(integer)))
        print('Decoded int as string:',str_int)
        return str_int;

# UTF-16LE: A character encoding that maps code points of Unicode character set to a sequence of 2 bytes (16 bits).
# UTF-16LE stands for Unicode Transformation Format - 16-bit Little Endian.