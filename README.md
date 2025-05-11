![](https://github.com/MinhPhanBabsonMSBA/Wayfair-Case-study/blob/main/wayfair%20logo.png)
# Wayfair Return Optimization & Customer Segmentation Study

## Executive Summary  
Wayfair engaged in an in-depth analysis to investigate how delivery performance, guarantee visibility, and customer behaviors influence product returns and revenue outcomes. Using December 2016 order-level data comprising over 123,000 observations, the analysis identified operational inefficiencies and customer segments that disproportionately impact profitability.

### Key Takeaways:
- **Guarantee visibility** reduces returns and raises average order value in targeted product categories
- **Delivery delays** significantly increase return rates, especially for large-parcel goods
- **Customer behavior differs by platform (desktop vs. mobile)**, influencing guarantee effectiveness
- **Segmentation via clustering** revealed four distinct customer profiles with unique value and return risk profiles
---
## Business Questions

1. **Does showing a product guarantee reduce return rates?**  
   ✔️ Yes — most notably for **Bedding** and **Desktop users**. Guarantees are associated with reduced returns and higher AOV.

2. **How does late delivery impact return behavior?**  
   ✔️ Late delivery is **strongly correlated** with return behavior (r = +0.63), especially among large parcel items.

3. **Are desktop and mobile users influenced differently by guarantees?**  
   ✔️ Yes — **Desktop users** benefit from guarantees; **mobile users** show mixed responses.

4. **Which product categories benefit most from guarantee visibility?**  
   ✔️ Bedding showed the clearest return reduction; Lighting had a moderate effect; Tabletop and Rugs showed no benefit.

5. **What are the most actionable customer segments?**  
   ✔️ Four segments identified:
   - **Premium Buyers (10%)**: high AOV, low returns — loyalty focus
   - **Value Shoppers (56%)**: low spend, no returns — frequency growth
   - **High-Return Customers (5%)**: high risk — UX and education needed
   - **Moderate Shoppers (29%)**: convertible via targeting and delivery management

6. **Where should Wayfair invest to reduce returns and grow profitably?**  
   ✔️ Invest in targeted guarantees, improved delivery SLAs, and platform-optimized UX messaging.

---

## Analytical Approach & Methodology

- **Data Source:** December 2016 order-level file, 123,542 entries
- **Feature Engineering:**
  - Created `Return_Rate`, `Delivery_Delay_Days`, `Is_Late`, `Order_Value_Numeric`, and binary flags for `Guarantee_Shown`
  - Categorized delivery types and derived segments via `ShipClassName`
- **Data Cleansing:** Minimal missing data (<3%); handled via listwise deletion or imputation
- **Statistical Methods:**
  - Z-test for proportions (Guarantee impact)
  - Chi-square tests (Delivery × Returns)
  - Correlation analysis (Delay vs. Returns)
  - K-Means clustering (with PCA)

---

## Summary Insights

### 1. Product Return Behavior
- Return rates ranged from 3%–12%, highest in **Rugs**, **Seasonal Decor**, and **Bedding**
- Products **with guarantees** had lower returns on average (5.83% vs. 5.90%)
- A/B testing showed significant improvement in **Bedding** (−0.89pp, p < 0.05)

### 2. Delivery Performance
- **25% of orders** were delivered late
- Delay positively correlated with return rates (r = +0.63)
- Late deliveries most common in **Large Parcel** categories

### 3. Platform Behavior Differences
- **Desktop**: Guarantees improved performance across metrics (AOV ↑, Returns ↓)
- **Mobile Web**: Higher AOV with guarantees but slight return increase; UI optimization required

### 4. Customer Segmentation (via Clustering)

| Segment              | % of Users | Avg Order Value | Return Rate | Description                         |
|----------------------|------------|------------------|-------------|-------------------------------------|
| Premium Buyers       | 10%        | $373.29          | 0.37%       | High spend, low return — loyalty target |
| Value Shoppers       | 56%        | $91.38           | 0.00%       | Low spend, high volume — promote frequency |
| High-Return Customers| 5%         | $137.99          | 90.04%      | High return risk — UX & policy intervention |
| Moderate Shoppers    | 29%        | $125.50          | 25.50%      | Mid-tier segment — optimize delivery and info |

---

## Strategic Recommendations

### 1. Strengthen Guarantee Strategy
- Expand guarantee visibility for categories with proven benefit (e.g., Bedding)
- Avoid blanket rollout to low-impact or high-risk categories without A/B validation
- On mobile, experiment with **icon-based guarantees**, microcopy, and collapsible labels

### 2. Improve Delivery SLA Adherence
- Prioritize on-time fulfillment for Large Parcel items
- Flag SKUs with history of late delivery and high returns
- Collaborate with 3PLs to improve warehouse-to-door timelines

### 3. Segment-Centric Campaigns
- Build **loyalty journeys** for Premium Buyers
- Launch **win-back or education flows** for High-Return Customers
- Use size guides, augmented reality, and visuals to reduce uncertainty pre-purchase

### 4. Platform-Specific Messaging
- Optimize **guarantee presentation** for mobile interfaces
- Run **platform-category A/B tests** to isolate impact pathways

---

## Potential Business Impact

- Reduced return costs via fulfillment improvements and guarantee optimization
- Higher revenue through targeted retention of Premium Buyers and upsell of Value Shoppers
- Improved mobile performance by reducing information friction

---

## Appendix

- **Data File:** `wayfair.csv`
- **Notebook Reference:** `Wayfair Analytics Report.ipynb`
- **Tools Used:** Python (Pandas, Seaborn, Matplotlib, Scikit-learn, StatsModels)
- **Visuals:** Cluster maps, A/B comparisons, return rate bar charts
