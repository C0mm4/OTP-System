from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, SerialForm, otpForm
from .models import Serial, Serialtable, mUser
from RestAPI.models import GetGenTime, OTPLogin
from .func import *
from RestAPI.models import GetGenTime

# Create your views here.

# 앱 기본 페이지, 기본 페이지가 게시판이기에 지정하지 않음
def index(request):
    return

# 로그인 하는 페이지
def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            tuser = mUser.objects.get(userID = form.get_user())
            if(tuser.isSReg): # 시리얼 미등록시 바로 로그인
                auth_login(request,form.get_user())
                return redirect ('index')
            else:      # 시리얼 등록시 ID,PW 세션에 저장 후 otp페이지로 리다이렉트
                ID = form.cleaned_data.get('username')
                PW = form.cleaned_data.get('password')
                encID, encPW = encryptText(ID, PW)
                request.session['id'] = encID
                request.session['pw'] = encPW
                return redirect ('/login/otp/')
            
    else:
        form = AuthenticationForm()
    return render(request,'login/login.html', {'form':form})


# OTP 사용한 로그인 시 로그인 기록을 쿠키로 저장해 쿠키에서 ID,PW 를 임시로 저장 후, 해당 함수에서 사용. 사용 후 쿠키는 폐기처분
def nlogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    # 해당 view에서는 template 단계에서 자동으로 POST 데이터를 받음. 이를 위해
    # 세션에 저장된 id, pw를 꺼내 context화 시킴
    id = request.session['id']
    pw = request.session['pw']
    ID, PW = decryptText(id, pw)
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            del request.session['id']
            del request.session['pw']
            auth_login(request,form.get_user())
    else:
        form = AuthenticationForm()
    # ID, PW를 context로 받아 template 내부에서 자동으로 POST 전송하도록 함
    return render(request, 'login/nlogin.html', {'form':form, 'ID':ID, 'PW':PW})
        
        
# 일반 로그인 후 OTP 사용 로그인 하는 페이지
def CheckOTP(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method =="POST":
        form = otpForm(request.POST)
        if form.is_valid(): 
            # 입력받은 OTP
            sIOTP = form.cleaned_data.get('otp')
            # 로그인할 사용자를 찾기 위해 id만 세션에서 꺼내옴
            id = request.session['id']
            # 암호화하여 세션에 저장하였기에 디코딩 함
            bid = id.encode('utf-8')
            bdecID = decrypt(bid)

            ID = bdecID.decode('utf-8')
            # 유저 객체와 시리얼 테이블 객체를 불러옴
            tuser = mUser.objects.get(userID = ID)
            tSTable = Serialtable.objects.get(id = tuser.sTable)
            #저장된 유저의 시리얼코드와 datetime을 이용 OTP 생성
            curr_t = getTime()
            curr_ST = Serialtable.objects.get(id = tuser.sTable)
            COTP, ECOTP = GetOTP(curr_ST.currentSerial, curr_t)
            print(COTP)
            IOTP = [0,0,0,0,0,0,0,0]
            for i in range(0,8):
                si = int(sIOTP[i])
                IOTP[i] = si
            # OTP 일치 시
            if(IOTP == COTP or IOTP == ECOTP):
                # 로그인 실행하는 페이지로 리다이렉트
                return redirect ('/login/nlogin/')
            

    else:
        form = otpForm()
        
    return render(request,'login/checkOTP.html', {'form':form})

# OTP 이용한 일회용 로그인 시 사용되는 페이지
def OneTimeLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        # 정확한 시간 계산을 위해 시간 정보 먼저 전달받음
        curr_t = getTime()
        # 일회용 로그인 기록을 불러들여 입력된 OTP와 비교하기 위한 쿼리
        # 비교 후 로그인 성공 시 해당 쿼리는 삭제됨 (최적화 목적)
        logs = OTPLogin.objects.all()
        form = otpForm(request.POST)
        Islogin = False
        if form.is_valid():
            sIOTP = form.cleaned_data.get('otp')
            IOTP = [0,0,0,0,0,0,0,0]
            id = 0
            for i in range(0,8):
                si = int(sIOTP[i])
                IOTP[i] = si
            for trylogin in logs:
                curr_User = mUser.objects.get(userID = trylogin.uID)
                curr_ST = Serialtable.objects.get(id = curr_User.sTable)
                COTP, ECOTP = GetOTP(curr_ST.currentSerial, curr_t)

                print(COTP)
                print(ECOTP)
                # OTP 일치 시
                if (IOTP == COTP or IOTP == ECOTP):
                    # 로그 삭제용 id 복사
                    id = trylogin.id
                    # 로그에서 사용자 ID, PW를 추출
                    ID = trylogin.uID
                    PW = trylogin.Password
                    # ID, PW를 암호 화 하여 세션에 저장
                    encID, encPW = encryptText(ID, PW)
                    request.session['id'] = encID
                    request.session['pw'] = encPW
                    # 로그 추출 후 삭제
                    curr_session = OTPLogin.objects.get(id = id)
                    curr_session.delete()
                    # 브레이크 코드 걸고 for문 탈출
                    Islogin = True
                    break
            # 브레이크 코드 True시
            if(Islogin):
                # 로그인 실행하는 페이지로 리다이렉트
                return redirect ('/login/nlogin')
    else:
        form = otpForm()
    return render(request, 'login/OTPlogin.html', {'form' : form})

            

# 회원가입하는 페이지
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # 폼에서 username, password 추출 후 django auth 모델 생성
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username =username, password = raw_password)

            # 자체적인 유저 테이블 등록함. PW값은 보안을 위해 저장하지 않음.
            nuser = mUser()
            nuser.userID = username
            nuser.hname = form.cleaned_data['hname']
            nuser.save()
            
            # 회원가입 성송 시 해당 계정으로 로그인함
            auth_login(request, user)
            
            return redirect ('index')
    else:
        form = UserForm()
    return render(request, 'login/signup.html', {'form':form})

# 사용자의 정보를 출력하는 페이지 시리얼 등록 여부를 확인 가능
def detailuser(request):
    cuser = request.user
    tuser = mUser.objects.get(userID = cuser.username)
    isDumy = tuser.isSReg
    if(cuser):
        return render(request, 'login/user_detail.html', {'puser' : cuser, 'tuser' : tuser, 'reg':isDumy})
    return redirect('index')

    
# 시리얼 등록시 사용하는 페이지
def regserial(request):
    if request.method == "POST":
        form = SerialForm(request.POST)
        if form.is_valid():
            # 시리얼 값을 시리얼 객체에 저장
            nSerial = Serial()
            nSerial.serialcode = form.cleaned_data['serialcode']
            cUser = mUser.objects.get(userID = request.user.username)
            cUser.isSReg = 0
            nTable = Serialtable(currentSerial = nSerial)

            # 시리얼의 genTime 값은 어플리케이션에서 보낸 JSON파일을 기반으로 작성
            createTime = GetGenTime.objects.get(uID = cUser.userID)
            nSerial.genTime = createTime.TimeCode

            # 테이블 저장
            nSerial.save()
            nTable.save()

            # 유저의 시리얼 테이블 인덱스 값을 입력해줌
            sTable = Serialtable.objects.get(currentSerial = nSerial).id
            cUser.sTable = sTable
            cUser.save()
        return redirect ('index')
    else:
        form = SerialForm

    return render(request, 'login/regserial.html', {'form':form})

