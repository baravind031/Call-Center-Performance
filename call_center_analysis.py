import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '1Dec to 3Jan Consultations.csv'
data = pd.read_csv(file_path)

# Display the column names for debugging
st.write('### Column Names')
st.write(data.columns)

# Title and Introduction
st.title('Call Center Performance Analysis')
st.write('Analysis of call center data from 1 Dec to 3 Jan.')

# Data Exploration
st.header('Task 1: Data Exploration')
st.write('### Summary Statistics')
key_numeric_columns = ['amount', 'timeDuration']
summary_statistics = data[key_numeric_columns].describe()
st.write(summary_statistics)

st.write('### Histogram of Call Charges')
plt.figure(figsize=(10, 6))
plt.hist(data['amount'].dropna(), bins=50, color='skyblue', edgecolor='black')
plt.title('Distribution of Call Charges')
plt.xlabel('Charge Amount')
plt.ylabel('Frequency')
st.pyplot(plt)

# Task 2: Call Center Performance Metrics
st.header('Task 2: Call Center Performance Metrics')
st.write('### Average TalkTime for Different Call Activities')
average_talktime_by_activity = data.groupby('consultationType')['timeDuration'].mean().reset_index()
average_talktime_by_activity.columns = ['Activity', 'AverageTalkTime']
st.write(average_talktime_by_activity)

st.write('Most Common Source of Calls')
most_common_source = data['source'].value_counts().idxmax()
st.write(f'The most common source of calls is: {most_common_source}')

st.write('Total Earnings and Spending')
total_earnings_users = data['amount'].sum()
total_spending_masters = data['astrologersEarnings'].sum()
st.write(f'Total earnings for users: {total_earnings_users}')
st.write(f'Total spending for masters: {total_spending_masters}')

highest_earning_user = data.loc[data['astrologersEarnings'].idxmax(), ['gid', 'guruName', 'amount', 'consultationType', 'timeDuration']]
st.write(f'Highest Earning User: {highest_earning_user}')

st.write('Relationship Between TalkTime and Charge')
correlation = data['timeDuration'].corr(data['amount'])
st.write(f'The correlation between TalkTime and Charge is: {correlation}')

# Task 3: Call Handling Analysis
st.header('Task 3: Call Handling Analysis')
st.write('Average Connection Time')
if 'connectTime' in data.columns and 'dialTime' in data.columns:
    data['connectTime'] = pd.to_datetime(data['connectTime'])
    data['dialTime'] = pd.to_datetime(data['dialTime'])
    data['connectionTime'] = (data['connectTime'] - data['dialTime']).dt.total_seconds()
    average_connection_time = data['connectionTime'].mean()
    st.write(f'The average connection time is: {average_connection_time} seconds')  
else:  
    st.write('connectTime or dialTime column is missing.')

st.write('Most Common Reason for Call Disconnection')
if 'unconnectTime' in data.columns and 'connectTime' in data.columns:
    data['unconnectTime'] = pd.to_datetime(data['unconnectTime'])
    data['disconnectionTime'] = (data['unconnectTime'] - data['connectTime']).dt.total_seconds()
    most_common_disconnection_reason = data['disconnectedBy'].value_counts().idxmax()
    st.write(f'The most common reason for call disconnection is: {most_common_disconnection_reason}')
else:
    st.write('unconnectTime or connectTime column is missing.')

st.write('HangUpTime Patterns')
if 'disconnectedBy' in data.columns:
    hangup_patterns = data['disconnectedBy'].value_counts()
    st.write(hangup_patterns)
else:
    st.write('hangUpTime column is missing.')

st.write('### Total calls based on astrologerCallStatus')
if 'astrologerCallStatus' in data.columns:
    astrologerCallStatus = data['astrologerCallStatus'].value_counts()
    st.write(astrologerCallStatus)
else:
    st.write('astrologerCallStatus column is missing.')

# Task 4: Order and Refund Analysis
st.header('Task 4: Order and Refund Analysis')
st.write('### Order Status Distribution')
if 'orderStatus' in data.columns:
    order_status_distribution = data['orderStatus'].value_counts()
    st.write(order_status_distribution)
else:
    st.write('orderStatus column is missing.')

st.write('### Total Refund Amount and Refund Status Distribution')
if 'amount' in data.columns and 'refundStatus' in data.columns:
    total_refund_amount = data['amount'].sum()
    refund_status_distribution = data['refundStatus'].value_counts()
    st.write(f'Total refund amount: {total_refund_amount}')
    st.write(refund_status_distribution)
else:
    st.write('refundAmount or refundStatus column is missing.')

# Task 6: Additional Visualizations
st.header('Task 6: Additional Visualizations')
st.write('### Trend in Call Charges Over Time')
if 'createdAt' in data.columns:
    data['createdAt'] = pd.to_datetime(data['createdAt'])
    data.set_index('createdAt', inplace=True)
    daily_charges = data['amount'].resample('D').sum()
    plt.figure(figsize=(10, 6))
    plt.plot(daily_charges.index, daily_charges.values, marker='o', linestyle='-')
    plt.title('Trend in Call Charges Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Charges')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.write('createdAt column is missing.')

st.write('### Relationship Between TalkTime and UserSpend')
if 'timeDuration' in data.columns and 'amount' in data.columns:
    plt.figure(figsize=(10, 6))
    plt.scatter(data['timeDuration'], data['amount'], alpha=0.5)
    plt.title('Relationship between TalkTime and UserSpend')
    plt.xlabel('TalkTime')
    plt.ylabel('UserSpend')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.write('timeDuration or amount column is missing.')
