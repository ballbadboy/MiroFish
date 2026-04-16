# Hashtag Clusters — Thai Beauty Social Media

## Overview

Hashtag clusters สำหรับ simulation ว่า agent ใช้ hashtag อะไร → ส่งผลต่อ reach และ persona ที่เห็น content

---

## Cluster 1: Surgery & Procedure Tags

### Rhinoplasty (เสริมจมูก)
```
Primary TH : #เสริมจมูก #จมูกโด่ง #rhinoplasty
Secondary  : #จมูกสวย #จมูกสูง #ทำจมูก #จมูกใหม่
Branded    : #[คลินิก]จมูก (ถ้า clinic ดัง)
English    : #rhinoplasty #nosejob #rhinoplastythailand
Volume     : 500K–2M posts (TikTok), 200K+ (IG)
Peak season: ต.ค.–ธ.ค., ม.ค.
```

### Filler (ฟิลเลอร์)
```
Primary TH : #ฟิลเลอร์ #ฟิลเลอร์ปาก #ฟิลเลอร์คาง
Secondary  : #ฟิลเลอร์เชียงใหม่ #ฟิลเลอร์กรุงเทพ #filler
Controversy: #ฟิลเลอร์เป็นก้อน #ฟิลเลอร์ผิดพลาด (crisis cluster)
Volume     : 1M+ posts
```

### Botox
```
Primary TH : #โบท็อกซ์ #botox #โบท็อก
Secondary  : #โบท็อกซ์กราม #botoxjaw #ลดกราม
Male-specific: #ผู้ชายโบท็อก #ผู้ชายดูแลตัวเอง
Volume     : 800K+ posts
```

### Double Eyelid (ทำตา)
```
Primary TH : #ทำตา #ทำหนังตา #double eyelid
Secondary  : #ตาสองชั้น #ตาสวย
Korean-style: #เปิดหัวตา #เปิดหางตา
```

### Breast Surgery (เสริมหน้าอก)
```
Primary TH : #เสริมหน้าอก #ทำหน้าอก
Coded (low-risk): #เสริมความมั่นใจ
Implant-specific: #motiva #nagor #mentor
```

### Body Surgery
```
#ดูดไขมัน #liposuction #เอวคอด
#ท้องแบน #tummytuck #abdominoplasty
#BBL (avoided ใน TH — ไม่ค่อยทำ)
```

---

## Cluster 2: Non-Surgical Treatment Tags

### Skin Whitening / Brightening
```
TH popular : #ผิวขาว #ผิวกระจ่างใส #whitening
IV-related : #กลูต้า #glutathione #วิตามินผิว
Laser      : #เลเซอร์หน้าใส #เลเซอร์ขาว #picosure
Trend 2024 : #skinglass #glassskin #glowskin
Volume     : 2M+ posts — TOP category
```

### Anti-Aging
```
TH popular : #ต่อต้านริ้วรอย #antiaging #หน้าใส
HIFU       : #HIFU #ultraformer #ยกกระชับ
Thread lift: #ร้อยไหม #threadlift #หน้าเรียว
Filler anti-age: #ฟิลเลอร์แก้มตอบ #ฟิลเลอร์ร่องแก้ม
```

### Acne Treatment
```
TH popular : #รักษาสิว #สิว #acne
Scar-specific: #รอยสิว #acnescar #เลเซอร์รอยสิว
GenZ-heavy : #สิวแพ้ #สิวฮอร์โมน
Volume     : 3M+ posts — GenZ primary driver
```

---

## Cluster 3: Persona-Specific Hashtag Clusters

### LGBTQ+ / Gender Affirmation Cluster
```
Community  : #สาวประเภทสอง #MTF #FFS #SRS #GRS
Information: #ฮอร์โมน #hormone #transgenderthailand
Support    : #pride #lgbtqthailand #สาวทรานส์
International: #mtftransformation #srsthailand #ffssurgery
Sensitive  : Agent ต้องระวัง — บาง hashtag ถูก shadow-ban บาง platform
```

