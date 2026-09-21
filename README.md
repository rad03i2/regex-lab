# Regex Lab

A small, local, script-friendly workbench for testing and applying Python regular expressions without sending text to an online tester.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: @rad03i2

## English

### Overview
Regex Lab turns Python's standard `re` engine into a predictable CLI and reusable package. It is useful when you need to inspect matches and capture groups, validate a whole value, replace text, split input, or integrate regex checks into scripts and CI.

### Why it exists
Online regex testers are convenient, but logs, configuration, source code, and business text may be private. Regex Lab keeps processing local and offers stable exit codes and JSON output for automation.

### Features
- `find`: match value, start/end offsets, numbered groups, and named groups.
- `fullmatch`: validate the entire input; exit `0` on match and `1` on no match.
- `replace`: substitutions with replacement count and safe output-file handling.
- `split`: split text around a pattern.
- `info`: inspect capture-group count and named-group indexes.
- Flags: `i` ignore case, `m` multiline, `s` dot-all, `x` verbose, `a` ASCII.
- Input from a literal argument, UTF-8 file, or stdin.
- JSON output for `find`, `fullmatch`, `split`, and `info` where useful.
- Unicode/Arabic text support; no network calls or runtime dependencies.

### Requirements & installation
Requires Python 3.10+.

```bash
git clone https://github.com/rad03i2/regex-lab.git
cd regex-lab
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
regex-lab --version
```

### Usage
```bash
regex-lab find "(?P<user>[\\w.-]+)@(?P<host>[\\w.-]+)" --text "mail a@example.com" --json
regex-lab fullmatch "[A-Z]{2}-\\d{4}" --text "IQ-2026"
regex-lab find "^error:" --flags im --file app.log
printf "one,two,three" | regex-lab split "," --json
regex-lab replace "\\s+" " " --text "too   many   spaces"
regex-lab info "(?P<id>\\d+)-(\\w+)" --json
```

`find` and `fullmatch` return exit code `1` when there is no match. Invalid input/patterns return `2`. Successful operations return `0`.

For `replace --output FILE`, an existing file is never overwritten unless `--force` is supplied.

### Configuration
There is no config file and no environment variable is required. This is intentional: commands are explicit and reproducible. Pattern length is limited to 10,000 characters, input to 5,000,000 characters, and `find --limit` to 10,000 matches.

### Python API
```python
from regex_lab import find_matches
matches = find_matches(r"(?P<num>\d+)", "A12 B34")
print(matches[0].groupdict)
```

### Project structure
```text
src/regex_lab/core.py   parsing, matching and transformations
src/regex_lab/cli.py    command-line interface
src/regex_lab/__main__.py module entry point
tests/                  unit and CLI tests
.github/workflows/ci.yml cross-platform CI
```

### Testing
```bash
python -m pip install -e . pytest
python -m pytest
```
CI runs the suite on Python 3.10, 3.12 and 3.13 across Ubuntu, Windows and macOS.

### Preview / screenshots
This is a terminal-first project. For a repository preview, capture `regex-lab find ... --json` and `regex-lab info ... --json` in a clean terminal. No screenshot is bundled because terminal appearance depends on the user's shell/theme.

### Security & privacy
All processing is local. Regex Lab does not upload input, use telemetry, require accounts, or execute matched text. See [SECURITY.md](SECURITY.md). Avoid putting secrets directly in command-line arguments; stdin or `--file` can reduce exposure through process listings.

### Limitations
Regex Lab uses Python's standard `re` engine, so syntax and behavior follow Python rather than PCRE/JavaScript. The engine has no timeout; malicious/pathological patterns can cause catastrophic backtracking. Size limits are defensive bounds, not a ReDoS guarantee. Matches are non-overlapping, binary files are unsupported, and `--file` expects UTF-8.

### Optional roadmap
Potential future additions include an opt-in interactive TUI, saved local pattern collections, and support for a timeout-capable regex engine as an optional backend. None are required for current functionality.

### Contributing & license
See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
Regex Lab أداة محلية لسطر الأوامر وحزمة بايثون لاختبار التعبيرات المنتظمة وتطبيقها باستخدام محرك `re` القياسي. تفيد في استخراج التطابقات والمجموعات، والتحقق من أن النص كاملًا يطابق نمطًا، والاستبدال، والتقسيم، وربط فحوص Regex بالسكربتات وCI.

