import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PDF construction
def tables(df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=3)
    pdf.add_page()

    font_path = os.path.join(BASE_DIR, "DejaVuSans.ttf")  # robust path
    pdf.add_font("DejaVu", style="", fname=font_path)      # fpdf2 syntax, no uni=True
    pdf.set_font("DejaVu", size=10)

    LEFT_X = 10
    RIGHT_X = pdf.w / 2
    Y_START = 2
    CELL_HEIGHT = 8
    ROWS_PER_COLUMN = 4

    col = 0
    row_count = 0

    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df = df.apply(lambda c: c.map(lambda x: str(x).strip() if pd.notnull(x) else ""))  # fixed for pandas 2.x

    for i in range(len(df)):
        if row_count == ROWS_PER_COLUMN:
            if col == 0:
                col = 1
                row_count = 0
            else:
                pdf.add_page()
                col = 0
                row_count = 0

        x_pos = LEFT_X if col == 0 else RIGHT_X
        y_pos = Y_START + (row_count * 70)
        pdf.set_xy(x_pos, y_pos)

        row = df.iloc[i]
        for j in row:
            width = (pdf.w / 2) - 10
            pdf.multi_cell(width, CELL_HEIGHT, str(j), align="L")
            pdf.set_x(x_pos)

        pdf.ln(2)
        row_count += 1

    return bytes(pdf.output())  # in-memory, no disk write

# UI/UX
st.image(os.path.join(BASE_DIR, "logo_image.jpg"), use_container_width=True)
st.title("ADDRESS ORGANIZER")

with st.form(key="Address"):
    data = st.file_uploader("Select your CSV file (Only provide .csv file)", type=["csv"])
    submit = st.form_submit_button("Submit")

if submit:
    if data is not None:
        try:
            df = pd.read_csv(data, encoding="utf-8-sig")
            st.dataframe(df.head(), use_container_width=True)  # preview

            with st.spinner("Generating PDF..."):
                pdf_bytes = tables(df)

            st.success("PDF ready!")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="Delivery Address.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please upload your CSV file")
