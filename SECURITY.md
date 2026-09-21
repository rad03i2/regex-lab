# Security Policy

Regex Lab is an offline text-processing utility. It does not require credentials, make network requests, or execute matched text as code.

## Important regex risk

Python's standard `re` engine has no execution timeout. A pathological expression can cause catastrophic backtracking and consume significant CPU. Regex Lab limits pattern and input sizes, but those limits do **not** prove a pattern is safe. Do not run untrusted regular expressions in security-sensitive or multi-tenant services. Use process isolation and an engine with enforceable timeouts for that use case.

Do not pass sensitive production data on a command line if your operating system exposes process arguments; prefer `--file` or stdin.

## Reporting

Please report security concerns privately through GitHub's available security-reporting mechanism when enabled. Do not publish credentials, private data, or exploitable details in a public issue.

# سياسة الأمان

الأداة محلية ولا تحتاج مفاتيح أو اتصالًا بالشبكة ولا تنفذ النص المطابق ككود. محرك `re` القياسي في بايثون لا يوفر مهلة تنفيذ؛ لذلك قد تسبب بعض الأنماط غير الموثوقة استهلاكًا عاليًا للمعالج. حدود الحجم الموجودة تقلل إساءة الاستخدام العرضية لكنها لا تجعل كل تعبير منتظم آمنًا. للبيئات متعددة المستخدمين استخدم عزل العمليات ومحركًا يدعم مهلة تنفيذ قابلة للفرض.
