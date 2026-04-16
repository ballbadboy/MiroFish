# Life Events — Beauty Decision Triggers

## Overview

Life events คือ **จุดเปลี่ยน** ที่ทำให้คนตัดสินใจทำทรีตเมนต์/ศัลยกรรมที่เคยเลื่อนมานาน
ต่างจาก Seasonal triggers ตรงที่ life events เป็น **personal milestone** ไม่ใช่ calendar event

---

## Category 1: Romantic / Relationship Milestones

### งานแต่งงาน (Wedding)
```
Timeline to trigger:
  T-12 months : เริ่ม research (rhinoplasty, weight loss)
  T-6 months  : Book surgery / คอร์สผิว
  T-3 months  : Botox/filler zone
  T-1 month   : Glow treatments, whitening drip
  T-1 week    : Final touch-up
  T+1 month   : Post-wedding maintenance start
```

| Persona | Priority Treatment | Budget Range |
|---------|-------------------|--------------|
| เจ้าสาว | Rhinoplasty, double eyelid, whitening | 50,000–300,000 บาท |
| เจ้าบ่าว | Liposuction, rhinoplasty, skin | 30,000–150,000 บาท |
| แม่เจ้าสาว/เจ้าบ่าว | Anti-aging, thread lift, filler | 50,000–200,000 บาท |
| Bridesmaid | Skin, botox, lip | 5,000–30,000 บาท |

**Simulation trigger phrase**: "แต่งงานปีหน้า อยากดูดีในวันสำคัญ"

---

### หย่าร้าง / เลิกกัน
- **Trigger**: ต้องการ "เริ่มต้นใหม่" ทางกายภาพ
- **Common treatments**: Body sculpting, rhinoplasty, "glow up" package
- **Emotional state**: เปราะบาง → ง่ายต่อการ upsell แต่ต้องระวัง boundary
- **Persona ที่เกิดบ่อย**: High-income homemaker (หลังหย่า), New Worker
- **Simulation**: `emotional_state: vulnerable` → `trust_in_authority` สูงกว่าปกติ 20%

---

### เริ่มความสัมพันธ์ใหม่ / Dating
- **Trigger**: อยากดูดีก่อน first impression
- **Treatments**: Lip filler, skin, laser hair removal
- **Platform**: TikTok → "ทำริมฝีปากก่อนไปเดต"

---

## Category 2: Career & Status Milestones

### เลื่อนตำแหน่ง / Promotion
```yaml
trigger_event: career_promotion
affected_personas: [corporate, new_worker]
typical_treatments:
  - botox_forehead: "ดูเป็นผู้ใหญ่ขึ้น ไม่เหนื่อย"
  - jawline_botox: "หน้าเรียว professional"
  - rhinoplasty: "ลงทุนระยะยาว"
budget_range_thb: [20000, 100000]
decision_speed: fast  # มีเงินพอแล้ว รอแค่ occasion
```

---

### เปลี่ยนงานใหม่ / Job Change
- **Trigger**: First impression ใหม่ในที่ทำงาน
- **Timeline**: ก่อน start date 1–2 เดือน
- **Common**: Skin brightening, subtle botox, hair
- **Persona**: Corporate, New Worker (25–35)

---

### เริ่มธุรกิจ / Business Launch
- **Trigger**: "ต้องดู credible ต่อ client"
- **Treatments**: Anti-aging (ดูฉลาด มั่นใจ), rhinoplasty
- **Persona**: Corporate, High-income

---

### Retirement / เกษียณ
- **Trigger**: "มีเวลา มีเงิน อยากดูแลตัวเอง"
- **Treatments**: Facelift, thread lift, comprehensive anti-aging
- **Persona**: High-income homemaker (สามีเกษียณ → ทั้งคู่ไปด้วย)

---

## Category 3: Body & Health Milestones

### หลังคลอดบุตร (Post-partum)
```
Timeline:
  T+3 months  : เริ่ม research body contouring
  T+6 months  : ปรึกษาหมอ (หยุดให้นม)
  T+9 months  : จอง procedure
  T+12 months : Mommy Makeover window
```

| Treatment | เหตุผล |
|-----------|--------|
| Tummy tuck | หน้าท้องหย่อน stretch marks |
| Breast surgery | หลังให้นมหน้าอกเปลี่ยน |
| Liposuction | น้ำหนักส่วนเกิน |
| Vaginal rejuvenation | ฟื้นฟูหลังคลอด |
| Thread lift / HIFU | เวลาตั้งท้องหยุด treatment |

