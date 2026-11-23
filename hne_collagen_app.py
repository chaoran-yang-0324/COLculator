"""
HNE : Collagen molar ratio calculator
Run with:  streamlit run hne_collagen_app.py
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="HNE : Collagen Calculator", page_icon="🧪")
st.title("🧪 HNE : Collagen Mixing Calculator")
st.caption("Tells you how much HNE stock to add to your collagen to hit a target molar ratio (collagen : HNE = 1 : N).")

# ---------------- Inputs ----------------
st.sidebar.header("Collagen (rat tail)")
col_conc_mg_ml = st.sidebar.number_input("Collagen stock concentration (mg/mL)", min_value=0.0, value=3.0, step=0.1)
col_mw_kda = st.sidebar.number_input("Collagen molecular weight (kDa)", min_value=1.0, value=300.0, step=1.0,
                                     help="Type I collagen triple helix is ~300 kDa.")
col_vol_ul = st.sidebar.number_input("Collagen volume you have (µL)", min_value=0.0, value=500.0, step=50.0)

st.sidebar.header("HNE stock")
hne_unit = st.sidebar.selectbox("HNE stock concentration unit", ["mM", "µM", "M", "mg/mL"])
hne_conc = st.sidebar.number_input(f"HNE stock concentration ({hne_unit})", min_value=0.0, value=10.0, step=0.5)
hne_mw = st.sidebar.number_input("HNE molecular weight (g/mol)", min_value=1.0, value=156.22, step=0.01,
                                 help="4-hydroxynonenal ≈ 156.22 g/mol. Only used if stock is in mg/mL.")

st.header("Target ratio")
preset = st.radio("Collagen : HNE", ["1:5", "1:10", "1:50", "Custom"], horizontal=True)
if preset == "Custom":
    ratio = st.number_input("HNE molecules per collagen molecule (N in 1:N)", min_value=0.0, value=20.0, step=1.0)
else:
    ratio = float(preset.split(":")[1])

# ---------------- Unit conversion ----------------
# Convert HNE stock to mol/L
to_molar = {"M": 1.0, "mM": 1e-3, "µM": 1e-6}
if hne_unit == "mg/mL":
    hne_molar = hne_conc / hne_mw          # mg/mL = g/L -> g/L ÷ g/mol = mol/L
else:
    hne_molar = hne_conc * to_molar[hne_unit]

col_molar = col_conc_mg_ml / (col_mw_kda * 1000)   # g/L ÷ g/mol = mol/L


def calc(n_ratio):
    """Return HNE volume (µL) and final concentrations for a 1:n_ratio mix."""
    col_mol = col_molar * col_vol_ul * 1e-6        # mol collagen
    hne_mol = n_ratio * col_mol                    # mol HNE needed
    hne_vol_ul = hne_mol / hne_molar * 1e6 if hne_molar > 0 else float("nan")
    total_ul = col_vol_ul + hne_vol_ul
    return {
        "Ratio": f"1:{n_ratio:g}",
        "HNE to add (µL)": hne_vol_ul,
        "Total volume (µL)": total_ul,
        "Final collagen (mg/mL)": col_conc_mg_ml * col_vol_ul / total_ul if total_ul else float("nan"),
        "Final HNE (µM)": hne_mol / (total_ul * 1e-6) * 1e6 if total_ul else float("nan"),
        "HNE % of total vol": 100 * hne_vol_ul / total_ul if total_ul else float("nan"),
    }

# ---------------- Output ----------------
if hne_molar <= 0 or col_vol_ul <= 0 or col_conc_mg_ml <= 0:
    st.warning("Enter non-zero collagen concentration, collagen volume, and HNE concentration.")
    st.stop()

r = calc(ratio)
st.metric(f"Add this much HNE stock to {col_vol_ul:g} µL collagen", f"{r['HNE to add (µL)']:.2f} µL")

c1, c2, c3 = st.columns(3)
c1.metric("Total volume", f"{r['Total volume (µL)']:.1f} µL")
c2.metric("Final collagen", f"{r['Final collagen (mg/mL)']:.3f} mg/mL")
c3.metric("Final HNE", f"{r['Final HNE (µM)']:.2f} µM")

# Practical warnings
if r["HNE to add (µL)"] < 0.5:
    st.warning("Under 0.5 µL is hard to pipette accurately — consider diluting your HNE stock first.")
if r["HNE % of total vol"] > 10:
    st.warning(f"HNE is {r['HNE % of total vol']:.1f}% of the final volume — this noticeably dilutes "
               "your collagen. Consider a more concentrated HNE stock. "
               "(If HNE is in ethanol, also check solvent tolerance.)")

st.subheader("All common ratios at once")
df = pd.DataFrame([calc(n) for n in [5, 10, 50] + ([ratio] if preset == "Custom" else [])])
st.dataframe(df.style.format({c: "{:.2f}" for c in df.columns if c != "Ratio"}), hide_index=True)

with st.expander("How the math works"):
    st.markdown(f"""
1. **Collagen molarity** = mass conc. ÷ MW = {col_conc_mg_ml} g/L ÷ {col_mw_kda*1000:,.0f} g/mol
   = **{col_molar*1e6:.3f} µM**
2. **Moles of collagen** = molarity × volume
3. **Moles of HNE needed** = ratio × moles of collagen
4. **HNE volume** = moles of HNE ÷ HNE stock molarity ({hne_molar*1e3:.3f} mM)

Note: the *molar ratio* doesn't change when you add volume — only the final
*concentrations* do. That's why the final concentrations are shown separately.
""")
