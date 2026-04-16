# Review Patterns — Social Media Behavior & Content Templates

## Overview

รูปแบบการรีวิวที่พบบน platform ต่างๆ สำหรับใช้ใน MiroFish simulation
แบ่งเป็น: Positive / Negative / Neutral และตาม platform

---

## Platform-Specific Review Formats

### TikTok Reviews

**Format**: Video-first, sound-driven, 30–180 วินาที

#### Positive TikTok Pattern
```
Hook (0–3 วิ): "ทำริมฝีปากมา 2 ชั่วโมงที่แล้ว 👄✨"
Content: POV / talking head + before transition + after reveal
Caption: "ปากสวยมาก หมอใจดีมาก ราคา [X] บาท 🌸 #ฟิลเลอร์ปาก #ริมฝีปาก #กรุงเทพ"
Sound: trending sound ที่ใช้กับ beauty content
CTA: "DM ถามราคาได้เลยน้าา"
Engagement pattern: save > share > comment
```

#### Negative TikTok Pattern
```
Hook: "ไปทำฟิลเลอร์มาแล้วเกิดอะไรขึ้น 😱" (drama hook)
Content: สาธยายขั้นตอน → แสดงผลที่ไม่ดี → reaction
Caption: ชื่อคลินิก (ตรงหรือเป็น code ที่คนรู้จัก) + ไม่แนะนำ
Viral potential: สูงมาก (negative content spread เร็วกว่า positive 3–5x)
Damage timeline: วัน 1–3 viral, วัน 4–7 clinic must respond, วัน 8–14 die down (ถ้าไม่มี celeb pickup)
```

#### Neutral/Educational TikTok
```
"รู้ไหม ฟิลเลอร์ปากทำแบบนี้ได้บ้าง..." (education format)
สร้าง awareness ไม่ใช่ hard sell
Creator: nano-influencer หรือ clinic staff
Trust level: สูง เพราะดูเป็น organic
```

---

### Instagram Reviews

**Format**: Image/Reel, longer caption, story swipe-up

#### Positive Instagram Pattern
```
Post type: Carousel (before → during → after → detail shots)
Caption (Thai): 
  "สรุปประสบการณ์ทำ [treatment] ที่ [คลินิก] 🌟
  
  ✅ จุดเด่น:
  - หมอใจเย็น อธิบายละเอียด
  - ผลออกมาเป็นธรรมชาติมากค่ะ
  - ราคา [X] บาท คุ้มมาก
  
  ❓ ถ้าอยากรู้รายละเอียดเพิ่ม comment ไว้เลยนะคะ
  
  #[treatment] #[คลินิก] #รีวิวความงาม #ก่อนหลัง"
  
Engagement: saves + comment "ราคาเท่าไหร่คะ"
```

#### Story Pattern (Instagram/Facebook)
```
Poll: "คิดว่าทำดีไหม? ✅ ดีมาก / ❌ ยังกังวล"
Slider: "😍 ชอบผลแค่ไหน?"
Q&A: รับคำถามแบบ real-time
Link sticker: → คลินิกเว็บไซต์ (ถ้า ≥10k followers)
```

---

### Facebook Reviews

**Format**: Text-heavy, group posts, long-form experience sharing

#### Positive Facebook Group Post
```
Title: "รีวิว [treatment] ที่ [คลินิก] ละเอียดมาก (ไม่ได้รับเงิน)"
Structure:
  1. ทำไมถึงเลือกคลินิกนี้ (200–300 คำ)
  2. ประสบการณ์วันทำ (รูปภาพ 5–10 รูป)
  3. Recovery timeline day by day
  4. ผลลัพธ์ตอนนี้ (1 เดือน/3 เดือน/6 เดือน)
  5. แนะนำไหม + ราคา
  
Group: "ทำศัลยกรรมกัน", "รีวิวคลินิกความงาม", "สาวประเภทสอง"
Trust level: สูงมาก — เพราะ long-form = ดูน่าเชื่อถือ
```

#### Negative Facebook Post
```
Damage level: สูง เพราะ share ง่าย, comment เยอะ, อยู่นาน
Pattern: post → viral ใน group → screenshot spread → อาจถึง mainstream media
Timeline: อยู่ใน search นาน (Google index Facebook posts)
```

---

### Pantip Reviews

**Format**: Q&A / Review thread, text + image

