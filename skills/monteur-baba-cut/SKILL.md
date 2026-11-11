---
name: monteur-baba-cut
description: Autonomous end-to-end AI motion graphics & video production engine (v6.5 Universal Spatial Physics & Procedural Vector Edition). Autonomously turns audio and assets into studio-grade animated videos (MP4) OR takes existing videos to auto-edit, master audio, and inject viral kinetic captions. Features universal spatial anchoring & mechanical pivot physics (zero offset drift, physical emitter-source locking), 100% pure procedural vector drawing (zero static AI image hallucinations, Catmull-Rom Bezier splines), adaptive macro cinematography (dynamic close-up to wide contextual zooming 1.08x - 2.5x), motion.dev true spring physics (Apple-grade tactile elasticity), viral doodle & stickman explainer animations, 3D spatial camera tilt & depth of field, simulated 3D interactive cursor & touch ripples, zero-setup auto-healing tool installation (FFmpeg, Node.js, AI libraries), procedural auto-SFX (whooshes, clicks, ticks, impacts), contextual AI caption polishing & ambiguity gate (non-destructive word alignment, typos fixing, asking on unknown audio), virtual camera 3D parallax, organic film grain, and social media safe-zone protection. Use whenever the user asks to produce a motion graphics video, auto-edit speech, subtitle a video, or mentions "Monteur Baba Cut" or "مونتير بابا كت" or "مونتير بابا" or "سينيور مونتير" or "ستيك مان" or "motion.dev".
---

# Monteur Baba Cut (v6.6) — Universal Spatial Physics & Procedural Engine
**المحرك السينمائي المتكامل لموشن جرافيك ومونتاج الفيديو بالذكاء الاصطناعي (Monteur Baba Cut Edition)**

---

## 🌟 الهوية والهدف
**Monteur Baba Cut (مونتير بابا كت)** هو محرك إنتاج موشن جرافيك سينمائي متكامل ومستقل بنسبة 100%. يعمل مباشرة عبر الكود الصافي (Python, SVG, CSS, GSAP, Canvas) لإنتاج فيديوهات احترافية بدقة المليمتر، دون الاعتماد على أي خدمات سحابية لتوليد الصور الثابتة أو اشتراكات خارجية.

---

## 🌐 الميثاق الفيزيائي والهندسي الشامل للمحرك (Universal Physical Laws)
هذه القوانين ليست أمثلة مخصصة لغرض معين، بل هي **مبادئ فيزيائية وهندسية عامة ومجردة تحكم أي كائن أو مشهد في الكون**:

### 1. قانون محور الارتكاز الميكانيكي العام (Universal Mechanical Pivot Law) ⚙️
* **ينطبق على أي كائن يدور أو يتأرجح أو يرتد في الكون** (عجلات، تروس، عقارب، أذرع ميكانيكية، مفاصل بشرية، أبواب، بندولات، مؤشرات، مكابس):
* **القاعدة:** يُمنع منعاً باتاً الدوران من نقطة عشوائية أو استخدام `transformOrigin` الافتراضي الذي يسبب انزياحاً عن المركز.
* **الحل الهندسي (`J(el, tx, ty)`):** يتم فصل نقطة تموضع المفصل (`tx, ty`) عن التحريك المحلي، ويُرسم العنصر في نقطة الصفر المحلي `(0, 0)`، فيدور حول مركزه الهندسي بالمليمتر بنظام:
  $$\text{transform} = \text{translate}(tx + x, ty + y) \cdot \text{rotate}(r) \cdot \text{scale}(sx, sy)$$
  *(راجع المرجع التفصيلي: [mechanical-joint-rigging.md](references/mechanical-joint-rigging.md))*

### 2. قانون الاقتران المطلق بين المصدر والمنبثق (Source-Emission Coupling Law) 💨💧
* **ينطبق على أي ظاهرة فيزيائية تنبثق في المشهد** (غازات، أدخنة، سوائل تنسكب، شرارات كهربائية، هالات ضوئية، نيران، موجات صوت، شظايا):
* **القاعدة:** لا يوجد تأثير ينشأ من العدم أو يطفو عشوائياً في الفراغ (`top: 50%` محظور نهائياً).
* كل انبعاث يقترن إحداثياً بنقطة خروجه الفعلية (`Boundary Vertex Attachment`):
  * الغازات والأبخرة تتصاعد حصراً من فوهة الخزان العلوية أو فتحة صمام التنفيس.
  * السوائل تتدفق داخل مسار الأنبوب الفعلي باستخدام دالة `path.getPointAtLength()`.
  * الهالات الضوئية تتطابق مركزياً مع فتيلة المصباح أو بؤرة الاشتعال بنسبة 1:1.

