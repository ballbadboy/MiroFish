# Treatment Risks — Adverse Events & Crisis Scenarios

## Overview

ข้อมูล risk และ adverse events สำหรับ beauty treatments
ใช้สำหรับ: Crisis simulation ใน MiroFish, Agent ที่รับบทลูกค้ากังวล, Crisis management training

> ⚠️ **Medical Disclaimer**: ข้อมูลนี้เป็น simulation reference เท่านั้น
> ไม่ใช่คำแนะนำทางการแพทย์ ต้องปรึกษาแพทย์ผู้เชี่ยวชาญ

---

## Category 1: Injectable Risks (Filler / Botox)

### Filler — Vascular Occlusion (หลอดเลือดอุดตัน)
```
Severity   : CRITICAL — อาจทำให้ตาบอดหรือเนื้อตายได้
Occurrence : Rare (~1:1,000–10,000 cases)
Warning signs:
  - ปวดมากทันทีหลังฉีด
  - ผิวเปลี่ยนสีเป็นขาว/ม่วง (blanching/livedo)
  - ตามัว / มองไม่ชัด
Required action: ละลาย filler ด้วย hyaluronidase ทันที

Simulation trigger: agent รายงาน "ตามัวหลังฉีด"
Crisis level: LEVEL 5 — clinic ต้อง escalate ทันที
Viral potential: สูงมาก (ตาบอด = headline news)
```

### Filler — Nodule / Granuloma
```
Severity   : MEDIUM
Occurrence : 0.01–1% depending on product
Warning signs: ก้อนแข็ง, บวม, แดง, เจ็บ ≥2 สัปดาห์หลังฉีด
Treatment  : Hyaluronidase (HA filler), steroid injection, surgical removal
Timeline   : อาจเกิดหลายเดือนภายหลัง

Simulation: agent โพสต์ "ฉีด filler มา 3 เดือน มีก้อนขึ้น"
Crisis level: LEVEL 3
Viral pattern: Facebook group shares, before/after ที่น่าตกใจ
```

### Botox — Ptosis (หนังตาตก)
```
Severity   : MEDIUM–HIGH (ส่งผลด้านจิตใจสูง)
Occurrence : 1–5% ของ forehead botox
Warning signs: หนังตาบนตก ภายใน 1–2 สัปดาห์
Treatment  : ยาหยอดตา apraclonidine, รอ 2–3 เดือน
Duration   : หายเองเมื่อ botox หมดฤทธิ์

Simulation: agent โพสต์รูป "หนังตาตกหลัง botox"
Crisis level: LEVEL 3
Social impact: medium — ไม่ถาวร แต่ distressing ใน simulation
```

### Botox — Asymmetry
```
Severity   : MEDIUM
Occurrence : 2–10% (technique-dependent)
Cause      : Dosing asymmetry, patient anatomy variation
Treatment  : Touch-up injection, รอหมดฤทธิ์
Timeline   : ปรากฏใน 2 สัปดาห์

Simulation: agent โพสต์ before/after ที่ asymmetric
Crisis level: LEVEL 2
```

---

## Category 2: Surgical Risks

### Rhinoplasty — Revision Rate
```
Industry revision rate: 5–15% ของทุก rhinoplasty
Common revision causes:
  - Asymmetry
  - Over-resection (จมูกสั้นเกิน / tip droopy)
  - Implant visibility / shifting (เสริมจมูก)
  - Breathing problems post-op

Simulation trigger: agent ทำ rhinoplasty แล้วไม่พอใจ
Crisis level: LEVEL 3–4 (ขึ้นกับ severity)
Community impact: คนที่ต้องแก้ไข → share ใน group → ลด trust clinic
```

### Breast Augmentation — Capsular Contracture
```
Severity   : MEDIUM–HIGH
Occurrence : 10–20% ของผู้ทำเสริมหน้าอก (long-term)
Grades     : Baker Grade I–IV
Grade III–IV: เจ็บ, แข็ง, รูปร่างเสีย → ต้องผ่าตัดแก้
Timeline   : อาจเกิดหลายปีภายหลัง

Simulation: long-term follow-up scenario
```

### Surgery — Infection
```
Severity   : HIGH
Occurrence : 1–3% ของ elective cosmetic surgery
Warning signs: ไข้, บวมแดง, มีหนอง, กลิ่น ≥ 3 วันหลังผ่าตัด
Treatment  : Antibiotics, drainage, revision

Simulation trigger: agent รายงาน infection หลัง 1 สัปดาห์
Crisis level: LEVEL 4 ถ้า clinic ปิดบัง → LEVEL 5
```

