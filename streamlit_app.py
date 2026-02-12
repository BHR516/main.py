import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. إعدادات الصفحة المتقدمة
st.set_page_config(page_title="Bahrain Eco-Smart | تدوير البحرين", page_icon="♻️", layout="wide")

# 2. ميزة الـ Dark Mode الاحترافية (Custom CSS)
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# تطبيق التنسيق بناءً على الوضع المختار
if st.session_state.dark_mode:
    bg_color = "#0e1117"
    text_color = "#ffffff"
    card_color = "#262730"
else:
    bg_color = "#f8fafc"
    text_color = "#1e293b"
    card_color = "#ffffff"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .card {{ background-color: {card_color}; padding: 25px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-top: 5px solid #10b981; margin-bottom: 20px; }}
    .status-badge {{ padding: 5px 12px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }}
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر وزر تبديل الوضع (Dark Mode)
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.title("🇧🇭 المنصة الوطنية لإعادة التدوير")
with col_toggle:
    st.button("🌙 وضع الليل / النهار" if not st.session_state.dark_mode else "☀️ وضع النهار", on_click=toggle_dark_mode)

# 4. قاعدة بيانات "عميقة" للحاويات
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

# 5. عرض لوحة التحكم الذكية
st.divider()
st.subheader("📊 حالة النظام المباشرة")
m1, m2, m3, m4 = st.columns(4)
m1.metric("جاهزية الشبكة", "98%", "🌐")
m2.metric("حاويات ممتلئة", "2", "⚠️")
m3.metric("توفير CO2", "450kg", "🌱")
m4.metric("المساهمين اليوم", "+342", "👤")

# 6. قسم الخريطة والبيانات التفصيلية
st.write("---")
c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown("### 🗺️ التغطية الجغرافية")
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="الامتلاء", color="الامتلاء",
                            color_continuous_scale='Greens' if not st.session_state.dark_mode else 'Viridis',
                            hover_name="المنطقة", hover_data=["الموقع الدقيق", "سعة الحاوية", "المواد"],
                            zoom=10, height=550)
    fig.update_layout(mapbox_style="carto-positron" if not st.session_state.dark_mode else "carto-darkmatter",
                      margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🔍 تفاصيل الحاوية المختارة")
    choice = st.selectbox("اختر الموقع للتفاصيل العميقة:", df['المنطقة'])
    row = df[df['المنطقة'] == choice].iloc[0]
    
    st.markdown(f"""
    <div class="card">
        <h3>منطقة {choice}</h3>
        <p>📍 <b>الموقع:</b> {row['الموقع الدقيق']}</p>
        <p>📦 <b>السعة الإجمالية:</b> {row['سعة الحاوية']}</p>
        <p>♻️ <b>المواد المستهدفة:</b> {row['المواد']}</p>
        <p>🕒 <b>آخر عملية صيانة/إفراغ:</b> {row['آخر إفراغ']}</p>
        <hr>
        <h4>مستوى الامتلاء الحالي:</h4>
        <h2 style='color: {"#ef4444" if row['الامتلاء'] > 80 else "#10b981"}'>{row['الامتلاء']}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 تحديث بيانات الحاوية"):
        with st.status("جاري الاتصال بحساسات الحاوية..."):
            time.sleep(1.5)
            st.write("تم جلب البيانات الحية بنجاح.")
            st.toast("تم التحديث!")

# 7. تذييل الموقع
st.sidebar.title("إعدادات المنصة")
st.sidebar.write(f"المستخدم: {user_name if 'user_name' in locals() else 'أدمن البحرين'}")
if st.sidebar.button("خروج"):
    st.switch_page("streamlit_app.py")