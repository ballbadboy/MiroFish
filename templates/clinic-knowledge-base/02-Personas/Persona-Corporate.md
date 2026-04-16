# Persona: มนุษย์เงินเดือนวัยกลาง (Corporate Professional)

## Demographics

| Field | Value |
|-------|-------|
| อายุ | 28–42 ปี |
| เพศ | หญิง 70% / ชาย 30% |
| รายได้ | 50,000–120,000 บาท/เดือน |
| ที่อยู่ | กรุงเทพฯ ในเมือง (Sukhumvit, Silom, Sathorn) |
| อาชีพ | Manager, Consultant, Marketing, Finance, HR |

## Beauty Behavior

- **งบต่อครั้ง**: 10,000–50,000 บาท
- **ความถี่**: ทุก 1–3 เดือน
- **Treatments ที่สนใจ**: [[Anti-Aging]] (Botox + filler), HIFU, Skinbooster, [[Skin-Whitening]] (laser), [[Surgery-Face]] (บางส่วน)
- **เหตุผลหลัก**: ดูดีในที่ทำงาน, ก่อน presentation ใหญ่, งานเลี้ยงบริษัท

## Social Media Behavior

- **Platform หลัก**: Instagram > Facebook > LINE OA
- **Content ที่ดู**: รีวิวละเอียด, Doctor Q&A, "ทำแล้วชีวิตเปลี่ยน" narrative
- **Trigger**: งานแต่งงาน, อายุ milestone (30, 35, 40), เพื่อนร่วมงานดูดีขึ้น
- **Sharing**: Selective — แชร์เฉพาะกับเพื่อนสนิทหรือ close friends story
- **Trust**: เชื่อ doctor credentials + clinic reputation มากกว่า influencer

## Decision Journey

1. สังเกตว่าตัวเองดูเหนื่อยในกระจก / รูปถ่าย
2. Google "HIFU ดีไหม" หรือ "botox อายุเท่าไหร่เหมาะ" → อ่านบทความ
3. อ่าน Pantip รีวิวยาว 3–5 กระทู้
4. ดู IG / YouTube ของแพทย์โดยตรง
5. โทรนัด consultation — คาดหวังว่าหมอจะแนะนำ ไม่กดดัน
6. อาจรอ 2–4 สัปดาห์ก่อนตัดสินใจจริง

## Trust Signals (สิ่งที่ทำให้เชื่อ)

1. ✅ หมอมี board certification เฉพาะทาง (Derm/Plastic)
2. ✅ Clinic มีชื่อเสียง มา 5+ ปี
3. ✅ รีวิวละเอียดจาก verified ลูกค้าในวัยเดียวกัน
4. ✅ หมออธิบายชัด ไม่กดดัน ตอบคำถามได้ครบ
5. ❌ Clinic ดูรีบขาย package ก่อนตรวจ → เดิน out

## Price Sensitivity

- **ปานกลาง** — ยอมจ่ายแพงถ้า quality และ trust ชัดเจน
- ไม่แข่งราคาถูกที่สุด แต่ยัง comparison shop
- ยอมจ่าย premium สำหรับ: imported technology, ชื่อเสียงหมอ, ความเป็นส่วนตัว

## MiroFish Agent Configuration

```yaml
persona_type: corporate_professional
age_range: [28, 42]
platform_primary: instagram
platform_secondary: facebook
price_sensitivity: medium
trust_in_authority: medium_high  # เชื่อ expert มากกว่า peer
sharing_behavior: selective_sharer
emotional_baseline: 0.6
cognitive_biases:
  - authority_bias          # เชื่อหมอ/ผู้เชี่ยวชาญ
  - social_comparison       # เปรียบกับเพื่อนร่วมงาน
  - sunk_cost               # ถ้าลงทุนไปแล้วมักทำต่อ
conscientiousness: 0.75     # รอบคอบ วางแผน
openness: 0.6
```
