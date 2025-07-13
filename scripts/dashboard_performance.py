import streamlit as st
import pandas as pd
import asyncio

# --------------------------------------------------------
# CACHED DB QUERY FUNCTION
# --------------------------------------------------------

@st.cache_data
def load_data(path):
    st.write("→ Loading data from disk...")
    df = pd.read_csv(path)
    return df

# --------------------------------------------------------
# ASYNC DATA LOADING + PAGINATION
# --------------------------------------------------------

async def async_load_and_paginate(path, page_size=3):
    st.write("→ Simulating async loading...")
    # Simulate a network delay
    await asyncio.sleep(1)
    df = pd.read_csv(path)
    total_rows = df.shape[0]
    
    page = st.number_input("Page number", 1, max(1, (total_rows // page_size)+1), 1)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    st.write(f"Showing rows {start_idx+1} to {min(end_idx,total_rows)}")
    st.dataframe(df.iloc[start_idx:end_idx])

# --------------------------------------------------------
# MAIN STREAMLIT APP
# --------------------------------------------------------

def main():
    st.title("🚀 Dashboard Performance Demo")

    # Choose test mode
    mode = st.radio(
        "Choose performance test:",
        ["Cache DB Query", "Async Pagination"]
    )

    csv_file = "outputs/google_trends.csv"

    if mode == "Cache DB Query":
        df = load_data(csv_file)
        st.write("✅ Data loaded (cached):", df)
    else:
        asyncio.run(async_load_and_paginate(csv_file))

if __name__ == "__main__":
    main()
