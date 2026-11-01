import streamlit as st
import pandas as pd
import os
import time
import csv

# ==========================================
# إعداداتك الشخصية (الروابط)
# ==========================================
TIKTOK_URL = "https://www.tiktok.com/@ethical_hacking99" 
YOUTUBE_URL = "https://youtube.com/@darknetsailorpro-o1l?si=oj8Z9hyMhNzqZpqX" 
# ==========================================

st.set_page_config(page_title="تسريبات تيليغرام - Darknetsailor", page_icon="🟢", layout="wide")

# تصميم الأمن السيبراني (مصفوفة خضراء داكنة وخطوط واضحة)
cyber_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    .stApp {
        background-color: #050a05;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
        color: #e0e0e0;
        font-family: 'Cairo', sans-serif;
    }
    
    h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #00ff41 !important; }
    
    .stTextInput>div>div>input {
        color: #00ff41 !important;
        background-color: #0a1c0a !important;
        border: 1px solid #00ff41 !important;
        border-radius: 8px;
        font-family: 'Cairo', sans-serif !important;
        font-size: 16px;
    }
    
    .stButton>button, .stDownloadButton>button {
        background-color: #0a1c0a !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 8px;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #00ff41 !important;
        color: #050a05 !important;
        box-shadow: 0 0 15px #00ff41;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #0a1c0a;
        border: 1px solid #00ff41;
        border-radius: 8px;
        color: #e0e0e0;
        padding: 10px 25px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #00ff41 !important; color: #050a05 !important; }

    /* تصميم البطاقة الاستخباراتية */
    .intel-card {
        background-color: #071407;
        border: 1px solid #00ff41;
        border-left: 6px solid #00ff41;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
        transition: 0.3s;
    }
    .intel-card:hover { box-shadow: 0 0 25px rgba(0, 255, 65, 0.3); transform: translateY(-2px); }
    
    .intel-title {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 900;
        border-bottom: 1px dashed #00ff41;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .intel-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .intel-item { font-size: 16px; }
    .intel-label { color: #00aa33 !important; font-weight: bold; margin-left: 5px;}
    .intel-value { color: #00ff41 !important; font-family: 'Share Tech Mono', monospace; font-size: 18px; }
    .empty-data { color: #444 !important; font-style: italic; }
    
    .social-links { text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #00aa33; }
    .social-links a { color: #00ff41; text-decoration: none; font-weight: bold; margin: 0 15px; font-size: 18px; }
    .social-links a:hover { text-shadow: 0 0 10px #00ff41; }
</style>
"""
st.markdown(cyber_css, unsafe_allow_html=True)

DB_FILE = 'telegram_db.csv'
COLUMNS = ['sys_id', 'first_name', 'last_name', 'phone', 'user_id', 'nickname', 'last_seen']

# دالة القراءة الدقيقة (باستخدام csv بدلاً من pandas)
def load_data():
    if not os.path.exists(DB_FILE):
        # بيانات تجريبية للتأكد من عمل الأداة
        data = [
            ['1', 'محمد', 'العربي', '222222', '11111', 'taaay', ''],
            ['2', 'Ali', '', '5555', '22222', 'Ali_Nick', '']
        ]
        df = pd.DataFrame(data, columns=COLUMNS)
        df.to_csv(DB_FILE, sep='|', index=False, header=False)
        return df

    data = []
    try:
        # محاولة القراءة بجميع الترميزات الممكنة
        encodings = ['utf-8-sig', 'utf-8', 'cp1251', 'latin1']
        for enc in encodings:
            try:
                with open(DB_FILE, 'r', encoding=enc) as f:
                    sample = f.read(1024)
                    delimiter = '|' if '|' in sample else ','
                    f.seek(0)
                    reader = csv.reader(f, delimiter=delimiter)
                    for row in reader:
                        # ضبط عدد الأعمدة ليكون 7 بالضبط
                        row = row[:7] + [''] * (7 - len(row))
                        data.append(row)
                break # إذا نجح الترميز نخرج من الحلقة
            except UnicodeDecodeError:
                continue
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
        return pd.DataFrame(columns=COLUMNS)

    df = pd.DataFrame(data, columns=COLUMNS)
    
    # حذف السطر الأول إذا كان يحتوي على العناوين
    if len(df) > 0:
        first_row_str = str(df.iloc[0].values)
        if 'Ñèñòåìíûé' in first_row_str or 'sys_id' in first_row_str.lower():
            df = df.iloc[1:]
            
    df = df.fillna('')
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        
    return df

def save_data(df):
    # الحفظ بفاصل | وبدون عناوين للحفاظ على نفس شكل الملف الأصلي
    df.to_csv(DB_FILE, sep='|', index=False, header=False, encoding='utf-8-sig')

# دالة رسم البطاقة
def render_card(row, show_download=True):
    def get_val(key):
        val = str(row.get(key, '')).strip()
        return val if val else '<span class="empty-data">---</span>'
    
    first = str(row.get('first_name', '')).strip()
    last = str(row.get('last_name', '')).strip()
    nick = str(row.get('nickname', '')).strip()
    
    name = f"{first} {last}".strip()
    if not name:
        name = f"@{nick}" if nick else "سجل بيانات"
    
    card_html = f"""
    <div class="intel-card">
        <div class="intel-title">👤 {name}</div>
        <div class="intel-grid">
            <div class="intel-item"><span class="intel-label">الإسم:</span> <span class="intel-value">{get_val('first_name')}</span></div>
            <div class="intel-item"><span class="intel-label">اللقب:</span> <span class="intel-value">{get_val('last_name')}</span></div>
            <div class="intel-item"><span class="intel-label">المعرف (@):</span> <span class="intel-value">{get_val('nickname')}</span></div>
            <div class="intel-item"><span class="intel-label">رقم الهاتف:</span> <span class="intel-value">{get_val('phone')}</span></div>
            <div class="intel-item"><span class="intel-label">User ID:</span> <span class="intel-value">{get_val('user_id')}</span></div>
            <div class="intel-item"><span class="intel-label">الرقم النظامي:</span> <span class="intel-value">{get_val('sys_id')}</span></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    if show_download:
        single_record_df = pd.DataFrame([row])
        csv_data = single_record_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=f"📥 تحميل بيانات هذا الحساب (فقط)",
            data=csv_data,
            file_name=f"leak_{row.get('user_id', 'unknown')}.csv",
            mime="text/csv",
            key=f"dl_{row.get('user_id')}_{time.time()}"
        )
    st.markdown("<br>", unsafe_allow_html=True)

df = load_data()

# ==========================================
# الواجهة الرئيسية
# ==========================================
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 55px; letter-spacing: 2px; text-shadow: 0 0 20px #00ff41; margin-bottom: 10px;'>
            تسريبات تيليغرام
        </h1>
        <h3 style='font-size: 22px; color: #a0a0a0 !important; font-weight: 400; margin-bottom: 30px;'>
            أداة استخباراتية مفتوح المصدر لعرض تسريبات تيليغرام
        </h3>
        <h2 style='font-size: 45px; letter-spacing: 6px; text-shadow: 0 0 25px #00ff41; font-family: "Share Tech Mono", monospace;'>
            DARKNETSAILOR
        </h2>
        <p style='font-size: 16px; color: #00aa33; font-weight: bold;'>بحار الشبكة المظلمة 🌑</p>
    </div>
    <hr style='border-color: #00ff41; margin-bottom: 30px;'>
""", unsafe_allow_html=True)

tab_search, tab_all, tab_add = st.tabs(["🔍 بحث عن حساب", "📁 تصفح التسريبات", "➕ إضافة تسريب جديد"])

# ==========================================
# 1. تبويب البحث
# ==========================================
with tab_search:
    query = st.text_input("🔎 ابحث عن اسم، لقب، رقم هاتف، أو معرف (User_ID):")
    
    if query:
        with st.spinner('جاري فحص السجلات...'):
            time.sleep(0.3)
            search_term = query.strip().lower()
            df_str = df.astype(str).apply(lambda x: x.str.lower())
            mask = df_str.apply(lambda row: row.str.contains(search_term, regex=False).any(), axis=1)
            results = df[mask]
            
        if not results.empty:
            st.success(f"✅ تم العثور على {len(results)} نتيجة.")
            for _, row in results.iterrows():
                render_card(row, show_download=True)
        else:
            st.error(f"❌ لا توجد أي سجلات تطابق: '{query}'")

# ==========================================
# 2. تبويب تصفح التسريبات
# ==========================================
with tab_all:
    total_count = len(df)
    st.markdown(f"<h3 style='text-align: center;'>إجمالي السجلات: <span style='color:#00ff41;'>{total_count:,}</span></h3>", unsafe_allow_html=True)
    st.info("💡 تصفح السجلات ببطاقات أنيقة. التحميل متاح فقط عند البحث.")
    
    if total_count > 0:
        records_per_page = 20
        total_pages = (total_count - 1) // records_per_page + 1
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page_num = st.number_input("الصفحة", min_value=1, max_value=total_pages, value=1, step=1)
        
        start_idx = (page_num - 1) * records_per_page
        end_idx = start_idx + records_per_page
        
        page_df = df.iloc[start_idx:end_idx]
        
        for _, row in page_df.iterrows():
            render_card(row, show_download=False)
    else:
        st.warning("⚠️ قاعدة البيانات فارغة.")

# ==========================================
# 3. تبويب إضافة تسريب جديد
# ==========================================
with tab_add:
    st.subheader("إضافة تسريب جديد إلى قاعدة البيانات")
    with st.form("add_leak_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_first = st.text_input("الاسم الأول")
            new_last = st.text_input("اللقب")
            new_phone = st.text_input("رقم الهاتف")
        with col2:
            new_user_id = st.text_input("معرف المستخدم (User_ID)")
            new_nick = st.text_input("المعرف (Nickname) بدون @")
            new_sys_id = st.text_input("الرقم النظامي (اختياري)")
            
        submit_add = st.form_submit_button("➕ إضافة إلى قاعدة البيانات")
        
        if submit_add:
            if not new_first and not new_nick and not new_phone:
                st.warning("⚠️ يجب إدخال معلومة واحدة على الأقل.")
            else:
                if new_user_id and str(new_user_id) in df['user_id'].values:
                    st.error("❌ هذا الـ User_ID موجود مسبقاً!")
                else:
                    new_row = pd.DataFrame([{
                        'sys_id': new_sys_id, 'first_name': new_first, 'last_name': new_last,
                        'phone': new_phone, 'user_id': new_user_id, 'nickname': new_nick, 'last_seen': ""
                    }])
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.success("✅ تم إضافة البيانات بنجاح!")
                    time.sleep(1)
                    st.rerun()

# ==========================================
# الروابط السفلية
# ==========================================
st.markdown(f"""
    <div class="social-links">
        <p style='color: #e0e0e0; margin-bottom: 15px;'>تابعنا على منصاتنا الرسمية:</p>
        <a href="{TIKTOK_URL}" target="_blank">🎵 تيك توك</a>
        <a href="{YOUTUBE_URL}" target="_blank">▶️ يوتيوب</a>
    </div>
    <p style='text-align:center; color:#004411; margin-top: 20px; font-family: monospace;'>
        System Secured & Powered by Darknetsailor 🛡️
    </p>
""", unsafe_allow_html=True)
