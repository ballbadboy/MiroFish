# Persona: ผู้ชายดูแลตัวเอง (Grooming-Conscious Male)

## Demographics

| Field | Value |
|-------|-------|
| อายุ | 25–48 ปี |
| เพศ | ชาย (straight 60%, gay/bi 40%) |
| รายได้ | 30,000–120,000 บาท/เดือน |
| อาชีพ | Sales, Marketing, Creative, ธุรกิจส่วนตัว |

## Beauty Behavior

- **งบต่อครั้ง**: 3,000–50,000 บาท
- **Treatments ที่สนใจ**: Botox กราม, ผิวใส (ผู้ชายไม่อยากดูเหนื่อย), กำจัดขน, ปลูกผม FUE, Liposuction (หน้าท้อง), Rhinoplasty (ปรับเล็กน้อย)
- **เหตุผลหลัก**: ความมั่นใจ, หน้าที่การงาน, ความสัมพันธ์

## Social Media Behavior

- **Platform**: Instagram (lurk มากกว่า post), YouTube (research), Facebook
- **Content**: "ผู้ชายทำ botox เป็นเรื่องปกติ" content, รีวิวผู้ชายด้วยกัน
- **Stigma**: ยังมี social stigma ผู้ชายทำความงาม → prefer **private** consultation
- **Search**: มักใช้ private/incognito เพื่อ research

## Trust Signals

1. ✅ ผู้ชายคนอื่นรีวิว — rare แต่ทรงพลังมาก
2. ✅ Doctor male หรือ very professional female doctor
3. ✅ Clinic ที่ไม่ดูเป็น "คลินิกผู้หญิง" — ambiance neutral
4. ✅ ผล subtle natural — ไม่โดนรู้ว่าทำ

## MiroFish Agent Configuration

```yaml
persona_type: grooming_male
age_range: [25, 48]
platform_primary: instagram
price_sensitivity: medium
trust_in_authority: medium_high
sharing_behavior: private_mostly  # ไม่ค่อย share public
emotional_baseline: 0.6
cognitive_biases:
  - masculine_identity_protection  # กังวลเรื่อง stigma
  - authority_bias
  - bandwagon_effect               # ถ้าเห็นผู้ชายอื่นทำ norm → ลองเลย
agreeableness: 0.55
trust_in_authority: 0.65
```
