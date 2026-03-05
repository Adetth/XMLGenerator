import streamlit as st
import time

st.title("XML Generation Speed Test: Streamlit")
st.write("This application runs Python on a backend server.")

# The input controls
num_records = st.number_input("Number of EPM Form Nodes to Generate:", min_value=1000, value=250000, step=10000)

if st.button("Start Benchmark"):
    st.info("Generating XML payload... Please wait.")
    
    # --- EXACT SAME PYTHON LOGIC ---
    start_time = time.time()
    
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n<EPM_Forms>\n'
    for i in range(int(num_records)):
        xml_string += f"""  <Form name="Banking_Rule_{i}">
    <DataGrid>
      <Dimensions>
        <Dim name="Account">EPM_Acc_{i % 100}</Dim>
        <Dim name="Period">Jan</Dim>
        <Dim name="Year">FY26</Dim>
      </Dimensions>
      <Cell value="{(i * 1234) % 150000}" />
    </DataGrid>
  </Form>\n"""
        
    xml_string += "</EPM_Forms>"
    
    end_time = time.time()
    time_taken = end_time - start_time
    # -------------------------------
    
    st.success(f"Done! Generated {len(xml_string):,} characters in {time_taken:.4f} seconds.")
