import streamlit as st
import pandas as pd
from statistics import mean
from datetime import datetime

def display_distance_bar_chart(current_df):
    current_month = st.toggle("Current Month Data", value = True)

    ret = current_df

    if current_month:
        st.header("Distance Traveled Per Destination")
        temp_df = pd.DataFrame(columns = ["Date", "Work", "Home", "Errand", "Food"])
        work_distance = []
        home_distance = []
        errand_distance = []
        food_distance = []
        dates = []

        for index, row in current_df.iterrows():
            if row["Destination"] == "Work":
                work_distance.append(row["Distance"])
                home_distance.append(0)
                errand_distance.append(0)
                food_distance.append(0)
            elif row["Destination"] == "Home":
                work_distance.append(0)
                home_distance.append(row["Distance"])
                errand_distance.append(0)
                food_distance.append(0)
            elif row["Destination"] == "Errand":
                work_distance.append(0)
                home_distance.append(0)
                errand_distance.append(row["Distance"])
                food_distance.append(0)
            elif row["Destination"] == "Food":
                work_distance.append(0)
                home_distance.append(0)
                errand_distance.append(0)
                food_distance.append(row["Distance"])
            dates.append(row["Date"])

        df_data = {"Date": dates, "Work": work_distance, "Home": home_distance, "Errand": errand_distance, "Food": food_distance}

        temp_df = pd.DataFrame(df_data, columns = ["Date", "Work", "Home", "Errand", "Food"])
        temp_df.set_index("Date", inplace = True)

        st.bar_chart(temp_df)
    else:
        left_column, right_column = st.columns((2,2))

        with left_column:
            month = st.selectbox("Select Month", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index = datetime.now().month - 1)
        with right_column:
            year = st.selectbox("Select Year", ["2023"])

        df = pd.read_csv("pages/TripData {}{}.csv".format(month, year))
        ret = df

        st.header("Distance Traveled Per Destination")
        temp_df = pd.DataFrame(columns = ["Date", "Work", "Home", "Errand", "Food"])
        work_distance = []
        home_distance = []
        errand_distance = []
        food_distance = []
        dates = []

        for index, row in df.iterrows():
            if row["Destination"] == "Work":
                work_distance.append(row["Distance"])
                home_distance.append(0)
                errand_distance.append(0)
                food_distance.append(0)
            elif row["Destination"] == "Home":
                work_distance.append(0)
                home_distance.append(row["Distance"])
                errand_distance.append(0)
                food_distance.append(0)
            elif row["Destination"] == "Errand":
                work_distance.append(0)
                home_distance.append(0)
                errand_distance.append(row["Distance"])
                food_distance.append(0)
            elif row["Destination"] == "Food":
                work_distance.append(0)
                home_distance.append(0)
                errand_distance.append(0)
                food_distance.append(row["Distance"])
            dates.append(row["Date"])

        df_data = {"Date": dates, "Work": work_distance, "Home": home_distance, "Errand": errand_distance, "Food": food_distance}

        temp_df = pd.DataFrame(df_data, columns = ["Date", "Work", "Home", "Errand", "Food"])
        temp_df.set_index("Date", inplace = True)

        st.bar_chart(temp_df)

    return ret



def display_mpg_bar_chart(df):
    st.header("Average MPG Per Destination")
    temp_df = pd.DataFrame(columns = ["Destination", "MPG"])
    work_distance = []
    home_distance = []
    errand_distance = []
    food_distance = []
    dates = []

    for index, row in df.iterrows():
        if row["Destination"] == "Work":
            work_distance.append(row["MPG"])
        elif row["Destination"] == "Home":
            home_distance.append(row["MPG"])
        elif row["Destination"] == "Errand":
            errand_distance.append(row["MPG"])
        elif row["Destination"] == "Food":
            food_distance.append(row["MPG"])
        dates.append(row["Date"])

    if len(work_distance) < 1:
        work_distance.append(0)
    if len(home_distance) < 1:
        home_distance.append(0)
    if len(errand_distance) < 1:
        errand_distance.append(0)
    if len(food_distance) < 1:
        food_distance.append(0)

    temp_df = pd.DataFrame([mean(work_distance), mean(home_distance), mean(errand_distance), mean(food_distance)], ["Work", "Home", "Errand", "Food"])

    st.bar_chart(temp_df)