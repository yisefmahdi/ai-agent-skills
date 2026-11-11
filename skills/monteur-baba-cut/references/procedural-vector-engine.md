# محرك الرسم الإجرائي المتجهي النقي (Procedural Vector Engine) ✏️📐
**دليل الهندسة البرمجية لرسم المشاهد، الماكينات، والبيئات بالكود الصافي 100% بدون أي توليد صور بالذكاء الاصطناعي.**

---

## 🎯 الفلسفة والهدف
* **صفر توليد صور بالذكاء الاصطناعي في الشروحات الهندسية والتوضيحية:**
  توليد الصور عبر الذكاء الاصطناعي يُنتج صوراً مسطحة، مشوشة الأبعاد، ميتة الحركة، وغير متطابقة عبر المشاهد (Inconsistent).
* **الحل الهندسي:** رسم كل عنصر عبر متجهات رياضية دقيقة (SVG Paths, Gradients, Catmull-Rom Bezier Splines).
* **المزايا:**
  1. تحكم كامل بالمليمتر في كل فريم.
  2. دقة لا نهائية (Infinite Resolution) بدون بكسلة.
  3. استقلالية تامة عن الإنترنت وسيرفرات الذكاء الاصطناعي (مجاني وفوري).
  4. إمكانية تحريك وتفكيك وتركيب كل برغي وماسورة وصمام بشكل منفصل.

---

## 📐 فئة الأشكال الرياضية الإجرائية (`ProceduralShapes`)

```python
import math

class ProceduralShapes:
    """محرك بناء متجهات رياضية دقيقة في الإحداثيات المحلية مع تحديد أبعاد الإحاطة ومحور الارتكاز."""
    def __init__(self):
        self.items = []
        self.minx = self.miny = 1e9
        self.maxx = self.maxy = -1e9

    def _update_box(self, pts):
        for x, y in pts:
            self.minx = min(self.minx, x)
            self.miny = min(self.miny, y)
            self.maxx = max(self.maxx, x)
            self.maxy = max(self.maxy, y)

    def rc(self, x, y, w, h, fill, rx=0, rot=0, stroke="none", stroke_w=0):
        """رسم مستطيل بمركزه الدقيق وتدويره حول نقطة المنتصف."""
        a = math.radians(rot)
        ca, sa = math.cos(a), math.sin(a)
        corners = [
            (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
            for dx in (-w / 2, w / 2)
            for dy in (-h / 2, h / 2)
        ]
        self._update_box(corners)
        rot_attr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ''
        stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_w}"' if stroke != "none" else ''
        self.items.append(
            f'<rect x="{x - w/2:.1f}" y="{y - h/2:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx:.1f}" fill="{fill}"{stroke_attr}{rot_attr}/>'
        )
        return self

    def el(self, cx, cy, rx, ry, fill, stroke="none", stroke_w=0):
        """رسم شكل بيضاوي حول مركزه الهندسي."""
        self._update_box([(cx - rx, cy - ry), (cx + rx, cy + ry)])
        stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_w}"' if stroke != "none" else ''
        self.items.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}"{stroke_attr}/>')
        return self

    def ci(self, cx, cy, r, fill, stroke="none", stroke_w=0):
        """رسم دائرة مركزية."""
        return self.el(cx, cy, r, r, fill, stroke, stroke_w)

    def pth(self, pts, fill="none", smooth=0.0, stroke="none", stroke_w=0, closed=True):
        """
        رسم مسار مضلع أو منحنى ناعم باستخدام خوارزمية Catmull-Rom Bezier Spline.
        smooth=0.0: زوايا هندسية حادة (صفائح معدنية، صخور قاسية).
        smooth=0.3 - 0.5: منحنيات ناعمة وطبيعية (طبقات التربة، تلال، انسكاب سائل).
        """
        n = len(pts)
        if n < 2:
            return self
        self._update_box(pts)
        stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round"' if stroke != "none" else ''
        
        if smooth <= 0.0 or n < 3:
            d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f}'
            for p in pts[1:]:
                d += f' L {p[0]:.1f} {p[1]:.1f}'
            if closed:
                d += ' Z'
        else:
            T = []
            for k in range(n):
                prev_p = pts[(k - 1) % n] if closed else pts[max(0, k - 1)]
                next_p = pts[(k + 1) % n] if closed else pts[min(n - 1, k + 1)]
                T.append(((next_p[0] - prev_p[0]) * smooth / 2, (next_p[1] - prev_p[1]) * smooth / 2))
            
            d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f}'
            limit = n if closed else n - 1
            for k in range(limit):
                p0 = pts[k]
                p1 = pts[(k + 1) % n]
                c1 = (p0[0] + T[k][0], p0[1] + T[k][1])
                c2 = (p1[0] - T[(k + 1) % n][0], p1[1] - T[(k + 1) % n][1])
                d += f' C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {p1[0]:.1f} {p1[1]:.1f}'
                self._update_box([c1, c2, p1])
            if closed:
                d += ' Z'
                
        self.items.append(f'<path d="{d}" fill="{fill}"{stroke_attr}/>')
        return self

    def ln(self, pts, stroke, width=2, dash=None):
        """رسم أنابيب أو كابلات أو خطوط إشارة."""
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
        return self.pth(pts, fill="none", smooth=0.0, stroke=stroke, stroke_w=width, closed=False)
```

