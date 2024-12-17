import streamlit as st
from streamlit_dnd import dnd_container, dnd_item

# Initialize session state for columns
if 'pipeline' not in st.session_state:
    st.session_state['pipeline'] = {
        "Interview": [],
        "Offered": [],
        "Invoiced/Placed": [],
        "Paid": []
    }

# Header
st.title("Recruitment Pipeline")

# Add new candidate form
with st.form("add_candidate"):
    st.subheader("Add Candidate")
    client = st.text_input("Client")
    vacancy = st.text_input("Vacancy")
    candidate_name = st.text_input("Candidate Name")
    salary = st.number_input("Salary", min_value=0)
    fee = st.number_input("Fee", min_value=0)
    column_to_add = st.selectbox("Add to Column", ["Interview", "Offered", "Invoiced/Placed", "Paid"])
    submitted = st.form_submit_button("Add Candidate")

    if submitted:
        new_candidate = {
            "client": client,
            "vacancy": vacancy,
            "candidate_name": candidate_name,
            "salary": salary,
            "fee": fee
        }
        st.session_state['pipeline'][column_to_add].append(new_candidate)
        st.success(f"Candidate {candidate_name} added to {column_to_add}!")

# Display columns with drag-and-drop functionality
columns = list(st.session_state['pipeline'].keys())
totals = {col: 0 for col in columns}

st.subheader("Pipeline")
col1, col2, col3, col4 = st.columns(4)

for i, col in enumerate(columns):
    with [col1, col2, col3, col4][i]:
        st.write(f"### {col}")
        
        # Drag-and-Drop Container
        with dnd_container(key=f"dnd_{col}"):
            for candidate in st.session_state['pipeline'][col]:
                dnd_item(
                    label=f"{candidate['candidate_name']} ({candidate['client']}, {candidate['vacancy']}) - Fee: £{candidate['fee']}",
                    key=f"item_{candidate['candidate_name']}"
                )
        
        # Calculate totals
        totals[col] += sum(c["fee"] for c in st.session_state['pipeline'][col])

# Display totals
st.subheader("Totals")
for col, total in totals.items():
    st.write(f"**{col}: £{total}**")

# Track invoices and payments
st.subheader("Invoice and Payment Tracker")
invoice_tracker = {}
for candidate in st.session_state['pipeline']["Invoiced/Placed"]:
    month = st.selectbox(
        f"Expected Invoice Month for {candidate['candidate_name']} ({candidate['client']})",
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"],
        key=f"invoice_{candidate['candidate_name']}"
    )
    invoice_tracker[candidate["candidate_name"]] = month

st.write(invoice_tracker)
