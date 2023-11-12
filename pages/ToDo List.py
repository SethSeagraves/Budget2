from turtle import left
import streamlit as st
import pandas as pd

st.set_page_config(page_title = "ToDo List", page_icon = ":money_with_wings", layout = "wide")

def main_page():
    left_col, right_col = st.columns([1, 2])

    df = pd.read_csv("pages/ToDo List Data/ToDoList.csv") 

    with left_col:
        st.title("Add New Item")

        name = st.text_input("Item Name")
        time_estimate = st.slider("Time Estimate (in hours)", 1, 10, 0)
        priority = st.slider("Priority", 1, 10, 3)

        submit_button = st.button("Submit")

        if submit_button:
            new_item = {"Item": name, "Time Estimate": time_estimate, "Priority": priority}
            df = pd.concat([df, pd.DataFrame([new_item])], ignore_index = True)

            df.to_csv("pages/ToDo List Data/ToDoList.csv", index = False)

    with right_col:
        st.header("ToDo Items")

        st.dataframe(df, use_container_width = True)

        # --- Delete prompt ---
        st.title("Remove Item")

        # --- Input for which row needs to be deleted from the todo list ---
        row_number = int(st.number_input("Item Row Number", value = 0))

        # --- Delete button ---
        delete_button = st.button("Remove")

        # --- Conditions when the delete button is pressed ---
        if delete_button:
            # --- Deletes the row number the user inputted from the todo list using the drop function ---
            df.drop([row_number], axis = 0, inplace = True)

            # --- Saves the new dataframe as the todo list csv ---
            df.to_csv("pages/ToDo List Data/ToDoList.csv", index = False)

            # --- Refreshes the window (kind of) to update the dataframe shown on the screen ---
            st.experimental_rerun()

if __name__ == "__main__":
    main_page()