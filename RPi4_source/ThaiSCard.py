# pyscard library
from smartcard.System import readers
from smartcard.util import toHexString
from datetime import datetime

class ThaiSCard:
    
    def __init__( self ):
        self.SELECT     = [0x00, 0xA4, 0x04, 0x00, 0x08]
        self.THAI_CARD  = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
        self.CMD_CID    = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]        # CID
        self.CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]    # TH Fullname
        self.CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]    # EN Fullname
        self.CMD_BIRTH  = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]        # Date of Birth
        self.CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]        # Gender
        self.CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]        # Card Issuer
        self.CMD_ISSUE  = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]        # Issue Date
        self.CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]        # Expire Date
        self.CMD_ADDRESS    = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]    # Address
        # Photo
        self.CMD_PHOTO1 = [0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO2 = [0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO3 = [0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO4 = [0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO5 = [0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO6 = [0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO7 = [0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO8 = [0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO9 = [0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO10 = [0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO11 = [0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO12 = [0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO13 = [0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO14 = [0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO15 = [0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO16 = [0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO17 = [0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO18 = [0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO19 = [0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF]
        self.CMD_PHOTO20 = [0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF]
        # connecting to smart card reader
        reader_list = readers()
        reader_index = 0
        reader = reader_list[ reader_index ]
        # print( "Using: ", reader )
        self.connection = reader.createConnection()
        self.connection.connect()
        ATR = self.connection.getATR()
        # print( "ATR: ", toHexString( ATR ) )
        if ( ATR[0]==0x38 & ATR[1]==0x67 ):
            self.REQUEST = [0x00, 0xC0, 0x00, 0x01]
        else:
            self.REQUEST = [0x00, 0xC0, 0x00, 0x00]
        self.DATA, self.SW1, self.SW2 = self.connection.transmit( self.SELECT+self.THAI_CARD )

    def thai2unicode( self, data ):
        result = ""
        result = bytes( data ).decode( 'tis-620' )
        return result

    def get_data( self, command, request=[0x00, 0xC0, 0x00, 0x00] ):
        DATA, SW1, SW2 = self.connection.transmit( command )
        DATA, SW1, SW2 = self.connection.transmit( request + [command[-1]] )
        return [ DATA, SW1, SW2 ]

    def ID( self ):
        id_req = self.get_data( self.CMD_CID, self.REQUEST )
        id_data = id_req[0]
        id_number = self.thai2unicode(id_data)
        return id_number

    def fullname( self ):
        name_req = self.get_data( self.CMD_THFULLNAME, self.REQUEST )
        name_data = name_req[0]
        # remove all of space bar
        name_data = [ c for c in name_data if c != 32 ]
        name_list = self.thai2unicode(name_data)
        name_list = name_list.split("#")
        # remove all of empty element
        name_list = [ e for e in name_list if e != '' ]
        return { "first_name": name_list[1], "sure_name": name_list[2] }
    
    def birthday( self ):
        bd_req = self.get_data( self.CMD_BIRTH, self.REQUEST )
        bd_data = bd_req[0]
        bday = self.thai2unicode(bd_data)
        bday = str(int(bday[0:4])-543) + '-' + bday[4:6] + '-' + bday[6:]
        Bday = datetime.strptime( bday, '%Y-%M-%d' )
        return Bday.date()
