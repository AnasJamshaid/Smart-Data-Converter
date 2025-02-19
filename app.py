import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl  
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="💿 Data Sweeper", layout="wide", page_icon="🔄")

# Custom Glassmorphism CSS
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }
        .glass-box {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1, h2, h3 {
            text-align: center;
            font-weight: bold;
        }
        .stButton>button {
            width: 100%;
            padding: 12px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 12px;
            background: #ff416c;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background: #ff4b2b;
        }
        .stDownloadButton>button {
            background: #17c3b2 !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: bold;
        }
        .stDownloadButton>button:hover {
            background: #14a398 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-box">', unsafe_allow_html=True)

# Header
st.markdown("<h1>💿 Data Sweeper - File Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🚀 Convert CSV ↔️ Excel | Remove Duplicates | Fill Missing Data | Visualize Instantly!</p>", unsafe_allow_html=True)
st.markdown("---")

# File Uploader
uploaded_files = st.file_uploader("📂 **Upload Your Files (CSV or Excel):**", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            else:
                st.error(f"❌ Unsupported File Type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"❌ Error Loading File: {e}")
            continue

        # File Info
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 8px;">
                <b>📄 File Name:</b> {file.name} | <b>📏 Size:</b> {file.size / 1024:.2f} KB
            </div>
        """, unsafe_allow_html=True)

        # Data Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        with st.expander(f"⚙️ Data Cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"📊 Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")

        # Select Specific Columns
        st.subheader("🎯 Select Columns for Conversion")
        selected_columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        with st.expander(f"📈 Show Charts for {file.name}"):
            if len(df.select_dtypes(include="number").columns) > 1:
                fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Trend Analysis")
                st.plotly_chart(fig)

        # File Conversion Options
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(label=f"⬇️ Download {file_name}", data=buffer, file_name=file_name, mime=mime_type)

st.markdown('</div>', unsafe_allow_html=True)
st.success("✅ All Files Processed Successfully!")