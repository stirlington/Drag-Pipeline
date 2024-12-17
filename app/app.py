import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for candidates
if 'candidates' not in st.session_state:
    st.session_state.candidates = []

# Function to add a candidate
def add_candidate(name, salary, client, vacancy, fee, invoice_month):
    candidate = {
        'Name': name,
        'Salary': salary,
        'Client': client,
        'Vacancy': vacancy,
        'Fee': fee,
        'Status': 'Interview',  # Default status
        'Invoice Month': invoice_month
    }
    st.session_state.candidates.append(candidate)

# Function to calculate totals for each column
def calculate_totals():
    totals = {column: 0 for column in columns}
    for candidate in st.session_state.candidates:
        totals[candidate['Status']] += candidate['Fee']
    return totals

# Function to delete a candidate
def delete_candidate(index):
    del st.session_state.candidates[index]

# Streamlit UI
st.title("Recruitment Pipeline")

# Input form for candidate details
with st.form(key='candidate_form'):
    name = st.text_input("Candidate Name")
    salary = st.number_input("Salary", min_value=0)
    client = st.text_input("Client Name")
    vacancy = st.text_input("Vacancy")
    fee = st.number_input("Fee", min_value=0)
    
    # Dropdown for expected invoice month
    months = [datetime(2023, m, 1).strftime("%B") for m in range(1, 13)]
    invoice_month = st.selectbox("Expected Invoice Month", months)
    
    submit_button = st.form_submit_button("Add Candidate")

    if submit_button:
        add_candidate(name, salary, client, vacancy, fee, invoice_month)
        st.success("Candidate added!")

# Define columns
columns = ['Interview', 'Offer', 'Started/Invoiced', 'Paid']
totals = calculate_totals()

# Create columns for drag and drop
for column in columns:
    with st.container():
        st.subheader(column)
        st.write(f"Total Fee: ${totals[column]}")  # Display total fee for the column
        if column in [candidate['Status'] for candidate in st.session_state.candidates]:
            candidates_in_column = [candidate for candidate in st.session_state.candidates if candidate['Status'] == column]
            for index, candidate in enumerate(candidates_in_column):
                candidate_box = st.empty()
                candidate_box.markdown(f"**{candidate['Name']}**\nSalary: {candidate['Salary']}\nClient: {candidate['Client']}\nVacancy: {candidate['Vacancy']}\nFee: {candidate['Fee']}\nExpected Invoice Month: {candidate['Invoice Month']}")
                
                # Button to delete the candidate
                if st.button("Delete", key=f"delete_{index}"):
                    delete_candidate(index)
                    st.experimental_rerun()  # Refresh the app to update the list

                # Button to move to the next stage
                if st.button("Move to Next Stage", key=f"move_{index}"):
                    # Move candidate to the next stage
                    next_index = (columns.index(column) + 1) % len(columns)
                    st.session_state.candidates[index]['Status'] = columns[next_index]
                    st.experimental_rerun()  # Refresh the app to update totals

# Display all candidates in a separate section
st.write("All Candidates with Expected Invoice Month:")
if st.session_state.candidates:
    candidates_df = pd.DataFrame(st.session_state.candidates)
    st.dataframe(candidates_df[['Name', 'Client', 'Vacancy', 'Fee', 'Invoice Month']])
else:
    st.write("No candidates added yet.")
