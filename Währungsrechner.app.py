import streamlit as st
import requests

# --- Seite Konfigurieren ---
st.set_page_config(page_title="Währungsrechner & Budget", page_icon="🌍", layout="wide")

@st.cache_data(ttl=3600)
def get_all_rates(base_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        return data['rates']
    except:
        return None

# --- UI Header ---
st.title("🌍 Universal Währungsrechner & Reiseplaner")
st.write("Berechnen Sie Ihre Wechselkurse und planen Sie Ihr Reisebudget sofort.")

# --- Hauptbereich: Währungsumrechner ---
st.markdown("### 1. Sofort-Währungsrechner")
initial_rates = get_all_rates("USD")

if initial_rates:
    all_currencies = sorted(list(initial_rates.keys()))
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        amount = st.number_input("Betrag:", min_value=0.0, value=1.0, step=1.0, format="%.2f")
    with col2:
        from_curr = st.selectbox("Von:", all_currencies, index=all_currencies.index("USD"))
    with col3:
        to_curr = st.selectbox("Nach:", all_currencies, index=all_currencies.index("EUR"))

    # الحساب اللحظي
    rates = get_all_rates(from_curr)
    if rates:
        rate = rates.get(to_curr)
        conversion_result = amount * rate
        st.metric(label=f"Ergebnis in {to_curr}", value=f"{conversion_result:,.2f}")
        st.info(f"Kurs: 1 {from_curr} = {rate:.4f} {to_curr}")

    st.divider()

    # --- القسم الجديد: حاسبة ميزانية السفر ---
    st.markdown("### 2. Reisebudget-Planer ✈️")
    st.write("Planen Sie Ihre Ausgaben in Ihrer Heimatwährung:")

    col_a, col_b = st.columns(2)
    
    with col_a:
        flight = st.number_input("Flugkosten:", min_value=0.0, value=0.0, step=10.0)
        hotel = st.number_input("Hotel/Unterkunft (Gesamt):", min_value=0.0, value=0.0, step=10.0)
    
    with col_b:
        food = st.number_input("Verpflegung & Aktivitäten:", min_value=0.0, value=0.0, step=10.0)
        others = st.number_input("Sonstige Ausgaben:", min_value=0.0, value=0.0, step=10.0)

    total_home = flight + hotel + food + others
    
    if rates:
        total_dest = total_home * rate
        
        st.markdown("#### **Budget-Zusammenfassung**")
        c1, c2 = st.columns(2)
        c1.metric("Gesamt ({})".format(from_curr), f"{total_home:,.2f}")
        c2.metric("Gesamt ({})".format(to_curr), f"{total_dest:,.2f}", delta_color="inverse")
        
        if total_home > 0:
            st.success(f"Ihr geplantes Budget beträgt ca. **{total_dest:,.2f} {to_curr}**.")

else:
    st.error("Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie Ihr Internet.")

st.divider()
st.caption("Echtzeit-Daten von ExchangeRate-API | Automatische Berechnung")
