import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Wish List", page_icon = ":money_with_wings:", layout = "wide")

def main_page():
    # --- Horizontal line at the top ---
    st.markdown("""---""")

    # --- Read in csv wishlist file as a pandas dataframe ---
    df = pd.read_csv("pages/Wish List Data/WishList.csv")

    # --- Set up the two column configuration with different sizes ---
    left_col, right_col = st.columns([1,2])

    # --- Things inside the left column ---
    with left_col:
        # --- Title ---
        st.title("Input New Purchase Item")

        # --- Input fields to add a new item to the wish list (different types of values) ---
        item_name = st.text_input("Item")
        quantity = int(st.number_input("Quantity", value = 0))
        approximate_price = st.number_input("Approximate Price")
        price = st.number_input("Price")
        necessity = st.number_input("Necessity (1-10)", value = 0)
        link = st.text_input("Link")

        # --- Submit button ---
        submit_button = st.button("Submit")

        # --- THings to be done when the submit button is pressed ---
        if submit_button:
            # --- Initializes a dictionary to append the new values to the wishlist csv file
            new_item = {"Purchase Item": item_name, "Quantity": quantity, "Approximate Price": approximate_price, "Price": price, "Necessity (1-10)": necessity, "Link": link}
            # df = df.append(new_item, ignore_index = True)
            df = pd.concat([df, pd.DataFrame([new_item])], ignore_index = True)

            # --- Writes the newly appended dataframe so it saves the new values ---
            df.to_csv("pages/Wish List Data/WishList.csv", index = False)

    # --- Calculates the sum of the approximate and actual prices of the items in the wishlist ---
    total_approximate = sum(df.loc[:,"Approximate Price"].values)
    total_price = sum(df.loc[:,"Price"].values)

    # --- Uses the query function for a dataframe to get the values in a row that meet a condition in seperate columns ---
    total_approximate_necessity_price = sum(df.query("Necessity >= 8")["Approximate Price"])
    total_necessity_price = sum(df.query("Necessity >= 8")["Price"])

    with right_col:
        # --- Write the totals for different conditions ---
        st.subheader("Total Approximate Price: ${}0".format(total_approximate))
        st.subheader("Total Actual Price: ${}0".format(total_price))
        st.subheader("Total Approximate Necessity Price: ${}0".format(total_approximate_necessity_price))
        st.subheader("Total Actual Necessity Price: ${}0".format(total_necessity_price))

        # --- Shows the wishlist dataframe on the website
        st.dataframe(df, use_container_width = True)

        # --- Delete prompt ---
        st.title("Delete Item")

        # --- Input for which row needs to be deleted from the wishlist ---
        row_number = int(st.number_input("Item Row Number", value = 0))

        # --- Delete button ---
        delete_button = st.button("Delete")

        # --- Conditions when the delete button is pressed ---
        if delete_button:
            # --- Deletes the row number the user inputed from the wishlist using the drop function ---
            df.drop([row_number], axis = 0, inplace = True)

            # --- Saves the new dataframe as the wishlist csv ---
            df.to_csv("pages/Wish List Data/WishList.csv", index = False)

            # --- Refreshes the window (kind of) to update the dataframe shown on the screen ---
            st.experimental_rerun()
        
# --- Login function ---
def login():
    # --- Makes the login stuff in the sidebar ---
    with st.sidebar:
        # --- Login title ---
        st.title("Login")

        # --- Get the user's input for username and password ---
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # --- Check if the username and password are correct ---
        if username == "admin" and password == "admin":
            st.success("You have successfully logged in!")
            st.session_state.logged_in = True  # Set the session state variable to True
            st.experimental_rerun()  # Rerun the app with the main page
        elif username != "" and password != "":
            st.error("Incorrect username or password")

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Initialize the session state variable
    login() if not st.session_state.logged_in else main_page()
