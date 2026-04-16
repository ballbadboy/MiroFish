# Market Players — Thai Beauty Clinic & Hospital Landscape

## Overview

ข้อมูลคู่แข่งและผู้เล่นหลักในตลาด beauty clinic / aesthetic hospital ไทย
ใช้เพื่อ: Competitive positioning, Simulation — agent เลือก provider, Benchmark pricing

> ⚠️ **Note for clinic**: กรุณาอัปเดตข้อมูลราคาและ positioning ทุก 6 เดือน ตลาดเปลี่ยนเร็ว

---

## Tier 1 — Hospital / Medical Center (Full-Service Surgical)

### Bumrungrad International Hospital
```
Type        : Private international hospital
Strength    : JCI, international brand, Med Tourist destination
Weakness    : ราคาสูงมาก, ไม่เน้น cosmetic เป็น primary
Target      : Med Tourist (Western, Middle East), High-income Thai
Notable for : Rhinoplasty package สำหรับ international, General plastic surgery
Pricing     : Premium (30–50% สูงกว่า specialty clinic)
AI crawlers : Strong online presence — มักติด top Google "plastic surgery Bangkok"
```

### Vejthani Hospital
```
Type        : Private hospital — strong aesthetics division
Strength    : JCI certified, ราคาถูกกว่า Bumrungrad 20–30%
Target      : Med Tourist (CLMV, Middle East), Corporate Thai
Notable for : Orthopedic + cosmetic combo packages
```

### Paolo Hospital / Bangkok Hospital Group
```
Type        : Network hospital chain
Strength    : หลายสาขา, brand trust, HA certified
Target      : Domestic Thai, regional Med Tourist
```

---

## Tier 2 — Specialty Aesthetic Clinics (Surgery Focus)

### Preecha Aesthetic Institute (PAI)
```
Type        : Specialty — pioneer SRS Thailand
Strength    : Dr. Preecha — world-known SRS surgeon, decades of experience
Target      : LGBTQ+ (MTF, FTM) globally
Notable for : SRS/GRS, FFS, MTF full package
Pricing     : Mid–premium (SRS ~250,000–450,000 THB)
Online      : Strong international community reputation, Reddit/RealSelf presence
Weakness    : Dr. Preecha aging → succession concern in community
```

### Kamol Cosmetic Hospital
```
Type        : Full-service cosmetic hospital
Strength    : SRS + FFS + general cosmetic, international patient coordinator
Target      : LGBTQ+ (Med Tourist), general cosmetic
Notable for : MTF complete transformation packages
Online      : Heavy international social media presence
```

### Suporn Clinic (Chonburi)
```
Type        : Specialty SRS clinic
Strength    : Dr. Suporn — proprietary SRS technique, cult following internationally
Target      : MTF SRS (Western — UK, Australia, USA)
Pricing     : Premium (SRS ~500,000–700,000 THB)
Weakness    : Location outside Bangkok, long waitlist (months)
Online      : Dedicated forums, YouTube documentary
```

### Yanhee Hospital
```
Type        : Aesthetic hospital
Strength    : Brand awareness สูงมากในไทย, multi-specialty, affordable
Target      : GenZ, New Worker, Med Tourist (CLMV, China)
Notable for : Whitening, rhinoplasty, eyes — mass market
Pricing     : Accessible (mid-tier)
Weakness    : ภาพลักษณ์ mass market → Homemaker/Corporate หลีกเลี่ยง
```

---

## Tier 3 — Premium Beauty Clinics (Non-Surgical Focus)

### Absolute Clinic
```
Type        : Premium non-surgical aesthetic clinic
Strength    : Strong dermatologist team, premium positioning
Target      : Homemaker, Corporate, High-income
Notable for : Laser, energy devices, injectables at premium quality
Pricing     : Premium (Botox 200+ บาท/unit)
```

### Dermaster Clinic
```
Type        : Dermatology-based aesthetic
Strength    : Medical credibility, conservative approach
Target      : Corporate, Homemaker
```

