import streamlit as st

st.title("XML Generator")

# Create a text input box
root_element = st.text_input("Enter the root element name:", "MyRoot")

# Create a button that triggers the code block below
if st.button("Generate XML"):
    # Your Python logic
    xml_string = f"<{root_element}>\n  <child>Data</child>\n</{root_element}>"
    
    # Show the code on screen
    st.code(xml_string, language="xml")
    
    # Streamlit has a built-in download button!
    st.download_button(
        label="Download XML File",
        data=xml_string,
        file_name="output.xml",
        mime="application/xml"
    )