### 3. قانون الكاميرا الماكرو التكيفية (Adaptive Macro Cinematography Law) 🎥🔍
* **القاعدة الصارمة (Anti-Wide Shot Law):**
  * **ممنوع الزووم البعيد نهائياً (No Wide Shots < 1.08x).**
  * مجال التقريب التوضيحي دائماً بين **`1.08x` إلى `2.5x`** (ماكرو إلى متوسط القرب).
  * العنصر النشط (خزان الحفر، المكبس، العداد، الفوهة) يملأ **35% إلى 65% من ارتفاع الكادر**.
  * الكاميرا تتحرك رأسياً بنعومة (Tilt-down) لمتابعة الحفر تحت الأرض، أو تندفع للأمام (Push-in) نحو فوهة الصمام عند رصد الغازات.
  *(راجع المرجع التفصيلي: [macro-cinematography.md](references/macro-cinematography.md))*

### 4. قانون الرسم الرياضي المتجهي النقي (100% Pure Procedural Geometry) ✏️📐
* **القاعدة الصارمة:** **إلغاء الاعتماد على صور الذكاء الاصطناعي المسطحة والمشوشة في هذا النمط.**
* يُبنى المشهد بالكامل من مسارات فيكتور ومعادلات رياضية متجهة عبر فئة `ProceduralShapes`:
  * المستطيلات الدقيقة `rc()`، الدوائر والبيضاويات `ci()`, `el()`، والأنابيب `ln()`.
  * المنحنيات العضوية وطبقات التربة والتلال والتصدعات عبر خوارزمية **Catmull-Rom Bezier Spline** `pth(pts, smooth=0.4)`.
  * استقلالية كاملة عن الإنترنت وسيرفرات التوليد، وتحكم مطلق في كل فريم بدقة لا نهائية.
  *(راجع المرجع التفصيلي: [procedural-vector-engine.md](references/procedural-vector-engine.md))*

### 5. قانون التماسك الكينماتيكي وبوابة التحقق الإلزامي (Kinematic Cohesion & Pre-Flight Gate) 🔗🛡️
* **القاعدة الصارمة:** يُمنع نهائياً رندر أي آلة أو مجسم بأجزاء مبعثرة أو مفككة ("كل شغلة في شقة").
* **سلسلة المفاصل الأمامية (Forward Kinematics Chain):** 
  * الجنزير أو القاعدة مثبتة على سطح الأرض مباشرة (`y == ground_line`).
  * الكابينة فوق الجنزير، والذراع يبدأ من مسمار الكابينة، والساعد يبدأ من مرفق الذراع، والمجرفة تبدأ من معصم الساعد بالمعادلات المثلثية:
    $$P_{\text{child}} = P_{\text{parent}} + L \cdot (\cos\theta, -\sin\theta)$$
* **بوابة الفحص والمعالجة الذاتية (`KinematicIntegrityChecker`):** فحص إلزامي آلي قبل الرندر للتحقق من:
  1. ملامسة الآلات للأرض (Zero Floating).
  2. تطابق مسامير المفاصل مع تجاويفها بفارق صفري مطلق (`Gap = 0.000px`).
  3. المعالجة الذاتية الفورية (Auto-Healing) لأي إحداثي شارد لضمان خروج المشهد متماسكاً بنسبة 100% من أول مرة.
  *(راجع المرجع التفصيلي: [mechanical-joint-rigging.md](references/mechanical-joint-rigging.md))*

---

## 🚫 دستور الحركة السينمائية ونفي العرض التقديمي (Anti-PPT Constitution)
* **حظر شرائح الباوربوينت:** ممنوع استخدام `<section class="scene">` والتبديل بينها بـ Fade-in و Fade-out.
* **المسرح الحي المستمر:** المشهد يتطور باستمرار وتنتقل الكاميرا بين تفاصيله بسلاسة، أو عبر قطع حركي مباشر (Kinetic Cut) مع إزاحة خفيفة `96px` وضبابية `blur ≤ 8px`.
* **قاعدة الـ 10 عناصر الحية (≥10 Active Elements):** في كل ثانية، يحتوي الكادر على ما لا يقل عن 10 عناصر فيزيائية أو بيئية متحركة (أبخرة متصاعدة، إبرة عداد تهتز، نبض إضاءة، جريان سائل، ذرات غبار، أرقام قياس HUD متغيرة، تروس تدور، تنفس كاميرا خفيف).
* **صفر نصوص ميتة:** النص محصور في مؤشرات قياس diegetic (العمق، الضغط، درجات الحرارة) أو عنوان قصير جداً (≤ 5 كلمات).
*(راجع المرجع التفصيلي: [anti-ppt-cinematics.md](references/anti-ppt-cinematics.md))*

---

