"""
CDR Intelligence Platform v2.0
Professional Call Detail Record Analysis System
Full-Featured Streamlit Cloud Version
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import re
import requests
import folium
from streamlit_folium import st_folium

# Optional imports with error handling - show warnings only once
REPORTLAB_AVAILABLE = False
PDFPLUMBER_AVAILABLE = False
PYPDF2_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CDR Intelligence Platform",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS STYLING - CLEAN LIGHT THEME WITH EXCELLENT CONTRAST
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Reset and Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1a1a1a;
    line-height: 1.6;
}

/* Main Container */
.main .block-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] * {
    color: #1a1a1a !important;
}

/* Typography */
h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 1rem;
    text-align: center;
}

h2 {
    font-size: 1.75rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 2rem 0 1.5rem 0;
}

h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 1rem;
}

/* Cards */
.hero-section {
    background: #ffffff;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.content-section {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

.form-section {
    background: #f9fafb;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 2rem;
}

.form-section h3 {
    color: #2563eb;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

/* Metrics */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-card {
    background: #ffffff;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.metric-card:hover {
    border-color: #2563eb;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
}

.metric-card .label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.metric-card .value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1a1a1a;
}

.metric-card .value.primary { color: #2563eb; }
.metric-card .value.success { color: #059669; }
.metric-card .value.danger { color: #dc2626; }

/* Alerts */
.alert {
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    font-weight: 500;
    border-left: 4px solid;
}

.alert-info {
    background: #eff6ff;
    border-left-color: #2563eb;
    color: #1e40af;
}

.alert-success {
    background: #f0fdf4;
    border-left-color: #059669;
    color: #065f46;
}

.alert-error {
    background: #fef2f2;
    border-left-color: #dc2626;
    color: #991b1b;
}

/* Form Elements */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 2px solid #d1d5db !important;
    border-radius: 6px !important;
    color: #1a1a1a !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #2563eb !important;
}

.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 2px solid #d1d5db !important;
    border-radius: 6px !important;
    color: #1a1a1a !important;
    padding: 0.75rem !important;
    font-size: 0.95rem !important;
}

.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
}

/* Buttons */
.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.stButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
}

.stDownloadButton > button {
    background: #059669 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.stDownloadButton > button:hover {
    background: #047857 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25) !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: #f9fafb !important;
    border: 2px dashed #d1d5db !important;
    border-radius: 8px !important;
    padding: 2rem !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #2563eb !important;
    background: #eff6ff !important;
}

/* Tables */
.dataframe {
    background: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #e5e7eb !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.dataframe thead th {
    background: #f9fafb !important;
    color: #374151 !important;
    font-weight: 600 !important;
    padding: 1rem 0.75rem !important;
    border-bottom: 2px solid #e5e7eb !important;
}

.dataframe tbody td {
    background: #ffffff !important;
    color: #1a1a1a !important;
    padding: 0.75rem !important;
    border-bottom: 1px solid #f3f4f6 !important;
}

.dataframe tbody tr:hover td {
    background: #f9fafb !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 6px !important;
    color: #374151 !important;
    font-weight: 600 !important;
}

.streamlit-expanderContent {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-top: none !important;
}

/* Radio */
.stRadio > div {
    background: #f9fafb !important;
    border-radius: 6px !important;
    padding: 1rem !important;
    border: 1px solid #e5e7eb !important;
}

.stRadio > div > label {
    color: #374151 !important;
    font-weight: 500 !important;
}

/* Responsive */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }
    
    .form-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .metrics-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }
    
    h1 {
        font-size: 2rem;
    }
    
    .hero-section {
        padding: 2rem 1rem;
    }
}

/* Text Colors for Better Contrast */
p {
    color: #374151;
}

.stMarkdown {
    color: #1a1a1a;
}

/* Sidebar specific styling */
[data-testid="stSidebar"] .stMarkdown {
    color: #1a1a1a !important;
}

[data-testid="stSidebar"] h3 {
    color: #1a1a1a !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

EXPECTED_COLUMNS = {
    "date": ["date", "call date", "calldate", "day"],
    "time": ["time", "call time", "calltime", "start time"],
    "duration": ["duration", "dur", "seconds", "secs", "call duration"],
    "number": ["number", "phone", "called number", "destination", "to", "from"],
    "type": ["type", "call type", "direction", "incoming", "outgoing"],
}

def detect_column(df_cols, hints):
    df_lower = {c.lower().strip(): c for c in df_cols}
    for hint in hints:
        if hint in df_lower:
            return df_lower[hint]
    return None

def auto_map_columns(df):
    mapping = {}
    for key, hints in EXPECTED_COLUMNS.items():
        col = detect_column(list(df.columns), hints)
        if col:
            mapping[key] = col
    return mapping

def parse_duration_to_seconds(series):
    def _parse(val):
        if pd.isna(val) or val == '' or val is None:
            return 0
        
        s = str(val).strip().lower()
        if s == '' or s == '0' or s == 'nan':
            return 0
            
        # Handle MM:SS or HH:MM:SS format
        if re.match(r"^\d+:\d{2}(:\d{2})?$", s):
            parts = list(map(int, s.split(":")))
            if len(parts) == 3:  # HH:MM:SS
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:  # MM:SS
                return parts[0] * 60 + parts[1]
        
        # Handle text formats like "5 min", "30 sec", "1 hr"
        if 'hr' in s or 'hour' in s:
            nums = re.findall(r'\d+', s)
            if nums:
                return int(nums[0]) * 3600
        elif 'min' in s:
            nums = re.findall(r'\d+', s)
            if nums:
                return int(nums[0]) * 60
        elif 'sec' in s or 's' == s[-1:]:
            nums = re.findall(r'\d+', s)
            if nums:
                return int(nums[0])
        
        # Handle plain numbers (assume seconds)
        try:
            return max(0, float(s))
        except:
            return 0
    
    return series.apply(_parse)

def seconds_to_hms(seconds):
    if pd.isna(seconds) or seconds < 0:
        return "0s"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"

def load_file(uploaded_file):
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file, encoding="utf-8", on_bad_lines="skip")
        elif name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
        elif name.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8", errors="replace")
            for sep in [",", "\t", "|", ";"]:
                try:
                    df = pd.read_csv(io.StringIO(content), sep=sep)
                    if len(df.columns) > 1:
                        return df
                except:
                    continue
        elif name.endswith(".pdf"):
            if not PDFPLUMBER_AVAILABLE and not PYPDF2_AVAILABLE:
                st.error("❌ PDF processing libraries not available. Please upload CSV or Excel files instead.")
                st.info("💡 **Alternative options:**")
                st.info("• Convert PDF to CSV using online tools")
                st.info("• Export data from your carrier's portal as CSV/Excel")
                st.info("• Use Adobe Acrobat's export feature")
                return None
                
            st.info("🔄 Extracting data from PDF... This may take a moment.")
            
            # Method 1: Advanced pdfplumber with better table detection
            if PDFPLUMBER_AVAILABLE:
                try:
                    uploaded_file.seek(0)
                    all_tables = []
                    all_text_data = []
                    
                    with pdfplumber.open(uploaded_file) as pdf:
                        st.info(f"📄 Processing {len(pdf.pages)} pages...")
                        
                        for i, page in enumerate(pdf.pages):
                            # Extract tables with better settings
                            table_settings = {
                                "vertical_strategy": "lines_strict",
                                "horizontal_strategy": "lines_strict",
                                "snap_tolerance": 3,
                                "join_tolerance": 3,
                                "edge_min_length": 3,
                                "min_words_vertical": 3,
                                "min_words_horizontal": 1,
                                "intersection_tolerance": 3,
                            }
                            
                            tables = page.extract_tables(table_settings)
                            if tables:
                                st.info(f"✓ Page {i+1}: Found {len(tables)} structured table(s)")
                                all_tables.extend(tables)
                            
                            # Also extract text for pattern matching
                            page_text = page.extract_text()
                            if page_text:
                                all_text_data.append(page_text)
                    
                    # Process structured tables first (most accurate)
                    if all_tables:
                        for table_idx, table in enumerate(all_tables):
                            if table and len(table) > 1:
                                try:
                                    # Better header cleaning
                                    headers = []
                                    for i, h in enumerate(table[0]):
                                        if h and str(h).strip():
                                            clean_header = str(h).strip().replace('\n', ' ').replace('\r', '')
                                            headers.append(clean_header)
                                        else:
                                            headers.append(f"Column_{i+1}")
                                    
                                    # Create DataFrame with better data cleaning
                                    rows = []
                                    for row in table[1:]:
                                        clean_row = []
                                        for cell in row:
                                            if cell is not None:
                                                clean_cell = str(cell).strip().replace('\n', ' ').replace('\r', '')
                                                clean_row.append(clean_cell if clean_cell else None)
                                            else:
                                                clean_row.append(None)
                                        rows.append(clean_row)
                                    
                                    df = pd.DataFrame(rows, columns=headers)
                                    
                                    # Remove completely empty rows and columns
                                    df = df.dropna(how='all').dropna(axis=1, how='all')
                                    
                                    # Validate if this looks like call data
                                    if len(df) > 0 and len(df.columns) >= 3:
                                        # Check for call-related keywords in headers
                                        header_text = ' '.join(headers).lower()
                                        call_keywords = ['phone', 'number', 'call', 'time', 'date', 'duration', 'contact']
                                        
                                        if any(keyword in header_text for keyword in call_keywords):
                                            st.success(f"✅ Extracted {len(df)} rows from structured table {table_idx + 1}")
                                            return df
                                        
                                        # Check data content for phone numbers
                                        sample_text = df.to_string().lower()
                                        if re.search(r'\d{10,15}', sample_text):
                                            st.success(f"✅ Extracted {len(df)} rows from table {table_idx + 1} (detected phone data)")
                                            return df
                                            
                                except Exception as e:
                                    st.warning(f"Table {table_idx + 1} parsing issue: {str(e)}")
                                    continue
                    
                    # Method 2: Enhanced text extraction and pattern matching
                    if all_text_data:
                        full_text = '\n'.join(all_text_data)
                        st.info(f"📝 Analyzing {len(full_text)} characters of extracted text")
                        
                        # Try structured text parsing first
                        lines = full_text.split('\n')
                        records = []
                        
                        # Enhanced regex patterns for better accuracy
                        patterns = {
                            'phone': r'(?:\+?1[-.\s]?)?(?:\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}|\d{10,15})',
                            'date': r'(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|\w{3}\s+\d{1,2},?\s+\d{4})',
                            'time': r'(?:\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AaPp][Mm])?)',
                            'duration': r'(?:\d{1,3}:\d{2}(?::\d{2})?|\d+\s?(?:sec|min|hr|hour|minute|second)s?|\d+)',
                            'amount': r'(?:\$?\d+\.?\d*)'
                        }
                        
                        # Look for header-like lines
                        potential_headers = []
                        for line in lines[:20]:  # Check first 20 lines for headers
                            line = line.strip()
                            if line and any(keyword in line.lower() for keyword in ['date', 'time', 'number', 'duration', 'call', 'phone']):
                                potential_headers.append(line)
                        
                        # Process each line for call records
                        for line_num, line in enumerate(lines):
                            line = line.strip()
                            if len(line) < 15:  # Skip very short lines
                                continue
                            
                            # Extract all pattern matches
                            phones = re.findall(patterns['phone'], line)
                            dates = re.findall(patterns['date'], line)
                            times = re.findall(patterns['time'], line)
                            durations = re.findall(patterns['duration'], line)
                            amounts = re.findall(patterns['amount'], line)
                            
                            # Determine call type with better accuracy
                            call_type = "Unknown"
                            line_lower = line.lower()
                            if any(word in line_lower for word in ['incoming', 'inbound', 'received', 'answered']):
                                call_type = "Incoming"
                            elif any(word in line_lower for word in ['outgoing', 'outbound', 'dialed', 'made']):
                                call_type = "Outgoing"
                            elif any(word in line_lower for word in ['missed', 'unanswered', 'declined']):
                                call_type = "Missed"
                            elif any(word in line_lower for word in ['sms', 'text', 'message']):
                                call_type = "SMS"
                            
                            # Only create record if we have essential data
                            if phones and (dates or times):
                                # Clean and validate phone number
                                phone = phones[0]
                                # Remove common formatting
                                clean_phone = re.sub(r'[^\d+]', '', phone)
                                
                                # Skip if phone number seems invalid
                                if len(clean_phone) < 10:
                                    continue
                                
                                record = {
                                    'Phone_Number': phone,
                                    'Date': dates[0] if dates else '',
                                    'Time': times[0] if times else '',
                                    'Duration': durations[0] if durations else '0',
                                    'Call_Type': call_type,
                                    'Amount': amounts[0] if amounts else '',
                                    'Line_Number': line_num + 1,
                                    'Raw_Text': line
                                }
                                records.append(record)
                        
                        # Create DataFrame if we found enough records
                        if len(records) >= 3:  # Require at least 3 records for reliability
                            df = pd.DataFrame(records)
                            
                            # Data quality validation
                            valid_phones = df['Phone_Number'].apply(lambda x: len(re.sub(r'[^\d]', '', str(x))) >= 10).sum()
                            phone_accuracy = valid_phones / len(df) * 100
                            
                            st.success(f"✅ Extracted {len(df)} call records using advanced pattern matching")
                            st.info(f"📊 Data Quality: {phone_accuracy:.1f}% valid phone numbers detected")
                            
                            # Show sample of extracted data for verification
                            with st.expander("📋 Sample Extracted Data (for verification)", expanded=False):
                                st.dataframe(df.head(10))
                            
                            return df
                        else:
                            st.warning(f"⚠️ Only found {len(records)} potential call records - may not be sufficient for analysis")
                    
                    st.error("❌ Could not extract structured call data from PDF")
                    st.info("💡 **Tips for better PDF extraction:**")
                    st.info("• Ensure PDF contains structured tables, not scanned images")
                    st.info("• Try converting PDF to Excel/CSV format first")
                    st.info("• Check if PDF is password protected")
                    
                except Exception as e:
                    st.error(f"PDF processing error: {str(e)}")
                    st.info("💡 Try uploading the file as CSV or Excel instead")
            
            # Fallback to PyPDF2 if pdfplumber fails
            elif PYPDF2_AVAILABLE:
                try:
                    uploaded_file.seek(0)
                    reader = PyPDF2.PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    
                    if text.strip():
                        st.info("📝 Extracted text from PDF, attempting to parse...")
                        # Simple text parsing logic here
                        lines = text.split('\n')
                        # Basic parsing - you can enhance this
                        st.warning("⚠️ Basic PDF text extraction - results may vary")
                        st.text_area("Extracted Text (first 1000 chars)", text[:1000])
                    else:
                        st.error("❌ No text could be extracted from PDF")
                        
                except Exception as e:
                    st.error(f"PyPDF2 processing error: {str(e)}")
            
            return None
        
        return None
    except Exception as e:
        st.error(f"File loading error: {str(e)}")
        return None

def clean_layout(fig, title=""):
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f9fafb",
        font=dict(color="#1a1a1a", family="Inter"),
        title_text=title,
        title_font=dict(size=16, color="#1a1a1a"),
        margin=dict(t=50, b=30, l=20, r=20),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e5e5e5", linecolor="#d1d5db")
    fig.update_yaxes(showgrid=True, gridcolor="#e5e5e5", linecolor="#d1d5db")
    return fig

def generate_pdf_report(results, filename):
    if not REPORTLAB_AVAILABLE:
        st.error("❌ PDF report generation not available. ReportLab library not installed.")
        return None
        
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=1*inch, bottomMargin=0.75*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#2563eb'), alignment=TA_CENTER)
    elements.append(Paragraph("CDR Analysis Report", title_style))
    elements.append(Spacer(1, 0.5*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Records', f"{results.get('total_records', 0):,}"],
        ['Total Duration', seconds_to_hms(results.get('total_duration', 0))],
        ['Average Duration', seconds_to_hms(results.get('avg_duration', 0))],
        ['Unique Numbers', str(results.get('unique_numbers', 0))],
    ]
    
    table = Table(summary_data, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(table)
    
    doc.build(elements)
    return buffer.getvalue()

# ══════════════════════════════════════════════════════════════════════════════
# BILL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def render_bill_analysis():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>CDR Intelligence Platform</h1>
        <p style="font-size: 1.1rem; color: #6b7280; margin-bottom: 0;">
            Advanced Call Detail Record Analysis & Forensic Investigation Suite
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="alert alert-info">Upload your phone bill or call records to begin comprehensive forensic analysis</div>', unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload Call Records", type=["csv", "xlsx", "xls", "txt", "pdf"], label_visibility="collapsed")
    with col2:
        sample = "Date,Time,Duration,Number,Type\n2024-01-01,09:15:00,120,+919876543210,Outgoing\n"
        st.download_button("Download Sample", data=sample, file_name="sample.csv", mime="text/csv", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not uploaded_file:
        st.markdown("""
        <div class="content-section" style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 3rem; margin-bottom: 2rem; opacity: 0.3; color: #9ca3af;">⬆</div>
            <h3 style="color: #374151; margin-bottom: 1rem;">No File Selected</h3>
            <p style="color: #6b7280;">Upload a call record file to begin forensic analysis</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    df = load_file(uploaded_file)
    if df is None or len(df) == 0:
        st.markdown("<div class='alert-box alert-error'>❌ <b>Could not read file</b><br><br>"
                   "Possible reasons:<br>"
                   "• PDF is scanned/image-based (needs OCR)<br>"
                   "• PDF is password-protected<br>"
                   "• No structured table found in PDF<br>"
                   "• File format not supported<br><br>"
                   "💡 <b>Solution:</b> Try exporting your bill as CSV or Excel from your carrier's portal</div>", 
                   unsafe_allow_html=True)
        return
    
    st.markdown(f'<div class="alert alert-success">Successfully loaded {len(df):,} records for analysis</div>', unsafe_allow_html=True)
    
    # Debug info for column mapping
    st.markdown(f'<div class="alert alert-info"><strong>Available Columns:</strong> {", ".join(df.columns.tolist())}</div>', unsafe_allow_html=True)
    
    with st.expander("Column Mapping Configuration", expanded=False):
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        auto_map = auto_map_columns(df)
        all_cols = ["(none)"] + list(df.columns)
        col1, col2, col3 = st.columns(3)
        with col1:
            sel_date = st.selectbox("Date", all_cols, index=all_cols.index(auto_map.get("date", "(none)")) if auto_map.get("date") in all_cols else 0)
            sel_time = st.selectbox("Time", all_cols, index=all_cols.index(auto_map.get("time", "(none)")) if auto_map.get("time") in all_cols else 0)
        with col2:
            sel_number = st.selectbox("Number", all_cols, index=all_cols.index(auto_map.get("number", "(none)")) if auto_map.get("number") in all_cols else 0)
            sel_type = st.selectbox("Type", all_cols, index=all_cols.index(auto_map.get("type", "(none)")) if auto_map.get("type") in all_cols else 0)
        with col3:
            sel_duration = st.selectbox("Duration", all_cols, index=all_cols.index(auto_map.get("duration", "(none)")) if auto_map.get("duration") in all_cols else 0)
        
        col_map = {
            "date": sel_date if sel_date != "(none)" else None,
            "time": sel_time if sel_time != "(none)" else None,
            "number": sel_number if sel_number != "(none)" else None,
            "type": sel_type if sel_type != "(none)" else None,
            "duration": sel_duration if sel_duration != "(none)" else None,
        }
        
        # Show what was mapped
        mapped_info = []
        for key, value in col_map.items():
            if value:
                mapped_info.append(f"{key.title()}: {value}")
        
        if mapped_info:
            st.markdown(f'<div class="alert alert-info"><strong>Mapped Fields:</strong> {" | ".join(mapped_info)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if not any(col_map.values()):
        st.markdown('<div class="alert alert-error">Please map at least one column to proceed with analysis</div>', unsafe_allow_html=True)
        return
    
    if not st.button("Begin Forensic Analysis", use_container_width=True, type="primary"):
        return
    
    # Get column mappings
    dur_col = col_map.get("duration")
    num_col = col_map.get("number")
    type_col = col_map.get("type")
    date_col = col_map.get("date")
    time_col = col_map.get("time")
    
    # Parse duration with better error handling
    if dur_col and dur_col in df.columns:
        df["_dur_sec"] = parse_duration_to_seconds(df[dur_col])
    else:
        df["_dur_sec"] = 0
    
    total_records = len(df)
    total_sec = df["_dur_sec"].sum() if "_dur_sec" in df.columns else 0
    avg_sec = df["_dur_sec"].mean() if "_dur_sec" in df.columns and len(df) > 0 else 0
    max_sec = df["_dur_sec"].max() if "_dur_sec" in df.columns and len(df) > 0 else 0
    unique_nums = df[num_col].nunique() if num_col and num_col in df.columns else 0
    
    # Overview
    st.markdown("## Executive Summary")
    st.markdown('<div class="content-section"><div class="metrics-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="label">Total Records</div><div class="value primary">{total_records:,}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="label">Total Duration</div><div class="value">{seconds_to_hms(total_sec)}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="label">Average Duration</div><div class="value">{seconds_to_hms(avg_sec)}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="label">Longest Call</div><div class="value danger">{seconds_to_hms(max_sec)}</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="metric-card"><div class="label">Unique Contacts</div><div class="value success">{unique_nums}</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Data Quality Report
    st.markdown("## Data Quality Assessment")
    st.markdown('<div class="content-section"><div class="metrics-grid">', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    valid_numbers = df[num_col].notna().sum() if num_col and num_col in df.columns else 0
    valid_dates = df[date_col].notna().sum() if date_col and date_col in df.columns else 0
    valid_times = df[time_col].notna().sum() if time_col and time_col in df.columns else 0
    valid_durations = (df["_dur_sec"] > 0).sum() if "_dur_sec" in df.columns else 0
    
    with c1:
        pct = (valid_numbers / total_records * 100) if total_records > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="label">Valid Numbers</div><div class="value success">{valid_numbers:,} ({pct:.1f}%)</div></div>', unsafe_allow_html=True)
    with c2:
        pct = (valid_dates / total_records * 100) if total_records > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="label">Valid Dates</div><div class="value success">{valid_dates:,} ({pct:.1f}%)</div></div>', unsafe_allow_html=True)
    with c3:
        pct = (valid_times / total_records * 100) if total_records > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="label">Valid Times</div><div class="value success">{valid_times:,} ({pct:.1f}%)</div></div>', unsafe_allow_html=True)
    with c4:
        pct = (valid_durations / total_records * 100) if total_records > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="label">Valid Durations</div><div class="value success">{valid_durations:,} ({pct:.1f}%)</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Call Type
    if type_col and type_col in df.columns:
        st.markdown("## 📞 Call Type Analysis")
        
        # Filter valid types
        valid_types_df = df[df[type_col].notna() & (df[type_col] != '') & (df[type_col] != 'nan')]
        
        if len(valid_types_df) > 0:
            type_counts = valid_types_df[type_col].value_counts().reset_index()
            type_counts.columns = ["Type", "Count"]
            
            # Pie chart
            fig = px.pie(type_counts, names="Type", values="Count", color_discrete_sequence=["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"], hole=0.4)
            clean_layout(fig, "Call Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed breakdown
            if "_dur_sec" in df.columns:
                type_analysis = valid_types_df.groupby(type_col).agg({
                    type_col: "count",
                    "_dur_sec": ["sum", "mean", "max"]
                }).reset_index()
                type_analysis.columns = ["Type", "Count", "Total Duration (s)", "Avg Duration (s)", "Max Duration (s)"]
                type_analysis["Total Duration"] = type_analysis["Total Duration (s)"].apply(seconds_to_hms)
                type_analysis["Avg Duration"] = type_analysis["Avg Duration (s)"].apply(seconds_to_hms)
                type_analysis["Max Duration"] = type_analysis["Max Duration (s)"].apply(seconds_to_hms)
                
                st.markdown("#### Detailed Call Type Breakdown")
                st.dataframe(type_analysis[["Type", "Count", "Total Duration", "Avg Duration", "Max Duration"]], use_container_width=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid call type data found</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-box alert-info'>ℹ️ Call type column not mapped - type analysis skipped</div>", unsafe_allow_html=True)
    
    # Top Numbers
    if num_col and num_col in df.columns and "_dur_sec" in df.columns:
        st.markdown("## 👤 Top Contacts")
        
        # Filter valid data
        valid_data = df[(df[num_col].notna()) & (df[num_col] != '') & (df[num_col] != 'nan') & (df["_dur_sec"] > 0)]
        
        if len(valid_data) > 0:
            top = valid_data.groupby(num_col)["_dur_sec"].agg(["count", "sum"]).sort_values("sum", ascending=False).head(10).reset_index()
            top.columns = [num_col, "Calls", "Total Seconds"]
            top["Duration"] = top["Total Seconds"].apply(seconds_to_hms)
            
            # Display with proper column names
            display_cols = [num_col, "Calls", "Duration"]
            st.dataframe(top[display_cols], use_container_width=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid call data found for top contacts analysis</div>", unsafe_allow_html=True)
    elif num_col and num_col in df.columns:
        st.markdown("## 👤 Top Contacts")
        
        # Just show call counts without duration
        valid_data = df[(df[num_col].notna()) & (df[num_col] != '') & (df[num_col] != 'nan')]
        
        if len(valid_data) > 0:
            top = valid_data.groupby(num_col).size().reset_index(name="Calls").sort_values("Calls", ascending=False).head(10)
            st.dataframe(top, use_container_width=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid phone numbers found</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-box alert-info'>ℹ️ Number column not mapped - top contacts analysis skipped</div>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FORENSIC ANALYSIS - COMPREHENSIVE
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("## 🔬 Forensic Analysis")
    
    # Prepare datetime column
    if date_col and time_col:
        try:
            # Clean and combine date/time
            df_clean = df.copy()
            df_clean[date_col] = df_clean[date_col].astype(str).str.strip()
            df_clean[time_col] = df_clean[time_col].astype(str).str.strip()
            
            # Remove rows with empty date/time
            df_clean = df_clean[(df_clean[date_col] != '') & (df_clean[time_col] != '') & 
                               (df_clean[date_col] != 'nan') & (df_clean[time_col] != 'nan')]
            
            if len(df_clean) > 0:
                # Try multiple datetime formats
                datetime_str = df_clean[date_col] + " " + df_clean[time_col]
                
                # Try different parsing methods
                for fmt in ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M',
                           '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d-%m-%Y %H:%M:%S', '%d-%m-%Y %H:%M']:
                    try:
                        df["_datetime"] = pd.to_datetime(datetime_str, format=fmt, errors='coerce')
                        valid_dates = df["_datetime"].notna().sum()
                        if valid_dates > len(df) * 0.1:  # At least 10% valid dates
                            break
                    except:
                        continue
                
                # If format parsing failed, try general parsing
                if "_datetime" not in df.columns or df["_datetime"].notna().sum() < len(df) * 0.1:
                    df["_datetime"] = pd.to_datetime(datetime_str, errors='coerce', infer_datetime_format=True)
                
                # Extract time components only for valid dates
                valid_datetime = df["_datetime"].notna()
                if valid_datetime.sum() > 0:
                    df.loc[valid_datetime, "_hour"] = df.loc[valid_datetime, "_datetime"].dt.hour
                    df.loc[valid_datetime, "_day_of_week"] = df.loc[valid_datetime, "_datetime"].dt.day_name()
                    df.loc[valid_datetime, "_date_only"] = df.loc[valid_datetime, "_datetime"].dt.date
                    has_datetime = True
                else:
                    has_datetime = False
            else:
                has_datetime = False
        except Exception as e:
            st.warning(f"DateTime parsing issue: {str(e)}")
            has_datetime = False
    else:
        has_datetime = False
    
    # Duration Statistics
    if dur_col:
        st.markdown("### ⏱️ Duration Statistics")
        valid_durations = df[df["_dur_sec"] > 0]["_dur_sec"]
        
        if len(valid_durations) > 0:
            min_sec = valid_durations.min()
            median_sec = valid_durations.median()
            p25_sec = valid_durations.quantile(0.25)
            p75_sec = valid_durations.quantile(0.75)
            p90_sec = valid_durations.quantile(0.90)
            p95_sec = valid_durations.quantile(0.95)
            
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            with c1:
                st.markdown(f"<div class='metric-card'><div class='label'>Min</div><div class='value'>{seconds_to_hms(min_sec)}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-card'><div class='label'>25th %ile</div><div class='value'>{seconds_to_hms(p25_sec)}</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='metric-card'><div class='label'>Median</div><div class='value'>{seconds_to_hms(median_sec)}</div></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='metric-card'><div class='label'>75th %ile</div><div class='value'>{seconds_to_hms(p75_sec)}</div></div>", unsafe_allow_html=True)
            with c5:
                st.markdown(f"<div class='metric-card'><div class='label'>90th %ile</div><div class='value'>{seconds_to_hms(p90_sec)}</div></div>", unsafe_allow_html=True)
            with c6:
                st.markdown(f"<div class='metric-card'><div class='label'>95th %ile</div><div class='value'>{seconds_to_hms(p95_sec)}</div></div>", unsafe_allow_html=True)
            
            # Duration Distribution
            fig = px.histogram(valid_durations, nbins=50, color_discrete_sequence=["#2563eb"])
            clean_layout(fig, "Call Duration Distribution")
            fig.update_xaxes(title="Duration (seconds)")
            fig.update_yaxes(title="Frequency")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid duration data found</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-box alert-info'>ℹ️ Duration column not mapped - duration analysis skipped</div>", unsafe_allow_html=True)
    
    # Call Type Analysis
    if type_col and num_col and type_col in df.columns and num_col in df.columns:
        st.markdown("### 📊 Call Direction Analysis")
        
        valid_data = df[(df[type_col].notna()) & (df[type_col] != '') & (df[type_col] != 'nan')]
        
        if len(valid_data) > 0:
            if "_dur_sec" in df.columns:
                type_stats = valid_data.groupby(type_col).agg({
                    num_col: "count",
                    "_dur_sec": ["sum", "mean"]
                }).reset_index()
                type_stats.columns = ["Type", "Count", "Total Duration (s)", "Avg Duration (s)"]
                type_stats["Total Duration"] = type_stats["Total Duration (s)"].apply(seconds_to_hms)
                type_stats["Avg Duration"] = type_stats["Avg Duration (s)"].apply(seconds_to_hms)
                st.dataframe(type_stats[["Type", "Count", "Total Duration", "Avg Duration"]], use_container_width=True)
            else:
                type_stats = valid_data.groupby(type_col).size().reset_index(name="Count")
                type_stats.columns = ["Type", "Count"]
                st.dataframe(type_stats, use_container_width=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid call direction data found</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-box alert-info'>ℹ️ Call type or number columns not mapped - direction analysis skipped</div>", unsafe_allow_html=True)
    
    # Temporal Analysis
    if has_datetime:
        st.markdown("### 📅 Temporal Patterns")
        
        # Hourly Distribution
        st.markdown("#### Hourly Call Distribution")
        hourly = df[df["_hour"].notna()].groupby("_hour").size().reset_index(name="Count")
        
        if len(hourly) > 0:
            fig = px.bar(hourly, x="_hour", y="Count", color_discrete_sequence=["#2563eb"])
            clean_layout(fig, "Calls by Hour of Day")
            fig.update_xaxes(title="Hour (24h format)", dtick=1)
            fig.update_yaxes(title="Number of Calls")
            st.plotly_chart(fig, use_container_width=True)
            
            # Peak Hours
            peak_hour = hourly.loc[hourly["Count"].idxmax(), "_hour"]
            peak_count = hourly["Count"].max()
            st.markdown(f"<div class='alert-box alert-info'>🔥 <b>Peak Hour:</b> {int(peak_hour)}:00 with {int(peak_count)} calls</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid time data found for hourly analysis</div>", unsafe_allow_html=True)
        
        # Day of Week Distribution
        st.markdown("#### Weekly Call Distribution")
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekly_data = df[df["_day_of_week"].notna()]
        
        if len(weekly_data) > 0:
            weekly = weekly_data.groupby("_day_of_week").size().reset_index(name="Count")
            weekly["_day_of_week"] = pd.Categorical(weekly["_day_of_week"], categories=day_order, ordered=True)
            weekly = weekly.sort_values("_day_of_week")
            
            fig = px.bar(weekly, x="_day_of_week", y="Count", color_discrete_sequence=["#2563eb"])
            clean_layout(fig, "Calls by Day of Week")
            fig.update_xaxes(title="Day of Week")
            fig.update_yaxes(title="Number of Calls")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid date data found for weekly analysis</div>", unsafe_allow_html=True)
        
        # Daily Timeline
        st.markdown("#### Daily Call Timeline")
        daily_data = df[df["_date_only"].notna()]
        
        if len(daily_data) > 0:
            daily = daily_data.groupby("_date_only").size().reset_index(name="Count")
            daily.columns = ["Date", "Count"]
            fig = px.line(daily, x="Date", y="Count", color_discrete_sequence=["#2563eb"])
            clean_layout(fig, "Calls Over Time")
            fig.update_xaxes(title="Date")
            fig.update_yaxes(title="Number of Calls")
            st.plotly_chart(fig, use_container_width=True)
            
            # Busiest Day
            busiest_day = daily.loc[daily["Count"].idxmax(), "Date"]
            busiest_count = daily["Count"].max()
            st.markdown(f"<div class='alert-box alert-info'>📆 <b>Busiest Day:</b> {busiest_day} with {int(busiest_count)} calls</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid date data found for daily timeline</div>", unsafe_allow_html=True)
    
    # Contact Frequency Analysis
    if num_col and num_col in df.columns:
        st.markdown("### 👥 Contact Frequency Analysis")
        
        # Filter valid numbers
        valid_numbers_df = df[df[num_col].notna() & (df[num_col] != '') & (df[num_col] != 'nan')]
        
        if len(valid_numbers_df) > 0:
            contact_freq = valid_numbers_df.groupby(num_col).size().reset_index(name="Call Count")
            
            if "_dur_sec" in df.columns:
                contact_dur = valid_numbers_df.groupby(num_col)["_dur_sec"].agg(["sum", "mean", "max"]).reset_index()
                contact_dur.columns = [num_col, "Total Duration", "Avg Duration", "Max Duration"]
                contact_freq = contact_freq.merge(contact_dur, on=num_col, how="left")
                contact_freq["Total Duration (HMS)"] = contact_freq["Total Duration"].apply(seconds_to_hms)
                contact_freq["Avg Duration (HMS)"] = contact_freq["Avg Duration"].apply(seconds_to_hms)
                contact_freq["Max Duration (HMS)"] = contact_freq["Max Duration"].apply(seconds_to_hms)
            
            contact_freq = contact_freq.sort_values("Call Count", ascending=False)
            
            # Top 20 Contacts
            st.markdown("#### Top 20 Most Contacted Numbers")
            if "_dur_sec" in df.columns:
                display_cols = [num_col, "Call Count", "Total Duration (HMS)", "Avg Duration (HMS)", "Max Duration (HMS)"]
                # Only include columns that actually exist
                available_cols = [col for col in display_cols if col in contact_freq.columns]
                st.dataframe(contact_freq.head(20)[available_cols], use_container_width=True)
            else:
                st.dataframe(contact_freq.head(20), use_container_width=True)
            
            # Contact Distribution
            if len(contact_freq) > 1:
                st.markdown("#### Contact Frequency Distribution")
                freq_dist = contact_freq["Call Count"].value_counts().sort_index().reset_index()
                freq_dist.columns = ["Calls per Contact", "Number of Contacts"]
                fig = px.bar(freq_dist.head(20), x="Calls per Contact", y="Number of Contacts", color_discrete_sequence=["#2563eb"])
                clean_layout(fig, "How many contacts called X times")
                st.plotly_chart(fig, use_container_width=True)
            
            # Single Call Contacts
            single_call = (contact_freq["Call Count"] == 1).sum()
            st.markdown(f"<div class='alert-box alert-warning'>⚠️ <b>One-time Contacts:</b> {single_call} numbers called only once</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-box alert-warning'>⚠️ No valid phone numbers found for contact analysis</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-box alert-info'>ℹ️ Number column not mapped - contact analysis skipped</div>", unsafe_allow_html=True)
    
    # Suspicious Pattern Detection
    if "_dur_sec" in df.columns and num_col and num_col in df.columns:
        st.markdown("### 🚨 Suspicious Pattern Detection")
        
        # Very short calls (< 5 seconds)
        very_short = df[df["_dur_sec"] < 5]
        if len(very_short) > 0:
            st.markdown(f"<div class='alert-box alert-warning'>⚠️ <b>Very Short Calls:</b> {len(very_short)} calls under 5 seconds (possible missed/rejected calls)</div>", unsafe_allow_html=True)
        
        # Very long calls (> 1 hour)
        very_long = df[df["_dur_sec"] > 3600]
        if len(very_long) > 0:
            st.markdown(f"<div class='alert-box alert-warning'>⚠️ <b>Very Long Calls:</b> {len(very_long)} calls over 1 hour</div>", unsafe_allow_html=True)
            display_cols = [col for col in [num_col, date_col, time_col, "_dur_sec"] if col and col in df.columns]
            if display_cols:
                st.dataframe(very_long[display_cols].head(10), use_container_width=True)
        
        # High frequency contacts (> 50 calls) - only if we have contact frequency data
        if 'contact_freq' in locals() and len(contact_freq) > 0:
            high_freq = contact_freq[contact_freq["Call Count"] > 50]
            if len(high_freq) > 0:
                st.markdown(f"<div class='alert-box alert-warning'>⚠️ <b>High Frequency Contacts:</b> {len(high_freq)} numbers with more than 50 calls</div>", unsafe_allow_html=True)
                st.dataframe(high_freq.head(10), use_container_width=True)
    else:
        st.markdown("<div class='alert-box alert-info'>ℹ️ Duration or number data not available - suspicious pattern detection limited</div>", unsafe_allow_html=True)
    
    # Raw Data Preview
    st.markdown("### 📋 Raw Data Preview")
    
    # Handle duplicate column names
    display_df = df.copy()
    cols = list(display_df.columns)
    seen = {}
    new_cols = []
    for col in cols:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    display_df.columns = new_cols
    
    st.dataframe(display_df.head(100), use_container_width=True)
    
    # Download Reports
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if REPORTLAB_AVAILABLE:
            try:
                results = {"total_records": total_records, "total_duration": total_sec, "avg_duration": avg_sec, "unique_numbers": unique_nums}
                pdf = generate_pdf_report(results, uploaded_file.name)
                if pdf:
                    st.download_button("📥 PDF Report", data=pdf, file_name=f"report_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"PDF generation error: {str(e)}")
        else:
            st.info("📄 PDF reports require reportlab library (install in progress...)")
    with col2:
        try:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Data", index=False)
            st.download_button("📥 Excel", data=output.getvalue(), file_name=f"data_{datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        except Exception as e:
            st.error(f"Excel export error: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════
# TOWER LOCATOR
# ══════════════════════════════════════════════════════════════════════════════

def render_tower_locator():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>Cell Tower Intelligence</h1>
        <p style="font-size: 1.1rem; color: #6b7280; margin-bottom: 0;">
            Advanced Cellular Infrastructure Geolocation & Network Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="alert alert-info">Locate cell tower positions using Mobile Country Code, Network Code, Location Area, and Cell ID parameters</div>', unsafe_allow_html=True)
    
    # Add demo mode toggle - DEFAULT TO TRUE for deployment
    col_demo, col_api = st.columns([1, 3])
    with col_demo:
        demo_mode = st.checkbox("Demo Mode (No API Key Required)", value=True, help="Use sample Bangalore tower data for testing")
    
    if not demo_mode:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        with st.expander("API Configuration", expanded=True):
            api_key = st.text_input("Unwired Labs API Key", type="password", help="Obtain your free API key from unwiredlabs.com")
            st.markdown("**Don't have an API key?** Get a free one at [unwiredlabs.com](https://unwiredlabs.com)")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        api_key = "demo_mode"
        st.markdown('<div class="alert alert-info">Demo Mode: Using sample Bangalore cell tower data</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-section"><div class="form-grid">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### Device & Network Parameters")
        device = st.selectbox("Device Type", ["iPhone", "Android"])
        
        # Set Bangalore-specific defaults
        if demo_mode:
            mcc = st.number_input("Mobile Country Code (MCC)", min_value=1, max_value=999, value=404, help="404 = India")
            lac = st.number_input("Location Area Code (LAC/TAC)", min_value=0, max_value=65535, value=1001, help="Sample Bangalore LAC")
        else:
            mcc = st.number_input("Mobile Country Code (MCC)", min_value=1, max_value=999, value=404, help="404 = India")
            lac = st.number_input("Location Area Code (LAC/TAC)", min_value=0, max_value=65535, value=1234)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### Network Configuration")
        radio = st.selectbox("Radio Technology", ["lte", "gsm", "umts", "nr"])
        
        if demo_mode:
            mnc = st.number_input("Mobile Network Code (MNC)", min_value=0, max_value=999, value=10, help="10 = Airtel India")
            cid = st.number_input("Cell ID (CID)", min_value=0, value=12345, help="Sample Bangalore Cell ID")
        else:
            mnc = st.number_input("Mobile Network Code (MNC)", min_value=0, max_value=999, value=20)
            cid = st.number_input("Cell ID (CID)", min_value=0, value=56789)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Add helpful information
    with st.expander("📋 Indian Network Codes Reference", expanded=False):
        st.markdown("""
        **Common Indian MNC Codes:**
        - **10** - Airtel (Bharti Airtel)
        - **20** - Vodafone Idea
        - **27** - Vodafone Idea
        - **40** - Airtel
        - **49** - Airtel
        - **92** - Airtel
        - **93** - Airtel
        - **94** - Airtel
        - **95** - Airtel
        - **96** - Airtel
        - **97** - Airtel
        - **98** - Airtel
        
        **MCC 404** = India
        """)
    
    if st.button("🗼 Initiate Tower Geolocation", use_container_width=True, type="primary"):
        if not demo_mode and not api_key:
            st.markdown('<div class="alert alert-error">API key is required to proceed with geolocation. Enable Demo Mode to test without API key.</div>', unsafe_allow_html=True)
            return
        
        # Show loading spinner
        with st.spinner('🔍 Locating cell tower...'):
            try:
                if demo_mode:
                    # Demo mode with realistic Bangalore coordinates
                    demo_towers = {
                        (404, 10, 1001, 12345): {"lat": 12.9716, "lon": 77.5946, "accuracy": 500, "location": "Bangalore City Center"},
                        (404, 10, 1002, 12346): {"lat": 12.9352, "lon": 77.6245, "accuracy": 750, "location": "Bangalore Electronic City"},
                        (404, 10, 1003, 12347): {"lat": 13.0358, "lon": 77.5970, "accuracy": 600, "location": "Bangalore Hebbal"},
                        (404, 20, 1001, 12345): {"lat": 12.9698, "lon": 77.7500, "accuracy": 800, "location": "Bangalore Whitefield"},
                        (404, 27, 1001, 12345): {"lat": 12.9141, "lon": 77.6101, "accuracy": 450, "location": "Bangalore Koramangala"},
                    }
                    
                    tower_key = (mcc, mnc, lac, cid)
                    if tower_key in demo_towers:
                        tower_data = demo_towers[tower_key]
                        lat, lon, acc = tower_data["lat"], tower_data["lon"], tower_data["accuracy"]
                        location_name = tower_data["location"]
                        result_status = "ok"
                        st.success(f"✅ Demo tower found: {location_name}")
                    else:
                        # Default Bangalore location if exact match not found
                        lat, lon, acc = 12.9716, 77.5946, 1000
                        location_name = "Bangalore (Approximate)"
                        result_status = "ok"
                        st.info(f"ℹ️ Using approximate Bangalore location for demo")
                else:
                    # Real API call
                    st.info(f"🌐 Querying Unwired Labs API...")
                    st.info(f"📡 Parameters: MCC={mcc}, MNC={mnc}, LAC={lac}, CID={cid}, Radio={radio}")
                    
                    payload = {
                        "token": api_key, 
                        "radio": radio, 
                        "mcc": mcc, 
                        "mnc": mnc,
                        "cells": [{"lac": lac, "cid": cid}], 
                        "address": 1
                    }
                    
                    resp = requests.post(
                        "https://us1.unwiredlabs.com/v2/process.php", 
                        json=payload, 
                        timeout=30,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    st.info(f"📊 API Response Status: {resp.status_code}")
                    
                    if resp.status_code != 200:
                        st.error(f"❌ API request failed with status code: {resp.status_code}")
                        st.error(f"Response: {resp.text}")
                        return
                    
                    result = resp.json()
                    st.info(f"📋 API Response: {result}")
                    result_status = result.get("status")
                
                if result_status == "ok":
                    if not demo_mode:
                        lat, lon, acc = result.get("lat"), result.get("lon"), result.get("accuracy", 0)
                        address = result.get("address", "")
                    
                    # Display results
                    st.markdown('<div class="content-section">', unsafe_allow_html=True)
                    st.markdown("### 🎯 Geolocation Results")
                    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="metric-card"><div class="label">Latitude</div><div class="value primary">{lat:.6f}</div></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="metric-card"><div class="label">Longitude</div><div class="value primary">{lon:.6f}</div></div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<div class="metric-card"><div class="label">Accuracy Radius</div><div class="value success">{acc:.0f}m</div></div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Additional info
                    if demo_mode:
                        st.info(f"📍 **Location**: {location_name}")
                    elif not demo_mode and 'address' in locals() and address:
                        st.info(f"📍 **Address**: {address}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Create and display map
                    st.markdown('<div class="content-section">', unsafe_allow_html=True)
                    st.markdown("### 🗺️ Interactive Tower Map")
                    
                    try:
                        # Create map with better styling
                        m = folium.Map(
                            location=[lat, lon], 
                            zoom_start=15,
                            tiles='OpenStreetMap'
                        )
                        
                        # Add accuracy circle
                        folium.Circle(
                            location=[lat, lon], 
                            radius=acc, 
                            color="#dc2626", 
                            fill=True, 
                            fill_opacity=0.2,
                            weight=2,
                            popup=f"Accuracy: {acc}m radius"
                        ).add_to(m)
                        
                        # Add tower marker
                        popup_text = f"""
                        <b>📡 Cell Tower</b><br>
                        <b>Coordinates:</b> {lat:.6f}, {lon:.6f}<br>
                        <b>Accuracy:</b> {acc}m<br>
                        <b>MCC:</b> {mcc} (India)<br>
                        <b>MNC:</b> {mnc}<br>
                        <b>LAC:</b> {lac}<br>
                        <b>CID:</b> {cid}<br>
                        <b>Technology:</b> {radio.upper()}
                        """
                        
                        if demo_mode:
                            popup_text += f"<br><b>Location:</b> {location_name}"
                        
                        folium.Marker(
                            location=[lat, lon], 
                            popup=folium.Popup(popup_text, max_width=300),
                            tooltip="Click for tower details",
                            icon=folium.Icon(color="red", icon="tower-broadcast", prefix="fa")
                        ).add_to(m)
                        
                        # Display map
                        map_data = st_folium(m, width="100%", height=500, returned_objects=["last_clicked"])
                        
                        # Show coordinates when map is clicked
                        if map_data['last_clicked']:
                            clicked_lat = map_data['last_clicked']['lat']
                            clicked_lng = map_data['last_clicked']['lng']
                            st.info(f"🖱️ Clicked coordinates: {clicked_lat:.6f}, {clicked_lng:.6f}")
                        
                    except Exception as map_error:
                        st.error(f"❌ Map display error: {str(map_error)}")
                        st.info("📍 **Tower Coordinates (Text Format):**")
                        st.code(f"Latitude: {lat:.6f}\nLongitude: {lon:.6f}\nAccuracy: {acc}m")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Export options
                    st.markdown("### 📥 Export Options")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Google Maps link
                        google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                        st.markdown(f'<a href="{google_maps_url}" target="_blank" style="text-decoration: none;"><div style="background: #4285f4; color: white; padding: 10px; border-radius: 5px; text-align: center; margin: 5px 0;">🗺️ Open in Google Maps</div></a>', unsafe_allow_html=True)
                    
                    with col2:
                        # Download coordinates as CSV
                        csv_data = f"Parameter,Value\nLatitude,{lat:.6f}\nLongitude,{lon:.6f}\nAccuracy,{acc}\nMCC,{mcc}\nMNC,{mnc}\nLAC,{lac}\nCID,{cid}\nRadio,{radio}"
                        st.download_button(
                            "📄 Download CSV",
                            data=csv_data,
                            file_name=f"tower_location_{mcc}_{mnc}_{lac}_{cid}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                else:
                    error_msg = result.get("message", "Unknown error occurred") if not demo_mode else "Demo mode error"
                    st.markdown(f'<div class="alert alert-error">❌ Geolocation failed: {error_msg}</div>', unsafe_allow_html=True)
                    
                    if not demo_mode:
                        st.markdown("### 🔧 Troubleshooting Tips:")
                        st.markdown("""
                        - **Check API Key**: Ensure your Unwired Labs API key is valid
                        - **Verify Parameters**: Make sure MCC, MNC, LAC, and CID are correct
                        - **Try Demo Mode**: Enable demo mode to test with sample data
                        - **Check Network**: Ensure you have internet connectivity
                        - **API Limits**: Check if you've exceeded your API quota
                        """)
                        
                        # Show API response for debugging
                        with st.expander("🔍 Debug Information", expanded=False):
                            st.json(result)
                    
            except requests.exceptions.Timeout:
                st.markdown('<div class="alert alert-error">⏱️ Request timeout. Please try again.</div>', unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown('<div class="alert alert-error">🌐 Connection error. Check your internet connection.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="alert alert-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                st.error(f"Full error details: {type(e).__name__}: {str(e)}")
    
    # Add information section
    st.markdown("---")
    st.markdown("### ℹ️ About Cell Tower Geolocation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **How it works:**
        - Uses cell tower parameters to find physical location
        - Queries cellular network databases
        - Returns approximate coordinates with accuracy radius
        - Useful for forensic analysis and network planning
        """)
    
    with col2:
        st.markdown("""
        **Parameter Guide:**
        - **MCC**: Mobile Country Code (404 for India)
        - **MNC**: Mobile Network Code (carrier specific)
        - **LAC/TAC**: Location/Tracking Area Code
        - **CID**: Cell ID (unique tower identifier)
        """)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem;">
        <div style="font-size: 1.5rem; font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">
            CDR Intelligence
        </div>
        <div style="font-size: 0.9rem; color: #6b7280; font-weight: 500;">
            Forensic Analysis Platform
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### Navigation")
    page = st.radio(
        "Select Module", 
        ["Cell Tower Intelligence", "CDR Analysis Suite"], 
        label_visibility="collapsed",
        key="navigation"
    )
    
    st.markdown('<hr style="margin: 2rem 0; border-color: #e2e8f0; border-width: 1px;">', unsafe_allow_html=True)
    
    # System Info
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb;">
        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.5rem;">System Status</div>
        <div style="font-size: 0.9rem; color: #059669; font-weight: 600;">● Online</div>
        <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 0.5rem;">v2.0 Professional</div>
    </div>
    """, unsafe_allow_html=True)

if page == "Cell Tower Intelligence":
    render_tower_locator()
else:
    render_bill_analysis()
