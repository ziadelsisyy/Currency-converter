import streamlit as st
import requests

# --- 1. Seite Konfigurieren ---
st.set_page_config(
    page_title="Währungsrechner Pro", 
    page_icon="💰", 
    layout="wide"
)

# قاموس بسيط لربط العملات بالأعلام (يمكنك التوسع فيه)
FLAG_MAP = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "EGP": "🇪🇬", "GBP": "🇬🇧", "JPY": "🇯🇵",
    "SAR": "🇸🇦", "AED": "🇦🇪", "CHF": "🇨🇭", "CAD": "🇨🇦", "AUD": "🇦🇺",
    "CNY": "🇨🇳", "TRY": "🇹🇷", "INR": "🇮🇳", "KWD": "🇰🇼"
}

@st.cache_data(ttl=3600)
def get_all_rates(base_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        return response.json()['rates']
    except:
        return None

# --- 2. Header & Branding ---
# إضافة اسمك في جهة اليمين باستخدام Columns
head1, head2 = st.columns([3, 1])
with head1:
    st.title("🌍 Universal Währungsrechner")
with head2:
    st.write("") # مسافة بادئة
    st.markdown(f"<p style='text-align: right; color: gray; padding-top: 20px;'>Entwickelt von:<br><b>Zeyad Elsisy</b></p>", unsafe_allow_html=True)

st.write("Berechnen Sie Ihre Wechselkurse und planen Sie Ihr Reisebudget mit Echtzeit-Daten.")
st.divider()

# --- 3. Sofort-Währungsrechner ---
st.markdown("### 1. Schnelle Umrechnung 💸")

initial_rates = get_all_rates("USD")
if initial_rates:
    all_currencies = sorted(list(initial_rates.keys()))
    
    # تحسين عرض قائمة العملات لتشمل الأعلام
    def format_func(option):
        flag = FLAG_MAP.get(option, "🏳️")
        return f"{flag} {option}"

    # تنظيم المدخلات في حاوية (Container) جذابة
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            amount = st.number_input("Betrag eingeben:", min_value=0.0, value=100.0, step=10.0)
        
        with c2:
            from_curr = st.selectbox("Von:", all_currencies, index=all_currencies.index("USD"), format_func=format_func)
            
        with c3:
            to_curr = st.selectbox("Nach:", all_currencies, index=all_currencies.index("EUR"), format_func=format_func)

        # الحساب اللحظي
        rates = get_all_rates(from_curr)
        if rates:
            rate = rates.get(to_curr)
            result = amount * rate
            
            # عرض النتيجة بشكل ضخم وواضح
            st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin-top: 10px;">
                    <h2 style="margin: 0; color: #1f77b4;">{result:,.2f} {to_curr}</h2>
                    <p style="margin: 0; color: #555;">1 {from_curr} = {rate:.4f} {to_curr}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- 4. Reisebudget-Planer ---
    st.markdown("### 2. Reisebudget-Planer ✈️")
    
    with st.expander("Budget-Details eingeben", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            flight = st.number_input("✈️ Flugkosten:", min_value=0.0, value=0.0)
            hotel = st.number_input("🏨 Hotel/Unterkunft:", min_value=0.0, value=0.0)
        with col_b:
            food = st.number_input("🍴 Verpflegung:", min_value=0.0, value=0.0)
            others = st.number_input("🎒 Sonstiges:", min_value=0.0, value=0.0)

    total_home = flight + hotel + food + others
    total_dest = total_home * rate

    # عرض النتائج في بطاقات (Metrics)
    st.markdown("#### **Budget-Zusammenfassung**")
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Gesamt ({from_curr})", f"{total_home:,.2f}")
    m2.metric(f"Gesamt ({to_curr})", f"{total_dest:,.2f}")
    
    if total_home > 0:
        share = (total_dest / total_home) if total_home != 0 else 0
        st.info(f"Das entspricht einem Budget von **{total_dest:,.2f} {to_curr}** am Zielort.")

else:
    st.error("Verbindung zum Server fehlgeschlagen. Bitte Internetverbindung prüfen.")

st.caption("© 2024 Zeyad Elsisy | Datenquelle: ExchangeRate-API")
