# Customer Concerns — Pre-Decision Anxieties & Objections

## Overview

ความกังวลและข้อโต้แย้งที่ลูกค้าแต่ละ persona มี ก่อนตัดสินใจทำทรีตเมนต์
ใช้สำหรับ: Agent dialogue simulation, Objection handling training, Content strategy

---

## Universal Concerns (ทุก Persona)

### 1. ความปลอดภัย
```
Concern: "ปลอดภัยไหม? มีความเสี่ยงอะไรบ้าง?"
Intensity: สูงมาก — barrier to first purchase
Trigger: ข่าว botched case, คนรู้จักมีประสบการณ์แย่
Reassurance needed:
  - แสดง credentials หมอชัดเจน
  - อธิบาย risk ตรงไปตรงมา (ไม่ซ่อน)
  - แสดง safety protocol
  - Emergency contact + follow-up plan
```

### 2. ผลลัพธ์ไม่ตรงตามที่คาด
```
Concern: "จะออกมาสวยแบบที่อยากได้จริงไหม?"
Intensity: สูง
Trigger: เห็น before/after ที่ไม่ดี, เพื่อนทำแล้วไม่พอใจ
Reassurance needed:
  - Reference before/after ที่ตรง expectation
  - Simulation ภาพก่อนทำ (ถ้ามี morphing software)
  - Consultation ละเอียด — align expectations
  - Revision policy ชัดเจน
```

### 3. ราคา / Hidden Costs
```
Concern: "จะมีค่าใช้จ่ายแอบแฝงไหม?"
Intensity: กลาง–สูง
Trigger: เพื่อนบอกราคาโดนบวกวันผ่าตัด
Reassurance needed:
  - All-inclusive quote เป็นลายลักษณ์อักษร
  - แยกรายการ: procedure, anesthesia, follow-up, medication
  - Revision policy (ฟรีหรือมีค่าใช้จ่าย)
```

---

## Persona-Specific Concerns

### New Worker (22–28 ปี)
```yaml
top_concerns:
  1. ราคาเกินงบ → ต้องกู้หรือผ่อน
    mitigation: เสนอ payment plan, ระบุ price tier ชัด
  
  2. เจ็บมากไหม / recovery นานไหม
    mitigation: content "recovery timeline ชัดเจน", pain scale
  
  3. กลัวคนรู้ว่าทำ
    mitigation: "natural-looking" guarantee, บอกว่า recovery ปิดบังได้
  
  4. ไม่รู้จะเริ่มต้นที่ไหน
    mitigation: educational content, quiz "suitable treatment for you"
  
  5. กังวลเรื่อง doctor credentials
    mitigation: แสดง bio ง่ายๆ "น่าไว้วางใจ ไม่ technical เกิน"
    
dialogue_pattern: |
  "อยากทำ แต่ราคา [X] บาท แพงไปหน่อยนะ 
  เดี๋ยวรอโปร หรือใครมีที่ถูกกว่านี้ไหม?"
```

### Corporate (28–42 ปี)
```yaml
top_concerns:
  1. ดูเป็นธรรมชาติ ไม่ให้คนรู้ว่าทำ
    mitigation: portfolio "subtle results", testimonials จากคนอาชีพใกล้เคียง
  
  2. Downtime กระทบงาน
    mitigation: แสดง "lunch-time procedure", recovery timeline ชัด
  
  3. Doctor เชี่ยวชาญจริงๆ ไหม
    mitigation: certificates, case volume, ก่อน/หลัง ที่ใกล้เคียง
  
  4. Clinic เชื่อถือได้ไหม (reputation)
    mitigation: Google reviews, press mentions, referral จาก peer
  
  5. ข้อมูล privacy (ไม่อยากให้คนอื่นรู้)
    mitigation: private consultation, ไม่ใช้รูปใน portfolio โดยไม่ขออนุญาต

dialogue_pattern: |
  "อยากให้ดูดีขึ้นแต่ไม่ overly done 
  ประชุมทุกวัน คนรู้แล้วกระอักวะ"
```

