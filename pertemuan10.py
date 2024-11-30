import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
from datetime import date

st.title("Pertemuan 10: Interaksi Streamlit dan Yahoo Finance")

kamus_ticker = {
    'GOOGL': 'Google',
    'AAPL' : 'Apple',
    'SBUX' : 'Starbucks',
    'MCD'  : "McDonald's Corp",
    'BMRI.JK' : 'PT Bank Mandiri (Persero) Tbk Pt',
    'BBRI.JK' : 'Bank Rakyat Indonesia (Persero) Tbk PT',
    'BBNI.JK' : 'Bank Negara Indonesia (Persero) Tbk PT',
    'BBCA.JK' : 'Bank Central Asia (Persero) Tbk PT',
    'TLKM.JK' : 'Telkom Indonesia Persero Tbk',
    'META' : 'Meta Platforms Inc',
    'NESN' : 'Nestle SA'
}

ticker_symbol = st.selectbox(
    'Silakan pilih kode perusahaan:',
    sorted(kamus_ticker.keys())
)

#st.write(ticker_symbol)
#ticker_symbol = 'GOOGL'
#ticker_symbol = 'AAPL'

ticker_data = yf.Ticker(ticker_symbol)
pilihan_periode= st.selectbox(
    "Pilih Periode:",
    ['1d','5d','1mo','3mo','6mo','1y','2y']
)
tgl_mulai = st.date_input(
    'Mulai tanggal',
    value=date.today()
)
tgl_akhir = st.date_input(
    'Sampai tanggal',
    value=date.today()
)

df_ticker = ticker_data.history(
    period = pilihan_periode,
    start = str(tgl_mulai),
    end = str(tgl_akhir),
)
#data harus dibuat string ketika akan mengambil historinya

pilihan_tampil_tabel = st.checkbox('Tampilkan tabel')
#st.write(pilihan_tampil_tabel)

if pilihan_tampil_tabel == True:
    st.write("## Lima Data Awal")
    st.write(df_ticker.head())

st.write(f"## Visualisasi Pergerakan Saham {kamus_ticker[ticker_symbol]}")

pilihan_atribut= st.multiselect(
    'Silakan pilih atribut yang akan ditampilkan:',
    ['Low','High','Open','Close','Volume']
)

grafik = px.line(
    df_ticker,
    y=pilihan_atribut,
    title= f"Harga Saham{kamus_ticker[ticker_symbol]}"
)

#case sensitive, jadi data kolom y harus sesuai dengan "Open" dan/atau "Close"
st.plotly_chart(grafik)



####################################################################################
#LATIHAN COBA COBA TUGAS
import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Title and description
st.title("Pertemuan 10: Interaksi Streamlit dan Yahoo Finance")
st.write("""
Aplikasi ini memungkinkan Anda untuk melihat data fundamental saham dari berbagai perusahaan dan membantu dalam pengambilan keputusan investasi.
""")

# Dictionary for company ticker symbols
kamus_ticker = {
    'GOOGL': 'Google',
    'AAPL' : 'Apple',
    'SBUX' : 'Starbucks',
    'MCD'  : "McDonald's Corp",
    'BMRI' : 'PT Bank Mandiri (Persero) Tbk Pt',
    'BBRI' : 'Bank Rakyat Indonesia (Persero) Tbk PT',
    'BBCA' : 'Bank Central Asia (Persero) Tbk PT',
    'TLKM' : 'Telkom Indonesia Persero Tbk',
    'META' : 'Meta Platforms Inc',
    'NESN' : 'Nestle SA'
}

# Select box for company selection
ticker_symbol = st.selectbox(
    'Silakan pilih kode perusahaan:',
    sorted(kamus_ticker.keys())
)

# Show company name
st.write(f"### {kamus_ticker[ticker_symbol]} ({ticker_symbol})")

# Get ticker data
ticker_data = yf.Ticker(ticker_symbol)

# Define date range for historical data
end_date = datetime.now()
start_date = end_date - timedelta(days=180)  # Last 6 months data

# Fetch historical data
df_ticker = ticker_data.history(start=start_date, end=end_date)

# Display data preview
st.write("## Data Harga Saham Terbaru")
st.write(df_ticker.tail())

# Candlestick Chart with Moving Averages
st.write("## Grafik Candlestick dengan Moving Averages")
df_ticker['SMA20'] = df_ticker['Close'].rolling(window=20).mean()  # Simple Moving Average
df_ticker['EMA20'] = df_ticker['Close'].ewm(span=20, adjust=False).mean()  # Exponential Moving Average

