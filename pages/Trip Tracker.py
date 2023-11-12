import streamlit as st
import pandas as pd
from datetime import datetime
from Trip_Tracker_Support import *
import os
import csv

# --- Get the time and date of the purhase entry ---
month = datetime.now().strftime("%m")
year = datetime.now().strftime("%Y")

st.set_page_config(page_title = "Trip Tracker", page_icon = ":money_with_wings:", layout = "wide")

def main_page():
    if os.path.exists("pages/Trip Tracker Data/TripData {}{}.csv".format(month, year)):
        df = pd.read_csv("pages/Trip Tracker Data/TripData {}{}.csv".format(month, year))
    else:
        with open("pages/Trip Tracker Data/TripData {}{}.csv".format(month, year), 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Distance", "Destination", "MPG"])
        df = pd.read_csv("pages/Trip Tracker Data/TripData {}{}.csv".format(month, year)) 

    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.title("Enter Trip Distance")

        date = st.date_input("Trip Data")
        distance = st.number_input("Trip Distance")
        destination = st.radio("Trip Destination", ("Work", "Home", "Errand", "Food"))
        mpg = st.number_input("MPG")

        submit_button = st.button("Submit")

        if submit_button:
            new_trip = {"Date": date, "Distance": distance, "Destination": destination, "MPG": mpg}
            df = pd.concat([df, pd.DataFrame([new_trip])], ignore_index = True)

            df.to_csv("pages/Trip Tracker Data/TripData {}{}.csv".format(month, year), index = False)

            st.success("Purchase Entry Complete!")
        
        st.markdown("""___""")

        dataframe = display_distance_bar_chart(df)

    total_distance = sum(df.loc[:,"Distance"].values)

    with right_col:
        st.header("Total Distance Traveled: {} miles".format(round(total_distance, 1)))

        st.dataframe(df, use_container_width = True)

        display_mpg_bar_chart(dataframe)


if __name__ == "__main__":
    main_page()