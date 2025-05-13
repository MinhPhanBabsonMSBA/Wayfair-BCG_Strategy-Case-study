![](https://github.com/MinhPhanBabsonMSBA/Wayfair-Case-study/blob/main/wayfair%20logo.png)

# Wayfair Return Optimization & Customer Segmentation Strategy Implementation using BCG matrix 

## Executive Summary  
Wayfair engaged in an in-depth analysis to investigate how delivery performance, guarantee visibility, and customer behaviors influence product returns and revenue outcomes. Using December 2016 order-level data comprising over 123,000 observations, the analysis identified operational inefficiencies and customer segments that disproportionately impact profitability. Predictive models and cost estimators were layered onto segmentation to generate a holistic strategy.

### Key Takeaways:
- **Guarantee visibility** reduces returns and raises average order value in targeted product categories
- **Delivery delays** significantly increase return rates, especially for large-parcel goods
- **Customer behavior differs by platform (desktop vs. mobile)**, influencing guarantee effectiveness
- **Segmentation via clustering** revealed four distinct customer profiles with unique value and return risk profiles
- **Logistic regression** identified return risk factors; return cost modeling enables financial risk mitigation
- **BCG Matrix strategy** informs category investment and guarantee rollout

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
  - Logistic Regression (Return Likelihood)

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

### 5. Return Prediction (Logistic Regression)

Top significant predictors of return likelihood:
- **Negative predictors** (low return risk): `Value Shopper`, `Premium Buyer`
- **Positive predictors** (high risk): Past return history, `Delivery_Status = Early` or `On Time`
- Use case: **Return Risk Scoring Engine** to gate promotions or adjust guarantees
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

### 5. Return Risk & Cost Integration
- Deploy real-time **return likelihood scores** at checkout
- Integrate **return cost model** into margin calculations and promo eligibility

### 6. Align Product Strategy via BCG Matrix

The **BCG (Boston Consulting Group) Matrix** helps prioritize resource allocation across product categories by mapping them on two dimensions: **return performance (cost impact)** and **sales volume (market traction)**. This analysis enables Wayfair to focus on **scaling profitable categories**, **fixing or testing marginal ones**, and **deprioritizing underperformers**.

| BCG Quadrant        | Category Examples     | Business Rationale                                                                 | Strategic Action                                                                 |
|---------------------|------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
|  **Stars**         | Bedding, Lighting      | High sales and **low return rates**. Guarantees are **proven effective** in reducing returns (e.g., Bedding: -0.89pp with guarantee, p < 0.05). Strong customer demand + ROI on promotion. | - Scale guarantees across Desktop & Mobile (after mobile UI testing)  <br>- Expand inventory and marketing  <br>- Explore bundling to increase AOV further |
|  **Cash Cows**     | Kitchen Furniture      | Strong, consistent revenue but **moderate return rates**. Large parcel = high delivery risk if late. No strong gain from guarantees. | - Maintain focus with **supply chain optimization**  <br>- Improve delivery SLA adherence  <br>- Reduce return friction (size guides, accurate specs) |
|  **Question Marks**| Rugs, Tabletop         | Inconsistent performers. Some have high returns despite guarantees (e.g., Rugs ↑ 1pp). Guarantees **may not be suitable**, or current messaging isn’t effective. | - Conduct **controlled A/B tests** with new copy/design  <br>- Pilot category-specific return policies  <br>- Test UX refinements (images, AR tools, reviews) |
|  **Dogs**          | (TBD – monitor quarterly) | Low sales + high returns (not yet observed but expected in niche or seasonal SKUs). These SKUs typically drain margin and customer trust. | - Monitor SKUs with low ROI-to-return ratio  <br>- Apply stricter return policies or remove guarantees  <br>- Phase out if performance remains flat or declines |

####  How to Use the Matrix
- Run **quarterly return-cost-to-revenue audits** by product category  
- Include **return severity (cost regression)** in category P&L review  
- Apply **A/B test results + return scoring model** to move categories across quadrants dynamically  
- Use the matrix to inform **guarantee budget allocation**, **category investment**, and **SKU-level lifecycle decisions**
---

## Potential Business Impact

- Lower return costs via **fulfillment and policy improvements**
- Higher customer profitability through **segmentation & targeting**
- Increased AOV and conversion through **UX-optimized guarantees**
- Improved operational efficiency via **risk scoring and cost forecasting**

---

## KPI Dashboard

| KPI                         | Baseline | Target     | Frequency |
|-----------------------------|----------|------------|-----------|
| Return Rate (Overall)       | ~5.9%    | < 5.5%     | Monthly   |
| AOV with Guarantee          | $134.75  | > $140     | Monthly   |
| On-Time Delivery Rate       | ~65%     | > 85%      | Monthly   |
| Premium Buyer Share         | 10.3%    | > 13%      | Quarterly |
| Return Cost per Order       | ~$20.75  | < $15.00   | Monthly   |

---

## Implementation Roadmap

| Phase                     | Timeline    | Deliverables                              |
|---------------------------|-------------|-------------------------------------------|
| Segment Activation        | Weeks 1–3    | CRM tagging, UX targeting                  |
| Guarantee Testing         | Weeks 3–6    | A/B test new formats on mobile/desktop     |
| Delivery Optimization     | Weeks 6–8    | Fulfillment changes and ETA transparency   |
| Return Cost Modeling      | Weeks 8–12   | Regression scoring + dashboard             |
| Strategic Realignment     | Weeks 12–16  | Apply BCG strategy to product roadmapping  |

---

## Appendix

- **Data Files:** `wayfair.csv`,`wayfair_part2.csv`
- **Notebook Reference:** `Wayfair Analytics Report.pdf`,`Wayfair ML models implementation.pdf`
- **Tools Used:** Python (Pandas, Seaborn, Matplotlib, Scikit-learn, StatsModels)
- **Models:** Logistic Regression, KMeans, PCA
- **Visuals:** Cluster maps, return drivers, cost curves, BCG matrix

---
