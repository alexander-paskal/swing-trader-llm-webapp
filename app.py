# __import__('pysqlite3')
# import sys
import sqlite3
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st

try:
    import yfinance as yf
    import plotly.graph_objs as go
    import plotly.io as pio
    from technical_page import technical_analysis_page
    from llm import initialize_llm
except:
    st.rerun()

st.set_page_config(layout="wide", page_title="Stock Analysis Agent", initial_sidebar_state="expanded")
# Sidebar for navigation between pages


pio.templates.default = "plotly_dark"

# Model selection
model_option = st.sidebar.selectbox("Select LLM Model", ['gpt-3.5-turbo',"gpt-4o","gpt-4o-mini"])
analysis = st.sidebar.selectbox("Select Analysis Type", ['technical', 'fundamental'])

stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
analyze_button = st.sidebar.button("📊 Analyze Stock", help="Click to start the stock analysis")
llm = initialize_llm(model_option, st.secrets["OPENAI_API_KEY"])
print(llm)
# Initialize session state
st.session_state.analyzed = False
st.session_state.stock_info = None
st.session_state.stock_data = None
st.session_state.result = None
st.session_state.llm = llm



st.markdown('<p class="big-font">Stock Analysis Agent</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="medium-font">Configuration</p>', unsafe_allow_html=True)




techno_tab, fundo_tab = st.tabs(["Technicals", "Fundamentals"])
print("Working")


with techno_tab:
    print("Working Tab")
    technical_analysis_page(stock_symbol, llm)
with fundo_tab:
    print("Fundos")
    st.text("Well Fuck me buddy")

if analyze_button:
    st.session_state.analyzed = False  # Reset analyzed state
    st.snow()


    
# Fetch stock info and data
# with st.spinner(f"Fetching data for {stock_symbol}..."):
#     stock = yf.Ticker(stock_symbol)
#     st.session_state.stock_info = stock.info
#     st.session_state.stock_data = get_stock_data(stock_symbol, period=time_period)

    # Create and run the crew
    # with st.spinner("Running analysis, please wait..."):
        
        # st.session_state.result = create_crew(stock_symbol, model_option)
    
    st.session_state.analyzed = True

# Display stock info if available
# if st.session_state.stock_info:
#     st.markdown('<p class="medium-font">Stock Information</p>', unsafe_allow_html=True)
#     info = st.session_state.stock_info
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown(f"**Company Name:** {info.get('longName', 'N/A')}")
#         st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
#     with col2:
#         st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
#         st.markdown(f"**Country:** {info.get('country', 'N/A')}")
#     with col3:
#         st.markdown(f"**Current Price:** ${info.get('currentPrice', 'N/A')}")
#         st.markdown(f"**Market Cap:** ${info.get('marketCap', 'N/A')}")

# Display CrewAI result if available
# print(st.session_state.result)
# if st.session_state.result:
#     st.markdown('<p class="medium-font">Analysis Result</p>', unsafe_allow_html=True)
#     st.markdown(st.session_state.result)

# # Display chart
# if st.session_state.analyzed and st.session_state.stock_data is not None:
#     st.markdown('<p class="medium-font">Interactive Stock Chart</p>', unsafe_allow_html=True)
#     st.plotly_chart(plot_stock_chart(st.session_state.stock_data, indicators), use_container_width=True)


st.markdown("---")
st.markdown('<p class="small-font">Created by Alex Paskal </p>', unsafe_allow_html=True)