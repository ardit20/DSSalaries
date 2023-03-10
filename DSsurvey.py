import pandas as pd
import streamlit as st

# Load the Kaggle survey dataset
df = pd.read_csv("kaggle.csv")

# Create a selectbox widget for choosing a country
countries = sorted(df["In which country do you currently reside?"].unique())
selected_country = st.sidebar.selectbox("Select a country", countries)

# Filter the DataFrame by the selected country and remove any rows where the yearly compensation is missing
country_df = df[df["In which country do you currently reside?"] == selected_country]
country_df = country_df[~country_df["What is your current yearly compensation (approximate $USD)?"].isnull()]

# Display a histogram of the yearly compensation for the selected country
st.write(f"Yearly compensation distribution for {selected_country}")
st.hist_chart(country_df["What is your current yearly compensation (approximate $USD)?"])

# Create a selectbox widget for choosing a wage range
wage_ranges = [
    "$0-$10,000",
    "$10,000-$20,000",
    "$20,000-$30,000",
    "$30,000-$40,000",
    "$40,000-$50,000",
    "$50,000-$60,000",
    "$60,000-$70,000",
    "$70,000-$80,000",
    "$80,000-$90,000",
    "$90,000-$100,000",
    "> $100,000"
]
selected_wage_range = st.sidebar.selectbox("Select a wage range", wage_ranges)

# Filter the DataFrame by the selected wage range and display a table of the top 10 countries with the highest number of respondents in that wage range
wage_min, wage_max = selected_wage_range.split("-")
wage_min = int(wage_min.replace("$", "").replace(",", ""))
wage_max = int(wage_max.replace("$", "").replace(",", ""))
wage_df = df[(df["What is your current yearly compensation (approximate $USD)?"].notnull()) & 
             (df["What is your current yearly compensation (approximate $USD)?"].astype(float) >= wage_min) & 
             (df["What is your current yearly compensation (approximate $USD)?"].astype(float) <= wage_max)]
top_countries = wage_df["In which country do you currently reside?"].value_counts().head(10)
st.write(f"Top 10 countries with respondents in the {selected_wage_range} wage range")
st.write(top_countries)

# Display the DataFrame filtered by both the selected country and wage range in a table
filtered_df = df[(df["In which country do you currently reside?"] == selected_country) & 
                 (df["What is your current yearly compensation (approximate $USD)?"].notnull()) & 
                 (df["What is your current yearly compensation (approximate $USD
