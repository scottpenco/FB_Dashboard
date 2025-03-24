# 📊 Facebook A/B Testing Dashboard

An interactive Streamlit dashboard analyzing the performance of Facebook advertising campaigns across gender segments using A/B testing data. The project simulates the role of a **Guest Services Analyst**, focusing on customer engagement, behavior trends, and campaign effectiveness.

---

## 🧠 Project Overview

This dashboard enables detailed exploration of marketing performance across gender, helping teams understand how different audiences engage with content. The analysis includes metric engineering, visual insights, and statistical testing to guide data-driven decisions.

---

## 📂 Features

### ✅ Key Components:
- **CTR and Conversion Rate Analysis** by gender
- **Custom Subplots** showing campaign performance for:
  - `Spent`
  - `Clicks`
  - `Total Conversions`
- **Pairwise Metric Relationships** using a lower-triangle scatter plot matrix
- **Distribution Comparisons** using gender-segmented box plots
- **Statistical Testing** with Shapiro-Wilk and Mann-Whitney U

### 📈 Sample Visualizations:
- 📊 CTR & Conversion Rate Box Plots
- 📉 Stacked Bar Charts by Campaign and Gender
- 🧩 Scatter Subplots for Campaign Metrics
- 📊 Summary Metrics with `st.metric()`

---

## 🧪 Hypothesis Testing

**Test Used:** Mann-Whitney U Test (non-parametric)

**Hypotheses:**

- **H₀ (Null Hypothesis):** No difference in CTR between male and female users.
- **H₁ (Alternative Hypothesis):** A difference exists in CTR between male and female users.

**Result:**

- U-statistic = `50333.5`
- p-value = `1.095 × 10⁻⁸`

✅ **Conclusion:** Statistically significant difference — **female users have higher CTR** despite lower total spend.

---

## 📁 Dataset

The data includes Facebook A/B test metrics such as:

- `impressions`, `clicks`, `spent`
- `approved_conversion`, `total_conversion`
- `campaign_id`, `gender`

📌 **Note:** Data subset includes first 761 rows for analysis.

---

## 🛠️ Tech Stack

- **Frontend & Interactivity:** Streamlit
- **Visualization:** Plotly, Seaborn, Matplotlib
- **Data Processing:** Pandas
- **Statistical Analysis:** Scipy (Shapiro-Wilk, Mann-Whitney U)

---

## 🚀 Getting Started

1. Clone the repo:

```bash
git clone https://github.com/yourusername/facebook-ab-gender-dashboard.git
cd facebook-ab-gender-dashboard