fig_candlestick = go.Figure(data=[go.Candlestick(
    x=df_ticker.index,
    open=df_ticker['Open'],
    high=df_ticker['High'],
    low=df_ticker['Low'],
    close=df_ticker['Close'],
    name='Harga'
)])
fig_candlestick.add_trace(go.Scatter(
    x=df_ticker.index, y=df_ticker['SMA20'], mode='lines', name='SMA 20 Hari', line=dict(color='blue', width=1)
))
fig_candlestick.add_trace(go.Scatter(
    x=df_ticker.index, y=df_ticker['EMA20'], mode='lines', name='EMA 20 Hari', line=dict(color='red', width=1)
))
fig_candlestick.update_layout(title=f'Candlestick dengan SMA dan EMA untuk {kamus_ticker[ticker_symbol]}',
                              xaxis_title='Tanggal', yaxis_title='Harga')
st.plotly_chart(fig_candlestick)

# Area Chart for Price Accumulation
st.write("## Grafik Area Akumulasi Harga")
fig_area = px.area(df_ticker, x=df_ticker.index, y='Close', title=f'Akumulasi Harga Penutupan {kamus_ticker[ticker_symbol]}')
st.plotly_chart(fig_area)

# Heatmap of Correlations
st.write("## Heatmap Korelasi Data Saham")
df_corr = df_ticker[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
fig_heatmap = px.imshow(df_corr, text_auto=True, title="Korelasi Antar Variabel Harga Saham")
st.plotly_chart(fig_heatmap)

# Scatter Plot for Close Price vs. Volume
st.write("## Scatter Plot: Harga Penutupan vs. Volume")
fig_scatter = px.scatter(
    df_ticker, x='Volume', y='Close',
    title=f'Harga Penutupan vs Volume untuk {kamus_ticker[ticker_symbol]}',
    labels={'Volume': 'Volume', 'Close': 'Harga Penutupan'},
    trendline='ols'  # Optional trendline to see correlation
)
st.plotly_chart(fig_scatter)

# Display financial ratios
st.write("## Rasio Keuangan")

# Fetch financial info
info = ticker_data.info
try:
    pe_ratio = info.get("trailingPE", None)
    pb_ratio = info.get("priceToBook", None)
    dividend_yield = info.get("dividendYield", None)
    market_cap = info.get("marketCap", None)
    
    # Creating a DataFrame for financial ratios
    ratios_data = {
        "Rasio": ["P/E Ratio", "P/B Ratio", "Dividend Yield (%)", "Market Cap (Billion USD)"],
        "Nilai": [
            pe_ratio,
            pb_ratio,
            dividend_yield * 100 if dividend_yield else None,  # Convert to percentage
            market_cap / 1e9 if market_cap else None  # Convert to billions
        ]
    }
    df_ratios = pd.DataFrame(ratios_data)
    st.write(df_ratios)
    
    # Bar chart for financial ratios
    st.write("## Visualisasi Rasio Keuangan")
    fig_ratios = px.bar(
        df_ratios,
        x="Rasio",
        y="Nilai",
        text="Nilai",
        title="Rasio Keuangan Utama",
        labels={"Nilai": "Nilai Rasio"}
    )
    fig_ratios.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_ratios)
    
    # Interpretation based on P/E ratio and Dividend Yield
    st.write("### Interpretasi Rasio")
    if pe_ratio:
        if pe_ratio < 15:
            st.write("**P/E Ratio rendah**: Saham ini mungkin undervalued. Potensi pembelian.")
        elif 15 <= pe_ratio <= 25:
            st.write("**P/E Ratio moderat**: Saham dalam nilai yang wajar. Bisa menjadi opsi untuk diinvestasikan.")
        else:
            st.write("**P/E Ratio tinggi**: Saham mungkin overvalued. Pertimbangkan risiko.")
    
    if dividend_yield:
        if dividend_yield > 0.03:
            st.write("**Dividend Yield tinggi**: Saham ini menawarkan dividen yang tinggi, cocok bagi investor yang mencari pendapatan pasif.")
        else:
            st.write("**Dividend Yield rendah**: Saham ini memiliki dividen rendah atau tidak ada, cocok untuk pertumbuhan kapital.")
except Exception as e:
    st.write("Data fundamental tidak tersedia untuk saham ini.")



###############################################################################
#Coba
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Judul dan deskripsi
st.title("Aplikasi Analisis Saham & Investasi")
st.write("""
Aplikasi ini menampilkan data fundamental dan teknikal saham, serta membantu dalam pengambilan keputusan investasi.
""")

# Kamus untuk memilih perusahaan
kamus_ticker = {
    'GOOGL': 'Google',
    'AAPL' : 'Apple',
    'SBUX' : 'Starbucks',
    'MCD'  : "McDonald's Corp",
    'BMRI' : 'PT Bank Mandiri (Persero) Tbk Pt',
    'BBRI' : 'Bank Rakyat Indonesia (Persero) Tbk PT',
    'BBCA' : 'Bank Central Asia (Persero) Tbk PT',
    'TLKM' : 'Telkom Indonesia Persero Tbk',
    'META' : 'Meta Platforms Inc',
    'NESN' : 'Nestle SA'
}

