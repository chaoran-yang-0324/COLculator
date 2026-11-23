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
    col_conc_mg_ml = st.number_input("Collagen concentration (mg/mL = µg/µL)", min_value=0.0, value=3.0)
    col_mw = st.number_input("Collagen molar mass (g/mol)", min_value=1.0, value=300000.0)
    hne_conc_mg_ml = st.number_input("HNE concentration (mg/mL = µg/µL)", min_value=0.0, value=1.0)
    hne_mw = st.number_input("HNE molar mass (g/mol)", min_value=1.0, value=156.22)

if st.button("Calculate"):
    if col_vol_ul <= 0 or col_conc_mg_ml <= 0 or hne_conc_mg_ml <= 0:
        st.error("Collagen volume and both concentrations must be greater than 0.")
    else:
        col_uM = col_conc_mg_ml / col_mw * 1e6                # µM
        hne_mM = hne_conc_mg_ml / hne_mw * 1000                # mM
        col_nmol = col_uM * col_vol_ul / 1000                  # nmol
        hne_nmol = ratio * col_nmol                            # nmol
        hne_vol_ul = hne_nmol / hne_mM                         # nmol ÷ mM = µL

        st.write(f"**Add {hne_vol_ul:.2f} µL of HNE stock.**")

        st.text(
            f"Collagen molarity = {col_conc_mg_ml:g} mg/mL ÷ {col_mw:g} g/mol = {col_uM:.3f} µM\n"
            f"HNE molarity      = {hne_conc_mg_ml:g} mg/mL ÷ {hne_mw:g} g/mol = {hne_mM:.3f} mM\n"
            f"Collagen amount   = {col_uM:.3f} µM × {col_vol_ul:g} µL = {col_nmol:.3f} nmol\n"
            f"HNE needed        = {ratio:g} × {col_nmol:.3f} nmol = {hne_nmol:.3f} nmol\n"
            f"HNE volume        = {hne_nmol:.3f} nmol ÷ {hne_mM:g} mM = {hne_vol_ul:.2f} µL"
        )
