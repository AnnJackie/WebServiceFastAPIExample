import pandas as pd
import streamlit as st

st.title("Streamlit Commands Example")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is simple preformatted text using st.text.")

st.code("""
def hello_world():
    print("Hello, Streamlit!")

hello_world()
""", language="python")

st.divider()

st.write("This is a simple string using st.write.")
st.write("You can also pass Markdown with **bold** and _italic_ text using st.write.")

data = {
    "Column 1": [1, 2, 3],
    "Column 2": [4, 5, 6],
}
df = pd.DataFrame(data)

st.write("Here is a DataFrame:", df)
st.write("Here is a DataFrame as table:")
st.table(df)
