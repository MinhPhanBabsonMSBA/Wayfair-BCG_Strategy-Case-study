# app.py

import streamlit as st
import pandas as pd
from datetime import date
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings("ignore")


# Page configuration
st.set_page_config(
    page_title="Wayfair Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sidebar Navigation
st.image("wayfair_logo.png", use_container_width=True)
st.sidebar.title("Wayfair Analytics Dashboard")
selected_page = st.sidebar.selectbox(
    "Select Section",
    [
        "Introduction",
        "Exploratory Data Analysis",
        "Machine Learning Models",
        "A/B Testing Insights",
        "Project Summary"
    ]
)

# Load data once globally
@st.cache_data
def load_data():
    return pd.read_csv("wayfair_part2.csv")
df = load_data()
# ----------------------------
# Introduction with Full Executive Summary
# ----------------------------
def show_introduction():
    st.markdown("<h1 style='font-size: 44px;'>Wayfair Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("### Executive Summary")

    st.markdown("""
    Wayfair engaged in an in-depth analysis to investigate how delivery performance, guarantee visibility, and customer behaviors influence product returns and revenue outcomes.  Using December 2016 order-level data comprising over 123,000 observations, the analysis identified operational inefficiencies and customer segments that disproportionately impact profitability.Predictive models and cost estimators were layered onto segmentation to generate a holistic strategy using the BCG matrix.
    """)

    st.markdown("### Business Questions")
    st.markdown("""
    1. **Does showing a product guarantee reduce return rates?**  

    2. **How does late delivery impact return behavior?**  

    3. **Are desktop and mobile users influenced differently by guarantees?**  

    4. **Which product categories benefit most from guarantee visibility?**  

    5. **What are the most actionable customer segments?**  

    6. **Where should Wayfair invest to reduce returns and grow profitably?**  
    
    """)

    st.markdown("### Analytical Approach & Methodology")
    st.markdown("""
    - **Data Source:** December 2016 order-level dataset (123,542 entries)  
    - **Feature Engineering:**  
      - Created `Return_Rate`, `Delivery_Delay_Days`, `Is_Late`, `Order_Value_Numeric`, and binary flags for `Guarantee_Shown`  
      - Categorized delivery types and derived customer segments via `ShipClassName`  
    - **Data Cleansing:** Minimal missing data (<3%) handled via listwise deletion or imputation  
    - **Statistical/ Machine Learning Methods Used:**  
      - Z-test for proportions (Guarantee impact)  
      - Chi-square tests (Delivery × Returns)  
      - Correlation analysis (Delivery delay vs. Returns)  
      - K-Means clustering (with PCA for dimension reduction)  
      - Logistic Regression (for return prediction modeling)  
    """)

# ----------------------------
# EDA Section
# ----------------------------
def show_eda():
    st.title("Exploratory Data Analysis")
    st.markdown("""
    This section explores key return behaviors and customer insights derived from Wayfair's December 2016 order-level dataset.
    Charts are based on confirmed analysis from the project notebook.
    """)

    # 1. Return Rate by Product Category (Corrected)
    st.subheader("1. Return Rate by Product Category")
    cat_df = (
        df.groupby('Product_Category')
        .agg(Total_Orders=('Order_ID', 'count'), Return_Rate=('Has_Return', 'mean'))
        .reset_index()
        .query("Total_Orders > 100")
        .sort_values('Return_Rate', ascending=False)
        .head(10)
    )
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=cat_df, x='Product_Category', y='Return_Rate', palette='Reds_r', ax=ax1)
    ax1.set_title("Top 10 Product Categories by Return Rate", fontsize=16)
    ax1.set_ylabel("Return Rate")
    ax1.set_xlabel("")
    ax1.tick_params(axis='x', rotation=45, labelsize=12)
    ax1.tick_params(axis='y', labelsize=12)
    st.pyplot(fig1)
    st.markdown("""
    - **Rugs**, **Tabletop**, and **Lighting** show high return rates.
    - These categories often suffer from sizing issues or mismatch in expectations.
    - Consider improved visual merchandising and product filters.
    """)

    # 2. Return Rate by Platform and Guarantee
    st.subheader("2. Return Rate by Platform and Guarantee Visibility")
    platform_df = df.groupby(['Platform_Name', 'Has_Guarantee'])['Has_Return'].mean().reset_index()
    platform_df['Guarantee'] = platform_df['Has_Guarantee'].map({0: 'No Guarantee', 1: 'Guarantee Shown'})
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=platform_df, x='Platform_Name', y='Has_Return', hue='Guarantee', palette='Set2', ax=ax2)
    ax2.set_title("Return Rate by Platform and Guarantee", fontsize=16)
    ax2.set_ylabel("Return Rate")
    ax2.tick_params(labelsize=12)
    st.pyplot(fig2)
    st.markdown("""
    - Desktop users benefit more from guarantee visibility than mobile users.
    - Guarantees reduce return rate primarily for high-AOV products.
    - Suggest platform-specific UI emphasis for guarantees.
    """)

    # 3. Return Rate by Delivery Status
    st.subheader("3. Return Rate by Delivery Status")
    delay_df = df.groupby('Delivery_Status')['Has_Return'].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=delay_df, x='Delivery_Status', y='Has_Return', palette='coolwarm', ax=ax3)
    ax3.set_title("Return Rate by Delivery Status", fontsize=16)
    ax3.tick_params(labelsize=12)
    st.pyplot(fig3)
    st.markdown("""
    - Late deliveries are associated with higher return rates.
    - On-time and early deliveries significantly reduce return risks.
    - Wayfair should optimize SLA performance for large-parcel items.
    """)

    # 4. Correlation Heatmap
    st.subheader("4. Correlation of Key Numerical Variables")
    fig4, ax4 = plt.subplots(figsize=(7, 6))
    corr = df[['Has_Return', 'Order_Value_Numeric', 'Actual_Delivery_Days', 'Guarantee_Shown']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
    ax4.set_title("Correlation Heatmap", fontsize=16)
    st.pyplot(fig4)
    st.markdown("""
    - Returns positively correlate with delivery delay and slightly with order value.
    - Guarantees are slightly negatively correlated with returns.
    - Most variables show small to moderate linear relationships.
    """)

    # 5. Histogram of Order Value
    st.subheader("5. Distribution of Order Values")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    sns.histplot(df['Order_Value_Numeric'], bins=50, kde=False, color='steelblue', ax=ax5)
    ax5.set_title("Histogram of Order Values", fontsize=16)
    ax5.set_xlabel("Order Value")
    ax5.set_ylabel("Order Count")
    ax5.tick_params(labelsize=12)
    st.pyplot(fig5)
    st.markdown("""
    - The majority of orders fall below $200.
    - A small tail of high-value orders presents higher return risk.
    - Marketing strategy can focus on retention at mid-to-high order tiers.
    """)

    # 6. Return Rate by Order Price Range
    st.subheader("6. Return Rate by Price Range")
    df['Price_Bin'] = pd.cut(df['Order_Value_Numeric'], bins=[0, 50, 100, 200, 300, 500, 1000])
    price_return_df = df.groupby('Price_Bin')['Has_Return'].mean().reset_index()
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=price_return_df, x='Price_Bin', y='Has_Return', palette='Blues_d', ax=ax6)
    ax6.set_title("Return Rate by Order Value Range", fontsize=16)
    ax6.set_xlabel("Price Range")
    ax6.set_ylabel("Return Rate")
    ax6.tick_params(labelsize=12)
    st.pyplot(fig6)
    st.markdown("""
    - Orders in the $200–$500 range show the highest return risk.
    - Guarantees and UI enhancements should be focused in this band.
    - Budget segments (<$100) present low return concerns.
    """)

    # 7. K-Means Customer Segments
    st.subheader("7. Customer Segments from Clustering")
    segment_df = pd.DataFrame({
        'Segment': ['Premium Buyers', 'Value Shoppers', 'High-Return Customers', 'Moderate Shoppers'],
        'Avg_Order_Value': [373.29, 91.38, 137.99, 125.50],
        'Return_Rate': [0.37, 0.00, 90.04, 25.50],
        'Customer_Pct': [10, 56, 5, 29]
    })
    fig7, ax7 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=segment_df,
                    x='Avg_Order_Value', y='Return_Rate', size='Customer_Pct',
                    hue='Segment', sizes=(300, 1500), ax=ax7, legend=False)
    for _, row in segment_df.iterrows():
        ax7.text(row['Avg_Order_Value'] + 5, row['Return_Rate'], row['Segment'], fontsize=12)
    ax7.set_xlabel("Average Order Value")
    ax7.set_ylabel("Return Rate")
    ax7.set_title("K-Means Customer Segments", fontsize=16)
    st.pyplot(fig7)
    st.markdown("""
    - Value Shoppers form the largest group (56%) with zero returns.
    - High-Return Customers (5%) create heavy cost burdens.
    - UX and education should be tailored by segment.
    """)

    # 8. Guarantee vs Return Rate (Simple Comparison)
    st.subheader("8. Guarantee Visibility and Return Rates")
    g_df = df.groupby('Has_Guarantee')['Has_Return'].mean().reset_index()
    g_df['Guarantee'] = g_df['Has_Guarantee'].map({0: 'No Guarantee', 1: 'Guarantee Shown'})
    fig8, ax8 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=g_df, x='Guarantee', y='Has_Return', palette='pastel', ax=ax8)
    ax8.set_title("Guarantee Effect on Return Rate", fontsize=16)
    ax8.tick_params(labelsize=12)
    st.pyplot(fig8)
    st.markdown("""
    - Guarantees lower the return rate slightly overall.
    - Their impact is more significant within specific categories and platforms.
    - Expand guarantees selectively on subjective or high-return SKUs.
    """)

    st.success("Exploratory analysis completed. Use these insights to drive modeling and strategic recommendations.")

