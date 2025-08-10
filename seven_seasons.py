import streamlit as st 
import pandas as pd
from fpdf import FPDF
import os

#pdf construction
def tables(x):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font ("Arial", "B", size = 16)
    
    left_x = 10
    right_x = pdf.w/2
    y_start = 10
    cell_hight = 9
    multicell_per_column = 3
    
    col = 0
    row_count = 0
    
    for i in range (len(df)):
        if row_count == multicell_per_column:
            if col == 0:
                col = 1
                row_count = 0
            else:
                pdf.add_page()
                col = 0
                row_count = 0
                
        x_pose = left_x if col == 0 else right_x
        y_pose = y_start + (row_count*90 +5)
        pdf.set_xy(x_pose , y_pose)
            
            
        row = df.iloc[i]
        for j in row:
            width = pdf.w / 2
            pdf.multi_cell(width, cell_hight, str(j), align = "L")
            pdf.set_x(x_pose)
            
        pdf.ln(10)   
        row_count += 1
            
        
            
    pdf.output("Delivery Address.pdf")
        


#UI/UX

st.image("logo_image.jpg" , use_container_width = True)

title = st.title("ADDRESS ORGANIZER")

with st.form(key = "Address"):
    data = st.file_uploader("Select your Excel file")
    submit = st.form_submit_button("Submit")
    
if submit:
    if data is not None:
        df = pd.read_excel(data)
        tables(df)
        st.write("Uploading Complete")
        st.success("PDF Created: Delivery Address.pdf")
    else:
        st.warning("Please upload your Excel file")

        #Download Button
        pdf_path = "Delivery Address.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as files:
                st.downnoad_button(label = ("Download"), data = files, file_name = pdf_path, mime = "application/pdf")
        else:
            st.warning("No File Detected....:(")
                


















