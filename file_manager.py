import pandas as pd
from openpyxl import load_workbook

EXCEL_FILE = 'event_data.xlsx'

def load_sheet(sheet_name):
    return pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

def save_sheet(df, sheet_name):
    book = load_workbook(EXCEL_FILE)
    writer = pd.ExcelWriter(EXCEL_FILE, engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

def add_entry(sheet_name, new_data):
    df = load_sheet(sheet_name)
    updated_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    save_sheet(updated_df, sheet_name)

def update_entry(sheet_name, index, updated_data):
    df = load_sheet(sheet_name)
    for key, value in updated_data.items():
        df.at[index, key] = value
    save_sheet(df, sheet_name)
