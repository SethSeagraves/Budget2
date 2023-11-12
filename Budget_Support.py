from cmath import nan
from xxlimited import foo
import streamlit as st

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statistics import mean
import os
import yaml as yml
from datetime import datetime

def login():
    with st.sidebar:
        st.title("Login")

        # Get the user's input for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Check if the username and password are correct
        if username == "admin" and password == "admin":
            st.success("You have successfully logged in!")
            st.session_state.logged_in = True  # Set the session state variable to True
            st.experimental_rerun()  # Rerun the app with the main page
        elif username != "" and password != "":
            st.error("Incorrect username or password")

def update_dropdown2(category, purchase_place, config):
    if category == "Seth's Income":
        purchase_place = st.selectbox("Income Type", config["Seth's Income"])
    elif category == "Alexa's Income":
        purchase_place = st.selectbox("Income Type", config["Alexa's Income"])
    elif category == "Housing":
        purchase_place = st.selectbox("Housing Purchase Type", config["Housing"])
    elif category == "Utilities":
        purchase_place = st.selectbox("Bill Type", config["Utilities"])
    elif category == "Savings":
        purchase_place = st.selectbox("Savings Type", config["Savings"])
    elif category == "Debt":
        purchase_place = st.selectbox("Debt Type", config["Debt"])
    elif category == "Automotive":
        purchase_place = st.selectbox("Automotive Purchase Type", config["Automotive"])
    elif category == "Groceries":
        purchase_place = st.selectbox("Store", config["Groceries"])
    elif category == "Insurance":
        purchase_place = st.selectbox("Insurance Type", config["Insurance"])
    elif category == "Restaurants":
        purchase_place = st.selectbox("Restaurants", config["Restaurants"])
    elif category == "Pet Supplies":
        purchase_place = st.selectbox("Pet Purchase Type", config["Pet Supplies"])
    elif category == "Personal":
        purchase_place = st.selectbox("Personal Purchase Type", config["Personal"])
    elif category == "Dates":
        purchase_place = st.selectbox("Date Type", config["Dates"])
    elif category == "Entertainment":
        purchase_place = st.selectbox("Entertainment Purchase Type", config["Entertainment"])
    elif category == "Mics Necessities":
        purchase_place = st.selectbox("Necessity Type", config["Mics Necessities"])
    elif category == "Gifts":
        purchase_place = st.selectbox("Gift Type", config["Gifts"])
    elif category == "Vacation":
        purchase_place = st.selectbox("Vacation Purchase Type", config["Vacation"])
    elif category == "Medical":
        purchase_place == st.selectbox("Medical Expence Type", config["Medical"])

    return purchase_place

def income_calculations(df):
    # --- Income Variables ---
    total_income = 0
    seth_total_income = 0
    alexa_income_total = 0

    for i in range(len(df)):
        if df.loc[i,"Category"] == "Seth's Income":
            seth_total_income += df.loc[i, "Amount"]
        elif df.loc[i,"Category"] == "Alexa's Income":
            alexa_income_total += df.loc[i, "Amount"]

    total_income = alexa_income_total + seth_total_income

    return seth_total_income, alexa_income_total, total_income

def display_income_info(total_income, seth_total_income, alexa_income_total):
    with st.container():
        st.title("Income")
        column1, column2, column3, column4, column5 = st.columns(5)

        if total_income == 0: # this is to fix the no income issue at the beginning of the month
            total_income = 1
            column1.metric("Total Income", "${:0.2f}".format(0))
            column2.metric("Seth's Total Income", "${:0.2f}".format(0), delta = round(seth_total_income/total_income, 3) * 100)
            column3.metric("Alexa's Total Income", "${:0.2f}".format(0), delta = round(alexa_income_total/total_income, 3) * 100)
        else:
            column1.metric("Total Income", "${:0.2f}".format(total_income))
            column2.metric("Seth's Total Income", "${:0.2f}".format(seth_total_income), delta = round(seth_total_income/total_income, 3) * 100)
            column3.metric("Alexa's Total Income", "${:0.2f}".format(alexa_income_total), delta = round(alexa_income_total/total_income, 3) * 100)
    
