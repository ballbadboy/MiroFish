# Platform Behavior — Social Media Dynamics for Beauty Simulation

## Overview

พฤติกรรมเฉพาะของแต่ละ platform ที่ส่งผลต่อ simulation dynamics
ใช้สำหรับ: กำหนด agent behavior, spread rate, trust formation ตาม platform

---

## TikTok

### Algorithm Behavior
```
Discovery mechanism : For You Page (FYP) — ไม่ต้อง follow
Content half-life  : 24–72 ชั่วโมง (ถ้าไม่ viral หาย), อาจ resurface เป็นเดือน
Virality trigger   : Watch-through rate >70% ใน 1 ชั่วโมงแรก
Sound effect       : ใช้ trending sound → +3x reach
Hashtag            : 5–10 tags optimal
```

### User Behavior Patterns
```yaml
tiktok_behaviors:
  scroll_speed: fast  # average 2.5 วิ/video ก่อน scroll
  decision_from_content:
    see_video: day_0
    search_more: day_0 to day_1
    dm_clinic: day_1 to day_2
    book_appointment: day_2 to day_7
  
  content_trust_levels:
    nano_influencer_(<10k): 0.85     # "คนจริง"
    micro_influencer_(10-100k): 0.65
    macro_influencer_(>100k): 0.40   # "ได้รับเงินแน่"
    clinic_official_account: 0.25   # "โฆษณา"
    ad_label: 0.15                  # "ข้าม"
  
  comment_behavior:
    ask_price: 0.45         # 45% ของ comment คือถามราคา
    tag_friend: 0.25
    share_experience: 0.20
    negative_warn: 0.10
```

### Crisis on TikTok
- **Spread speed**: เร็วที่สุดในทุก platform
- **Peak**: 6–18 ชั่วโมงหลัง post
- **Amplifier**: Duet / Stitch feature — คนอื่นรีแอคต่อ
- **Clinic response**: ต้อง respond ใน comment ภายใน 4 ชั่วโมง

---

## Instagram

### Algorithm Behavior
```
Discovery : Explore page + Reels feed
Content types: Photo (stories), Carousel (saves), Reels (reach)
Half-life  : Post 2–3 วัน, Reel 3–7 วัน, Story 24 ชั่วโมง
Save signal: Instagram ให้น้ำหนัก saves > likes
```

### User Behavior Patterns
```yaml
instagram_behaviors:
  content_format_preference:
    before_after_carousel: trust_level_0.80
    single_photo_result: trust_level_0.55
    reels_transformation: trust_level_0.70
    story_q_and_a: trust_level_0.75
  
  dm_behavior:
    message_type: price_inquiry  # 60% ถาม ราคา
    response_time_expectation_hours: 2
    conversion_if_response_<1hr: 0.65
    conversion_if_response_>24hr: 0.15
  
  persona_engagement:
    corporate: saves_quietly_then_dm
    high_income_homemaker: lurk_only_then_ask_friend
    genz: comment_public_then_dm
```

### Instagram-Specific Dynamics
- **Private browsing**: Grooming male ดู IG แบบ anonymous (no account)
- **Highlight**: Clinic ที่มี organized Highlights (Before/After, Prices, FAQ) → trust สูงกว่า
- **Story polls**: ใช้ดี engagement แต่ไม่ convert โดยตรง

---

## Facebook (Groups & Pages)

### Algorithm Behavior
```
Groups     : Organic reach ยังดีอยู่ใน closed groups
Pages      : Reach ต่ำมากโดยไม่ boost (5–10% ของ followers)
Content    : Long-form text + photos → ได้ engagement สูงใน group
Half-life  : Post ใน group อยู่ใน search นาน (ถาม-ตอบ ย้อนหลังได้)
```

### Group Dynamics
```yaml
facebook_group_dynamics:
  major_groups:
    - name: "ทำศัลยกรรมกัน"
      members: 500000+
      content_type: reviews, questions, before/after
      persona_dominant: new_worker, corporate
    
    - name: "สาวประเภทสอง / MTF Thailand"
      members: 100000+
      content_type: journey sharing, clinic recommendations
      persona_dominant: lgbtq_gender_affirming
    
    - name: "แม่บ้านแชร์ประสบการณ์"
      members: private
      content_type: word_of_mouth, referrals
      persona_dominant: high_income_homemaker
  
  trust_dynamics:
    long_time_member: 0.90   # คนที่อยู่ใน group นาน
    new_account: 0.30        # suspect seed review
    verified_experience: 0.95  # มีรูป timeline ชัดเจน
    anonymous_warning: 0.60  # warn แต่ไม่มีรูปยืนยัน
```

