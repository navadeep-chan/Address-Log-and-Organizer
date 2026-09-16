import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import io
import barcode
from barcode.writer import ImageWriter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_barcode_image(code_str):
    """Generates an in-memory PNG barcode without text underneath."""
    code128 = barcode.get_barcode_class('code128')
    writer = ImageWriter()
    
    # Configure writer options to suppress human-readable text and adjust padding
    writer_options = {
        'write_text': False,
        'module_height': 12.0,
        'module_width': 0.25,
        'quiet_zone': 2.0
    }
    
    fp = io.BytesIO()
    code128(code_str, writer=writer).write(fp, options=writer_options)
    fp.seek(0)
    return fp

def tables(df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    font_path = os.path.join(BASE_DIR, "DejaVuSans.ttf")
    pdf.add_font("DejaVu", style="", fname=font_path)
    pdf.set_font("DejaVu", size=9)

    LEFT_X = 10
    RIGHT_X = (pdf.w / 2) + 5
    COLUMN_WIDTH = (pdf.w / 2) - 15
    
    Y_START = 10
    BLOCK_HEIGHT = 92  # Fits 3 blocks comfortably within A4 height (297mm)
    ROWS_PER_COLUMN = 3
    CELL_HEIGHT = 5.5

    col = 0
    row_count = 0

    # Data cleaning
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df = df.apply(lambda c: c.map(lambda x: str(x).strip() if pd.notnull(x) else ""))

    for i in range(len(df)):
        # Page & Column wrap logic: 3 items per column, 2 columns per page
        if row_count == ROWS_PER_COLUMN:
            if col == 0:
                col = 1
                row_count = 0
            else:
                pdf.add_page()
                col = 0
                row_count = 0

        x_pos = LEFT_X if col == 0 else RIGHT_X
        y_pos = Y_START + (row_count * BLOCK_HEIGHT)
        pdf.set_xy(x_pos, y_pos)

        row = df.iloc[i]
        
        # Split address columns from the last barcode column
        address_items = row.iloc[:-1]
        barcode_value = str(row.iloc[-1]).strip()

        # Render address text details
        for val in address_items:
            if val:
                pdf.multi_cell(COLUMN_WIDTH, CELL_HEIGHT, str(val), align="L")
                pdf.set_x(x_pos)

        if barcode_value:
            try:
                barcode_stream = generate_barcode_image(barcode_value)
                
                # Add a 2mm gap below the final line of text
                barcode_y = pdf.get_y() + 2  
                
                barcode_w = 60
                barcode_h = 15
                
                pdf.image(barcode_stream, x=x_pos, y=barcode_y, w=barcode_w, h=barcode_h)
            except Exception:
                pass

        row_count += 1

    return bytes(pdf.output())

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
            st.dataframe(df.head(), use_container_width=True)

            with st.spinner("Generating PDF..."):
                pdf_bytes = tables(df)

            st.success("PDF ready!")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="Delivery_Address.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please upload your CSV file")
