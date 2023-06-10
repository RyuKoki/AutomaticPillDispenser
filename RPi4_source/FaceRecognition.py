import face_recognition
import cv2
import numpy as np
import mysql.connector as mysql

class FaceRecognition():

    def __init__( self ):
        # class attributes
        # self.HOST = "192.168.43.11"
        self.HOST = "localhost"
        self.DATABASE = "medtest01"
        self.USER = "root"
        self.PASSWORD = "123456"
        self.know_encodings = []
        self.know_name = []
        self.know_IDN = []
        # connecting to database
        mydb = mysql.connect( host=self.HOST, 
                              database=self.DATABASE, 
                              user=self.USER, 
                              password=self.PASSWORD )
        print( "Connected to:", mydb.get_server_info() )
        self.cursor = mydb.cursor()
        self.cursor.execute( "SELECT IDN, first_name, face FROM medtest01.medapp_elder;" )
        # getting face infomation from database
        for i in self.cursor:
            carry = i[ 2 ].replace( '"', '' )
            pic = eval( 'np.array(' + carry + ')' )
            self.know_encodings.append( pic )
            self.know_name.append( i[1] )
            self.know_IDN.append(i[0])
    
    def find_facecode(self):
        # opening web camera
        cam = cv2.VideoCapture( 0 )
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # set frame width
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # set frame height
        
        process_this_frame = True
        while( True ):
            # capture image
            ret, frame = cam.read()
            frame = cv2.flip( frame, 1 )

            if( process_this_frame ):
                # Convert the image to small and from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                small_frame = cv2.resize( frame, (0, 0), fx=0.25, fy=0.25 )
                rgb_small_frame = cv2.cvtColor( small_frame, cv2.COLOR_BGR2RGB )
                
                # Find all faces and do face encodings in camera
                face_locations = face_recognition.face_locations( rgb_small_frame )
                face_encoding = face_recognition.face_encodings( rgb_small_frame, face_locations )

            process_this_frame = not process_this_frame
            
            for top, right, bottom, left in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # show image and rec frame that detect face
            cv2.imshow("frame", frame)
            command = cv2.waitKey(10)
            if command==ord('q') or len(face_locations)>= 1: 
                print ("Ending program")
                import time
                time.sleep( 3 )
                cam.release()
                cv2.destroyAllWindows()
                break  # end program
        return face_encoding[0]


    def face_detrog( self , facecode ):
        face_IDN = []
        face_fname = ''
        face_distance = face_recognition.face_distance( self.know_encodings, facecode )
        best_match_index = np.argmin( face_distance )
        face_percent = 1 - face_distance[best_match_index]
        # if similar > 60 % return name else = unknow
        if face_percent > 0.6:
            IDN = self.know_IDN[best_match_index]
            face_fname = self.know_name[best_match_index]
        else:
            IDN = ''
        face_IDN.append(IDN)
        return [face_IDN[0], face_fname]
    
    def all_id(self):
        return self.know_IDN
