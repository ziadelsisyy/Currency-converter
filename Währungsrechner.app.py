import streamlit as st
import requests

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="Multi-Currency Pro", 
    page_icon="💰", 
    layout="wide"
)

# --- 2. قاموس اللغات (Translations) ---
languages = {
    "العربية": {
        "title": "🌍 محول العملات العالمي ومخطط الرحلات",
        "dev_by": "تطوير بواسطة:",
        "calc_title": "1. المحول الفوري",
        "amount": "المبلغ:",
        "from": "من:",
        "to": "إلى:",
        "result": "النتيجة بـ",
        "rate": "سعر الصرف:",
        "budget_title": "2. مخطط ميزانية السفر ✈️",
        "flight": "✈️ تكلفة الطيران:",
        "hotel": "🏨 الفندق/الإقامة:",
        "food": "🍴 الطعام والأنشطة:",
        "others": "🎒 مصاريف أخرى:",
        "summary": "ملخص الميزانية",
        "total": "الإجمالي",
        "footer": "© 2024 زياد السيسي | البيانات من ExchangeRate-API"
    },
    "English": {
        "title": "🌍 Universal Currency Converter & Planner",
        "dev_by": "Developed by:",
        "calc_title": "1. Instant Converter",
        "amount": "Amount:",
        "from": "From:",
        "to": "To:",
        "result": "Result in",
        "rate": "Exchange Rate:",
        "budget_title": "2. Travel Budget Planner ✈️",
        "flight": "✈️ Flight Cost:",
        "hotel": "🏨 Hotel/Accommodation:",
        "food": "🍴 Food & Activities:",
        "others": "🎒 Others:",
        "summary": "Budget Summary",
        "total": "Total",
        "footer": "© 2024 Zeyad Elsisy | Data from ExchangeRate-API"
    },
    "Deutsch": {
        "title": "🌍 Universal Währungsrechner & Planer",
        "dev_by": "Entwickelt von:",
        "calc_title": "1. Sofort-Rechner",
        "amount": "Betrag:",
        "from": "Von:",
        "to": "Nach:",
        "result": "Ergebnis in",
        "rate": "Wechselkurs:",
        "budget_title": "2. Reisebudget-Planer ✈️",
        "flight": "✈️ Flugkosten:",
        "hotel": "🏨 Unterkunft:",
        "food": "🍴 Verpflegung:",
        "others": "🎒 Sonstiges:",
        "summary": "Budget-Zusammenfassung",
        "total": "Gesamt",
        "footer": "© 2024 Zeyad Elsisy | Daten von ExchangeRate-API"
    },
    "Русский": {
        "title": "🌍 Универсальный Конвертер Валют",
        "dev_by": "Разработано:",
        "calc_title": "1. Мгновенный Конвертер",
        "amount": "Сумма:",
        "from": "Из:",
        "to": "В:",
        "result": "Результат в",
        "rate": "Курс обмена:",
        "budget_title": "2. Планировщик Бюджета ✈️",
        "flight": "✈️ Перелет:",
        "hotel": "🏨 Отель/Жилье:",
        "food": "🍴 Питание:",
        "others": "🎒 Прочее:",
        "summary": "Итоговый Бюджет",
        "total": "Итого",
        "footer": "© 2024 Зияд Эльсиси | Данные от ExchangeRate-API"
    }
}

# --- 3. اختيار اللغة في الشريط الجانبي أو الأعلى ---
col_lang_1, col_lang_2 = st.columns([3, 1])
with col_lang_2:
    selected_lang = st.selectbox("🌐 Language / اللغة", list(languages.keys()))

# تفعيل النصوص بناءً على اللغة المختارة
txt = languages[selected_lang]

# ضبط اتجاه النص للعربية
if selected_lang == "العربية":
    st.markdown("""<style> body { text-align: right; direction: rtl; } </style>""", unsafe_allow_html=True)

# --- 4. جلب البيانات ---
@st.cache_data(ttl=3600)
def get_all_rates(base_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        return requests.get(url).json()['rates']
    except: return None

# --- 5. Header & Branding ---
h1, h2 = st.columns([3, 1])
with h1:
    st.title(txt["title"])
with h2:
    st.markdown(f"<p style='text-align: right; color: #007bff; font-weight: bold;'>{txt['dev_by']}<br>Zeyad Elsisy</p>", unsafe_allow_html=True)

# --- 6. المحول الفوري ---
st.markdown(f"### {txt['calc_title']}")

FLAG_MAP = {"USD": "🇺🇸", "EUR": "🇪🇺", "EGP": "🇪🇬", "GBP": "🇬🇧", "JPY": "🇯🇵", "RUB": "🇷🇺", "SAR": "🇸🇦", "AED": "🇦🇪"}

initial_rates = get_all_rates("USD")
if initial_rates:
    all_currencies = sorted(list(initial_rates.keys()))
    
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: amount = st.number_input(txt["amount"], min_value=0.0, value=100.0)
        with c2: from_curr = st.selectbox(txt["from"], all_currencies, index=all_currencies.index("USD"), format_func=lambda x: f"{FLAG_MAP.get(x, '🏳️')} {x}")
        with c3: to_curr = st.selectbox(txt["to"], all_currencies, index=all_currencies.index("EUR"), format_func=lambda x: f"{FLAG_MAP.get(x, '🏳️')} {x}")

        rates = get_all_rates(from_curr)
        if rates:
            rate = rates.get(to_curr)
            res = amount * rate
            st.success(f"### {res:,.2f} {to_curr}")
            st.caption(f"{txt['rate']} 1 {from_curr} = {rate:.4f} {to_curr}")

    st.divider()

    # --- 7. ميزانية السفر ---
    st.markdown(f"### {txt['budget_title']}")
    col_a, col_b = st.columns(2)
    with col_a:
        f_cost = st.number_input(txt["flight"], min_value=0.0)
        h_cost = st.number_input(txt["hotel"], min_value=0.0)
    with col_b:
        food_cost = st.number_input(txt["food"], min_value=0.0)
        o_cost = st.number_input(txt["others"], min_value=0.0)

    total_h = f_cost + h_cost + food_cost + o_cost
    total_d = total_h * rate

    st.markdown(f"#### **{txt['summary']}**")
    m1, m2 = st.columns(2)
    m1.metric(f"{txt['total']} ({from_curr})", f"{total_h:,.2f}")
    m2.metric(f"{txt['total']} ({to_curr})", f"{total_d:,.2f}")

st.divider()
st.caption(txt["footer"])
