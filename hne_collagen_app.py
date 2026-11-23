"""
HNE : Collagen volume calculator
Run with:  streamlit run hne_collagen_app.py
"""
import streamlit as st

st.title("HNE : Collagen Calculator")

# Main inputs
col_vol_ul = st.number_input("Collagen volume (µL)", min_value=0.0, value=500.0)
ratio = st.number_input("Ratio (collagen : HNE = 1 : N), enter N", min_value=0.0, value=10.0)

# Stock settings (rarely change)
with st.expander("Stock settings"):
    col_conc_mg_ml = st.number_input("Collagen stock (mg/mL)", min_value=0.0, value=3.0)
    col_mw_kda = st.number_input("Collagen MW (kDa)", min_value=1.0, value=300.0)
    hne_mM = st.number_input("HNE stock (mM)", min_value=0.0, value=10.0)

if st.button("Calculate"):
    if col_vol_ul <= 0 or col_conc_mg_ml <= 0 or hne_mM <= 0:
        st.error("Collagen volume, collagen stock, and HNE stock must be greater than 0.")
    else:
        col_uM = col_conc_mg_ml / (col_mw_kda * 1000) * 1e6   # µM
        col_nmol = col_uM * col_vol_ul / 1000                  # nmol
        hne_nmol = ratio * col_nmol                            # nmol
        hne_vol_ul = hne_nmol / hne_mM                         # nmol ÷ mM = µL

        st.write(f"**Add {hne_vol_ul:.2f} µL of HNE stock.**")

        st.text(
            f"Collagen molarity = {col_conc_mg_ml} mg/mL ÷ {col_mw_kda:g} kDa = {col_uM:.3f} µM\n"
            f"Collagen amount   = {col_uM:.3f} µM × {col_vol_ul:g} µL = {col_nmol:.3f} nmol\n"
            f"HNE needed        = {ratio:g} × {col_nmol:.3f} nmol = {hne_nmol:.3f} nmol\n"
            f"HNE volume        = {hne_nmol:.3f} nmol ÷ {hne_mM:g} mM = {hne_vol_ul:.2f} µL"
        )
