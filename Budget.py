import streamlit as st

import pandas as pd
from datetime import datetime
import yaml as yml
from Budget_Support import *
import os
import csv

# --- Get the time and date of the purhase entry ---
day = datetime.now().strftime("%d")
month = datetime.now().strftime("%m")
year = datetime.now().strftime("%Y")
time = datetime.now().strftime("%H:%M:%S")

st.set_page_config(page_title = "Budget Tracker", page_icon = ":money_with_wings:", layout = "wide")

def main_page():
    if os.path.exists("Budgeting Web App Data/purchases {}{}.csv".format(month, year)):
        # --- Set up CSV file to store purchases ---
        # df = pd.read_csv("Budgeting Web App Data/purchases {}{}.csv".format(month, year)) # Windows
        # df = pd.read_csv("/media/sseagraves0513/Seth's USB/Work Computer/Documents/Python Code/Websites/Budgeting Web App/Budgeting Web App Data/purchases {}{}.csv".format(month, year)) # Raspberry Pi
        df = pd.read_csv("Budgeting Web App Data/purchases {}{}.csv".format(month, year)) # Mac
    else: # --- Create a new file for the new month
        with open("Budgeting Web App Data/purchases {}{}.csv".format(month, year), 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Month", "Day", "Year", "Time", "Purchaser", "Category", "Place", "Amount", "Notes"])
        df = pd.read_csv("Budgeting Web App Data/purchases {}{}.csv".format(month, year)) # Mac

    with open("config.yml", "r") as f:
        config = yml.load(f, Loader = yml.FullLoader)

    left_column, right_column = st.columns((2,5)) # size of each column is 2/5th of the screen width (this is better than 1/3)
    with left_column:
        # --- Column Title ---
        st.title("Enter Purchase Amount")

        # --- Category and purchase options session states to initialize drop down menus ---
        if "category_option" not in st.session_state:
            st.session_state.category_option = ""

        if "purchase_place" not in st.session_state:
            st.session_state.purchase_category = ""

        # --- Purchase Category Dropdown ---
        categories_list = list(config.keys())
        category = st.selectbox("Category", categories_list, key = "category_option")

        # --- Initialize purchase place so if statements work correctly ---
        purchase_place = None
        if category != "":
            purchase_place = st.selectbox("Entery Purchase Type", config[category])

        # --- New purchase place entry ---
        new_entry = 0
        if purchase_place == "New Entry":
            new_entry = st.text_input("Enter New Entry")
            purchase_place = new_entry

        # --- Purchase amount field ---
        purchase_amount = st.number_input("Amount")

        # --- Select the purchaser ---
        purchaser = st.radio("Select Purchaser", ["Alexa", "Seth", "Both"], horizontal = True)

        # --- Notes text entry field ---
        notes = st.text_input("Notes")

        # --- Submit button
        submit_button = st.button("Submit")

        # --- Adds "new_data" to csv file when submit button is pushed
        if submit_button:
            new_data = {"Month": month, "Day": day, "Year": year, "Time": time, "Purchaser": purchaser, "Category": category, "Place": purchase_place, "Amount": purchase_amount, "Notes": notes}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index = True)
            df.to_csv("Budgeting Web App Data/purchases {}{}.csv".format(month, year), index = False)
            if new_entry:
                with open("onfig.yml") as f:
                    config = yml.load(f, Loader = yml.FullLoader)
                    config[category].append(new_entry)
                with open("config.yml", 'w') as f:
                    yml.dump(config, f)

            st.success("Purchase Entry Complete!")

        st.markdown("""___""")
      
        # display_pi_chart(list_of_purchase_totals)
        budget_projection = st.toggle("Show Budget Projection Info", value = False)
    
    if budget_projection:
        projected_budget_right_column(df, right_column)
    else:
        default_budget_right_column(df, right_column)

if __name__ == "__main__":
    # if "logged_in" not in st.session_state:
    #     st.session_state.logged_in = False  # Initialize the session state variable
    # login() if not st.session_state.logged_in else main_page()
    main_page()