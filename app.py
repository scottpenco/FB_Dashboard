import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data.csv")[:761]

# Preprocess data
df['CTR'] = df['clicks'] / df['impressions']
df['Conversion Rate'] = df['approved_conversion'] / df['clicks'].replace(0, 1)

# Define colors
color_map = {'M': 'lightblue', 'F': 'pink'}
metrics = ['spent', 'clicks', 'total_conversion']

# Title and context
st.title("📊 Facebook A/B Testing Results by Gender")
st.markdown("""
This dashboard analyzes performance data from a Facebook advertising A/B test campaign.
We compare metrics across **gender segments** to understand behavior and trends.
""")

st.subheader("🔍 Metric Relationships by Campaign (Campaign IDs: 1178, 936, 916)")

cols_to_plot = ['impressions', 'clicks', 'spent', 'total_conversion', 'approved_conversion']
df['campaign_id'] = df['campaign_id'].astype(str)
target_campaigns = ['1178', '936', '916']

# Filter and clean
subset = df[df['campaign_id'].isin(target_campaigns)][cols_to_plot + ['campaign_id']]
subset = subset.dropna(subset=cols_to_plot)

# Only proceed if data exists
if not subset.empty:
    num_metrics = len(cols_to_plot)
    fig = make_subplots(
        rows=num_metrics,
        cols=num_metrics,
        shared_xaxes=True,
        shared_yaxes=True,
        horizontal_spacing=0.01,
        vertical_spacing=0.01
    )

    # Set distinct campaign colors
    campaign_colors = {
        '1178': '#636EFA',  # Blue
        '936': '#EF553B',   # Red
        '916': '#00CC96'    # Green
    }

    # Add scatter plots (lower triangle only)
    for i in range(num_metrics):
        for j in range(i):
            x_col = cols_to_plot[j]
            y_col = cols_to_plot[i]
            for campaign_id in target_campaigns:
                campaign_data = subset[subset['campaign_id'] == campaign_id]
                fig.add_trace(
                    go.Scattergl(
                        x=campaign_data[x_col],
                        y=campaign_data[y_col],
                        mode='markers',
                        marker=dict(color=campaign_colors[campaign_id], opacity=0.5, size=6),
                        name=campaign_id,
                        showlegend=(i == num_metrics - 1 and j == 0)  # show legend only once
                    ),
                    row=i+1,
                    col=j+1
                )

            # Set axis titles for outer plots
            if j == 0:
                fig.update_yaxes(title_text=y_col, row=i+1, col=j+1)
            if i == num_metrics - 1:
                fig.update_xaxes(title_text=x_col, row=i+1, col=j+1)

    # Update layout
    fig.update_layout(
        height=1200,
        width=1200,
        title_text="Pairwise Metric Relationships by Campaign (Lower Triangle)",
        showlegend=True,
        legend_title="Campaign ID",
        margin=dict(t=80, l=20, r=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=False)
else:
    st.warning("No data available for the selected campaigns and metrics.")



# Metrics Overview
st.subheader("🔢 Key Metrics by Gender")
grouped = df.groupby('gender').agg({
    'clicks': 'sum',
    'impressions': 'sum',
    'spent': 'sum',
    'approved_conversion': 'sum'
}).reset_index()
grouped['CTR'] = grouped['clicks'] / grouped['impressions']
grouped['Conversion Rate'] = grouped['approved_conversion'] / grouped['clicks'].replace(0, 1)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Clicks (M/F)", f"{grouped['clicks'][1]} / {grouped['clicks'][0]}")
    st.metric("Total Spend (M/F)", f"${grouped['spent'][1]:.2f} / ${grouped['spent'][0]:.2f}")
with col2:
    st.metric("CTR (M/F)", f"{grouped['CTR'][1]*100:.2f}% / {grouped['CTR'][0]*100:.2f}%")
    st.metric("Conversion Rate (M/F)", f"{grouped['Conversion Rate'][1]*100:.2f}% / {grouped['Conversion Rate'][0]*100:.2f}%")

# Prepare grouped data for plotting
stacked_data = df.groupby(['campaign_id', 'gender'])[metrics].sum().reset_index()
campaign_ids = stacked_data['campaign_id'].unique()



# Create subplots: one for each metric
fig = make_subplots(
    rows=1,
    cols=len(metrics),
    subplot_titles=[f"{metric.capitalize()} per Campaign" for metric in metrics],
    shared_yaxes=False
)

for col_index, metric in enumerate(metrics, start=1):
    for gender in ['M', 'F']:
        gender_data = stacked_data[stacked_data['gender'] == gender]
        fig.add_trace(
            go.Bar(
                x=gender_data['campaign_id'],
                y=gender_data[metric],
                name=f"{gender} - {metric}",
                marker_color=color_map[gender],
                showlegend=(col_index == 1)  # Only show legend once
            ),
            row=1,
            col=col_index
        )

    fig.update_xaxes(title_text="Campaign ID", row=1, col=col_index)
    fig.update_yaxes(title_text=metric.capitalize(), row=1, col=col_index)

# Layout tweaks
fig.update_layout(
    height=500,
    width=1200,
    title_text="📊 Campaign Metrics by Gender (Stacked Bars)",
    barmode='stack',
    legend_title="Gender",
    margin=dict(t=60, l=40, r=20, b=40)
)

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""1. Males (M) accounted for majority of ad spending across all campaigns.
2. Campaign 1178 has the highest spent with alot allocated to M. 
3. Female spending remains low across all campaigns. 
4. Females show lower engagement in clicks and conversion rates but still remain stable across campaigns.
Futher investigation on why males show significantly higher engagement and coversion rate should be explored.""")


st.subheader("""A/B testing between genders""")
# Row: CTR by Gender
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 CTR Distribution by Gender")
    fig_ctr = px.box(df, x='gender', y='CTR', color='gender', color_discrete_map=color_map)
    fig_ctr.update_layout(showlegend=False)
    st.plotly_chart(fig_ctr, use_container_width=True)

# Row: Conversion Rate by Gender
with col2:
    st.subheader("🎯 Conversion Rate by Gender")
    fig_conv = px.box(df, x='gender', y='Conversion Rate', color='gender', color_discrete_map=color_map)
    fig_conv.update_layout(showlegend=False)
    st.plotly_chart(fig_conv, use_container_width=True)

st.markdown("""**Hypotheses:**

- **H₀ (Null Hypothesis):** There is no difference in the distribution of Click-Through Rates (CTR) between male and female users.
- **H₁ (Alternative Hypothesis):** There is a difference in the distribution of CTR between male and female users.
""")

st.markdown("""Shapiro-Wilk Test for Male CTR: p-value = **3.988559358954938e-18**""")
st.markdown("""Shapiro-Wilk Test for Female CTR: p-value = **1.8043290664073437e-13**""")

st.markdown("""Failed Normalcy Test, therefore use **ManUWitney** as test statistic.""")


# Row: Campaign performance
st.subheader("📊 Campaign Summary by Gender")
campaign_summary = df.groupby(['campaign_id', 'gender']).agg({
    'clicks': 'sum',
    'spent': 'sum',
    'approved_conversion': 'sum'
}).reset_index()
campaign_summary['Conversion Rate'] = campaign_summary['approved_conversion'] / campaign_summary['clicks'].replace(0, 1)

st.dataframe(campaign_summary)

st.markdown("""Mann-Whitney U Test Results: U-statistic = **50333.5**, p-value = **1.095 × 10⁻⁸**
The CTR difference between male and female is **statistically significant**""")

st.markdown(""" 
✅ Since the p-value is significantly less than 0.05, we **reject the null hypothesis**.  
📊 **Conclusion:** There is a **statistically significant difference** in CTR between male and female users.""")

st.markdown("""#### CTR Analysis by Gender

1. Females(F) have significantly higher CTR than Males (M), suggesting that they egage more with ad content compared with Males.
2. Despite higher ad spend and clicks from male audiences in previous graphs, they convert less effectively in terms of CTR.
3. Female users may be more receptive to the campaign messaging, leading to higher engagement despite lower total ad spend.
4. Campaign optimizations should focus on improving male engagement, as they represent a **costly but inefficient audience**.
5. Increased spending on Female user ad campaigns could tap into the higher Female CTR market.  """)