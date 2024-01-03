import hashlib
from datetime import datetime
from cryptography.fernet import Fernet

# 서버 실행 시 쿠키 암호화에 사용되는 값 재설정
key = Fernet.generate_key()
fernet = Fernet(key)

# 암호화
def encrypt(str):
    encrypt_str = fernet.encrypt((str))
    return encrypt_str

#복호화
def decrypt(str):
    decrypt_str = fernet.decrypt(str)
    return decrypt_str

# OTP 값 생성 시 사용될 enum 선언 문자를 ASCII 값에 매핑함.
enumdic = {'0' : 48, '1' : 49, '2' : 50, '3' : 51, '4' : 52, '5' : 53, '6' : 54, '7' : 55, '8' : 56, '9' : 57,
            'a' : 97, 'b' : 98, 'c' : 99, 'd' : 100, 'e' : 101, 'f' : 102}

# OTP 값 생성 시 enum 참조해서 문자를 ASCII 값으로 리턴
def StoI(str):
    return enumdic[str]

# OTP 값 생성 시 Text를 sha256 해싱함
def hash(str):
    result = hashlib.sha256(str.encode())
    return result.hexdigest()

# SerialCode, TimeCode 값을 이용, 8자리 OTP값을 생성
def GenOTP(SN, TimeCode):
    code = [0, 0, 0, 0, 0, 0, 0, 0]
    ti = str(TimeCode)
    OriginStr = SN + ti
    HashedStr = hash(OriginStr)
    for i in range(0,8):
        sum = 0
        for j in range(0,8):
            sum += StoI(HashedStr[i*8+j])
        code[i] = sum % 10
    return code

# 시리얼 객체와 현재 시간에 맞는 OTP 값을 생성
def GetOTP(Obj_Serial, curr_t):
    con_curr_t = convertMinute(curr_t)
    con_ST_t = convertMinute(Obj_Serial.genTime)
    curr_dt = int(con_curr_t - con_ST_t)
    err_dt = curr_dt - 1     
    COTP = GenOTP(Obj_Serial.serialcode, curr_dt)
    ECOTP = GenOTP(Obj_Serial.serialcode, err_dt)
    return COTP, ECOTP

# 쿠키에 들어갈 ID, PW 값을 암호화함
def encryptText(id, pw):
    ID = id
    PW = pw
    bID = ID.encode('utf-8')
    bPW = PW.encode('utf-8')
    bencID = encrypt(bID)
    bencPW = encrypt(bPW)
    encID = bencID.decode('utf-8')
    encPW = bencPW.decode('utf-8')
    return encID, encPW

# 암호화된 쿠키 내부의 ID, PW를 복호화함
def decryptText(id, pw):
    bid = id.encode('utf-8')
    bpw = pw.encode('utf-8')
    bdecID = decrypt(bid)
    bdecPW = decrypt(bpw)
    ID = bdecID.decode('utf-8')
    PW = bdecPW.decode('utf-8')
    return ID, PW

# 현재 시간을 yymmddHHMM 형태로 리턴해줌. 
def getTime():
    curr_t = datetime.now().strftime('%y%m%d%H%M')
    return curr_t

# yymmddHHMM 형태의 문자열을 분단위 정수값으로 바꿔줌
def convertMinute(curr_t):
    currdate = datetime.strptime(curr_t,'%y%m%d%H%M')
    return currdate.timestamp() / 60
