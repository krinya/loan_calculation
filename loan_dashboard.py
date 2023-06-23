import streamlit as st
import pandas as pd
import plotly.express as px
template = 'plotly'

# Function to calculate loan data
def loan_amount(principal, rate, term):
    # Calculate monthly interest rate
    monthly_rate = rate / 12
    # Calculate monthly payment using the formula assuming linear payments
    monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** (-term))
    # Initialize remaining principal and total amount
    remaining_principal = principal
    total_amount = 0

    # Initialize data frame
    data = pd.DataFrame()

    # Iterate over loan term and calculate some values for each month
    for month in range(1, term + 1):
        # Calculate interest amount
        interest_amount = remaining_principal * monthly_rate
        # Calculate principal amount
        principal_amount = monthly_payment - interest_amount
        # Update remaining principal and total amount
        remaining_principal = remaining_principal - principal_amount
        total_amount = total_amount + monthly_payment
        # Print the result
        data_one_iter = pd.DataFrame({
            'month': [month],
            'monthly_payment': [monthly_payment],
            'interest_amount': [interest_amount],
            'remaining_principal': [remaining_principal],
            'total_amount': [total_amount]})
        data = pd.concat([data, data_one_iter], ignore_index=True)
    data['interest_monthly_ratio'] = data['interest_amount'] / data['monthly_payment']
    
    return data, total_amount

st.title('Calculate Loan - Dashboard')

col1, col2, col3 = st.columns(3)

with col1:
    principal = st.number_input('Principal amount', min_value=0, value=100000, step=1)
with col2:  
    interes_rate = st.number_input('Interest rate', min_value=0.000, value=0.050, step=0.001)
with col3:
    term = st.number_input('Term (in months)', min_value=0, value=120, step=1)

data, total_amount = loan_amount(principal, interes_rate, term)

# create a line graph with x axis as month and y axis as remaining principal
fig_remining_principal = px.line(data, x='month', y='remaining_principal', template=template)
fig_interest_payed = px.line(data, x='month', y=['interest_amount', 'monthly_payment'], template=template)
fig_interest_payment_ratio = px.line(data, x='month', y='interest_monthly_ratio', template=template)

st.write('Monthly installment: ', round(data['monthly_payment'][0]))
st.write('Total amount payed at the end of the loan period: ', round(total_amount))

show_brake_down = st.checkbox('Show loan breakdown per month')
if show_brake_down:
    st.markdown('## Loan breakdown per month')
    st.dataframe(data)
    # create download button with streamlit, donload the data frame as csv file
    st.download_button(label='Download data', data=data.to_csv(index=False), file_name='loan_breakdown.csv', mime='text/csv')

st.markdown('## Remaining principal over time')
st.plotly_chart(fig_remining_principal, theme=None)

st.markdown('## Monthly installment breakdown per month over time')
st.plotly_chart(fig_interest_payed, theme=None)

st.markdown('## Interest / monthly payment instalment over time')
st.plotly_chart(fig_interest_payment_ratio, theme=None)
