# work/training/E6.md — یادداشت آموزش اجباری گروه E6 (data-results-integrity)
### الگو/نمونهٔ پُرشده: ایجنت باید منابع را واقعاً بخواند، تاریخ بزند و امضا کند.
### بدون این یادداشت (task/14 + task/15 گام ۱) هیچ خروجی E6 پذیرفته نمی‌شود.

**ایجنت:** <aid> · **تاریخ شروع/پایان:** <date> / <date> · **تأییدکننده:** <owner/lead>

| # | منبع | آموختهٔ کلیدی (≤۳ خط) | کاربرد در وظیفهٔ E6 |
|---|---|---|---|
| 1 | W3C PROV-O / PROV-DM — w3.org/TR/prov-o/ | واژگان استاندارد منشأ داده (entity/activity/agent) | هر عدد manuscript باید زنجیرهٔ provenance داشته باشد: دادهٔ خام → تبدیل → جدول |
| 2 | Crossref REST API + DOI resolution — api.crossref.org / doi.org | حل DOI و تطبیق فراداده (عنوان/سال/نویسنده) در چند ثانیه | آزمون وجودِ تک‌تک مراجع؛ کشف ارجاع به مقالهٔ ناموجود یا ربوده‌شده (hijacked) |
| 3 | DataCite Metadata Schema — schema.datacite.org | حداقل فیلدهای استناد دادهٔ پژوهشی + نسخه‌بندی | سنجش آمادگی deposit (Option C): آیا مجموعه‌داده نسخه و DOI می‌گیرد؟ |
| 4 | COPE: citation manipulation & paper mills — publicationethics.org/guidance | سیگنال‌ها: حلقه‌های استنادی، عبارات شکنجه‌شده (tortured phrases)، مجلات hijack | غربال الگوهای مشکوک در فهرست مراجع manuscript |
| 5 | Elsevier Research Integrity — elsevier.com/about/policies/research-integrity | تعهدات ناشر + ابزارهای غربال تصویر/متن | هم‌راستاسازی gateهای E6 با آنچه دفتر editorial واقعاً اجرا می‌کند |
| 6 | چک‌لیست سلامت تصاویر (Elsevier/FEBS image-integrity guidance) | انواع دستکاری: duplication، splicing، scale-bar ناسازگار، کنتراست غیرخطی | بازرسی اشکال manuscript + هر تصویر میکروسکوپی/نموداری ضمیمه |
| 7 | Retraction Watch Database — retractionwatch.com | پایگاه retract/hijack با API رایگان | کراس‌چک مراجع حساس پیش از تأیید وجود |

**خودآزمون پایان آموزش (هر سه باید «بله» باشند):**
- [ ] می‌توانم برای یک عدد دلخواه از جدول ۲، زنجیرهٔ provenance را با PROV بیان کنم.
- [ ] یک مرجع را end-to-end راستی‌آزمایی کردم (DOI → فراداده → تطبیق با متن استناد).
- [ ] سه سیگنال paper-mill را روی یک فهرست مراجع واقعی تمرین کرده‌ام.

**امضا:** آموزش دیده و منابع بالا خوانده شد — <aid> — <date>
