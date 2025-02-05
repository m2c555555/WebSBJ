import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import urllib.parse


def line_callback(request):
    
    # รับค่าจากพารามิเตอร์ GET ที่ส่งมาจาก LINE
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code or not state:
        return HttpResponse("Invalid response from LINE", status=400)

    # นำ code ไปแลกเปลี่ยนเป็น access token
    token_data = line_exchange_token(code)

    if token_data is None:
        return HttpResponse("Failed to get access token", status=400)

    # ดึงข้อมูลโปรไฟล์ผู้ใช้จาก LINE
    user_profile = get_line_user_profile(token_data["access_token"])

    if user_profile is None:
        return HttpResponse("Failed to get user profile", status=400)

    context = {
        "display_name": user_profile.get("displayName", "Unknown"),
        "user_id": user_profile.get("userId", "N/A"),
        "picture_url": user_profile.get("pictureUrl", ""),
        "status_message": user_profile.get("statusMessage", "No status message")
    }
    # แสดงข้อมูลผู้ใช้เป็น JSON (สำหรับทดสอบ)
    return render(request, 'app_main/main.html', context)



def line_exchange_token(code):
    if not code:
        return None  # ❌ หยุดทันทีถ้าไม่มี code

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://192.168.1.59:8000/line/complete/line/",  # ต้องตรงกับ LINE Developers
        "client_id": "2006842390",  # ✅ เปลี่ยนเป็น string
        "client_secret": "10729f15d6939ae4be07424229421ee1"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post("https://api.line.me/oauth2/v2.1/token", data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # ✅ ส่งค่า access token กลับ
    else:
        return None  # ❌ ถ้าแลก token ไม่ได้ให้ return None


def get_line_user_profile(access_token):
    url = "https://api.line.me/v2/profile"
    headers = {
        "Authorization": f"Bearer {access_token}"  # ส่ง Access Token
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # ได้ข้อมูลโปรไฟล์กลับมา
    else:
        return {"error": "Failed to fetch profile", "status_code": response.status_code}



@login_required

def main(request):
    return render(request, 'app_main/main.html')

