import os
import pandas as pd

from library.library_db import Reader

#Part responsible for readers
readers_path = "./library/data/readers.xlsx"
readers_columns = ["ID", "Name", "Surname", "Phone", "City", "Street", "Apartment", "Postal Code"]

"""
Pandas readers =====
"""

def prepare_readers_file():
    os.makedirs("./library/data", exist_ok=True)
    if not os.path.exists(readers_path):
        df = pd.DataFrame(columns=readers_columns)
        df.to_excel(readers_path, index=False)

def load_readers():
    prepare_readers_file()
    return pd.read_excel(readers_path)

def load_readers_object():
    df = load_readers()
    return [Reader.from_dict(row) for _, row in df.iterrows()]

def add_reader(reader: Reader):
    df = load_readers()
    new_id = 1 if df.empty else int(df["ID"].max()) + 1
    reader._Reader__id = new_id
    Reader._Reader__readerID = new_id
    df = pd.concat([df, pd.DataFrame([reader.to_dict()])], ignore_index=True)
    df.to_excel(readers_path, index=False)

def remove_reader(reader_id: int):
    df = load_readers()
    df = df[df["ID"] != reader_id]
    df.to_excel(readers_path, index=False)

def edit_reader(reader_id: int, updated_reader: Reader):
    df = load_readers()
    if reader_id in df["ID"].values:
        df.loc[df["ID"] == reader_id, ["Name", "Surname", "Phone", "City", "Street", "Apartment", "Postal Code"]] = [
            updated_reader.name,
            updated_reader.surname,
            updated_reader.phone_num,
            updated_reader.address.city if updated_reader.address else "",
            updated_reader.address.street if updated_reader.address else "",
            updated_reader.address.apartment if updated_reader.address else "",
            updated_reader.address.postal_code if updated_reader.address else ""
        ]
        df.to_excel(readers_path, index=False)
    else:
        return(f"No reader with ID {reader_id}.")

def search_reader(query: str):
    df = load_readers()
    query = query.lower()
    mask = (
        df["Name"].str.lower().str.contains(query) |
        df["Surname"].str.lower().str.contains(query) |
        df["Phone"].astype(str).str.contains(query)
    )
    return df[mask]