# ----------------------------
# Machine Learning Models Section
# ----------------------------
def show_ml_models():
    st.title("Machine Learning Models")

    # Objective
    st.markdown("### Objective")
    st.markdown("""
    This model predicts whether an order will be returned using order-level data, customer segment, guarantee visibility, delivery experience, and product category information.
    """)

    # Model Comparison Table
    st.markdown("### Models Performance Summary")
    st.dataframe(pd.DataFrame({
        "Model": ["Logistic Regression", "Random Forest", "Gradient Boosting", "XGBoost"],
        "Accuracy": [0.9741, 0.9765, 0.9762, 0.9756],
        "AUC": [0.9972, 0.9962, 0.9970, 0.9969]
    }))
    st.markdown("""
    - All models performed well with **AUC > 0.996**, indicating high classification power.  
    - **Random Forest** and **Gradient Boosting** slightly outperformed others on accuracy.  
    - **Logistic Regression** offers strong interpretability and is preferred for actionable insights.
    """)

    # Logistic Regression Class Performance
    st.markdown("### Logistic Regression - Classification Report")
    st.markdown("""
    | Class            | Precision | Recall | F1-score |
    |------------------|-----------|--------|----------|
    | No Return (0)    | 1.00      | 0.97   | 0.99     |
    | Return (1)       | 0.69      | 1.00   | 0.82     |

    - Recall for return class is **1.00**, capturing all actual returns.  
    - The model slightly over-predicts returns, reflected in the 0.69 precision.  
    - This tradeoff is acceptable to **minimize unflagged costly returns**.
    """)

    # Top Predictive Features
    st.markdown("### Top Predictive Features")
    feature_df = pd.DataFrame({
        "Feature": [
            "Customer_Segment_Value Shoppers",
            "Customer_Segment_Premium Buyers",
            "Customer_Return_Rate",
            "Actual_Delivery_Days",
            "Order_Value_Numeric"
        ],
        "Coefficient": [-2.64, -1.76, 1.32, 1.14, -0.92]
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=feature_df, x='Coefficient', y='Feature', palette='coolwarm', ax=ax)
    ax.set_title("Feature Importance from Logistic Regression", fontsize=16)
    ax.set_xlabel("Coefficient")
    ax.tick_params(labelsize=12)
    st.pyplot(fig)

    st.markdown("""
    - **Value Shoppers (-2.64)** and **Premium Buyers (-1.76)** are significantly less likely to return orders.  
    - **Value Shoppers (56% of users)** and **Premium Buyers (10%)** drive reliable profits with low return rates.  
    - **High-Return Customers (5%)** create operational costs and should be deprioritized.  
    - **Customer's past return rate** and **late deliveries** increase return likelihood.  
    - **Higher order values** slightly decrease return probability.
   
    """)

    # Business Strategy
    st.markdown("### Business Strategy Recommendations")
    st.markdown("""
    1. Focus retention and loyalty efforts on **Premium Buyers**.  
    2. Scale guarantees strategically where returns are high, but loyal segments exist.  
    3. Prioritize **delivery performance**, particularly for large-parcel goods, to reduce return risk.  
    4. Deploy **Logistic Regression** for production as it's accurate, interpretable, and stable.  
    5. Pair model predictions with segmentation for **tailored CX strategy** and fraud flagging.
    """)


# ----------------------------
# A/B Testing Section
# ----------------------------
def show_ab_testing():
    st.title("A/B Testing: Guarantee Visibility Impact")

    st.markdown("### Objective")
    st.markdown("""
    Evaluate whether displaying product guarantees reduces return rates across product categories,
    platforms, and customer segments using a controlled A/B test framework.
    """)

    st.markdown("### Overall Test Result")
    st.markdown("""
    - **Control Group (No Guarantee):** 5.90% return rate  
    - **Treatment Group (Guarantee):** 5.83% return rate  
    - **p-value:** 0.63 → No statistically significant effect overall
    """)

    # Chart 1: Return Rate by Product Category
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    product_ab = pd.DataFrame({
        "Product_Category": ["Bedding", "Lighting", "Rugs", "Tabletop"],
        "Control_Return_Rate": [0.065, 0.072, 0.110, 0.088],
        "Treatment_Return_Rate": [0.052, 0.061, 0.111, 0.087]
    })
    product_melted = product_ab.melt(id_vars="Product_Category", var_name="Group", value_name="Return Rate")
    product_melted["Group"] = product_melted["Group"].map({
        "Control_Return_Rate": "Control",
        "Treatment_Return_Rate": "Treatment"
    })
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=product_melted, x="Product_Category", y="Return Rate", hue="Group", palette="Set2", ax=ax1)
    ax1.set_title("Return Rate by Product Category", fontsize=14)
    st.pyplot(fig1)

    st.markdown("""
    - **Bedding** and **Lighting** categories saw return rate reductions under the treatment group.
    - **Rugs** and **Tabletop** showed no significant difference between groups.
    - Guarantees should be expanded in product categories where size/fit perception matters.
    """)

    # Chart 2: Return Rate by Platform
    platform_ab = pd.DataFrame({
        "Platform": ["Desktop", "Mobile"],
        "Control_Return_Rate": [0.058, 0.064],
        "Treatment_Return_Rate": [0.053, 0.065]
    })
    platform_melted = platform_ab.melt(id_vars="Platform", var_name="Group", value_name="Return Rate")
    platform_melted["Group"] = platform_melted["Group"].map({
        "Control_Return_Rate": "Control",
        "Treatment_Return_Rate": "Treatment"
    })
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    sns.barplot(data=platform_melted, x="Platform", y="Return Rate", hue="Group", palette="Set1", ax=ax2)
    ax2.set_title("Return Rate by Platform", fontsize=14)
    st.pyplot(fig2)

    st.markdown("""
    - **Desktop users** benefited most from guarantee visibility with lower return rates.
    - **Mobile users** showed little to no difference in return behavior.
    - Mobile UX may not be optimal for viewing or interpreting guarantee information.
    """)

    # Chart 3: Return Rate by Customer Segment
    segment_ab = pd.DataFrame({
        "Customer_Segment": ["Premium Buyers", "Value Shoppers", "High-Return Customers", "Moderate Shoppers"],
        "Control_Return_Rate": [0.005, 0.00, 0.91, 0.26],
        "Treatment_Return_Rate": [0.004, 0.00, 0.86, 0.22]
    })
    segment_melted = segment_ab.melt(id_vars="Customer_Segment", var_name="Group", value_name="Return Rate")
    segment_melted["Group"] = segment_melted["Group"].map({
        "Control_Return_Rate": "Control",
        "Treatment_Return_Rate": "Treatment"
    })
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=segment_melted, y="Customer_Segment", x="Return Rate", hue="Group", palette="coolwarm", ax=ax3)
    ax3.set_title("Return Rate by Customer Segment", fontsize=14)
    st.pyplot(fig3)

    st.markdown("""
    - **High-Return Customers** showed a meaningful drop in return rate when guarantees were shown.
    - **Moderate Shoppers** also returned less in the treatment group.
    - **Value Shoppers** had no returns in either group — guarantees are not necessary for this segment.
    """)

    # Summary Recommendations
    st.markdown("### Strategic Recommendations")
    st.markdown("""
    - Guarantees should not be universally applied — focus on high-return segments and sensitive product categories.
    - **Desktop UX** should emphasize guarantees where most effective (e.g., Bedding, Lighting).
    - Pair guarantee deployment with **customer return profiling** for optimal ROI.
    """)

    st.success("A/B test shows that guarantee visibility has measurable impact when deployed selectively.")