def display_purchases_info(total_purchases, total_income, housing_total, utilities_total, debt_total, automotive_total, groceries_total, insurance_total, dates_total, entertainment_total, misc_necessities_total, gifts_total, restaurants_total, pet_supplies_total, personal_total):
    with st.container():
        st.title("Purchases")
        column1, column2, column3, column4, column5 = st.columns(5)

        column1.metric("Total Purchases", "${:0.2f}".format(total_purchases), delta = round(total_purchases/total_income, 3) * 100)
        column2.metric("Housing", "${:0.2f}".format(housing_total), delta = round(housing_total/total_income, 3) * 100)
        column3.metric("Utilities", "${:0.2f}".format(utilities_total), delta = round(utilities_total/total_income, 2) * 100)
        column4.metric("Debt", "${:0.2f}".format(debt_total), delta = round(debt_total/total_income, 3) * 100)
        column5.metric("Automotive", "${:0.2f}".format(automotive_total), delta = round(automotive_total/total_income, 3) * 100)

    with st.container():
        column6, column7, column8, column9, column10 = st.columns(5)

        column6.metric("Groceries", "${:0.2f}".format(groceries_total), delta = round(groceries_total/total_income, 3) * 100)
        column7.metric("Insurance", "${:0.2f}".format(insurance_total), delta = round(insurance_total/total_income, 3) * 100)
        column8.metric("Dates", "${:0.2f}".format(dates_total), delta = round(dates_total/total_income, 3) * 100)
        column9.metric("Entertainment", "${:0.2f}".format(entertainment_total), delta = round(entertainment_total/total_income, 3) * 100)
        column10.metric("Misc Necessities", "${:0.2f}".format(misc_necessities_total), delta = round(misc_necessities_total/total_income, 3) * 100)

    with st.container():
        column11, column12, column13, column14, column15 = st.columns(5)

        column11.metric("Gifts", "${:0.2f}".format(gifts_total), delta = round(gifts_total/total_income, 3) * 100)
        column12.metric("Restaurants", "${:0.2f}".format(restaurants_total), delta = round(restaurants_total/total_income, 3) * 100)
        column13.metric("Pet Supplies", "${:0.2f}".format(pet_supplies_total), delta = round(pet_supplies_total/total_income, 3) * 100)
        column14.metric("Personal", "${:0.2f}".format(personal_total), delta = round(personal_total/total_income, 3) * 100)

def display_savings_info(total_savings, total_income, vacation_total, retirement_total, house_total, car_total, wedding_total, emergency_total):
    with st.container():
        st.title("Savings")
        column1, column2, column3, column4, column5 = st.columns(5)

        column1.metric("Total Savings", "${:0.2f}".format(total_savings), delta = round(total_savings/total_income, 3) * 100)
        column2.metric("Vacation", "${:0.2f}".format(vacation_total), delta = round(vacation_total/total_income, 3) * 100)
        column3.metric("Retirement", "${:0.2f}".format(retirement_total), delta = round(retirement_total/total_income, 3) * 100)
        column4.metric("House", "${:0.2f}".format(house_total), delta = round(house_total/total_income, 3) * 100)
        column5.metric("Car", "${:0.2f}".format(car_total), delta = round(car_total/total_income, 3) * 100)

    with st.container():
        column6, column7, column8, column9, column10 = st.columns(5)

        column6.metric("Wedding", "${:0.2f}".format(wedding_total), delta = round(wedding_total/total_income, 3) * 100)
        column7.metric("Emergency", "${:0.2f}".format(emergency_total), delta = round(emergency_total/total_income, 3) * 100)

def display_pi_chart(list_of_purchase_totals):
    categories = ["Housing", "Utilities", "Debt", "Automotive", "Groceries", "Insurance", "Restaurants", "Pet Supplies", "Personal", "Dates", "Entertainment", "Misc", "Gifts"]
    list_of_purchase_totals = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    arr = np.random.normal(1, 1, size = 100)
    fig, ax = plt.subplot()
    ax.hist(arr, bins = 20)

    st.pyplot(fig)

def purchase_totals_dict(df):
    with open("config.yml") as f:
        config = yml.load(f, Loader = yml.FullLoader)

    categories = list(config.keys())

    totals_dict = {}
    for i in range(len(df)):
        totals_dict[df.loc[i,"Category"]] = 0

    for i in range(len(df)):
        totals_dict[df.loc[i,"Category"]] += df.loc[i,"Amount"]

    return totals_dict

def total_purchase_value(totals_dict):
    exclusion_list = ["Seth's Income", "Alexa's Income", "Insurance"]

    purchases_total = 0
    for category in totals_dict:
        if category not in exclusion_list:
            purchases_total += totals_dict[category]

    return purchases_total