---

## 🎨 لوحات الألوان الهندسية الصافية (Engineering Palettes)
ممنوع استخدام ألوان باهتة عشوائية؛ تستخدم لوحات صناعية متناسقة عالية التباين:

### لوحة المقطع الهندسي الصناعي (Industrial Cutaway):
* **الأسفلت والطبقة السطحية:** `#26292B` (سطح أسمنتي), `#1A1C1E` (طبقة قاعية)
* **طبقات التربة:** `#5C4033` (طمي بني داكن), `#8B5A2B` (رمل وحصى), `#3D2817` (تربة مضغوطة)
* **الفولاذ والمعدن:** `#4A6572` (هيكل خارجي صلب), `#344955` (حديد معتم), `#F9AA33` (طلاء تحذيري أصفر), `#E0E0E0` (صمامات ومفاصل كروم)
* **البترول والوقود:** `#1E1B18` (بترول خام داكن), `#C99700` (بنزين ذهبي متلألئ), `#E65100` (تحذير اشتعال)
* **الأبخرة والغازات:** `#E0F7FA` (أبخرة غازية شفافة مع تلاشي بالـ Opacity: 0.6 -> 0.0)

---

## 🏗️ بناء الأصول الهندسية بالكود الصافي

### 1. مقطع الأرض والتربة (Ground Strata Cutaway):
```python
def draw_ground_cutaway(sh, width=1920, top_y=320, depth=760):
    # طبقة الأسفلت
    sh.rc(width/2, top_y + 12, width, 24, fill="#2C3437")
    # خط الأمان الأصفر على الأسفلت
    sh.rc(width/2, top_y + 2, width, 4, fill="#F9A825")
    # طبقة الرمل والحصى
    sh.rc(width/2, top_y + 70, width, 90, fill="#8D6E63")
    # طبقة الطمي والتربة الرسوبية العميقة
    sh.rc(width/2, top_y + 350, width, 470, fill="#4E342E")
    # صخور طبيعية مدفونة في التربة
    sh.pth([(200, top_y+200), (280, top_y+170), (340, top_y+220), (260, top_y+260)], fill="#3E2723", smooth=0.4)
    sh.pth([(1400, top_y+300), (1490, top_y+260), (1560, top_y+320), (1450, top_y+380)], fill="#3E2723", smooth=0.4)
```

### 2. خزان الوقود المزدوج مع فوهة الأبخرة (Underground Dual-Wall Tank):
```python
def draw_fuel_tank(sh, cx=960, cy=680, w=560, h=280):
    # جدار الخرسانة الخارجي المقاوم للتسريب
    sh.rc(cx, cy, w + 40, h + 40, fill="#37474F", rx=35)
    # الفراغ العازل المزدوج (Dual-Wall Interstitial Space)
    sh.rc(cx, cy, w + 16, h + 16, fill="#263238", rx=25)
    # جدار الخزان الفولاذي الأساسي
    sh.rc(cx, cy, w, h, fill="#455A64", rx=18)
    
    # مستوى الوقود الداخلي (Liquid Level)
    sh.rc(cx, cy + 40, w - 16, h - 90, fill="#FFB300", rx=8)
    
    # فوهة الخزان العلوية (Flange & Manhole Pivot)
    flange_y = cy - h/2 - 20
    sh.rc(cx, flange_y, 90, 40, fill="#78909C", rx=6)
    
    # أنبوب التنفيس وخروج الغازات (Vent Pipe)
    sh.rc(cx + 80, flange_y - 80, 16, 160, fill="#90A4AE")
    # صمام الأمان الحلقي
    sh.ci(cx + 80, flange_y - 160, 18, fill="#D32F2F")
    
    # إرجاع نقطة انطلاق الغاز بدقة مطلقة
    return {
        "vent_emitter_x": cx + 80,
        "vent_emitter_y": flange_y - 180,
        "manhole_x": cx,
        "manhole_y": flange_y
    }
```
بهذه الطريقة، يتم رسم المشهد بدقة تصنيع حقيقية، مع إرجاع إحداثيات الانبعاث بدقة 100% لربط تأثير الغازات مباشرة بالفوهة.