#### Classic Pantip Pattern
```
Title: "รีวิว/ถามหน่อยนะคะ [treatment] ที่ [คลินิก] [ราคา]บาท คุ้มไหม?"
Structure: Q&A + personal experience
Trust: สูงมาก สำหรับ Homemaker 35+ และ Corporate
Indexing: ติด Google นาน — "rhinoplasty pantip" ยังขึ้นรีวิวเก่าปี 2018
Competitive: คู่แข่งอาจ seed positive reviews ที่นี่
```

---

### Google Maps Reviews

**Format**: Rating + short text, ต้องเป็น Google account จริง

#### Positive Google Review
```
Rating: ⭐⭐⭐⭐⭐
Text: "หมอใจดีมาก ให้คำปรึกษาดี ผลออกมาสวยมากค่ะ staff ทุกคนน่ารัก 
       ราคาเหมาะสม แนะนำเลยค่ะ จะกลับมาทำอีกแน่นอน"
Photo: before/after (ถ้าลูกค้ายอม)
Response: clinic ต้อง respond ทุก review ภายใน 48 ชม.
```

---

## Sentiment Templates for Simulation

### Positive Sentiment Phrases (Thai)

```yaml
positive_phrases:
  high_trust:
    - "หมอฝีมือดีมาก แนะนำเลยค่ะ"
    - "ผลออกมาเป็นธรรมชาติ ไม่รู้ว่าทำ"
    - "คุ้มค่าเงินมากๆ จะกลับมาทำอีก"
    - "staff ใจดี ดูแลดีตลอด"
    - "recovery เร็วกว่าที่คิด"
  medium_trust:
    - "ก็โอเคนะคะ ผลออกมาตามที่หมอบอก"
    - "ราคาพอรับได้ ผลดี"
    - "แนะนำถ้าใครสนใจ"
```

### Negative Sentiment Phrases (Thai)

```yaml
negative_phrases:
  mild:
    - "รอนานมาก กว่าจะได้เจอหมอ 2 ชั่วโมง"
    - "ราคาแพงกว่าที่บอกนิดหน่อย"
    - "ผลยังไม่ชัดเท่าที่คิด ต้องรอดู"
  severe:
    - "อย่าไปเลย หมอทำผิดพลาด แก้ไม่ได้"
    - "ฉีด filler แล้วเป็นก้อน ต้องไปละลาย"
    - "บอก[ราคา]บาท พอมาจ่ายจริงบวกเพิ่มอีกเยอะ"
    - "หมอไม่ฟัง ทำตามใจตัวเอง ผลไม่ตรงที่บอก"
  crisis_level:
    - "ตาพร่ามัวหลังฉีด filler ต้องรีบไปรพ."
    - "ผ่าตัดแล้วติดเชื้อ ปิดบังไม่บอก"
```

### Neutral/Educational Phrases

```yaml
neutral_phrases:
  - "กำลังหาข้อมูล ใครเคยทำที่ไหนบ้างคะ?"
  - "ราคาประมาณนี้ปกติไหมคะ?"
  - "recovery กี่วันถึงกลับทำงานได้?"
  - "ความเจ็บปวดเป็นยังไงบ้าง?"
```

---

## MiroFish Review Simulation Config

```yaml
review_simulation:
  platforms:
    tiktok:
      positive_spread_rate: 0.30   # 30% ของ positive reviews viral
      negative_spread_rate: 0.75   # 75% ของ negative reviews viral
      avg_reach_positive: 5000
      avg_reach_negative: 25000
      decay_days: 14
    
    facebook_group:
      positive_spread_rate: 0.40
      negative_spread_rate: 0.60
      avg_reach_positive: 800
      avg_reach_negative: 3000
      decay_days: 30  # อยู่นานกว่า
      trust_weight: 0.85  # ผู้อ่านเชื่อมากกว่า
    
    google_maps:
      spread_rate: 0.15  # ไม่ viral แต่ permanent
      trust_weight: 0.90
      decay_days: 730  # อยู่นาน 2 ปี
    
    pantip:
      spread_rate: 0.20
      trust_weight: 0.88
      decay_days: 365  # Google-indexed นาน
  
  review_generation:
    after_treatment_days: [1, 7, 30, 90, 180]
    positive_rate_default: 0.72
    negative_rate_default: 0.15
    neutral_rate_default: 0.13
    negative_boost_on_incident: 3.0  # คูณ 3 ถ้ามี crisis
  
  word_of_mouth:
    offline_multiplier: 2.5  # Word-of-mouth offline > online review
    persona_sharer_rates:
      genz_experimenter: 0.85
      lgbtq_gender_affirming: 0.90
      high_income_homemaker: 0.30  # share แต่ private
      corporate: 0.20
      grooming_male: 0.10
```