### Facebook-Specific Dynamics
- **Screenshot culture**: post ถูก screenshot → spread ออก group
- **Admin role**: admin ที่ดีลบ spam → group น่าเชื่อถือขึ้น
- **Messenger**: การนัด clinic มักผ่าน Messenger ไม่ใช่เว็บ

---

## LINE

### Behavior Patterns
```yaml
line_behaviors:
  usage_context: private_1on1_or_small_groups
  clinic_interaction:
    - add_clinic_OA (Official Account)
    - chat_for_appointment
    - receive_promotions
  
  trust_dynamics:
    personal_recommendation_via_line: 0.95  # เพื่อนส่งให้ = trust สูงมาก
    clinic_broadcast_message: 0.30          # spam-like
  
  persona_primary_users:
    high_income_homemaker: LINE_is_primary_contact
    new_worker: LINE_for_appointment_only
    genz: LINE_is_old_school_rarely_used
```

---

## Google (Search + Maps)

### Search Behavior
```yaml
google_search_patterns:
  query_types:
    informational: "ทำจมูกดีไหม", "filler ปากเจ็บไหม"
    navigational: "คลินิก[ชื่อ] เบอร์โทร"
    transactional: "ทำจมูกราคาถูก กรุงเทพ", "คลินิกเสริมจมูกใกล้ BTS"
    comparison: "เสริมจมูก vs filler จมูก"
  
  click_behavior:
    position_1: click_rate_0.30
    position_2: click_rate_0.15
    position_3: click_rate_0.10
    google_maps_listing: click_rate_0.25
    
  review_trust:
    google_maps_4.8+_50reviews: 0.85
    google_maps_4.5+_200reviews: 0.90
    google_maps_<4.0: avoid (0.10 conversion)
```

---

## Pantip

### Behavior Patterns
```yaml
pantip_behaviors:
  user_demographic: 25–45, higher education, research-oriented
  content_half_life: years  # ติด Google search นาน
  
  trust_dynamics:
    detailed_review_with_photos: 0.92
    short_positive_review: 0.55  # suspect paid
    negative_review_detailed: 0.85
  
  search_query_pattern:
    template: "[treatment] [clinic_name] pantip"
    example: "เสริมจมูก Absolute clinic pantip"
    
  persona_users:
    high_income_homemaker: pantip_primary_research_platform
    corporate: pantip_for_decision_validation
    genz: เปิดดูแต่ไม่ post (ดู old gen)
```

---

## MiroFish Platform Config

```yaml
platform_simulation:
  agent_platform_assignment:
    genz_experimenter:
      primary: tiktok
      secondary: instagram
      tertiary: google_maps
      time_spent_hours_per_day: {tiktok: 4, instagram: 1.5}
    
    corporate:
      primary: instagram
      secondary: google
      tertiary: pantip
      time_spent_hours_per_day: {instagram: 0.5, google: 0.3}
    
    high_income_homemaker:
      primary: facebook
      secondary: line
      tertiary: pantip
      time_spent_hours_per_day: {facebook: 1.5, line: 2}
    
    lgbtq_gender_affirming:
      primary: facebook_groups
      secondary: twitter_x
      tertiary: discord
      time_spent_hours_per_day: {facebook: 2, twitter: 1.5}
    
    grooming_male:
      primary: instagram  # lurk mode
      secondary: youtube
      time_spent_hours_per_day: {instagram: 0.5, youtube: 0.8}
    
    medical_tourist:
      primary: google
      secondary: youtube
      tertiary: realself
      time_spent_hours_per_day: {google: 1, youtube: 0.5}
  
  cross_platform_spread:
    tiktok_to_instagram: 0.40    # content repurposed
    facebook_to_line: 0.70       # screenshot shared
    pantip_to_google: 1.0        # Google indexes Pantip
    instagram_to_facebook: 0.30
```