def show_summary():
    st.title("Project Summary & Business Strategy")

    st.markdown("## Strategic Objective")
    st.markdown("""
    Wayfair's analytics initiative focused on identifying operational inefficiencies and customer behavior patterns
    that contribute to high return rates and lost revenue. Through predictive modeling and segmentation,
    we developed data-driven strategies to reduce returns, improve delivery reliability, and maximize customer profitability.
    """)

    st.markdown("## Strategic Implementation Areas")

    st.markdown("### 1. **Guarantee Visibility Strategy**")
    st.markdown("""
    - Roll out **guarantee visibility** for high-impact categories like **Bedding** and **Lighting**.
    - Emphasize guarantees in **desktop platforms**, where it demonstrably lowers returns.
    - Test messaging on mobile platforms before broad deployment, due to mixed results.
    """)

    st.markdown("### 2. **Delivery Performance Enhancement**")
    st.markdown("""
    - Improve SLA adherence for **large-parcel shipments** to prevent return spikes tied to delivery delays.
    - Use delivery data to predict and proactively flag high-risk orders.
    - Invest in logistics forecasting for peak periods like holidays and regional surges.
    """)

    st.markdown("### 3. **Customer Segmentation & Retention Plan**")
    st.markdown("""
    - **Premium Buyers (10%)**: Focus on loyalty with guarantees and high-tier support.
    - **Value Shoppers (56%)**: Encourage repeat purchases with volume discounts.
    - **High-Return Customers (5%)**: Offer education or require order confirmations to prevent losses.
    - **Moderate Shoppers (29%)**: Convert through delivery accuracy and platform personalization.
    """)

    st.markdown("### 4. **Return Risk Modeling Integration**")
    st.markdown("""
    - Use the **logistic regression return predictor** (AUC ~ 0.997) to score new orders in real-time.
    - Create interventions (messaging, guarantees, delivery checks) based on predicted return risk.
    - Deploy return-risk scores into the customer service backend for proactive assistance.
    """)

    st.markdown("### 5. BCG Matrix-Based Category Investment Strategy")

    st.markdown("""
    The BCG Matrix classifies Wayfair's product categories based on their **market share** and **growth rate**,
    allowing us to align investments with strategic returns. Each quadrant informs a different business tactic:
    """)

    st.markdown("####  Stars (High Growth, High Share)")
    st.markdown("""
    - **Example:** Bedding  
    - These categories are performing well and expanding.  
    - **Strategy:** Invest aggressively with guarantees, fast shipping, and promotional boosts to maintain momentum.  
    - Monitor supply chain efficiency to prevent stock-outs or fulfillment lags.
    """)

    st.markdown("####  Cash Cows (Low Growth, High Share)")
    st.markdown("""
    - **Example:** Furniture  
    - These are mature, high-revenue drivers with low expansion potential.  
    - **Strategy:** Maintain SLAs and fulfillment quality.  
    - Avoid over-investment in promotions. Optimize for margin, not growth.
    """)

    st.markdown("####  Question Marks (High Growth, Low Share)")
    st.markdown("""
    - **Example:** Lighting  
    - These have strong market potential but low capture so far.  
    - **Strategy:** Test placement of guarantees, UX personalization, and mobile optimization.  
    - Evaluate whether to expand or phase out based on returns and conversion rates.
    """)

    st.markdown("####  Dogs (Low Growth, Low Share)")
    st.markdown("""
    - **Examples:** Tabletop, Wall Decor  
    - These categories are stagnant and underperforming.  
    - **Strategy:** Minimize investment unless bundled or seasonal opportunity arises.  
    - Evaluate for long-term pruning or repurposing (e.g., gifting or clearance channels).
    """)

    st.markdown("""
    By overlaying the BCG matrix with our **return rate analysis** and **customer segmentation**,
    we can better align merchandising, marketing spend, and operational focus.
    """)

# ----------------------------
# Route to Selected Page
# ----------------------------
if selected_page == "Introduction":
    show_introduction()
elif selected_page == "Exploratory Data Analysis":
    show_eda()
elif selected_page == "Machine Learning Models":
    show_ml_models()
elif selected_page == "A/B Testing Insights":
    show_ab_testing()
elif selected_page == "Project Summary":
    show_summary()

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    f"<p style='font-size: 13px; color: gray;'>"
    f"© {date.today().year} Wayfair Analytics Project | Built with Streamlit"
    f"</p>",
    unsafe_allow_html=True
)
