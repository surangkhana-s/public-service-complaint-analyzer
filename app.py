import re
import pandas as pd
import streamlit as st
import pythainlp
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.tag import pos_tag

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Public Service Complaint Analyzer", page_icon="🚨", layout="wide")

# 1. Regex & Cleansing (PII Masking)
def clean_text_and_mask_pii(text: str):
    phone_pattern = r'0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}'
    id_pattern = r'\b\d{1}-\d{4}-\d{5}-\d{2}-\d{1}\b|\b\d{13}\b'
    cleaned = re.sub(phone_pattern, '[ANONYMIZED PHONE]', text)
    cleaned = re.sub(id_pattern, '[ANONYMIZED ID]', cleaned)
    return cleaned

# 2. Tokenization & Normalization
def tokenize_and_normalize(text: str):
    tokens = word_tokenize(text, engine="newmm", keep_whitespace=False)
    stopwords = set(thai_stopwords())
    return [w for w in tokens if w not in stopwords and len(w) > 1 and not w.startswith('[ANONYMIZED')]

# 3. Topic Identification
def identify_topic(text: str):
    categories = {
        "ถนนและจราจร": ["ถนน", "ไฟจราจร", "ทางข้าม", "ทางเท้า", "รถติด", "ฝาท่อ", "หลุม", "ซอย"],
        "ขยะและสิ่งแวดล้อม": ["ขยะ", "กลิ่นเหม็น", "น้ำเสีย", "ต้นไม้", "มลพิษ", "คลอง"],
        "ระบบไฟฟ้าและประปา": ["ไฟดับ", "เสาไฟ", "ไฟส่องสว่าง", "น้ำไม่ไหล", "ท่อน้ำแตก", "ประปา"],
        "เสียงรบกวน": ["เสียงดัง", "สถานบันเทิง", "ตั้งแผงลอย", "สุนัขเห่า", "มั่วสุม"]
    }
    for category, keywords in categories.items():
        if any(kw in text for kw in keywords):
            return category
    return "เรื่องร้องเรียนทั่วไป"

# ประเมินความเร่งด่วน
def evaluate_urgency(text: str):
    high_keywords = ["ด่วน", "อันตราย", "อุบัติเหตุ", "ไฟไหม้", "บาดเจ็บ", "ทันที"]
    if any(kw in text for kw in high_keywords):
        return "🔴 ด่วนที่สุด"
    return "🟢 ปกติ"

# 4. POS & NER (Location & Key Nouns)
def extract_entities(text: str):
    tokens = word_tokenize(text, engine="newmm")
    pos_tags = pos_tag(tokens, engine="perceptron")
    key_nouns = [word for word, tag in pos_tags if tag in ['NCCN', 'NPRP'] and len(word) > 1]
    locations = re.findall(r'(?:ซอย|ถนน|บริเวณ|หน้า|แถว)\s*([^\s]+)', text)
    return list(set(key_nouns))[:8], list(set(locations))

# UI Interface
st.title("🚨 Public Service Complaint Analyzer")
st.subheader("ระบบวิเคราะห์และคัดกรองข้อความร้องเรียนบริการสาธารณะ")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 วิเคราะห์ข้อความเดี่ยว", "📁 วิเคราะห์ไฟล์ CSV"])

with tab1:
    user_input = st.text_area("กรอกข้อความร้องเรียน:", height=100)
    if st.button("ประมวลผล", type="primary") and user_input.strip():
        cleaned = clean_text_and_mask_pii(user_input)
        tokens = tokenize_and_normalize(cleaned)
        topic = identify_topic(cleaned)
        urgency = evaluate_urgency(cleaned)
        nouns, locs = extract_entities(cleaned)
        
        c1, c2 = st.columns(2)
        c1.metric("หมวดหมู่ปัญหา", topic)
        c2.metric("ระดับความเร่งด่วน", urgency)
        
        st.write("**ข้อความหลังซ่อนข้อมูลส่วนตัว (PII Masking):**", cleaned)
        st.write("**ผลการตัดคำ (Tokens):**", tokens)
        st.write("**คำสำคัญ (Key Nouns):**", nouns)
        st.write("**พิกัด/สถานที่:**", locs if locs else "ไม่ระบุ")

with tab2:
    uploaded_file = st.file_uploader("อัปโหลด CSV (ต้องมีคอลัมน์ 'text')", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'text' in df.columns:
            df['ข้อความที่ลบ PII'] = df['text'].apply(clean_text_and_mask_pii)
            df['หมวดหมู่'] = df['ข้อความที่ลบ PII'].apply(identify_topic)
            df['ความเร่งด่วน'] = df['ข้อความที่ลบ PII'].apply(evaluate_urgency)
            st.dataframe(df[['text', 'หมวดหมู่', 'ความเร่งด่วน']], use_container_width=True)
            st.bar_chart(df['หมวดหมู่'].value_counts())
