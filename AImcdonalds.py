import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="McD HR AI – Demo", layout="wide")

st.title("🍟 McDonald's Hrvatska – AI za brže i sretnije restorane ")
st.markdown("**Napravio bivši crew-ovac Branimir aka Dr. Lobby/Pomfri Kandža (2 godine na flooru). Nisam samo radio u McDonaldsu, I was lovin'it!**")

tab1, tab2, tab3 = st.tabs(["📅 Automatski raspored", "🎓 Trening novaka", "📊 Prognoza gužve"])

# ==================== TAB 1 – RASPORED ====================
with tab1:
    st.header("Automatsko pravljenje rasporeda - općenito napisano za next shift")
    
    col1, col2 = st.columns(2)
    with col1:
        broj_zaposlenih = st.slider("Broj raspoloživih ljudi", 8, 25, 16)
        bolovanja = st.number_input("Broj ljudi na bolovanju", 0, 10, 2)
        st.info(f"Raspoloživo za smjenu: **{broj_zaposlenih - bolovanja}**")
    
    with col2:
        ocekivana_guzva = st.selectbox("Očekivana gužva", ["Normalan dan", "Petak/Subota", "Praznik / Drive-in ludilo"])
        guzva_faktor = {"Normalan dan": 1.0, "Petak/Subota": 1.4, "Praznik / Drive-in ludilo": 1.8}[ocekivana_guzva]
    
    if st.button("Generiraj raspored za sljedeću smjenu", type="primary"):
        potrebno = int(12 * guzva_faktor)
        if (broj_zaposlenih - bolovanja) < potrebno:
            st.error(f"⚠️ FALE TI {potrebno - (broj_zaposlenih - bolovanja)} LJUDI za ovu gužvu!")
        else:
            st.success(f"✅ Imaš dovoljno ljudi – možeš čak i ranije zatvoriti liniju!")
        
        # Lažni raspored
        imena = ["Ana", "Marko", "Luka", "Iva", "Petra", "Ivan", "Maja", "Josip", "Klara", "Dino"]
        random.shuffle(imena)
        raspored = pd.DataFrame({
            "Pozicija": ["Floor kuhinje", "Grill", "Friteza", "Friteza", "Linija 1", "Linija 2", "Drive ", "Kasa 1", "Kasa 2", "Runner"],
            "Ime": imena[:10],
            "Početak": ["14:00"]*4 + ["15:00"]*6,
            "Kraj": ["22:00"]*7 + ["23:00"]*3
        })
        st.dataframe(raspored, use_container_width=True)

# ==================== TAB 2 – TRENING NOVAKA ====================
with tab2:
    st.header("Interaktivni trening novaka – chatbot")
    st.markdown("Primjer: kako se radi Big Mac- ogledno napisano, ne prikazuje pravo slaganje sendviča. Novi bi mogli pitati AI app: sutra radim grill, objasni mi kako se radi?")
    
    if st.button("Pokreni simulaciju treninga"):
        st.write("🤖 **AI trener:** Dobrodošao/la! Danas radimo Big Mac. Spremi se – tajmer kreće za 3… 2… 1… GO!")
        st.progress(0)
        for i in range(1, 76):
            st.progress(i/75)
            if i == 15: st.info("Donji dio peciva + umak  + krastavci + salata + sir")
            if i == 30: st.info("Govedina x2")
            if i == 50: st.info("Srednji dio peciva + umak + zelena salata")
            if i == 65: st.info("Još jedna govedina + završni dio peciva")
            if i == 74: st.info("zamotaj i pošalji ")
        st.success("✅ Gotovo za 75 sekundi – odličan posao! Sljedeći put ciljamo još brže!")

# ==================== TAB 3 – PROGNOZA GUŽVE ====================
with tab3:
    st.header("Prognoza gužve za sljedeći dan")
    
    dani = ["Pon", "Uto", "Sri", "Čet", "Pet", "Sub", "Ned"]
    sati = [f"{h:02d}:00" for h in range(7, 24)]
    podaci = [random.randint(20, 180) for _ in range(17)]
    if st.checkbox("Petak – najveća gužva"):
        podaci = [int(x*1.6) for x in podaci]
    
    df = pd.DataFrame({"Sat": sati, "Broj narudžbi (prognoza)": podaci})
    fig = px.line(df, x="Sat", y="Broj narudžbi (prognoza)", markers=True, title="Prognoza narudžbi po satu")
    st.plotly_chart(fig, use_container_width=True)
    
    max_idx = podaci.index(max(podaci))

    st.warning(f"ŠPICA je u {sati[max_idx]} – pripremi +3 čovjeka na liniji!")
    # Dodaj ovo na kraj tvog app.py (prije footer-a)

tab1, tab2, tab3, tab4 = st.tabs(["Raspored", "Trening", "Prognoza", "Tagalog"])

with tab4:
    st.header("🇵🇭 Tagalog podrška – za crew i menadžere")
    
    izbor = st.radio("Odaberi:", ["Trening za filipinske zaposlenike", "Tutor za hrvatske menadžere"])
    
    if izbor == "Trening za filipinske zaposlenike":
        st.subheader("Paano gumawa ng Big Mac?")
        st.write("1. Lower bun → special sauce → lettuce → onion → beef patty → pickles → cheese")
        st.write("2. Middle bun → sauce → lettuce → onion → beef patty → cheese")
        st.write("3. Top bun → serve with smile 😊")
        st.success("Salamat po! Magaling ka talaga! 🎉")
        
    else:
        st.subheader("Osnovne fraze za menadžere")
        fraze = {
            "Hvala": ("Salamat", "sa-LA-mat"),
            "Molim": ("Pakiusap", "pa-ki-U-sap"),
            "Odličan posao!": ("Magaling!", "ma-GA-ling"),
            "Super si to napravio/la": ("Ang galing mo!", "ang GA-ling mo"),
            "Brže molim te": ("Bilisan mo nga", "bi-LI-san mo nga"),
            "Dobrodošao u tim": ("Maligayang pagdating!", "ma-li-ga-yang pag-da-TING"),
        }
        
        for hr, (tag, izgovor) in fraze.items():
            col1, col2, col3 = st.columns([2,2,3])
            col1.write(f"**{hr}**")
            col2.write(tag)
            col3.write(f"*{izgovor}*")
            
        st.balloons()