### لماذا هذا المشروع؟
مواقع اختبار Regex مريحة، لكن السجلات والكود وملفات الإعداد قد تحتوي بيانات خاصة. لذلك يعالج Regex Lab النص محليًا ويوفر مخرجات JSON ورموز خروج ثابتة مناسبة للأتمتة.

### الميزات
- `find` لعرض النص المطابق وموقع البداية والنهاية والمجموعات العادية والمسماة.
- `fullmatch` للتحقق من النص كاملًا؛ يرجع `0` عند التطابق و`1` عند عدمه.
- `replace` للاستبدال مع حماية ملفات الإخراج من الكتابة فوقها دون `--force`.
- `split` لتقسيم النص حول النمط.
- `info` لمعرفة عدد مجموعات الالتقاط وأسماء المجموعات.
- دعم الأعلام `i/m/s/x/a`، والإدخال من النص أو ملف UTF-8 أو stdin.
- مخرجات JSON، ودعم Unicode والعربية، وبدون اتصال شبكي أو اعتماديات تشغيل خارجية.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث.

```bash
git clone https://github.com/rad03i2/regex-lab.git
cd regex-lab
python -m venv .venv
python -m pip install -e .
regex-lab --version
```

في Windows فعّل البيئة بـ `.venv\Scripts\activate`، وفي macOS/Linux استخدم `source .venv/bin/activate`.

### أمثلة الاستخدام
```bash
regex-lab find "\\d+" --text "رقم 123 ورقم 456" --json
regex-lab fullmatch "[A-Z]{2}-\\d{4}" --text "IQ-2026"
regex-lab find "^error:" --flags im --file app.log
regex-lab replace "\\s+" " " --text "مسافات   كثيرة"
regex-lab info "(?P<id>\\d+)-(\\w+)" --json
```

النجاح يرجع رمز `0`. أوامر البحث والتحقق ترجع `1` عند عدم وجود تطابق، والمدخل أو النمط غير الصالح يرجع `2`.

### الإعداد
لا يحتاج المشروع ملف إعداد أو متغيرات بيئة. الحد الأقصى للنمط 10,000 محرف، وللنص 5,000,000 محرف، ولنتائج `find` عشرة آلاف نتيجة.

### استخدام الحزمة برمجيًا
```python
from regex_lab import find_matches
matches = find_matches(r"(?P<num>\d+)", "A12 B34")
print(matches[0].groupdict)
```

### بنية المشروع
الكود الأساسي في `src/regex_lab/core.py`، وواجهة الأوامر في `cli.py`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`.

### الاختبارات
```bash
python -m pip install -e . pytest
python -m pytest
```
يختبر GitHub Actions إصدارات Python 3.10 و3.12 و3.13 على Ubuntu وWindows وmacOS.

### المعاينة
المشروع مخصص للطرفية؛ يمكن أخذ لقطة لأمر `find --json` وأمر `info --json` لعرضه في صفحة المشروع. لا توجد صورة مضمّنة لأن مظهر الطرفية يعتمد على النظام والثيم.

### الخصوصية والأمان
المعالجة محلية بالكامل، بلا رفع بيانات أو Telemetry أو حسابات أو تنفيذ للنص ككود. راجع [SECURITY.md](SECURITY.md). يُفضّل تمرير البيانات الحساسة عبر stdin أو ملف بدل وضعها مباشرة في arguments.

### القيود
الأداة تتبع صيغة Regex الخاصة ببايثون وليست PCRE أو JavaScript. محرك `re` لا يملك مهلة تنفيذ، لذلك قد تسبب الأنماط الخبيثة أو سيئة التصميم catastrophic backtracking. حدود الحجم لا تضمن الحماية من ReDoS. التطابقات غير متداخلة، والملفات الثنائية غير مدعومة، و`--file` يتوقع UTF-8.

### تطوير اختياري
يمكن مستقبلًا إضافة TUI اختيارية، ومكتبة أنماط محلية، ومحرك اختياري يدعم مهلة تنفيذ. هذه إضافات مستقبلية وليست وعودًا بميزات موجودة حاليًا.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص وفق [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