def display_purchases_bar_chart(current_df):
    st.title("Purchases")
    current_month = st.toggle("Current Month Data", value = True)

    if current_month:
        display_categories = purchases_options(current_df)
        purchase_totals = purchase_totals_dict(current_df)

        st.subheader("Total Purchases: ${}".format(round(total_purchase_value(purchase_totals), 2))) # subtract health insurance because it is taken out of paycheck 

        display_dict = {}
        for category in display_categories:
            display_dict[category] = purchase_totals[category]

        st.bar_chart(display_dict, height = 500)

        purchase_list(current_df)

        display_purchase_place_bar_chart(current_df)

    else:
        left_column, right_column = st.columns((2,2))

        with left_column:
            month = st.selectbox("Select Month", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index = datetime.now().month - 1)
        with right_column:
            year = st.selectbox("Select Year", ["2023"])
        
        df = pd.read_csv("Budgeting Web App Data/purchases {}{}.csv".format(month, year)) # Mac)

        display_categories = purchases_options(df)
        purchase_totals = purchase_totals_dict(df)

        st.subheader("Total Purchases: ${}".format(round(total_purchase_value(purchase_totals), 2)))

        display_dict = {}
        for category in display_categories:
            display_dict[category] = purchase_totals[category]

        st.bar_chart(display_dict, height = 500)

        purchase_list(df)

        display_purchase_place_bar_chart(df)

def purchase_list(df):
    show_purchase_list = st.toggle("Show Purchases List", value = False)

    if show_purchase_list:
        st.dataframe(df, use_container_width = True)

def display_saving_bar_chart():
    st.title("Savings")

    with open("savings_config.yml") as f:
        savings_rates = yml.load(f, Loader = yml.Loader)

    total_savings = 0
    retirement_total = 0

    file_dir = "Budgeting Web App Data"

    for filename in os.listdir(file_dir):
        f = os.path.join(file_dir, filename)
        df = pd.read_csv(f)

        for index, row in df.iterrows():
            if row["Category"] == "Savings" and row["Place"] == "Other":
                total_savings += row["Amount"]
            if row["Category"] == "Savings" and row["Place"] == "Retirement":
                retirement_total += row["Amount"]

    adjust_rates = st.toggle("Adjust Savings Rates", value = False)

    if adjust_rates:
        savings_rates["Vacation"][0] = st.slider("Vacation Rate", 1, 100, savings_rates["Vacation"][0])
        savings_rates["House"][0] = st.slider("House Rate", 1, 100, savings_rates["House"][0])
        savings_rates["Car"][0] = st.slider("Car Rate", 1, 100, savings_rates["Car"][0])
        savings_rates["Wedding"][0] = st.slider("Wedding Rate", 1, 100, savings_rates["Wedding"][0])
        savings_rates["Emergency"][0] = st.slider("Emergency Rate", 1, 100, savings_rates["Emergency"][0])

        st.caption("Total Savings Rate: {}%".format(savings_rates["Vacation"][0] + savings_rates["House"][0] + savings_rates["Car"][0] + savings_rates["Wedding"][0] + savings_rates["Emergency"][0]))

        with open("savings_config.yml", "w") as f:
            yml.dump(savings_rates, f)

        
    st.subheader("Total Savings: ${}".format(total_savings))# + retirement_total))

    savings_totals = {"Retirement": retirement_total, "Vacation": savings_rates["Vacation"][0] * .01 * total_savings, "House": savings_rates["House"][0] * .01 * total_savings, "Car": savings_rates["Car"][0] * .01 * total_savings, "Wedding": savings_rates["Wedding"][0] * .01 * total_savings, "Emergency": savings_rates["Emergency"][0] * .01 * total_savings}

    st.bar_chart(savings_totals, height = 500)

def display_purchase_place_bar_chart(df):
    categories = df.loc[:,"Category"].tolist() # Gets a list of all the categories used in the purchases dataframe
    categories = list(set(categories)) # Removes all the duplicate entries in the list of categories
    categories.sort()

    left_column, right_column = st.columns((2,2))
    with left_column:
        category = st.selectbox("Select a Category", categories, index = categories.index("Restaurants")) # set default index to the restaurnats because that's what I look at the most

    places = []
    for index, row in df.iterrows():
        if row["Category"] == category:
            places.append(row["Place"])

    places = list(set(places))

    display_dict = {}
    for place in places:
        display_dict[place] = 0

    places = list(set(places))
    for index, row in df.iterrows():
        for place in places:
            if row["Place"] == place and row["Category"] == category:
                display_dict[place] += row["Amount"]
    
    total = 0
    for place in display_dict:
        total += display_dict[place]

    with right_column:
        st.subheader("Category Total: ${}".format(round(total, 2)))
        
    st.bar_chart(display_dict, height = 500)

def default_budget_right_column(df, right_column):
    with right_column:
            seth_total_income, alexa_income_total, total_income = income_calculations(df)

            display_income_info(total_income, seth_total_income, alexa_income_total)
            st.markdown("""___""")
            display_purchases_bar_chart(df)
            st.markdown("""___""")
            # display_purchases_info(total_purchases, total_income, housing_total, utilities_total, debt_total, automotive_total, groceries_total, insurance_total, dates_total, entertainment_total, misc_necessities_total, gifts_total, restaurants_total, pet_supplies_total, personal_total)        
            # display_savings_info(total_savings, total_income, vacation_total, retirement_total, house_total, car_total, wedding_total, emergency_total)
            display_saving_bar_chart()

