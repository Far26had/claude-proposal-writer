# claude-proposal-writer

یک [Claude Code Skill](https://docs.claude.com/en/docs/claude-code/skills) برای نوشتنِ **پروپوزال‌های فارسیِ برنده** — به‌ویژه برای خدماتِ هوش مصنوعی، نرم‌افزار، وب و مشاوره. خروجی، یک پروپوزالِ ساختارمندِ ۱۲ بخشی (RTL) است که به‌جای فروشِ ابزار، از مشکل و ارزشِ کلاینت شروع می‌کند.

> A Claude Code Skill for writing client-winning business proposals in Persian/Farsi (RTL), especially for AI, software, web, and consulting services.

## چه می‌کند

بر پایه‌ی متدولوژیِ اثبات‌شده‌ی نوشتنِ پروپوزال ساخته شده و این اصول را نهادینه می‌کند:

- **سه قانون طلایی:** درباره‌ی کلاینت بنویس نه خودت، نتیجه بفروش نه ابزار، کوتاه و شفاف بمان.
- **چارچوب ۱۲ بخشی:** خلاصه‌ی اجرایی، درکِ وضعیت، راه‌حل، دامنه (شامل/غیرشامل)، زمان‌بندی، ارزش/ROI، سرمایه‌گذاری، و قدم بعدی.
- **بازبینیِ خودکار** بر اساس چک‌لیستِ ۸ اشتباهِ رایج.
- **خروجی PDF فارسیِ راست‌به‌چپ** با فونتِ جاسازی‌شده‌ی **Vazirmatn** و پالتِ رنگیِ حرفه‌ای (سرمه‌ای/طلایی/فیروزه‌ای).

## نصب

این ریپو را در پوشه‌ی skillهای Claude Code کپی کنید:

```bash
# سطح پروژه
git clone https://github.com/Far26had/claude-proposal-writer .claude/skills/proposal-writer

# یا سطح کاربر (همه‌ی پروژه‌ها)
git clone https://github.com/Far26had/claude-proposal-writer ~/.claude/skills/proposal-writer
```

سپس در Claude Code کافی است بگویید: «یک پروپوزال برای [کلاینت] بنویس» — اسکیل خودکار فعال می‌شود.

## ساختار

| مسیر | توضیح |
|---|---|
| `SKILL.md` | دستورالعمل اصلی: قوانین، گردش کار، و جدولِ ۱۲ بخش |
| `references/methodology.md` | راهنمای تفصیلیِ هر بخش + اشتباهات رایج + چک‌لیست |
| `references/example-proposal.md` | نمونه‌ی کاملِ مرجع (وب‌سایت + دستیار هوشمند) |
| `scripts/md_to_pdf.py` | تبدیلِ پروپوزالِ Markdown به PDF فارسیِ RTL |
| `examples/` | دو نمونه‌ی تولیدشده (فروشگاه اینترنتی، کلینیک درمانی) |

## ساخت PDF

```bash
pip install markdown          # نیازمندی
python scripts/md_to_pdf.py examples/proposal-clinic.md
```

اسکریپت، Markdown را به HTMLِ استایل‌دارِ RTL تبدیل و با Chrome یا Edge (حالت headless) چاپ می‌کند. فونتِ Vazirmatn به‌صورت base64 در خروجی جاسازی می‌شود، پس نیازی به نصبِ فونت روی سیستم نیست. فقط به Chrome یا Edge نیاز دارد.

رنگ‌های سازمانی در بالای `scripts/md_to_pdf.py` به‌صورت متغیر تعریف شده‌اند؛ برای برندِ دیگر کافی است همان مقادیر hex را عوض کنید.

> فونتِ Vazirmatn تحت مجوز [SIL Open Font License 1.1](scripts/fonts/OFL.txt) بازتوزیع شده است.

## اعتبار

متدولوژی برگرفته از راهنمای نوشتنِ پروپوزالِ [Careerpreneur Academy](https://careerpreneuracademy.com/proposal-writing.html) — دوره مشاور هوش مصنوعی.

## مجوز

[MIT](LICENSE)
