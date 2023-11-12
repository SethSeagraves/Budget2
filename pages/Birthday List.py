import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Birthday LIst", page_icon = ":money_with_wings:", layout = "wide")

def main_page():
    left_col, right_col = st.columns([1,2])

    df = pd.read_csv("pages/Birthday List Data/BirthdayList.csv") 

    with left_col:
        st.title("Add New Item")

        name = st.text_input("Item Name")
        cost = st.number_input("Cost")
        link = st.text_input("Link")

        submit_button = st.button("Submit")

        if submit_button:
            new_item = {"Item": name, "Cost": cost, "Link": link}
            df = pd.concat([df, pd.DataFrame([new_item])], ignore_index = True)

            df.to_csv("pages/Birthday List Data/BirthdayList.csv", index = False)
            

    total_cost = sum(df.loc[:,"Cost"].values)

    with right_col:
        st.header("Total Cost: ${}".format(total_cost))

        st.dataframe(df, use_container_width = True)

        # --- Delete prompt ---
        st.title("Remove Item")

        # --- Input for which row needs to be deleted from the wishlist ---
        row_number = int(st.number_input("Item Row Number", value = 0))

        # --- Delete button ---
        delete_button = st.button("Remove")

        # --- Conditions when the delete button is pressed ---
        if delete_button:
            # --- Deletes the row number the user inputed from the wishlist using the drop function ---
            df.drop([row_number], axis = 0, inplace = True)

            # --- Saves the new dataframe as the wishlist csv ---
            df.to_csv("pages/Birthday List Data/BirthdayList.csv", index = False) 

            # --- Refreshes the window (kind of) to update the dataframe shown on the screen ---
            st.experimental_rerun()

if __name__ == "__main__":
    main_page()

