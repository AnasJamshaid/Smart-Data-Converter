import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl  # Ensure OpenPyXL is installed for Excel handling

# Set up Modern UI
st.set_page_config(page_title="💿 Data Sweeper", layout='wide', page_icon="🔄")
st.title("💿 Data Sweeper - File Converter")
st.write("🚀 Convert CSV ↔️ Excel | Remove Duplicates | Fill Missing Data | Visualize Your Data Instantly!")

# Mobile Indication Message
if st.session_state.get('is_mobile', False):
    st.markdown(
        """
        <div style="text-align:center; background-color:#ffcc00; padding:10px; border-radius:10px; font-size:18px;">
            📱 **Use the sidebar to upload files** 📂
        </div>
        """, unsafe_allow_html=True
    )

# Sidebar UI
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4228/4228684.png", width=120)
st.sidebar.title("🔧 Data Sweeper Tools")
st.sidebar.markdown("### 📂 Upload Your Files")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)  # Professional icon

# Developer Credit
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Developed By")
st.sidebar.markdown("**Muhammad Ans Jamshaid**")
st.sidebar.markdown("---")

# File Uploader
uploaded_files = st.sidebar.file_uploader(
    "Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True
)

if uploaded_files:
    st.sidebar.success("✅ Files Uploaded Successfully!")
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read File
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            else:
                st.error(f"❌ Unsupported File Type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"❌ Error Loading File: {e}")
            continue

        # Display File Details
        st.sidebar.markdown(f"**📄 File:** `{file.name}`")
        st.sidebar.markdown(f"**📏 Size:** `{file.size / 1024:.2f} KB`")

        # Data Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        enable_cleaning = st.sidebar.checkbox(f"✅ Enable Cleaning for {file.name}")

        if enable_cleaning:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates ({file.name})"):
                    original_shape = df.shape[0]
                    df.drop_duplicates(inplace=True)
                    st.success(f"✅ **Duplicates Removed!** {original_shape - df.shape[0]} duplicates found.")

            with col2:
                if st.button(f"📊 Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ **Missing Values Filled!**")

        # Column Selection
        st.subheader("🎯 Select Columns for Conversion")
        selected_columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        show_charts = st.sidebar.checkbox(f"📈 Show Charts for {file.name}")
        if show_charts:
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion Options
        st.subheader("🔄 File Conversion")
        conversion_type = st.sidebar.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
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

st.sidebar.info("🚀 All Files Processed Successfully!")