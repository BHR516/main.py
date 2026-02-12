import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="مواقع حاويات إعادة التدوير", page_icon="♻️", layout="wide")

# 2. إدارة وضع الليل والنهار
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

if st.session_state.dark_mode:
    bg_color, text_color, card_color, map_style = "#0e1117", "#FFFFFF", "#262730", "carto-darkmatter"
else:
    bg_color, text_color, card_color, map_style = "#FFFFFF", "#000000", "#F0F2F6", "open-street-map"

# 3. تطبيق التنسيق (CSS) لإظهار الأرقام والحروف بوضوح
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    [data-testid="stMetricValue"] {{ color: {text_color} !important; font-weight: bold !important; }}
    h1, h2, h3, h4, p, span, label {{ color: {text_color} !important; }}
    .card {{ 
        background-color: {card_color} !important; 
        color: {text_color} !important; 
        padding: 20px; border-radius: 15px; border-top: 5px solid #10b981; margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. قاعدة البيانات المطورة (مع ساعات العمل)
data = {
    'المنطقة': ['المنامة', 'الرفاع', 'سترة', 'البسيتين', 'مدينة حمد', 'الحد'],
    'تفتح': ['08:00 AM', '09:00 AM', '07:00 AM', '24 ساعة', '08:00 AM', '06:00 AM'],
    'تغلق': ['10:00 PM', '09:00 PM', '08:00 PM', '-', '11:00 PM', '09:00 PM'],
    'المواد المطلوبة': ['بلاستيك، ورق', 'بلاستيك فقط', 'معدن، زجاج', 'جميع المواد', 'إلكترونيات', 'كرتون'],
    'تاريخ الإفراغ': ['اليوم 10:00 AM', 'أمس 04:00 PM', 'اليوم 07:00 AM', 'اليوم 12:00 PM', 'منذ يومين', 'أمس 09:00 PM'],
    'lat': [26.2361, 26.1300, 26.1547, 26.2550, 26.1150, 26.2490],
    'lon': [50.5831, 50.5550, 50.6070, 50.6750, 50.5050, 50.6480],
    'الامتلاء': [85, 40, 60, 95, 20, 70],
    'الشعار': ['♻️']*6
}
df = pd.DataFrame(data)

# 5. الهيدر
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.title("📍 مواقع حاويات إعادة التدوير")
with col_toggle:
    st.button("🌙" if not st.session_state.dark_mode else "☀️", on_click=toggle_dark_mode)

# 6. الخريطة المطورة (تكبير الدوائر وإضافة التفاصيل)
st.write("---")
c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown("### 🗺️ الخريطة التفاعلية")
    # تم إلغاء ربط الحجم بالامتلاء لجعل كل الدوائر "كبيرة وواضحة" (Size=25)
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", 
                            color="الامتلاء",
                            color_continuous_scale='RdYlGn_r',
                            hover_name="المنطقة",
                            # إضافة التفاصيل الجديدة في الـ Hover
                            hover_data={
                                'lat': False, 'lon': False, 'الامتلاء': True,
                                'تفتح': True, 'تغلق': True, 'المواد المطلوبة': True, 'تاريخ الإفراغ': True
                            },
                            zoom=10, height=600)
    
    # تكبير الدوائر بشكل ثابت (Update Marker Size)
    fig.update_traces(marker={'size': 25, 'opacity': 0.8})
    
    fig.update_layout(mapbox_style=map_style, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🔍 بطاقة المعلومات التفصيلية")
    choice = st.selectbox("اختر الحاوية:", df['المنطقة'])
    row = df[df['المنطقة'] == choice].iloc[0]
    
    st.markdown(f"""
    <div class="card">
        <h2 style='text-align: center;'>♻️ {choice}</h2>
        <hr>
        <p>⏰ <b>ساعات العمل:</b> من {row['تفتح']} إلى {row['تغلق']}</p>
        <p>📋 <b>المواد المطلوبة:</b> {row['المواد المطلوبة']}</p>
        <p>🚛 <b>آخر موعد إفراغ:</b> {row['تاريخ الإفراغ']}</p>
        <p>📊 <b>حالة الامتلاء الحالية:</b></p>
        <h1 style='text-align: center; color: {"#ef4444" if row['الامتلاء'] > 80 else "#10b981"} !important;'>{row['الامتلاء']}%</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 تحديث البيانات الميدانية"):
        with st.status("جاري جلب البيانات من حساسات البحرين..."):
            time.sleep(1)
            st.success("تم التحديث!")