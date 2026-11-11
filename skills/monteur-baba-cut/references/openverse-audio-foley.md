# محرك الأصوات والمؤثرات الواقعية عبر Openverse (Openverse Audio & Foley Engine) 🎧🔊
**دليل جلب المؤثرات الصوتية الحقيقية والموسيقى التصويرية المرخصة تجارياً (CC0 / Creative Commons) وتضمينها تلقائياً في مشاهد الفيديو.**

---

## 🎯 الفلسفة والهدف
* **الفرق بين الأصوات الإجرائية (Procedural SFX) والأصوات الواقعية (Real Foley):**
  * الأصوات الإجرائية (المولدة بالمعادلات الرياضية داخلياً) ممتازة للتكتكة والنقرات السريعة وحركات الـ UI البسيطة.
  * ولكن في المشاهد الهندسية والقصصية والوثائقية (مثل حفر الأرض، تسريب الغاز، محركات الشاحنات، والموسيقى السينمائية الفخمة)، لا غنى عن **أصوات واقعية حية مسجلة في الميدان والاستوديوهات**.
* **محرك Openverse:**
  * يوفر وصولاً قانونياً ومجانياً 100% لأكبر مكتبة صوتية مفتوحة المصدر (Freesound, Wikimedia, Jamendo) خاضعة للمشاع الإبداعي بدون أي قيود أو حقوق ملكية مقلقة.

---

## 🏗️ المعمارية الهندسية ونظام الكاش الذكي (Smart Hybrid Caching)

```
                 تحليل سياق المشهد (Scene Semantic Tag)
                                   │
                                   ▼
                   فحص الكاش المحلي (Local Cache)
             هل ملف `sfx_cache/sfx_{tag}.wav` موجود؟
                                   │
                    ┌──────────────┴──────────────┐
                    ▼ نعم                         ▼ لا
             استخدام الملف فوراً          استعلام Openverse API
             (0.001 ثانية)                (q="{query}", license="commercial")
                                                  │
                                                  ▼
                                         تنزيل الصوت وتحويله
                                       (FFmpeg 44.1kHz Stereo WAV)
                                                  │
                                                  ▼
                                       حفظه في الكاش للاستخدام القادم
                                                  │
                       (في حالة انقطاع الإنترنت: Fallback إجرائي فوري)
```

---

## 📋 القواميس الصوتية المجهزة (Preset Semantic Foley Mappings)

تتضمن وحدة [`openverse_fetcher.py`](../scripts/openverse_fetcher.py) ربطاً تلقائياً بين الكلمات الدلالية واستعلامات البحث الاحترافية:

| التاج الدلالي (`Semantic Tag`) | سياق الاستخدام في الفيديو | استعلام البحث في Openverse |
|---|---|---|
| `excavator_digging` | مشهد حفر الأرض، الأساسات، والمشاريع الهندسية | `excavator digging diesel dirt` |
| `gas_leak_hiss` | تصاعد غازات البترول، الصمامات، وضغط الهواء | `gas leak steam air pressure hiss` |
| `liquid_trickle` | تسريب الوقود في التربة، انسكاب الماء، أو الزيت | `liquid water dripping puddle splash` |
| `metal_vault` | نزول الخزان الفولاذي، الأبواب الحديدية، والحاويات | `heavy metal container hollow clank` |
| `ui_click` | نقر الأزرار، التفاعل مع الشاشات والمؤشر | `mouse click switch button` |
| `fast_whoosh` | الانتقال السريع بين الكروت والمشاهد | `fast whoosh air cinematic transition` |
| `deep_impact` | خطاف بداية الفيديو، سقوط العناوين الضخمة | `cinematic sub bass impact drop` |
| `ambient_tech_bgm` | موسيقى تصويرية هادئة تحت الإعلانات التقنية (مثل آيفون) | `ambient technology light corporate background` |

---

## 🔒 التحقق والأمان القانوني (100% Commercial & Legal Safety)
* جميع الاستعلامات مفلترة بـ `license_type="commercial,modification"`.
* الأولوية القصوى تكون دائماً لرخص **CC0 (Public Domain)** حيث تكون الملكية عامة ومجانية تماماً.
* لا يتوقف الفيديو أبداً إذا انقطع الاتصال؛ المحرك يمتلك بديلاً داخلياً (Procedural Waveform Fallback) يضمن إنهاء الرندر تحت أي ظرف.
