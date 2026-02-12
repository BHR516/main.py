# تطبيق التنسيق الجمالي مع التركيز على إظهار الأرقام
st.markdown(f"""
    <style>
    /* تغيير خلفية التطبيق ولون الخط الأساسي */
    .stApp {{ 
        background-color: {bg_color} !important; 
        color: {text_color} !important; 
    }}
    
    /* هذا الجزء هو السر لإظهار الأرقام (Metrics) */
    [data-testid="stMetricValue"] {{
        color: {text_color} !important;
        font-weight: bold !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {text_color} !important;
    }}

    /* إجبار البطاقات والنصوص على الوضوح */
    .card {{ 
        background-color: {card_color} !important; 
        color: {text_color} !important; 
        padding: 25px; 
        border-radius: 20px; 
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); 
        border-top: 5px solid #10b981; 
        margin-bottom: 20px;
    }}
    
    .card h3, .card h4, .card p, .card b, .card span {{ 
        color: {text_color} !important; 
    }}

    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, label {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)