### High-Income Homemaker (38–58 ปี)
```yaml
top_concerns:
  1. ผลออกมาสวย ดูเป็นธรรมชาติ ไม่ overdone
    concern_intensity: 0.95
    mitigation: "graceful aging" portfolio, elite before/after
  
  2. หมอเข้าใจความต้องการจริงๆ ไหม
    concern_intensity: 0.90
    mitigation: 30+ min consultation, personal follow-up
  
  3. Clinic ให้ความเป็นส่วนตัว
    concern_intensity: 0.85
    mitigation: private room, ไม่มีคิวรอนาน, VIP experience
  
  4. แล้วถ้าไม่พอใจทำอะไรได้บ้าง
    concern_intensity: 0.80
    mitigation: revision policy ชัด, lifetime relationship
  
  5. สามีจะรู้สึกอย่างไร (สังคม peer judgment)
    concern_intensity: 0.70  # ไม่พูดตรงๆ แต่มีผลต่อ decision
    mitigation: "ดูดีขึ้น คนรอบข้างสังเกต"

dialogue_pattern: |
  "เพื่อนใน group แนะนำมา อยากลองดู 
  แต่อยากให้ดูเป็นธรรมชาติ ไม่ตึงจนเกิน"
```

### Gen Z (18–26 ปี)
```yaml
top_concerns:
  1. ราคาเกิน budget (price ceiling 10,000 บาท)
    mitigation: entry-level options, starter packages
  
  2. Clinic มีประวัติแย่บน TikTok/social ไหม
    mitigation: clean social presence, respond ทุก comment ดี
  
  3. เพื่อนคนอื่นทำแล้วเป็นยังไง (peer validation)
    mitigation: UGC reviews, nano-influencer content
  
  4. ตอบ DM ช้า → ไปที่อื่น
    concern_intensity: 0.95
    mitigation: response time <1 hr, auto-reply + human follow-up
  
  5. เจ็บปวดหรือเปล่า (low pain tolerance content)
    mitigation: video "ทำแบบไม่เจ็บ" content, numbing cream protocol

dialogue_pattern: |
  "เห็น TikTok แล้วสนใจ DM ไปแล้ว 
  ถ้าตอบช้าไปคลินิกอื่นเลย"
```

### LGBTQ+ / Gender Affirming
```yaml
top_concerns:
  1. หมอ non-judgmental เข้าใจ gender identity
    concern_intensity: 1.0  # สูงสุด
    mitigation: แสดง LGBTQ+-affirming stance ชัดเจน, community endorsement
  
  2. ผลลัพธ์ตรงกับ gender identity (ไม่ใช่แค่ "สวย")
    concern_intensity: 0.95
    mitigation: FFS/SRS portfolio ที่ตรง identity
  
  3. Community trust — ใครในกลุ่มเคยใช้บ้าง
    concern_intensity: 0.95
    mitigation: community ambassador, peer testimonials
  
  4. ปลอดภัยทางกฎหมาย (SRS documentation Thailand)
    concern_intensity: 0.80
    mitigation: อธิบาย legal process ชัด, document assistance
  
  5. Financial planning สำหรับ long journey
    concern_intensity: 0.70
    mitigation: payment plan, package bundling for multi-stage journey

dialogue_pattern: |
  "ใน community บอกว่า [คลินิก] ดี 
  แต่อยากรู้ว่าหมอเข้าใจ MTF จริงๆ ไหม 
  ไม่ใช่แค่รับเงินอย่างเดียว"
```