**Simulation phrase**: "คลอดมาแล้ว 6 เดือน อยากดูแลร่างกายบ้าง"
**Persona**: Homemaker, Corporate female

---

### ลดน้ำหนักสำเร็จ (Post-weight loss)
- **Trigger**: ผิวหย่อน หลังลดน้ำหนักมาก (>15 กก.)
- **Treatments**: Skin tightening, tummy tuck, arm/thigh lift, breast lift
- **Emotional**: ภูมิใจแต่ frustrate ที่ผิวไม่ตาม
- **Platform**: Facebook groups (Weight loss community → clinic community)

---

### ผ่านโรคร้ายแรง / Recovery
- **Trigger**: "รอดมาแล้ว อยากดูแลตัวเอง"
- **Treatments**: Skin repair, scar treatment, reconstruction
- **Persona**: ทุกกลุ่ม (depends on condition)

---

### วันเกิด (Birthday Milestone)
```yaml
birthday_triggers:
  - age: 30
    phrase: "ก้าวเข้า 30 อยากลงทุนตัวเอง"
    treatments: [rhinoplasty, filler, botox_start]
    decision_weight: high
  - age: 40
    phrase: "40 แล้ว anti-aging ต้องจริงจัง"
    treatments: [thread_lift, thermage, facelift_consult]
    decision_weight: very_high
  - age: 50
    phrase: "50 อยากดูดีให้นานที่สุด"
    treatments: [facelift, comprehensive_anti_aging]
    decision_weight: high
  - age: 25
    phrase: "25 แล้ว เริ่ม botox ป้องกันริ้วรอย"
    treatments: [baby_botox, filler_start]
    persona: [corporate, new_worker]
    decision_weight: medium
```

---

## Category 4: Social & Cultural Events

### ก่อนงานเลี้ยง / Reunion
- **Trigger**: กลับไปเจอเพื่อนเก่า / งาน reunion โรงเรียน
- **Phrase**: "กลับไปเจอเพื่อนสมัยมัธยม อยากดูดีกว่าเดิม"
- **Treatments**: กอง quick-result: botox, filler, skin glow
- **Decision speed**: Fast (2–4 สัปดาห์)

---

### ก่อนเดินทางต่างประเทศ
- **Trigger**: Photo opportunities, meeting people
- **Treatments**: Quick treatments ก่อนออกเดินทาง
- **Persona**: Corporate, Med Tourist (reverse: คนไทยไปต่างประเทศ ทำก่อน)

---

### Gender Affirmation Journey (LGBTQ+)
```
Timeline (MTF typical):
  Year 1–2 : Hormone therapy, community research
  Year 2–3 : FFS consultation, laser hair removal
  Year 3–4 : FFS surgery (ถ้าพร้อม)
  Year 4–5 : SRS consultation + planning
  Year 5–7 : SRS (ถ้าเลือกทำ)
```
- **Trigger type**: Identity milestone ไม่ใช่ calendar
- **Community-driven**: ทุก decision ผ่าน peer review ใน community
- **Persona**: LGBTQ+ (ดู Persona-LGBTQ.md)

---

## MiroFish Simulation Configuration

```yaml
life_event_triggers:
  wedding:
    timeline_months_before: [12, 6, 3, 1]
    treatment_urgency_multiplier: 2.5
    budget_flexibility: high
    trigger_phrases:
      - "แต่งงานปีหน้า อยากเตรียมตัว"
      - "อีก 6 เดือนจะแต่ง"
      - "อยากสวยในวันแต่งงาน"
  
  post_partum:
    trigger_months_after_birth: [3, 6, 9, 12]
    treatment_focus: [body_contouring, breast, skin]
    emotional_state: proud_but_insecure
    trigger_phrases:
      - "คลอดมาแล้ว อยากดูแลร่างกาย"
      - "หน้าท้องหย่อนหลังคลอด"
  
  birthday_milestone:
    ages: [25, 30, 35, 40, 45, 50]
    sentiment_boost_by_age:
      25: 0.10
      30: 0.20
      35: 0.15
      40: 0.25
      50: 0.20
  
  career_event:
    types: [promotion, new_job, business_start]
    treatment_urgency_multiplier: 1.5
    decision_speed_days: 14

  divorce_separation:
    emotional_state: vulnerable
    trust_boost: 0.20  # ง่ายต่อการรับคำแนะนำ
    trigger_phrases:
      - "อยากเริ่มต้นใหม่"
      - "เลิกกันแล้ว อยากเปลี่ยนตัวเอง"
```
