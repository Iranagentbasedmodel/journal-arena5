# task/10-corpus.md — ساخت کورپوس مطالعه (پیش‌نیاز همهٔ گروه‌ها)
### هدف: برای هر گروه ≥۱۰۰ مقالهٔ هم‌محور (چکیده+بدنه در حد دسترسی) + لجر استشهاد. بدون کلید API.

## 0. تعاریف
- **axis مشترک**: همیشه از خودِ manuscriptِ نوشته‌شده برای ژورنال هدف استخراج می‌شود —
  عنوان + Keywords → `work/corpus/axis.json`. **hardcode کردن محور در کد/پلی‌بوک ممنوع**؛
  فهرست داخلی فقط fallback است (با تگ «fallback» در axis.json ثبت می‌شود).
- **tier-1 journals** (تصمیم ثبت‌شدهٔ مالک): Energy & Buildings, Applied Energy,
  Building & Environment, Journal of Environmental Management, Science of the Total
  Environment, Water Research + خودِ هدف.
- **سطوح شاهد**: body > abstract > metadata (قانون ۴ SKILL).metadata تنها برای فهرست،
  هرگز قابل استشهاد نیست.

## 1. گام‌ها (به‌ترتیب)
0. **محور**: `python3 engine/run.py corpus axis --manuscript <txt> --work work`
   (پیش از هر چیز؛ خروجی = axis.json، مرجع یکتای محور).
1. **بذر**: همهٔ ~۹۳ مرجع manuscript + ۲۴ منبع زندهٔ sources/CORPUS.md → `work/corpus/seeds.jsonl`.
2. **توسعهٔ هر گروه تا ≥۱۰۰**: کوئری روی OpenAlex/Crossref (هر دو بدون کلید):
   - OpenAlex: `https://api.openalex.org/works?search=<axis terms>&filter=from_publication_date:<d>,primary_location.source.display_name.search:<journal>&per-page=25&mailto=<owner email>`
   - برف‌پاشی: برای هر بذر، `cites:W…` و `referenced_works` از OpenAlex.
   - پنجره‌ها: E2/E7/E10 → ۲۴ ماه اخیر اجباری؛ بقیه → ۱۰ سال اخیر + کلاسیک‌های مرجع.
3. **دسترسی**: OA از `open_access.oa_url` / Unpaywall (با پارامتر email، بدون کلید) /
   PMC / DOAJ. بدنهٔ paywall → فقط چکیده، تگ `abstract-level` (نصف وزن رأی).
4. **لجر**: هر مقاله = یک خط در `work/ledger.jsonl`:
   `{gid, source_id:"g4-037", cite, doi, url, tier, date_read, takeaway_3_lines, quote_bank:[{quote, locator}]}`
   - quote_bank: برای body ۲–۵ نقل‌قول دقیق با محل (§/¶/جدول)؛ برای abstract ۱–۲.
   - **این بانک تنها منبع مجاز لنگرهای `[L:…]` در قانون ۲ است.**
5. **اشتراک بین گروهی**: مقالهٔ مشترک = یک ردیف با `gid:"shared"` + فهرست مصرف‌کنندگان.

## 2. بودجه و انضباط
- **سیاست شمارش (تصمیم مالک ۲۰۲۶-۱۰-۱۱):** صدتایِ شمارش‌پذیر هر گروه = مقالاتی با
  **دسترسی به متن کامل** از **هر ژورنالی**؛ اولویت انتخاب ژورنال: (۱) هم‌محوری با
  موضوع مقاله، (۲) امتیاز و سطح علمی. مقالات بدون دسترسی به متن کامل: مطالعهٔ
  چکیده‌های کلیدی‌شان **اجباری** است ولی در ۱۰۰تا **شمرده نمی‌شوند**؛ به‌جایش
  **امتیاز ویژه (bonus)** گروه‌اند (برای نسخهٔ امتیازدهی آینده). موج مطالعه = ۱۰ ایجنت.
- POL: فقط خواندنی؛ هیچ آپلودی از manuscript/humanizer؛ رعایت robots و ToS ناشران؛
  نرخ درخواست مؤدبانه (mailto در OpenAlex، ≤۱ req/s).
- هر ردیف لجر بدون `takeaway_3_lines` = خوانده‌نشده محسوب می‌شود (قانون ارزش-تصمیم).

## 3. خروجی
`work/corpus/<gid>/list.jsonl` + `work/ledger.jsonl` + گزارش پوشش:
`{gid, n_total, n_body, n_abstract, pct_body, journals_covered, months_covered}`.
