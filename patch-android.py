#!/usr/bin/env python3
"""يعدّل AndroidManifest.xml: يفكّ قفل الدوران ويضيف أذونات الخدمة الصوتية. آمن للتشغيل أكثر من مرة."""
import re, sys, pathlib

p = pathlib.Path("android/app/src/main/AndroidManifest.xml")
if not p.exists():
    sys.exit("AndroidManifest.xml not found: run `npx cap add android` first")
x = p.read_text(encoding="utf-8")

# 1) فكّ قفل الاتجاه: احذف أي android:screenOrientation من كل activity
x, n = re.subn(r'\s+android:screenOrientation="[^"]*"', "", x)
print(f"removed screenOrientation attributes: {n}")

# 2) تأكد أن تغيير الاتجاه لا يعيد إنشاء النشاط (يحفظ التشغيل الصوتي)
m = re.search(r'android:configChanges="([^"]*)"', x)
need = ["orientation", "screenSize", "screenLayout", "smallestScreenSize", "keyboardHidden", "keyboard", "uiMode", "navigation", "locale"]
if m:
    have = set(m.group(1).split("|"))
    merged = m.group(1) + "".join("|" + k for k in need if k not in have)
    x = x.replace(m.group(0), f'android:configChanges="{merged}"')
else:
    x = x.replace("<activity", '<activity android:configChanges="' + "|".join(need) + '"', 1)

# 3) الأذونات
perms = [
    "android.permission.INTERNET",
    "android.permission.FOREGROUND_SERVICE",
    "android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK",
    "android.permission.WAKE_LOCK",
    "android.permission.POST_NOTIFICATIONS",
]
add = ""
for q in perms:
    if f'android:name="{q}"' not in x:
        add += f'    <uses-permission android:name="{q}" />\n'
if add:
    x = x.replace("</manifest>", add + "</manifest>")
    print("added permissions:\n" + add)

p.write_text(x, encoding="utf-8")
print("manifest patched OK")