## 🚀 ترسانة المحرك الإضافية
* **محرك هندسة الصوت والمؤثرات الواقعية (Openverse Real Foley & Sound Design):** استعلام وتنزيل تلقائي للمؤثرات الصوتية الحقيقية (حفر الحفارات، فحيح الغازات، ارتطام المعادن، والموسيقى التصويرية) المرخصة تجارياً 100% (CC0 / Creative Commons) مع كاش محلي فائق السرعة وبديل إجرائي أوفلاين. *(راجع المرجع: [openverse-audio-foley.md](references/openverse-audio-foley.md))*
* **محرك فيزياء الزنبرك الحقيقي (Motion.dev Spring Engine):** ارتداد لمسي فائق السلاسة بنظام Apple Tactile Springs (`stiffness: 380, damping: 22, mass: 0.8`).
* **الكاميرا المكانية ثلاثية الأبعاد (3D Spatial Tilt & Tilt-Shift):** منظور سينمائي مداري بطيء (`RotateX: 14°`, `RotateY: -16°`) مع ظلال ناعمة متعددة الطبقات.
* **مؤشر اليد والماوس التفاعلي الحي (Simulated 3D Cursor & Touch):** نقر حقيقي مع موجة ارتداد دائرية متوهجة (`Touch Ripple`) ومؤثرات كليك متزامنة.
* **منظومة الدودل والستيك مان الفيروسي (Viral Doodle & Stickman):** شخصيات ريجد تفاعلية (أفكار، مقارنات، أرباح، أزرار) مرسومة بالفيكتور الصافي.
* **التدقيق اللغوي الذكي وبوابة التحقق من الكلمات (AI Caption Polishing & Ambiguity Gate):** محاذاة صوتية غير هدّامة، وتصحيح للأخطاء الإملائية مع الحفاظ على التوقيتات بدقة أجزاء الثانية.
* **التثبيت الذاتي التلقائي (Zero-Setup Auto-Healing):** تجهيز بيئة التشغيل بالكامل (FFmpeg, Node.js, fast-whisper, numpy) ذاتياً بدون تدخل يدوي.
* **الهيكل القياسي الموحد لتنظيم المشاريع (Standardized Studio Project Workspace):** يقوم المحرك تلقائياً بإنشاء مجلد مخصص لكل مشروع بدون ترقيم عشوائي يجمع كافة المدخلات والمخرجات بشكل ثابت:
  * `projects/<project_name>/`
    * `input/`: المواد الخام الأصلية (audio, video, images) التي يرميها المستخدم.
    * `transcript/`: ملفات التفريغ الصوتي بالكلمة والملي ثانية.
    * `assets/`: الأصول الصوتية المعالجة والمؤثرات Foley والخطوط.
    * `composition/`: كود الموشن والرندر الصافي (`index.html`, `hyperframes.json`).
    * `review/`: لقطات الفحص السريعة والـ Contact Sheet.
    * `<project_name>_Master_<aspect>.mp4`: الفيديو النهائي المعتمد في جذر مجلد المشروع مباشرة.

---

## 🛠️ أوامر التشغيل المباشرة (CLI Execution)

### 1. إلقاء مجلد خام بالكامل للمونتاج التلقائي (Smart Auto-Ingest)
```bash
python .agents/skills/monteur-baba-cut/scripts/engine.py \
  --input "path/to/my_raw_files_folder" \
  --name "My_Viral_Reel"
```

### 2. إنتاج فيديو موشن جرافيك من صوت محدد (9:16)
```bash
python .agents/skills/monteur-baba-cut/scripts/engine.py \
  --audio "path/to/voiceover.wav" \
  --name "Monteur_Baba_Course_Ad" \
  --style "viral_doodle"
```

### 3. مونتاج ودبلجة فيديو حالي وإضافة كابشن حركي فائق الدقة
```bash
python .agents/skills/monteur-baba-cut/scripts/engine.py \
  --video "raw_footage.mp4" \
  --name "Podcast_Highlights"
```

### 4. إنتاج فيديو هندسي وثائقي بنظام الفيكتور والمقطع العرضي (Cutaway 16:9)
```bash
python .agents/skills/monteur-baba-cut/scripts/engine.py \
  --audio "path/to/voiceover.wav" \
  --name "Engineering_Excavator_Doc" \
  --aspect "16:9" \
  --style "engineering_cutaway"
```

---

## 📚 المراجع الهندسية الداخلية المستقلة (Internal References)
تتضمن المهارة مكتبة وثائق هندسية كاملة مدمجة داخل مجلد `references/`:
1. [procedural-vector-engine.md](references/procedural-vector-engine.md): دليل رسم الأشكال والماكينات بالكود ومعادلات Bezier.
2. [mechanical-joint-rigging.md](references/mechanical-joint-rigging.md): نظام المفاصل المحلية `J()` وإلغاء زحزحة الدوران وربط الانبعاثات.
3. [anti-ppt-cinematics.md](references/anti-ppt-cinematics.md): معايير الحركة المستمرة ونفي العروض التقديمية وقاعدة الـ 10 عناصر.
4. [macro-cinematography.md](references/macro-cinematography.md): قواعد زوايا الكاميرا الماكرو ونسب التقريب (1.08x - 2.5x).
5. [openverse-audio-foley.md](references/openverse-audio-foley.md): دليل جلب المؤثرات الصوتية والموسيقى الواقعية المرخصة تجارياً من Openverse.