ticker_symbol = st.selectbox('Pilih kode perusahaan:', sorted(kamus_ticker.keys()))
st.write(f"### {kamus_ticker[ticker_symbol]} ({ticker_symbol})")

# Pilihan periode waktu dengan date_input
start_date = st.date_input("Pilih tanggal mulai", datetime.now() - timedelta(days=180))
end_date = st.date_input("Pilih tanggal akhir", datetime.now())

# Mengambil data saham
ticker_data = yf.Ticker(ticker_symbol)
df_ticker = ticker_data.history(start=start_date, end=end_date)

# Candlestick Chart dengan Moving Averages
st.write("## Candlestick dengan Moving Averages")
df_ticker['SMA20'] = df_ticker['Close'].rolling(window=20).mean()
df_ticker['EMA20'] = df_ticker['Close'].ewm(span=20, adjust=False).mean()

fig_candlestick = go.Figure(data=[go.Candlestick(
    x=df_ticker.index, open=df_ticker['Open'], high=df_ticker['High'],
    low=df_ticker['Low'], close=df_ticker['Close'], name='Harga'
)])
fig_candlestick.add_trace(go.Scatter(x=df_ticker.index, y=df_ticker['SMA20'], name='SMA 20 Hari', line=dict(color='blue')))
fig_candlestick.add_trace(go.Scatter(x=df_ticker.index, y=df_ticker['EMA20'], name='EMA 20 Hari', line=dict(color='red')))
st.plotly_chart(fig_candlestick)

# Heatmap Korelasi
st.write("## Heatmap Korelasi")
df_corr = df_ticker[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
fig_heatmap = px.imshow(df_corr, text_auto=True, title="Korelasi Antar Variabel")
st.plotly_chart(fig_heatmap)

# Rasio Keuangan dan Statistik
st.write("## Key Statistik Keuangan")

# Mengambil data finansial
info = ticker_data.info
financial_metrics = {
    "Performance": {
        "ROA (%)": info.get("returnOnAssets") * 100 if info.get("returnOnAssets") else None,
        "ROE (%)": info.get("returnOnEquity") * 100 if info.get("returnOnEquity") else None,
        "GPM (%)": info.get("grossMargins") * 100 if info.get("grossMargins") else None,
        "OPM (%)": info.get("operatingMargins") * 100 if info.get("operatingMargins") else None,
        "NPM (%)": info.get("profitMargins") * 100 if info.get("profitMargins") else None,
    },
    "Valuation": {
        "EPS": info.get("trailingEps"),
        "P/B Ratio": info.get("priceToBook"),
        "Revenue Per Share (RPS)": info.get("revenuePerShare"),
        "Book Value Per Share (BVPS)": info.get("bookValue"),
        "Cash Flow Per Share (CFPS)": info.get("freeCashflow") / info["sharesOutstanding"] if info.get("freeCashflow") and info.get("sharesOutstanding") else None,
        "Current Price-to-Earnings (P/E)": info.get("trailingPE"),
    },
    "Solvency": {
        "Current Ratio (CR)": info.get("currentRatio"),
        "Debt-to-Equity Ratio (DER)": info.get("debtToEquity"),
    },
    "Dividend": {
        "Dividend Yield (%)": info.get("dividendYield") * 100 if info.get("dividendYield") else None,
        "Payout Ratio (%)": info.get("payoutRatio") * 100 if info.get("payoutRatio") else None,
    }
}

# Menampilkan data metrik keuangan dalam tabel
for category, metrics in financial_metrics.items():
    st.write(f"### {category}")
    df_metrics = pd.DataFrame(metrics.items(), columns=["Rasio", "Nilai"])
    st.write(df_metrics)

# Simulasi investasi (Return on Investment)
st.write("## Simulasi Investasi")
investasi_awal = st.number_input("Masukkan jumlah investasi awal ($)", min_value=1, value=1000)
harga_awal = df_ticker['Close'].iloc[0] if not df_ticker.empty else None
harga_akhir = df_ticker['Close'].iloc[-1] if not df_ticker.empty else None

if harga_awal and harga_akhir:
    return_investasi = (harga_akhir - harga_awal) / harga_awal * 100
    nilai_akhir = investasi_awal * (1 + return_investasi / 100)
    st.write(f"Jika Anda berinvestasi ${investasi_awal:.2f} pada tanggal {start_date} di {kamus_ticker[ticker_symbol]}, nilai investasi Anda sekarang akan menjadi ${nilai_akhir:.2f}, dengan pertumbuhan sebesar {return_investasi:.2f}%.")

# Visualisasi Tren Volume dan Harga
st.write("## Grafik Tren Volume dan Harga")
fig_volume = px.bar(df_ticker, x=df_ticker.index, y='Volume', title="Volume Perdagangan")
st.plotly_chart(fig_volume)
fig_close = px.line(df_ticker, x=df_ticker.index, y='Close', title="Harga Penutupan Saham")
st.plotly_chart(fig_close)

