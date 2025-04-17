import streamlit as st
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Analisador SAFT", layout="wide")
# LOGIN SIMPLES
def check_password():
    def password_entered():
        if st.session_state["password"] == "coutinho123":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("❌ Password incorreta")
        st.stop()

check_password()
st.title("📊 Analisador SAFT - Centro de Análise Avançada")

uploaded_files = st.file_uploader(
    "Carrega até 12 ficheiros SAFT (.xml)",
    type="xml",
    accept_multiple_files=True
)

def parse_saft(files):
    registos = []

    for f in files:
        try:
            tree = ET.parse(f)
            root = tree.getroot()

            for inv in root.iter():
                if inv.tag.lower().endswith("invoice"):
                    data = None
                    total = None
                    cliente = None

                    for elem in inv.iter():
                        tag = elem.tag.lower()
                        if tag.endswith("invoicedate"):
                            try:
                                data = datetime.strptime(elem.text.strip(), "%Y-%m-%d").date()
                            except:
                                pass
                        elif tag.endswith("grosstotal"):
                            try:
                                total = float(elem.text.strip())
                            except:
                                pass
                        elif tag.endswith("customertaxid"):
                            cliente = elem.text.strip()

                    if data and total is not None:
                        registos.append({
                            "Data": data,
                            "Cliente": cliente or "Desconhecido",
                            "Total Faturado (€)": total
                        })
        except Exception as e:
            st.warning(f"Erro ao processar {f.name}: {e}")

    return pd.DataFrame(registos)

if uploaded_files:
    if len(uploaded_files) > 12:
        st.error("⚠️ Só podes carregar até 12 ficheiros.")
    else:
        df = parse_saft(uploaded_files)

        if df.empty:
            st.warning("Nenhuma fatura encontrada nos ficheiros carregados.")
        else:
            st.sidebar.header("📌 Seleciona a Análise")
            escolha = st.sidebar.radio("Tipo de análise:", [
                "Totais por Dia",
                "Totais por Cliente",
                "Totais por Mês",
                "Exportar para Excel"
            ])

            if escolha == "Totais por Dia":
                st.subheader("📅 Totais Faturados por Dia")
                df_dia = df.groupby("Data").sum().reset_index()
                st.dataframe(df_dia)
                st.line_chart(df_dia.set_index("Data"))

            elif escolha == "Totais por Cliente":
                st.subheader("👥 Totais por Cliente")
                df_cliente = df.groupby("Cliente").sum().reset_index()
                st.dataframe(df_cliente)
                st.bar_chart(df_cliente.set_index("Cliente"))

            elif escolha == "Totais por Mês":
                st.subheader("🗓️ Totais por Mês")
                df["AnoMes"] = df["Data"].astype("datetime64[ns]").dt.to_period("M").astype(str)
                df_mes = df.groupby("AnoMes").sum().reset_index()
                st.dataframe(df_mes)
                st.bar_chart(df_mes.set_index("AnoMes"))

            elif escolha == "Exportar para Excel":
                st.subheader("📥 Exportação para Excel")
                output = BytesIO()
                df.to_excel(output, index=False, sheet_name="SAFT")
                st.download_button(
                    label="📂 Descarregar Excel",
                    data=output.getvalue(),
                    file_name="analise_saft.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

      