### Anesthesia Risks
```
General anesthesia risks:
  - Adverse reaction (rare, ~1:10,000)
  - Aspiration
  - PONV (Post-operative nausea/vomiting) — common

Simulation note: สำหรับ medical tourist scenario
  ถ้า clinic ไม่มี anesthesiologist → red flag สำหรับ Med Tourist persona
```

---

## Category 3: Laser / Energy Device Risks

### Hyperpigmentation Post-Laser
```
Severity   : MEDIUM (cosmetic, not medical danger)
Occurrence : 5–20% ใน darker skin tones (Fitzpatrick IV–VI)
Cause      : Wrong parameter setting, no sun protection
Timeline   : เกิดใน 2–4 สัปดาห์
Treatment  : Topical depigmenting agents, ≥6 เดือน

Simulation: agent รายงาน "ผิวคล้ำขึ้นหลังเลเซอร์"
Crisis level: LEVEL 2–3
Thai market note: Skin type IV–V prevalent → clinic ต้องระวังมาก
```

### Burns from Energy Devices
```
Severity   : HIGH
Cause      : Incorrect device settings, inexperienced operator
Appearance: รอยไหม้, water blisters, scarring
Simulation: LEVEL 4–5 crisis
Viral potential: สูงมาก — รูป burn ก่อน/หลัง viral เร็ว
```

---

## Category 4: SRS / FFS Risks (LGBTQ+)

### SRS — Stenosis / Dilation Issues
```
Context    : Post-SRS vaginal care requires lifelong dilation
Risk if non-compliance: Stenosis → ต้องผ่าตัดแก้
Community awareness: LGBTQ+ community รับรู้ดี — mentor ช่วยเตรียมพร้อม
Simulation: long-term follow-up agent (6 months post-SRS)
```

### FFS — Nerve Damage
```
Severity   : HIGH
Risk area  : Forehead recontouring → supraorbital nerve
Symptom    : หน้าผากชา (temporary หรือ permanent)
Timeline   : ชั่วคราว = 3–6 เดือน, ถาวร = rare
```

---

## Crisis Simulation Scenarios

### Scenario A: Filler Occlusion Viral Post
```yaml
scenario_id: filler_occlusion_viral
trigger: agent_reports_vision_change_post_filler
timeline:
  hour_0: patient_reports_blurring
  hour_1: tiktok_post_goes_live
  hour_6: 50000_views
  hour_12: major_facebook_groups_share
  hour_24: news_media_pickup
  day_3: clinic_reputation_score -0.60
  day_7: booking_drop -45%
  day_30: recovery_depends_on_clinic_response

clinic_response_options:
  good: immediate_acknowledgment + treatment + public_statement
  bad: denial + silence → accelerates damage
  outcome_good: recovery_70%_in_90_days
  outcome_bad: permanent_30%_trust_loss
```

### Scenario B: Botched Rhinoplasty Before/After
```yaml
scenario_id: rhinoplasty_botch_before_after
trigger: patient_posts_unsatisfactory_result
severity: level_3
spread_platform: facebook_group → instagram → pantip
damage_timeline_weeks: 4
trust_recovery_months: 6
recommended_clinic_action:
  - reach_out_to_patient_privately
  - offer_complimentary_revision
  - post_public_response_respectfully
  - share_educational_content_on_revision_expectations
```

---

## MiroFish Risk Configuration

```yaml
risk_simulation:
  adverse_event_rates:
    filler_occlusion: 0.0005      # 0.05%
    botox_ptosis: 0.03            # 3%
    rhinoplasty_dissatisfied: 0.12 # 12% want revision
    laser_hyperpigmentation: 0.10 # 10% dark skin
    surgery_infection: 0.02       # 2%
  
  crisis_levels:
    level_1: minor_complaint
      trust_impact: -0.05
      viral_probability: 0.10
    level_2: visible_complication
      trust_impact: -0.15
      viral_probability: 0.25
    level_3: significant_outcome_dissatisfaction
      trust_impact: -0.30
      viral_probability: 0.50
    level_4: medical_complication
      trust_impact: -0.55
      viral_probability: 0.75
    level_5: permanent_harm_or_media_crisis
      trust_impact: -0.80
      viral_probability: 0.95
  
  recovery_curve:
    without_good_response: months_to_recover: 18
    with_transparent_response: months_to_recover: 4
    with_compensation_and_transparency: months_to_recover: 2
```
