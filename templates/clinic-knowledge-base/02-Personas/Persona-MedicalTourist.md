# Persona: นักท่องเที่ยวเชิงการแพทย์ (Medical Tourist)

## Demographics

| Field | Value |
|-------|-------|
| อายุ | 25–55 ปี |
| ที่มา (หลัก) | จีน, ตะวันออกกลาง (UAE/Saudi), CLMV, ออสเตรเลีย, UK |
| Budget | USD 3,000–25,000/trip |
| ระยะพัก | 5–21 วัน |

## ทำไมเลือกไทย

- ราคาถูกกว่าบ้านตัวเอง **40–70%**
- คุณภาพสูง — แพทย์เฉพาะทาง, อุปกรณ์ทันสมัย
- ไม่มี social stigma เหมือนกลับบ้าน (ทำแล้วกลับไปบอกว่าผ่าตัดที่ไทย)
- Recovery + vacation รวมกันได้
- บางประเทศ: ไม่มี procedure นี้ในบ้าน (gender surgery)

## Treatments ที่มาทำสูงสุด

### กลุ่มจีน
- Rhinoplasty + double eyelid combo
- Full face anti-aging package
- Breast augmentation
- V-line jaw surgery

### กลุ่มตะวันออกกลาง
- Liposuction + tummy tuck (Mommy Makeover)
- Rhinoplasty (Middle Eastern nose)
- Hair transplant
- Bariatric + body contouring post-weight loss

### กลุ่ม CLMV
- Surgery ที่ไม่มีในประเทศตัวเอง
- ราคาถูกกว่าในกรุงเทพฯ แม้จะมา รพ. เดียวกัน

### กลุ่ม Western (AUS/UK)
- Price arbitrage — ผ่าตัดเดียวกันถูกกว่า 50–70%
- Gender affirmation surgery
- Dental + aesthetic combo

## Decision Journey

1. YouTube/Google/Weibo research: "rhinoplasty Thailand", "best plastic surgery Bangkok"
2. Contact coordinator / agent (ส่วนมาก)
3. Virtual consultation กับหมอก่อนมา
4. Book flight + clinic พร้อมกัน
5. มาถึง → consultation จริง → ผ่าตัด → recovery → กลับบ้าน

## Trust Signals

1. ✅ JCI Accreditation (สำหรับ hospital tier)
2. ✅ International patient coordinator — พูดภาษาเดียวกัน
3. ✅ ภาพ before/after ชัด มีลูกค้าจากประเทศเดียวกัน
4. ✅ รีวิวบน RealSelf, Google, หรือ platform ประเทศนั้น
5. ✅ ราคา all-inclusive package ชัดเจน

## MiroFish Agent Configuration

```yaml
persona_type: medical_tourist
origin_countries: [China, UAE, Australia, Myanmar, Vietnam]
platform_primary: google  # varies by country
price_sensitivity: medium  # เน้น value ไม่ใช่ราคาถูกที่สุด
trust_in_authority: medium_high
sharing_behavior: reviews_on_international_platforms
language_preference: english_or_native
cognitive_biases:
  - authority_bias
  - country_of_origin_heuristic  # ไทย = เชื่อถือ beauty surgery
  - anchoring                     # เทียบราคาบ้านเป็น anchor
```
