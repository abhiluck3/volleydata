import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# File path
FILE_PATH = 'Abhijit_PVL_Score Sheet Data.xlsx'
SHEET_NAME = 'Sheet1'

# Load data
@st.cache_data
def load_data():
    return pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

# Save data
def save_data(new_data):
    book = load_workbook(FILE_PATH)
    writer = pd.ExcelWriter(FILE_PATH, engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    existing_data = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    updated_data.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    writer.save()

# Streamlit App
st.title("🔵 PVL Score Sheet - Data Entry Form")

# Load columns
data = load_data()
columns = data.columns.tolist()

with st.form("entry_form", clear_on_submit=True):
    st.subheader("Fill the Details Below:")
    form_data = {}
    for col in columns:
        form_data[col] = st.text_input(f"{col}", value="", key=col)
    
    submitted = st.form_submit_button("Submit Entry")
    
    if submitted:
        if all(value.strip() != "" for value in form_data.values()):
            new_row = pd.DataFrame([form_data])
            save_data(new_row)
            st.success("✅ New data entry added successfully!")
            st.dataframe(load_data())
        else:
            st.error("❌ Please fill all fields before submitting.")

st.sidebar.info("Built by Abhishek Jain 💎 | Prime Table Tennis 🏓")