def projected_budget_right_column(df, right_column):
    number_of_weeks = 52
    seth_tax_rate = 0.28 # --- governemnt taxes 28% of my money ---
    alexa_tax_rate = 0.15 # --- governemnt takes 15% of alexa's money ---

    seth_number_hours_worked = 50
    seth_hourly_rate = 49.09
    seth_weekly_income = seth_number_hours_worked * seth_hourly_rate
    seth_annual_income = seth_weekly_income * number_of_weeks
    alexa_annual_income = 10000

    total_income_bt = seth_annual_income + alexa_annual_income # --- bt means before tax ---

    seth_annual_income_at = (seth_weekly_income * (1 - seth_tax_rate)) * 52 # --- at means after tax ---
    alexa_annual_income_at = alexa_annual_income * (1 - alexa_tax_rate)
    total_income_at = seth_annual_income_at + alexa_annual_income_at

    seth_monthly_income_at = (seth_annual_income_at / 365) * 30
    alexa_monthly_income_at = alexa_annual_income_at / 12
    total_monthly_income = seth_monthly_income_at + alexa_monthly_income_at

    expenses = {"House Payment": 3720.0, "Groceries": 600.0, "Fuel": 400.0, "Car Insurance": 0.0, "Utilities": 500.0, "Health Insurance": 220.0}
    savings = {"Vacation": 10, "Retirement": 5, "House": 8, "Car": 0, "Wedding": 60, "Emergency": 11}
    savings_amounts = {"Vacation": 0, "Retirement": 0, "House": 0, "Car": 0, "Wedding": 0, "Emergency": 0}

    expenses_catagories = list(expenses.keys())
    savings_catagories = list(savings.keys())

    total_expenses = 0
    for expense in expenses:
        total_expenses += expenses[expense]
    
    remainder_after_expenses = total_monthly_income - total_expenses

    total_savings = 0
    for saving in savings:
        total_savings += (savings[saving] * 0.01) * remainder_after_expenses
        savings_amounts[saving] = (savings[saving] * 0.01) * remainder_after_expenses

    spending_money = total_monthly_income - total_expenses - total_savings

    with right_column:
        st.markdown("""___""")
        st.title(":green[Income]")
        left_I, right_I = st.columns(2)
        with left_I:
            st.header("Seth's Income")
            st.subheader("Annual Income: $:green[{}]".format(round(seth_annual_income, 2)))
            st.subheader("Annual Income (After Tax): $:green[{}]".format(round(seth_annual_income_at, 2)))
            st.subheader("Monthly Income: $:green[{}]".format(round(seth_monthly_income_at, 2)))
        with right_I:
            st.header("Alexa's Income")
            st.subheader("Annual Income: $:green[{}]".format(round(alexa_annual_income, 2)))
            st.subheader("Annual Income (After Text: $:green[{}]".format(round(alexa_annual_income_at, 2)))
            st.subheader("Monthly Income: $:green[{}]".format(round(alexa_monthly_income_at, 2)))
        st.markdown("""___""")

        st.title(":red[Expenses]")
        st.bar_chart(expenses, height = 500, color = "#d0312d")
        st.markdown("""___""")

        st.title(":violet[Savings]")
        st.subheader("{}: ${}".format(savings_catagories[0], round(savings_amounts["Vacation"], 2)))
        st.subheader("{}: ${}".format(savings_catagories[1], round(savings_amounts["Retirement"], 2)))
        st.subheader("{}: ${}".format(savings_catagories[2], round(savings_amounts["House"], 2)))
        st.subheader("{}: ${}".format(savings_catagories[3], round(savings_amounts["Car"], 2)))
        st.subheader("{}: ${}".format(savings_catagories[4], round(savings_amounts["Wedding"], 2)))
        st.subheader("{}: ${}".format(savings_catagories[5], round(savings_amounts["Emergency"], 2)))

def purchases_options(df):
    categories = df.loc[:,"Category"].tolist()
    categories = list(set(categories))

    default_categories = ["Automotive", "Dates", "Debt", "Entertainment", "Gifts", "Groceries", "Insurance", "Misc Necessities", "Personal", "Pet Supplies", "Restaurants", "Utilities", "Savings", "Medical"]

    default_categories2 = []
    for category in default_categories:
        if category in categories:
            default_categories2.append(category)

    display_categories = st.multiselect("Select Purchase Categories", categories, default = default_categories2)

    return display_categories
          



