import streamlit as st 
import pandas as pd
from fpdf import FPDF
import os

# PDF construction
def tables(df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=3)
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=14)
    
    left_x = 10
    right_x = pdf.w / 2
    y_start = 2
    cell_height = 8
    multicell_per_column = 4
    
    col = 0
    row_count = 0
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df = df.map(lambda x: str(x).strip() if pd.notnull(x) else "")
    
    for i in range(len(df)):
        if row_count == multicell_per_column:
            if col == 0:
                col = 1
                row_count = 0
            else:
                pdf.add_page()
                col = 0
                row_count = 0
                
        x_pos = left_x if col == 0 else right_x
        y_pos = y_start + (row_count * 70)
        pdf.set_xy(x_pos, y_pos)
        
        row = df.iloc[i]
        for j in row:
            width = (pdf.w / 2) - 10
            pdf.multi_cell(width, cell_height, str(j), align="L")
            pdf.set_x(x_pos)
            
        pdf.ln(2)   
        row_count += 1

    pdf.output("Delivery Address.pdf")

# UI/UX
st.image("logo_image.jpg", use_container_width=True)
st.title("ADDRESS ORGANIZER")

with st.form(key="Address"):
    data = st.file_uploader("Select your CSV file (Only provide .csv file)", type=["csv"])  # ← changed
    submit = st.form_submit_button("Submit")
    
if submit:
    if data is not None:
        df = pd.read_csv(data)  # ← changed
        tables(df)
        st.write("Uploading Complete")
        st.success("PDF Created: Delivery Address.pdf")

        pdf_path = "Delivery Address.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as files:
                st.download_button(
                    label="Download",
                    data=files,
                    file_name=pdf_path,
                    mime="application/pdf"
                )
        else:
            st.warning("No File Detected....:(")
    else:
        st.warning("Please upload your CSV file")  # ← changed
