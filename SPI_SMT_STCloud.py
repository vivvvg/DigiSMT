#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:58:41 2024

@author: vivekairmac
"""

import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
def get_client():
    client = MongoClient(st.secrets["db_path"])  # Adjust the connection string as needed
    return client

def get_unique_qrcodes(collection):
    # Fetch unique QR codes from the specified collection
    unique_qrcodes = collection.distinct("2D code")  # Replace 'qrcode' with your actual field name
    return unique_qrcodes

def get_data_by_qrcode(collection, qrcode):
    # Fetch data for a specific QR code
    data = list(collection.find({"2D code": qrcode}))  # Replace 'qrcode' with your actual field name
    return data


# Main app function
def main():
    st.title("DigiSMT - Manufacturing Intelligence for SMT")
    st.header("SPI Station")

    # MongoDB setup
    client = get_client()
    db = client['maindb']  # Replace with your database name
    collection = db['SPI']  # Replace with your collection name

    # Fetch unique QR codes
    unique_qrcodes = get_unique_qrcodes(collection)

    # Dropdown for selecting QR code
    selected_qrcode = st.selectbox("Select a QR Code:", unique_qrcodes)

    if selected_qrcode:
        # Fetch data associated with the selected QR code
        data = get_data_by_qrcode(collection, selected_qrcode)

        if data:
            document = data[0]

            # Display main document fields
            st.write(f"### Details for QR Code: {selected_qrcode}")
            for key, value in document.items():
                if key != "points" and key != "_id":
                    st.write(f"**{key}**: {value}")

            # Display points data
            if "points" in document:
                points_df = pd.DataFrame(document["points"])

                # Filtering options for Judgment result
                judgment_options = points_df["Judgment result"].unique()
                selected_judgment = st.selectbox("Filter by Judgment Result:", ["All"] + list(judgment_options))

                # Filter DataFrame based on selected judgment result
                if selected_judgment != "All":
                    filtered_df = points_df[points_df["Judgment result"] == selected_judgment]
                else:
                    filtered_df = points_df

                # Display the filtered DataFrame
                st.write("### Points Data:")
                st.dataframe(filtered_df)

                # Download button with QR code and selected judgment in filename
                if not filtered_df.empty:
                    csv = filtered_df.to_csv(index=False)
                    # Create filename based on QR code and selected judgment
                    filename_suffix = selected_judgment if selected_judgment != "All" else "All"
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f"{selected_qrcode}_{filename_suffix}.csv",
                        mime="text/csv"
                    )
            else:
                st.write("No points data available.")

        else:
            st.write("No data found for the selected QR code.")

if __name__ == "__main__":
    main()
    
    
    
    
        #         # Prepare data for download
        #     if not filtered_df.empty:
        #         # Create a new DataFrame for download with additional document details
        #         download_df = pd.concat([pd.DataFrame([{
        #             "Line Name": document["Line name"],
        #             "Machine Name": document["Machine Name"],
        #             "Operator name": document["Operator name"],
        #             "Insp program name": document["Insp program name"],
        #             "2D code": document["2D code"],
        #             "Insp pad cnt": document["Insp pad cnt"],
        #             "NG cnt": document["NG cnt"],
        #             "WARN cnt": document["WARN cnt"],
        #         }]), filtered_df], axis=1)

        #         csv = download_df.to_csv(index=False)

        #         # Create filename based on QR code and selected judgment
        #         filename_suffix = selected_judgment if selected_judgment != "All" else "All"
        #         st.download_button(
        #             label="Download Data as CSV",
        #             data=csv,
        #             file_name=f"{selected_qrcode}_{filename_suffix}.csv",
        #             mime="text/csv"
        #         )
        # else:
        #     st.write("No points data available.")