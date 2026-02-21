import streamlit as st
import requests

# --- إعدادات الصفحة (Seite Konfigurieren) ---
st.set_page_config(page_title="Währungsrechner", page_icon="💰", layout="centered")

# --- قائمة العملات (Währungsliste) ---
currencies = {
    "EUR": "Euro (€)",
    "USD": "US-Dollar ($)",
    "EGP": "Ägyptisches Pfund (EGP)",
    "CHF": "Schweizer Franken (CHF)",
    "SAR": "Saudi-Riyal (SAR)",
    "AED": "VAE-Dirham (AED)",
    "KWD": "Kuwait-Dinar (KWD)",
    "RUB": "Russischer Rubel (RUB)",
    "CAD": "Kanadischer Dollar (CAD)",
    "SEK": "Schwedische Krone (SEK)",
    "NOK": "Norwegische Krone (NOK)"
}

st.title("💰 Währungsrechner Pro")
st.write("Wandeln Sie Ihre Währungen in Echtzeit um.")
st.markdown("---")

# --- جلب أسعار الصرف (Wechselkurse abrufen) ---
@st.cache_data(ttl=3600)
def get_exchange_rates(base_currency):
    try:
        # استخدام API لجلب الأسعار الحقيقية
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        return data['rates']
    except:
        return None

# --- واجهة المستخدم (Benutzeroberfläche) ---
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Betrag:", min_value=0.0, value=1.0, step=1.0)
    from_curr = st.selectbox("Von:", list(currencies.keys()), format_func=lambda x: f"{x} - {currencies[x]}")

with col2:
    st.write("") # Platzhalter
    st.write("")
    to_curr = st.selectbox("Nach:", list(currencies.keys()), index=1, format_func=lambda x: f"{x} - {currencies[x]}")

# --- عملية التحويل (Umrechnungsprozess) ---
rates = get_exchange_rates(from_curr)

if rates:
    rate = rates.get(to_curr)
    if rate:
        result = amount * rate
        
        # عرض النتيجة (Ergebnis anzeigen)
        st.success(f"### {amount:,.2f} {from_curr} = {result:,.2f} {to_curr}")
        
        # تفاصيل إضافية
        st.info(f"Aktueller Kurs: 1 {from_curr} = {rate:.4f} {to_curr}")
    else:
        st.error("Fehler bei der Umrechnung.")
else:
    st.error("Verbindungsfehler. Bitte prüfen Sie Ihre Internetverbindung.")

st.divider()
st.caption("Daten bereitgestellt von ExchangeRate-API. Aktualisierung stündlich.")