### Grooming Male
```yaml
top_concerns:
  1. คนจะรู้ว่าทำ (masculine identity concern)
    concern_intensity: 0.95
    mitigation: "subtle", "natural", no mention in front of staff
  
  2. Clinic ดูเป็น "ผู้ชาย" ไปได้บ้าง ไม่ feminine เกิน
    concern_intensity: 0.85
    mitigation: neutral clinic aesthetic, male before/after
  
  3. ผลต้อง "ดูดีขึ้น แต่ไม่ดู done"
    concern_intensity: 0.90
    mitigation: portfolio of subtle male results
  
  4. ไม่มั่นใจว่า treatment เหมาะกับผู้ชายไหม
    concern_intensity: 0.75
    mitigation: content "ผู้ชายทำ botox เป็นเรื่องปกติ" + male-specific dosing
  
  5. Research แบบ incognito — ไม่อยากให้ track
    mitigation: ไม่ retarget ads aggressive เกินไป

dialogue_pattern: |
  "ดูข้อมูลมาสักพักแล้ว แต่ไม่ได้ถามใคร 
  แค่อยากดูดีขึ้นนิดหน่อย ไม่ให้รู้ว่าทำ"
```

### Medical Tourist
```yaml
top_concerns:
  1. จะเกิดอะไรขึ้นถ้ามี complication หลังกลับบ้าน
    concern_intensity: 0.95
    mitigation: international follow-up protocol, local doctor network
  
  2. Language barrier — communicate กับ team ได้ไหม
    concern_intensity: 0.90
    mitigation: English/Chinese/Arabic coordinator ที่พูดได้จริง
  
  3. Cost total (including travel, stay)
    mitigation: all-inclusive package คำนวณให้ล่วงหน้า
  
  4. Credentials verifiable from home country
    concern_intensity: 0.85
    mitigation: website credentials, Google Scholar, RealSelf profile
  
  5. Cultural/dietary needs during recovery
    mitigation: halal food available (Middle East), Chinese-speaking nurse (China)

dialogue_pattern: |
  "I've done a lot of research and your clinic 
  came up highly recommended. Can your coordinator 
  communicate in English throughout the process?"
```

---

## Objection Handling Scripts (Simulation)

```yaml
objection_responses:
  "แพงเกินไป":
    trigger_personas: [genz, new_worker]
    agent_response_good: |
      "เข้าใจค่ะ ทางคลินิกมีแพ็คเกจ [X] บาท 
       ที่ครอบคลุม [treatment] + follow-up ด้วย 
       หรือถ้าสนใจผ่อน 0% ก็มีให้บริการนะคะ"
    agent_response_bad: |
      "ราคานี้ถูกที่สุดแล้วค่ะ" (ไม่ตอบ concern จริงๆ)
  
  "กลัวไม่เป็นธรรมชาติ":
    trigger_personas: [corporate, high_income_homemaker, grooming_male]
    agent_response_good: |
      "เข้าใจเลยค่ะ นี่คือ before/after ของลูกค้า 
       ที่ผลออกมา subtle แบบที่หลายคนพูดถึง 
       หมอจะ consult ก่อนว่าต้องการผลแบบไหน"
  
  "รอโปรก่อน":
    trigger_personas: [genz, new_worker]
    urgency_response: |
      "ช่วงนี้มีโปร [X] อยู่ถึงสิ้นเดือนนะคะ 
       ถ้าจองวันนี้ได้ราคานี้เลย"
```

---

## MiroFish Concern Simulation

```yaml
concern_simulation:
  pre_decision_barrier_weights:
    safety: 0.30
    result_expectation: 0.25
    price: 0.20
    trust_in_doctor: 0.15
    privacy: 0.10
  
  concern_resolution_events:
    positive_review_seen:
      reduces_concern: [result_expectation, trust_in_doctor]
      strength: 0.20
    
    friend_recommendation:
      reduces_concern: [safety, trust_in_doctor, privacy]
      strength: 0.40
    
    negative_news_seen:
      increases_concern: [safety]
      strength: 0.50
    
    transparent_consultation:
      reduces_concern: [safety, result_expectation, price]
      strength: 0.35
    
    price_promotion:
      reduces_concern: [price]
      strength: 0.45
      side_effect: increases_concern_quality: 0.10  # ถูกเกินไป = กังวล quality
  
  decision_threshold:
    convert_to_booking: concern_total < 0.30  # ถ้า concern < 30% → จอง
    remain_researching: concern_total 0.30–0.60
    exit_consideration: concern_total > 0.60
```
