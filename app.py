import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl  # Ensure OpenPyXL is installed for Excel handling

# Set up Modern UI with Dark Theme and Glassmorphism
st.set_page_config(page_title="💿 Data Sweeper", layout='wide', page_icon="🔄")

# Apply Custom CSS for Enhanced Dark Theme and Glassmorphism
st.markdown(
    """
    <style>
        body {
            background-color: #0a0a0a; /* Deeper dark */
            color: #f0f0f0; /* Lighter text */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Modern font */
        }
        .stApp {
            background-color: #0a0a0a;
        }
        .css-1adrfps { /* This class targets the main container */
            background-color: #0a0a0a;
            color: #f0f0f0;
        }
        .stTextInput>label, .stNumberInput>label, .stSelectbox>label, .stMultiSelect>label {
            color: #f0f0f0;
        }
        .css-16idsys p, .css-16idsys div, .css-1adrfps h1, .css-1adrfps h2, .css-1adrfps h3, .css-1adrfps h4, .css-1adrfps h5, .css-1adrfps h6 {
           color: #f0f0f0;
        }
        .sidebar .sidebar-content {
            background-color: rgba(30, 30, 30, 0.5); /* Darker glass */
            backdrop-filter: blur(15px); /* Stronger blur */
            border: 1px solid rgba(255, 255, 255, 0.05); /* Subtle border */
            color: #f0f0f0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Add shadow for depth */
        }
        .streamlit-expanderHeader {
            color: #f0f0f0 !important;
            transition: color 0.3s ease;
        }
        .streamlit-expanderHeader:hover {
            color: #ffffff !important; /* Highlight expander */
        }
        .stButton>button {
            background-color: #222; /* Darker button */
            color: #f0f0f0;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.2s ease; /* Enhanced transition */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stButton>button:active {
            transform: scale(0.95);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); /* Less shadow on press */
        }
        .stDownloadButton>button {
            background-color: #388e3c; /* Darker green */
            color: #f0f0f0;
            border: none;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stDownloadButton>button:active {
            transform: scale(0.95);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        .stAlert {
            background-color: rgba(30, 30, 30, 0.7); /* Opaque alert */
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: #f0f0f0;
            border-radius: 5px; /* Rounded corners */
        }
        .dataframe {
            color: #f0f0f0;
        }
        table {
            color: #f0f0f0;
        }
        .stProgress>div>div>div {
            background-color: #388e3c; /* Green progress bar */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💿 Data Sweeper - File Converter")
st.write("🚀 Convert CSV ↔️ Excel | Remove Duplicates | Fill Missing Data | Visualize Your Data Instantly!")

# File Uploader in the Main Body
st.markdown("### 📂 Upload Your Files")
st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)  # Professional icon
uploaded_files = st.file_uploader(
    "Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True
)

if uploaded_files:
    st.success("✅ Files Uploaded Successfully!")
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
        st.markdown(f"**📄 File:** `{file.name}`")
        st.markdown(f"**📏 Size:** `{file.size / 1024:.2f} KB`")

        # Data Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        enable_cleaning = st.checkbox(f"✅ Enable Cleaning for {file.name}")

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
        show_charts = st.checkbox(f"📈 Show Charts for {file.name}")
        if show_charts:
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

# Sidebar UI
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4228/4228684.png", width=120)
    st.title("🔧 Data Sweeper Tools")

    # Developer Credit (Animated)
    st.markdown("---")
    st.markdown("### 🛠️ Developed By")
    st.markdown("<div style='animation: fadeIn 2s;'>**Muhammad Ans Jamshaid**</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.info("🚀 All Files Processed Successfully!")