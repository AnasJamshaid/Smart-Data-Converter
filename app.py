import streamlit as st
import pandas as pd
import os
from io import BytesIO

# OpenPyXL Fix
import openpyxl  

# Set up Modern UI
st.set_page_config(page_title="💿 Data Sweeper", layout='wide', page_icon="🔄")
st.title("💿 Data Sweeper - File Converter")
st.write("🚀 Convert CSV ↔️ Excel | Remove Duplicates | Fill Missing Data | Visualize Your Data Instantly!")

# File Uploader
uploaded_files = st.file_uploader(
    "📂 Upload Your Files (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read File
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')  # 🛠 Fix for Excel
            else:
                st.error(f"❌ Unsupported File Type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"❌ Error Loading File: {e}")
            continue

        # Display File Details
        st.write(f"📄 **File Name:** `{file.name}` | 📏 **Size:** `{file.size / 1024:.2f} KB`")
        
        # Preview Data
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"✅ Enable Cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ **Duplicates Removed!**")

            with col2:
                if st.button(f"📊 Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ **Missing Values Filled!**")

        # Select Specific Columns
        st.subheader("🎯 Select Columns for Conversion")
        selected_columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Charts for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion Options
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # ✅ Fixed
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"⬇️ Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All Files Processed Successfully!")
