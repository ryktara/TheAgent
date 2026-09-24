<div dir="rtl">

# دليل البدء السريع في Foundry

هذا الدليل لمؤسس لديه فكرة واشتراك في Claude Code. ثبّت الأدوات أولًا:
[INSTALL-WINDOWS.md](INSTALL-WINDOWS.md) أو [INSTALL-MAC-LINUX.md](INSTALL-MAC-LINUX.md).

## 1. اكتب سطرًا واحدًا

افتح مجلدًا فارغًا لتطبيقك، وشغّل <code dir="ltr">claude</code>، ثم اكتب:

<div dir="ltr">

```
/foundry "A POS for my two cafes in Dubai, Arabic and English receipts"
```

</div>

تكفي جملة واحدة. اذكر نوع النشاط والمدينة أو الدولة وما تعرفه مسبقًا (اللغات، مزوّد الدفع، العمل دون اتصال). كل معلومة تذكرها توفّر عليك سؤالًا.

## 2. أجب عن 10 أسئلة على الأكثر

يطابق Foundry وصفك مع حزمة مجال (مطعم، تجزئة، تداول، أو عامة) ويطرح **7 أسئلة على الأكثر**، ثم **3 أسئلة متابعة على الأكثر**. لكل سؤال قيمة افتراضية؛ اضغط Enter لقبولها. تأتي أولًا الأسئلة التي يصعب تغيير إجاباتها لاحقًا (الدولة، نموذج الخدمة).

بعد الإجابات يعمل Foundry وحده حتى تجهز خطة المهام.

## 3. ماذا تحصل عليه

| الأمر | ما تستلمه |
|-------|-----------|
| <code dir="ltr">/foundry</code> | مواصفات المنتج، نموذج المجال، قرارات المعمارية، مخطط قاعدة البيانات، عقد الواجهة البرمجية، نظام التصميم، مواصفة لكل شاشة، نموذج التهديدات، قائمة الامتثال، خطة مهام (60 مهمة على الأكثر) |
| <code dir="ltr">/foundry-build</code> | شيفرة تعمل، مهمة بعد مهمة: تطبيق ويب قابل للتثبيت (PWA)، واجهة برمجية، قاعدة بيانات Postgres، اختبارات، ولقطات شاشة بالوضعين الفاتح والداكن وبالاتجاهين |
| <code dir="ltr">/release</code> | ملفات Docker، إعدادات النشر، دليل التشغيل، اختبار دخان، أدلة المستخدم |

تطبيقات الجوال (Expo) ضمن خطة التطوير. كل تطبيق اليوم يبدأ على الويب.

## 4. أين تُحفظ الملفات

كل ما يكتبه Foundry عن تطبيقك موجود في المجلد <code dir="ltr">.foundry/</code> داخل مستودع التطبيق:
<code dir="ltr">brief.md</code>، <code dir="ltr">prd.md</code>، <code dir="ltr">decisions.yaml</code>، <code dir="ltr">adr/</code>، <code dir="ltr">screens/</code>، <code dir="ltr">tickets/</code>، <code dir="ltr">wizard/</code>، <code dir="ltr">handoff.md</code>.
الشيفرة بجانبه في <code dir="ltr">apps/</code> و<code dir="ltr">packages/</code>. لا يُحفظ شيء في مكان آخر.

## 5. البناء والاستئناف

<div dir="ltr">

```
/foundry-build            implements the next 4 tickets
/foundry-build --n 10     implements the next 10
/foundry-resume           continues exactly where the last session stopped
```

</div>

أغلق الطرفية متى شئت. يسجّل الملف <code dir="ltr">.foundry/handoff.md</code> المرحلة والمهمة النشطة والأمر التالي؛ تعرضه الجلسة الجديدة عند بدئها، ويكمل <code dir="ltr">/foundry-resume</code> منه.

## 6. قراءة لوحة الحالة

<div dir="ltr">

```
python scripts/foundry.py status
```

```
FOUNDRY STATUS  cafe-pos
phase: 11   tickets: 12/49 done   active: T-013   generation: 3
dod: 30/34 runs passed (88%)   blockers: 0   wizards pending: 1 (payments-tap)
tokens so far: ...   cost $41.20 (blended $3.43/ticket; ...)   est. remaining 37 tickets ...
escalations: 0
next: T-014   command: /foundry-build
```

</div>

| الحقل | المعنى |
|-------|--------|
| <code dir="ltr">phase</code> | من 0 إلى 10 = التخطيط، 11 = البناء |
| <code dir="ltr">tickets</code> | المنجز من الإجمالي؛ <code dir="ltr">active</code> = المهمة الجارية |
| <code dir="ltr">dod</code> | الفحوص الآلية (الأنواع، التنسيق، الاختبارات، سهولة الوصول، اللقطات) الناجحة لكل محاولة |
| <code dir="ltr">blockers</code> | مشكلات أوقفت البناء؛ تظهر كل واحدة في سطر <code dir="ltr">blocker:</code> |
| <code dir="ltr">wizards pending</code> | خطوات بشرية ما زالت مطلوبة منك (القسم 7) |
| <code dir="ltr">cost</code>، <code dir="ltr">est. remaining</code> | الاستهلاك حتى الآن وتقدير الباقي |
| <code dir="ltr">next</code>، <code dir="ltr">command</code> | المهمة التالية وما يجب كتابته |

## 7. المعالجات: خطوات لا ينفذها غيرك

تحتاج بعض المهام إلى سرّ أو حساب لا يحصل عليه إلا إنسان: مفتاح مزوّد الدفع، اسم نطاق، ترخيص جهة تنظيمية. يبني Foundry الميزة خلف مفتاح تشغيل ويكتب معالجًا:

- <code dir="ltr">.foundry/wizard/&lt;name&gt;.md</code>: سبب الحاجة والخطوات بدقة.
- <code dir="ltr">.foundry/wizard/&lt;name&gt;.ps1</code> (ويندوز) أو <code dir="ltr">.sh</code> (ماك ولينكس): شغّله والصق كل قيمة عند طلبها. يتحقق من الصيغة ويكتب <code dir="ltr">.env.local</code> (لا يُرفع إلى المستودع) ويختبر القيم.

حتى تشغّله تعمل الميزة ببديل مؤقت. يعرض <code dir="ltr">status</code> كل معالج لم يُنفَّذ بعد.

## 8. تأكيد الإطلاق (التطبيقات الخاضعة للتنظيم)

في المجالات الخاضعة للتنظيم (مثل تطبيق التداول) يبقى الإطلاق متوقفًا حتى يؤكد شخص مسمّى أن خطوات الترخيص والامتثال اكتملت. بعد معالج <code dir="ltr">regulator-licence</code>:

<div dir="ltr">

```
python scripts/foundry.py release confirm --by "Your Name"
```

</div>

يسجّل هذا الأمر من وافق على الإطلاق. ينفذه شخص فقط، ولا ينفذه أي وكيل نيابة عنك.

## معلومات مفيدة

- يعمل Foundry فقط داخل جلسة Claude Code التي سجّلت الدخول إليها. لا يوجد مفتاح API لإعداده.
- يحتاج البناء إلى أداة رسم الشيفرة codebase-memory-mcp؛ ويتحقق منها <code dir="ltr">/foundry-setup</code> ويسجّلها.

</div>
