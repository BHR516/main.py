import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="مواقع حاويات إعادة التدوير", page_icon="♻️", layout="wide")

# 2. منطق تبديل الوضع (Dark/Light Mode)
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# تحديد ألوان قوية للوضوح التام
if st.session_state.dark_mode:
    bg_color = "#0e1117"
    text_color = "#FFFFFF" # أبيض ناصع
    card_color = "#262730"
    map_style = "carto-darkmatter"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000" # أسود فحم (لضمان الوضوح)
    card_color = "#F0F2F6"
    map_style = "open-street-map"

# 3. تطبيق CSS لإجبار الألوان على الظهور
st.markdown(f"""
    <style>
    /* تغيير خلفية التطبيق ولون الخط الأساسي */
    .stApp {{ 
        background-color: {bg_color} !important; 
        color: {text_color} !important; 
    }}
    
    /* تنسيق اسم المنصة الجديد */
    .main-title {{
        color: #10b981 !important;
        font-weight: bold;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }}

    /* إجبار البطاقات على إظهار النصوص بوضوح */
    .card {{ 
        background-color: {card_color} !important; 
        color: {text_color} !important; 
        padding: 25px; 
        border-radius: 20px; 
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); 
        border-top: 5px solid #10b981; 
        margin-bottom: 20px;
    }}
    
    /* ضمان تلوين كل أنواع النصوص داخل البطاقة */
    .card h3, .card h4, .card p, .card b, .card span {{ 
        color: {text_color} !important; 
    }}

    /* ضمان تلوين النصوص العامة في ستريمليت */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, label {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. الهيدر الجديد
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.markdown('<p class="main-title">📍 مواقع حاويات إعادة التدوير</p>', unsafe_allow_html=True)
with col_toggle:
    st.button("🌙 وضع الليل" if not st.session_state.dark_mode else "☀️ وضع النهار", on_click=toggle_dark_mode)

# 5. البيانات
data = {
    'المنطقة': ['المنامة', 'الرفاع', 'سترة', 'البسيتين', 'مدينة حمد', 'الحد'],
    'الموقع الدقيق': ['بجانب باب البحرين', 'ممشى الاستقلال - البوابة 2', 'خلف مجمع سترة التجاري', 'ساحل البسيتين الجديد', 'دوار 17 - قرب المسجد', 'حديقة الحد الكبرى'],
    'سعة الحاوية': ['5000L', '2000L', '3500L', '5000L', '2500L', '3500L'],
    'المواد': ['بلاستيك، ورق، معدن', 'بلاستيك فقط', 'زجاج، ورق', 'متعدد المواد', 'إلكترونيات', 'كرتون وورق'],
    'آخر إفراغ': ['قبل ساعتين', 'أمس', 'قبل 5 ساعات', 'الآن', 'منذ يومين', 'قبل 3 ساعات'],
    'lat': [26.2361, 26.1300, 26.1547, 26.2550, 26.1150, 26.2490],
    'lon': [50.5831, 50.5550, 50.6070, 50.6750, 50.5050, 50.6480],
    'الامتلاء': [85, 15, 40, 95, 10, 60]
}
df = pd.DataFrame(data)

# 6. لوحة الإحصائيات
st.divider()
st.subheader("📊 حالة النظام المباشرة")
m1, m2, m3, m4 = st.columns(4)
m1.metric("جاهزية الشبكة", "98%")
m2.metric("حاويات ممتلئة", "2")
m3.metric("توفير CO2", "450kg")
m4.metric("المساهمين اليوم", "+342")

# 7. الخريطة والتفاصيل
st.write("---")
c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown("### 🗺️ الخريطة التفاعلية")
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="الامتلاء", color="الامتلاء",
                            color_continuous_scale='RdYlGn_r',
                            hover_name="المنطقة", hover_data=["الموقع الدقيق"],
                            zoom=10, height=550)
    fig.update_layout(mapbox_style=map_style, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🔍 تفاصيل الموقع")
    choice = st.selectbox("اختر المنطقة:", df['المنطقة'])
    row = df[df['المنطقة'] == choice].iloc[0]
    
    st.markdown(f"""
    <div class="card">
        <h3>منطقة {choice}</h3>
        <p>📍 <b>الموقع:</b> {row['الموقع الدقيق']}</p>
        <p>📦 <b>السعة:</b> {row['سعة الحاوية']}</p>
        <p>♻️ <b>المواد:</b> {row['المواد']}</p>
        <p>🕒 <b>آخر إفراغ:</b> {row['آخر إفراغ']}</p>
        <hr>
        <h4 style="margin-bottom:0px;">مستوى الامتلاء:</h4>
        <h2 style='color: {"#ef4444" if row['الامتلاء'] > 80 else "#10b981"}; margin-top:0px;'>{row['الامتلاء']}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 تحديث البيانات"):
        with st.status("جاري الاتصال..."):
            time.sleep(1)
            st.success("تم التحديث!")