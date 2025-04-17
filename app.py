import streamlit as st
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
import pandas as pd

st.title("🧾 Analisador de SAFT - Totais por Dia")

uploaded_file = st.file_uploader("Carrega o ficheiro SAFT (.xml)", type="xml")

if uploaded_file:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        # Recolher todas as faturas
        invoices = []
        for elem in root.iter():
            if elem.tag.lower().endswith("invoice"):
                invoices.append(elem)

        # Totais por dia
        totais_por_dia = defaultdict(float)

        for invoice in invoices:
            data_fatura = None
            valor_fatura = None

            for elem in invoice.iter():
                tag = elem.tag.lower()
                if tag.endswith("invoicedate"):
                    try:
                        data_fatura = datetime.strptime(elem.text.strip(), "%Y-%m-%d").date()
                    except:
                        pass
                if tag.endswith("grosstotal"):
                    try:
                        valor_fatura = float(elem.text.strip())
                    except:
                        pass

            if data_fatura and valor_fatura is not None:
                totais_por_dia[data_fatura] += valor_fatura

        # Mostrar resultados
        df = pd.DataFrame(sorted(totais_por_dia.items()), columns=["Data", "Total Faturado (€)"])
        st.subheader("📅 Totais por Dia")
        st.dataframe(df)

        # Gráfico (opcional)
        st.line_chart(df.set_index("Data"))

    except Exception as e:
        st.error(f"Erro ao processar o ficheiro: {e}")
        app.py
        import streamlit as st
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
import pandas as pd

st.title("📂 Analisador de SAFT - Múltiplos ficheiros (até 12)")

uploaded_files = st.file_uploader(
    "Carrega até 12 ficheiros SAFT (.xml)", 
    type="xml", 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 12:
        st.error("⚠️ Só podes carregar até 12 ficheiros.")
    else:
        totais_por_dia = defaultdict(float)

        for f in uploaded_files:
            try:
                tree = ET.parse(f)
                root = tree.getroot()

                invoices = []
                for elem in root.iter():
                    if elem.tag.lower().endswith("invoice"):
                        invoices.append(elem)

                for invoice in invoices:
                    data_fatura = None
                    valor_fatura = None

                    for elem in invoice.iter():
                        tag = elem.tag.lower()
                        if tag.endswith("invoicedate"):
                            try:
                                data_fatura = datetime.strptime(elem.text.strip(), "%Y-%m-%d").date()
                            except:
                                pass
                        if tag.endswith("grosstotal"):
                            try:
                                valor_fatura = float(elem.text.strip())
                            except:
                                pass

                    if data_fatura and valor_fatura is not None:
                        totais_por_dia[data_fatura] += valor_fatura

            except Exception as e:
                st.warning(f"Erro ao processar {f.name}: {e}")

        # Mostrar resultados
        df = pd.DataFrame(sorted(totais_por_dia.items()), columns=["Data", "Total Faturado (€)"])
        st.subheader("📅 Totais Faturados por Dia (todos os ficheiros)")
        st.dataframe(df)
        st.line_chart(df.set_index("Data"))
        