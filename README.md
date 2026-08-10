# 🚨 Public Service Complaint Analyzer

เว็บแอปพลิเคชันสำหรับวิเคราะห์ จัดกลุ่ม และคัดกรองข้อความร้องเรียนบริการสาธารณะ

## 🛠️ เทคนิค NLP ที่ใช้
1. **Regex & Cleansing:** ลบเบอร์โทรศัพท์และเลขบัตรประชาชน (PII Masking)
2. **Tokenization & Normalization:** ตัดคำและลบ Stopwords ด้วย PyThaiNLP
3. **Topic Identification:** จัดกลุ่มประเภทปัญหาด้วย Rule-based Keyword Matching
4. **POS Tagging & NER:** สกัดคำนามสำคัญ และระบุพิกัดสถานที่จากข้อความ

## 🤖 Prompts ที่ใช้สั่งการ AI
- *"เขียน Regex ตรวจจับเบอร์โทรศัพท์ไทยและเลขบัตรประชาชนเพื่อทำ PII Masking"*
- *"เขียนฟังก์ชัน PyThaiNLP ตัดคำ ลบ Stopwords และสกัดพิกัดสถานที่"*
- *"สร้าง UI ด้วย Streamlit รองรับการพิมพ์ข้อความและการอัปโหลดไฟล์ CSV"*
