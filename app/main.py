import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_and_combine_data, create_summary_table 

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Solar Resource Comparative Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading (Cached for performance) ---
combined_df = load_and_combine_data()

# --- Main Logic ---
if combined_df is not None:
    
    st.title("☀️ Solar Resource Comparative Dashboard")
    st.markdown("Use the sidebar controls to filter countries and analyze irradiance metrics (GHI, DNI, DHI).")

    # --- Sidebar for Interactive Filters ---
    st.sidebar.header("Country Selection")
    
    all_countries = combined_df['Country'].unique().tolist()
    
    # Create checkboxes for each country
    selected_countries = []
    for country in all_countries:
        if st.sidebar.checkbox(country, value=True):
            selected_countries.append(country)
            
    # Filter the data based on selections
    filtered_df = combined_df[combined_df['Country'].isin(selected_countries)]
    
    # --- Main Content Layout ---
    
    if not filtered_df.empty:
        
        # 1. Summary Table Section
        st.header("1. Comparative Performance Metrics")
        summary_df = create_summary_table(filtered_df)
        st.dataframe(summary_df)
        
        # 2. Boxplot Visualization Section
        st.header("2. Irradiance Distribution Analysis")
        
        # Streamlit columns for side-by-side plots
        col1, col2, col3 = st.columns(3)
        
        metrics = ['GHI', 'DNI', 'DHI']
        
        for i, metric in enumerate(metrics):
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(
                x='Country', 
                y=metric, 
                data=filtered_df, 
                ax=ax, 
                palette='viridis',
                hue='Country',
                legend=False
            )
            ax.set_title(f'Distribution of {metric}', fontsize=12)
            ax.set_xlabel('Country')
            ax.set_ylabel(rf'{metric} ($\text{{W/m}}^2$)')
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Display plots in the columns
            if i == 0:
                col1.pyplot(fig)
            elif i == 1:
                col2.pyplot(fig)
            else:
                col3.pyplot(fig)
                
            plt.close(fig) # Close figure to free memory
            
    else:
        st.warning("Please select at least one country in the sidebar to view the data.")

else:
    st.error("Application failed to load necessary data files. Check your file paths in `app/utils.py` and ensure files are in the `data/` folder.")