### Better Skin Clinic / Let Me In
```
Type        : Mid-market accessible
Strength    : Locations หลายแห่ง BTS/MRT, ราคาเข้าถึงได้
Target      : GenZ, New Worker
Pricing     : Accessible (Botox 80–120 บาท/unit)
```

### Puttharaksa Aesthetic
```
Type        : Volume mid-market
Strength    : Social media presence, content marketing
Target      : GenZ, New Worker
```

---

## Tier 4 — Korean-Concept Clinics

### ID Hospital Bangkok / Korean-affiliated clinics
```
Type        : Korean aesthetic concept (franchise/concept)
Strength    : Korean beauty halo effect, V-line, rhinoplasty technique
Target      : GenZ (Korean-influenced), Corporate
Notable for : Double eyelid, V-line jaw, rhinoplasty Korean style
Pricing     : Mid–premium
Online      : Strong Instagram/TikTok content
```

---

## Market Dynamics

### Competitive Pressures

```
1. Social media democratization
   → GenZ ดู TikTok → มองหา clinic ที่ content ดี ไม่ใช่ clinic ที่แพงสุด

2. Korean wave influence
   → Double eyelid, V-line เพิ่มขึ้น เพราะ K-drama/K-pop

3. Medical tourism growth
   → CLMV patients เพิ่มทุกปี เพราะ infrastructure ดีขึ้น
   → Middle East (UAE, Saudi) เพิ่มหลัง COVID

4. Price transparency pressure
   → Shopee/Lazada model ทำให้ลูกค้าคาดหวัง transparent pricing
   → Groupon-style platforms (Klook, Wongnai) กดราคา tier 2–3

5. Doctor hopping
   → หมอย้ายคลินิก ลูกค้าตาม → clinic ต้องสร้าง brand ไม่ใช่แค่พึ่งหมอคนเดียว
```

### Positioning Map

```
                    HIGH QUALITY
                         │
           Preecha    Kamol
    Bumrungrad           │      Suporn
                         │
HIGH PRICE ──────────────┼────────────── LOW PRICE
                         │
          Absolute   Dermaster
                         │
                   Yanhee   Wongnai-listed
                         │
                    LOW QUALITY
```

---

## MiroFish Competitive Configuration

```yaml
market_players:
  competitors:
    - id: yanhee
      tier: 2
      specialty: [whitening, rhinoplasty, general]
      target_personas: [genz, new_worker, medical_tourist_clmv]
      price_index: 0.6  # relative to premium = 1.0
      trust_score_overall: 0.70
      social_presence: strong
    
    - id: preecha_pai
      tier: 2
      specialty: [srs, ffs, lgbtq_surgery]
      target_personas: [lgbtq_gender_affirming, medical_tourist_western]
      price_index: 0.85
      trust_score_overall: 0.92
      community_trust: 0.97  # extremely high in LGBTQ+ community
    
    - id: bumrungrad
      tier: 1
      specialty: [general_plastic, medical_tourism]
      target_personas: [medical_tourist_western, high_income_homemaker]
      price_index: 1.5
      trust_score_overall: 0.88
      jci_certified: true
    
    - id: absolute_clinic
      tier: 3
      specialty: [non_surgical, injectables, laser]
      target_personas: [high_income_homemaker, corporate]
      price_index: 1.2
      trust_score_overall: 0.85

  competitive_events:
    - type: price_cut
      trigger: competitor reduces price >15%
      agent_response: reconsider_decision
      affected_personas: [genz, new_worker]
    
    - type: viral_botch
      trigger: competitor has viral negative incident
      agent_response: avoid_competitor
      trust_decay: 0.40
      recovery_months: 6
    
    - type: celebrity_endorsement
      trigger: competitor gains celebrity client
      agent_response: increased_consideration
      affected_personas: [genz, new_worker, corporate]
      trust_boost: 0.15
```
