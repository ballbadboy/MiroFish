# Thai Beauty Clinic — MiroFish Knowledge Base

> **วิธีใช้:** Upload ทั้ง vault นี้เข้า MiroFish ผ่าน Graph Build
> ไฟล์ทั้งหมดเป็น Markdown — Zep จะแปลง [[links]] และ relationships เป็น knowledge graph อัตโนมัติ

## โครงสร้าง Vault

| โฟลเดอร์ | เนื้อหา |
|---------|---------|
| [[01-Treatments]] | บริการทั้งหมด + ราคา + recovery time |
| [[02-Personas]] | กลุ่มลูกค้า 7 ประเภท พร้อม behavior ใน social media |
| [[03-Triggers]] | ปฏิทินทริกเกอร์ตามฤดูกาล + ชีวิต |
| [[04-Competitive]] | ปัจจัยเปรียบเทียบ + กลุ่ม market players |
| [[05-Social-Simulation]] | รูปแบบรีวิว + hashtags + behavior ต่อ platform |
| [[06-Risks]] | ความเสี่ยงที่ลูกค้ากังวล — สำคัญมากสำหรับ simulate crisis |

## ข้อมูลที่ต้องเพิ่มจากคลินิกเอง

- [ ] รีวิวจริงจากลูกค้า (Google Maps, Pantip, Facebook)
- [ ] ราคาของคลินิกนี้โดยเฉพาะ
- [ ] รายชื่อและ credentials ของแพทย์
- [ ] อุปกรณ์/เทคโนโลยีที่มี
- [ ] โปรโมชั่นปัจจุบัน
- [ ] Competitor หลักในพื้นที่

## MiroFish Simulation Templates แนะนำ

1. **Launch Treatment ใหม่** — inject event = โพสต์ประกาศ treatment ใหม่
2. **ทดสอบราคา** — Scenario A: ราคา X vs Scenario B: ราคา Y
3. **Crisis Response** — inject = รีวิวแย่ 1 อัน → ดู sentiment cascade
4. **โปรโมชั่น Flash Sale** — inject = โพสต์โปร → ดู viral potential
