# task/12-council.md — شورای نخبگان (Tier 2): verdict نهایی
### ترکیب: ۵–۷ عضو = پرخوان‌ترین ایجنت‌ها (بیشترین ردیف لجر در ≥۲ گروه) + رؤسای E2 و E4.
### ورودی: matrix v3 کامل + همهٔ findings + نتایج arena + گزارش پوشش کورپوس.

## 1. قواعد تجمیع
- وزن شاهد: body=1.0، abstract=0.5، metadata=0 (قانون ۴).
- آیتم‌های متنازع → یک دور attack/defend/revise (رویهٔ arena) پیش از رأی‌گیری.
- رأی = اکثریت وزنی؛ وتوی E10 بر تورم ادعا محفوظ است.
- هیچ verdict بدون ≥۱ لنگر ادبی body-tier یا ≥۲ لنگر abstract-tier.

## 2. سه پاسخ اجباری (کتبی، با لنگر)
1. **این پژوهش چه چیزی به ادبیات اضافه کرد؟** (حداکثر ۵ جمله؛ هر جمله یک لنگر؛
   مرزهای «اضافه» صریح: چه چیزی اضافه نشده.)
2. **با رفع ایرادات، قابلیت ارسال دارد یا توسعه ضروری است؟** — اگر ضروری است،
   **چرا**: فهرست P0 (بلاکر) با دلیل اینکه بدون آن، ارسال = اتلاف اعتبار.
3. **ارزش علمی در برابر محور داوری ژورنال هدف** — مقایسه صریح با ۲۴ ماه اخیر
   (لنگرهای E7) و سطح significance مورد انتظار داوران.

## 3. قالب verdict
```json
{"verdict": "submittable | revise-then-submit | develop-first",
 "scientific_merit_score": 0-5, "novelty": "confirmed|partial|unproven",
 "p0_blockers": [{"item":"...","why":"...","owner":"E?/coder/writer","effort":"d"}],
 "p1_before_submission": [...], "p2_nice_to_have": [...],
 "answers": {"q1_added": "...", "q2_submittable": "...", "q3_merit": "..."},
 "dissent": "..."}
```
خروجی: `work/council-verdict.md` + `work/roadmap.jsonl` (اولویت‌دار، ownerدار).
**قاعدهٔ نهایی:** roadmap فقط کار تصمیم‌دار؛ هیچ «بررسی بیشتر شود» بدون owner و
روز شمار مجاز نیست.