### Grooming Male Cluster
```
TH         : #ผู้ชายดูแลตัวเอง #ผู้ชายสวย #mengrooming
Normalized : #ผู้ชายทำโบท็อกได้ #menbeauty
International: #mengrooming #menskincare #menaesthetics
Volume     : เติบโต YoY 40% (2022–2024) แต่ยังน้อยกว่า female tags
```

### Medical Tourist Cluster (Thai-targeted)
```
English    : #plasticsurgerythailand #aestheticthailand #bangkokplasticsurgery
Destination: #bangkokbeauty #beautyinbangkok
Trust tags : #jciaccredited #boardcertified #thaisurgeon
```

---

## Cluster 4: Emotion & Journey Tags

### Decision Journey Tags
```
Research phase: #คิดจะทำ #อยากทำ #รีวิว[treatment]
Pre-procedure: #นัดทำ #วันนี้ทำ #ก่อนทำ
Recovery      : #dayX #วันที่X หลังทำ #recovery
Result        : #ก่อนหลัง #beforeafter #ผลลัพธ์
```

### Emotional Tags
```
Positive outcome: #มั่นใจขึ้น #ชอบตัวเองมากขึ้น #คุ้มมาก
Fear/concern    : #กลัวเจ็บ #กลัวผิดพลาด #กังวล
FOMO           : #ทำเลย #โปรดี #ราคาดี
```

---

## Cluster 5: Crisis / Negative Clusters

> ⚠️ **Simulation note**: เมื่อ agent ใช้ hashtag เหล่านี้ → trigger crisis scenario

```yaml
crisis_hashtags:
  filler:
    - "#ฟิลเลอร์ผิดพลาด"
    - "#ฟิลเลอร์เป็นก้อน"
    - "#filler_gone_wrong"
  botox:
    - "#โบท็อกซ์หนังตาตก"
    - "#botox_fail"
  surgery:
    - "#ผ่าตัดผิดพลาด"
    - "#revision_surgery"
    - "#แก้ผ่าตัด"
  clinic_specific:
    - "#[clinicname]ไม่แนะนำ"
    - "#[clinicname]review_bad"
```

---

## MiroFish Hashtag Simulation Config

```yaml
hashtag_simulation:
  reach_multipliers:
    trending_sound_bonus: 3.0   # TikTok sound trending → 3x reach
    top_hashtag_bonus: 2.0      # hashtag volume >1M → 2x
    niche_hashtag_bonus: 1.5    # niche tag → better targeting, 1.5x engagement rate
    crisis_hashtag_spread: 4.0  # crisis tags spread 4x faster
  
  hashtag_clusters_by_persona:
    genz_experimenter:
      primary: ["#ทำริมฝีปาก", "#สิว", "#ก่อนหลัง", "#TikTokBeauty"]
      platform: tiktok
      avg_hashtags_per_post: 8
    
    lgbtq_gender_affirming:
      primary: ["#สาวประเภทสอง", "#MTF", "#FFS", "#SRS"]
      platform: facebook_groups
      avg_hashtags_per_post: 3
    
    corporate:
      primary: ["#botox", "#ผิวสวย", "#antiaging"]
      platform: instagram
      avg_hashtags_per_post: 5
    
    high_income_homemaker:
      primary: []  # ไม่ค่อยใช้ hashtag
      platform: facebook
      avg_hashtags_per_post: 1
    
    grooming_male:
      primary: ["#ผู้ชายดูแลตัวเอง", "#mengrooming"]
      platform: instagram
      avg_hashtags_per_post: 4
    
    medical_tourist:
      primary: ["#plasticsurgerythailand", "#bangkokbeauty"]
      platform: google
      avg_hashtags_per_post: 0  # ใช้ search แทน
  
  viral_threshold:
    tiktok: 50000  # views ก่อน algorithm push
    instagram: 1000  # saves
    facebook: 500   # shares
    pantip: 50      # replies
```
