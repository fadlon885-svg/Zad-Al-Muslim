# زاد المسلم: بناء الـ APK (دوران الشاشة + الصوت في الخلفية)

## الطريقة الأسهل: بناء تلقائي على GitHub (بدون تثبيت أي شيء)
1. أنشئ مستودعًا جديدًا في github.com (Private).
2. ارفع كل محتويات هذا المجلد كما هي، بما فيها المجلد المخفي `.github`.
3. افتح تبويب **Actions** ثم **Build APK** ثم **Run workflow**.
4. بعد 5 إلى 10 دقائق افتح التشغيل المكتمل ونزّل **zad-almuslim-apk** من الأسفل، وفيه `app-debug.apk`.
5. ثبّته على الهاتف (اسمح بالتثبيت من مصدر غير معروف).

## على جهازك (Node 22 و Java 21 و Android Studio)
```
npm install
npx cap add android
python3 scripts/patch-android.py
npx cap sync android
cd android && ./gradlew assembleDebug
```
الناتج: `android/app/build/outputs/apk/debug/app-debug.apk`

## ماذا يفعل المشروع؟
- **الدوران:** السكربت `scripts/patch-android.py` يحذف قفل `screenOrientation` من AndroidManifest، فيتبع التطبيق إعداد الدوران التلقائي في هاتفك (فعّله من لوحة الإعدادات السريعة).
- **الصوت في الخلفية:** إضافة `@capgo/capacitor-media-session` تشغّل خدمة أمامية (Foreground Service) مع إشعار تحكم (تشغيل، إيقاف، التالي، السابق) أثناء تشغيل القرآن أو أذكار حصن المسلم. ملف index.html يستدعيها تلقائيًا داخل الـ APK فقط، ولا تتأثر نسخة المتصفح.

## إن توقف الصوت بعد إطفاء الشاشة
بعض الأجهزة (سامسونج، شاومي، أوبو) توقف التطبيقات في الخلفية بقوة. من إعدادات البطارية للتطبيق اختر **غير مقيّد / Unrestricted**.
