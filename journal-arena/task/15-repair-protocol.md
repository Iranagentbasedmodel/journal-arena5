# task/15-repair-protocol.md — پروتکل تعمیر اجرای ناقص (چهار خرابی رایج)
### ترتیب اجباری است؛ پرش از هر گام = خروجی همان گام باطل. هیچ finding سوخت نمی‌شود:
### یافته‌های قرنطینه‌شده در گام ۵ **re-anchor** می‌شوند، نه بازنویسی.

## خرابی‌های تحت پوشش
A) شمارش کورپوس گروه زیر ۱۰۰ · B) ledger.jsonl ساخته/پر نشده (لنگر صفر) ·
C) درصد body زیر ۶۰٪ · D) یادداشت آموزشی task/14 گروه نوشته نشده.

## گام ۰ — توقف موج گروه
موج ارزیابی گروه متوقف می‌شود. یافته‌های موجود حذف نمی‌شوند؛ `run.py check` آن‌ها
را قرنطینه نگه می‌دارد (⛔) و در matrix شمرده نمی‌شوند. این رفتارِ درست قانون ۲ است.

## گام ۱ — دروازهٔ آموزش (خرابی D)
`templates/training-note-<gid>.md` → کپی به `work/training/<gid>.md`.
ایجنت باید منابع را **واقعاً بخواند** و فیلدهای «تاریخ/تأییدکننده» را پر کند.
یادداشت بدون تاریخ = ناقص. بدون آن، ادامهٔ پروتکل مجاز نیست.

## گام ۲ — رساندن شمارش به ≥۱۰۰ (خرابی A)
```
python3 engine/run.py corpus topup --gid E6 --work work --need 150   # استخر نامزد بزرگ‌تر از ۱۰۰ (ریزش body طبیعی است)
python3 engine/run.py corpus coverage --work work        # تا سبز شدن ردیف گروه
```
topup از سه مسیر تأمین می‌کند: واژگان تخصصی integrity (برای E6)، محور مقاله،
و صفحه‌بندی کوئری‌ها؛ dedup با DOI خودکار است.

## گام ۳ — دروازهٔ بدنهٔ کامل (خرابی C؛ سیاست مالک ۲۰۲۶-۱۰-۱۱: شمارش‌پذیر = دسترسی متن کامل از هر ژورنال، اولویت هم‌محوری سپس سطح ژورنال؛ abstract-only = مطالعهٔ اجباری + امتیاز ویژه، خارج از شمارش ۱۰۰تا)
```
python3 engine/run.py corpus bodies --gid E6 --work work --max 30   # بچ‌های مؤدبانه، تکرارپذیر
```
متن OA در `work/corpus/E6/bodies/<sid>.txt` ذخیره و tier ردیف به body ارتقا می‌یابد.
**۳ب — اگر پس از جاروی کامل، OA واقعاً کافی نبود** (نه تنبلی، paywall مستند):
```
python3 engine/run.py corpus coverage --gid E6 --work work --exception "N DOIs paywalled, no OA copy; see bodies log"
```
استثنا در `coverage-exception.json` ثبت می‌شود و شورا طبق قانون ۴ نصف‌وزن اعمال
می‌کند. استثنا باید دلیل + فهرست DOI داشته باشد؛ «وقت نشد» قابل قبول نیست.

## گام ۴ — ساخت و تکمیل لجر (خرابی B)
```
python3 engine/run.py ledger init     --gid E6 --work work
python3 engine/run.py ledger autofill --gid E6 --work work   # نقل‌قول‌های واقعی از bodies/ با پرچم verified=False
# ایجنت‌ها می‌خوانند (اول bodyها) و takeaway_3_lines + quote_bank را پر می‌کنند
python3 engine/run.py ledger check  --gid E6 --work work     # تا VERDICT: complete
python3 engine/run.py ledger anchors --gid E6 --work work    # کاتالوگ لنگرهای معتبر
```
قاعدهٔ پرکردن: body ≥ ۲ نقل‌قول با locator، abstract ≥ ۱؛ هر نقل‌قول ≥۱۵ نویسه و
**دقیقاً از متن منبع**. ابزار هیچ نقل‌قولی نمی‌سازد؛ ساخت نقل‌قول = تخلف قانون ۷.

## گام ۵ — re-anchor و اجرای مجدد
۱. ایجنت همان گروه، هر finding قرنطینه‌شده را با کاتالوگ anchors تطبیق می‌دهد و
   ردیف را با `lit_quote_id` + `lit_quote` + `lit_tier` واقعی **بازصادر** می‌کند
   (claim_id حفظ می‌شود؛ متن قضاوت فقط در صورت تغییر شاهد اصلاح می‌شود).
۲. یافته‌ای که لنگر مناسب ندارد = واقعاً بی‌شاهد بوده → همان قرنطینه می‌ماند
   و در council-input به‌عنوان «شکاف شاهد» گزارش می‌شود.
۳. `run.py check` → `run.py matrix` → `run.py council` دوباره اجرا می‌شوند.

## دروازهٔ خروج پروتکل
`coverage` سبز (یا استثنا ثبت‌شده) + `ledger check` کامل + `check findings` بدون
قرنطینهٔ بی‌دلیل + یادداشت آموزشی دارای تاریخ. بدون هر چهار، موج بعدی گروه آغاز نمی‌شود.
