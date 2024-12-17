import streamlit as st
from streamlit_sortable import sortable

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
        items = [
            f"{c['candidate_name']} ({c['client']}, {c['vacancy']}) - Fee: £{c['fee']}"
            for c in st.session_state['pipeline'][col]
        ]
        updated_items = sortable(items, key=f"sortable_{col}")
        
        # Update session state based on drag-and-drop changes
        if updated_items != items:
            updated_candidates = []
            for item in updated_items:
                name = item.split(" ")[0]
                candidate_data = next(c for c in st.session_state['pipeline'][col] if c["candidate_name"] == name)
                updated_candidates.append(candidate_data)
            st.session_state['pipeline'][col] = updated_candidates
        
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
