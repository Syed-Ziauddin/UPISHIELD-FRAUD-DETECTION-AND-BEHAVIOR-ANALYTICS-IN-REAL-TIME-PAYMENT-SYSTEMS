# 🛡️ UPISHIELD --- Fraud Detection & Behavior Analytics in Real-Time Payment Systems

> **An end-to-end analytics and machine-learning project for detecting
> suspicious UPI-style payment behavior in real time.**

UPISHIELD is designed to demonstrate how a modern payment-security
pipeline can combine **SQL analytics, behavioral profiling, rule-based
risk signals, machine learning/anomaly detection, and interactive
reporting** to identify potentially fraudulent transactions before they
become costly incidents.

The project is intentionally structured as a portfolio-ready
data/analytics project. It focuses not only on building a model, but
also on answering the business questions that matter to a payment
company:

-   Which transactions look abnormal?
-   What changed in the customer's normal behavior?
-   Which merchants, devices, locations, time windows or transaction
    patterns create elevated risk?
-   How can analysts prioritize alerts instead of reviewing every
    transaction?
-   How can the system explain *why* a transaction was flagged?

> **Data note:** UPI transaction data is sensitive and generally not
> available as an unrestricted public production dataset. This
> repository should use synthetic, anonymized, or otherwise legally
> shareable data. Replace the dataset description below with the exact
> source used in your project.

------------------------------------------------------------------------

## 📌 Project Snapshot

  -----------------------------------------------------------------------
  Area                                Details
  ----------------------------------- -----------------------------------
  Project                             UPISHIELD

  Domain                              FinTech / Payments / Fraud
                                      Analytics

  Primary Use Case                    Real-time suspicious transaction
                                      detection

  Analytics                           SQL, EDA, behavioral analytics

  ML                                  Classification and/or anomaly
                                      detection

  Reporting                           Dashboard and fraud-monitoring
                                      views

  Data                                Synthetic / anonymized transaction
                                      data

  Output                              Risk score, alert level, reason
                                      codes

  Audience                            Data Analysts, Business Analysts,
                                      Fraud Teams, FinTech Recruiters
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🎯 Executive Summary

Digital payments have made financial transactions extremely fast and
convenient. That same speed creates a narrow window for fraud detection:
once an unauthorized payment succeeds, recovery can be difficult.

UPISHIELD addresses this problem with a layered detection approach.

Instead of depending on a single rule such as **"large transaction =
fraud"**, the system evaluates the transaction in context. For example,
a ₹20,000 transaction may be perfectly normal for one customer but
highly unusual for another. A transaction made from a new device, at an
unusual hour, immediately after several rapid payments, can deserve a
higher risk score even when the amount itself is ordinary.

The proposed pipeline therefore combines:

1.  **Transaction-level features**
2.  **Historical customer behavior**
3.  **Velocity and frequency signals**
4.  **Device and beneficiary novelty**
5.  **Time and location behavior**
6.  **Rule-based risk indicators**
7.  **Machine-learning/anomaly scores**
8.  **Explainable alert reasons**
9.  **Analytical dashboards**

The objective is not simply to maximize model accuracy. Fraud detection
is a highly imbalanced problem, so the project emphasizes **precision,
recall, F1-score, PR-AUC, false positives, and business impact** rather
than accuracy alone.

------------------------------------------------------------------------

## 🧩 Problem Statement

Payment platforms process a large number of transactions continuously. A
fraud-monitoring team cannot manually investigate every event.

Traditional approaches can face several limitations:

-   Static rules may miss new fraud patterns.
-   Very sensitive rules can generate too many false positives.
-   A transaction's risk depends on customer context.
-   Fraudsters can distribute activity across multiple small
    transactions.
-   Unusual device, timing and beneficiary behavior can be difficult to
    capture with amount-only rules.
-   Analysts need explainable reasons for alerts.
-   Detection must happen quickly enough to support intervention.

### Business Problem

> **How can a payment platform identify high-risk transactions in near
> real time while minimizing false positives and providing useful
> explanations to fraud analysts?**

UPISHIELD treats fraud detection as a **risk-ranking problem**, not
merely a binary classification problem.

------------------------------------------------------------------------

# 🏗️ System Architecture

![UPISHIELD Architecture](https://github.com/Syed-Ziauddin/UPISHIELD-FRAUD-DETECTION-AND-BEHAVIOR-ANALYTICS-IN-REAL-TIME-PAYMENT-SYSTEMS/blob/main/architecture.png)

The architecture is organized into six logical layers:

### 1. Transaction Ingestion

Receives a payment event containing fields such as:

-   transaction ID
-   user/customer ID
-   timestamp
-   amount
-   merchant
-   transaction type
-   device
-   location
-   beneficiary
-   transaction status

### 2. Data Validation & Enrichment

The incoming event is validated and enriched with historical
information.

Examples:

-   transaction count in the last 5/15/60 minutes
-   average transaction amount
-   user's normal transaction hours
-   number of previous transactions with the beneficiary
-   device familiarity
-   location consistency

### 3. Risk Feature Engineering

Raw fields are converted into analytical signals.

Examples:

``` text
amount_deviation
transaction_velocity
new_device_flag
new_beneficiary_flag
unusual_hour_flag
location_deviation
failed_attempt_count
customer_risk_score
```

### 4. Detection Layer

UPISHIELD can combine:

-   deterministic rules
-   statistical anomaly detection
-   supervised ML
-   ensemble risk scoring

### 5. Decision Layer

Transactions can be categorized as:

  Risk          Example Action
  ------------- --------------------------------------------
  🟢 Low        Allow
  🟡 Medium     Allow + monitor / step-up verification
  🟠 High       Review / additional authentication
  🔴 Critical   Block or hold according to business policy

### 6. Monitoring & Reporting

Fraud analysts can monitor:

-   alert volume
-   fraud rate
-   high-risk transactions
-   fraud by hour
-   fraud by merchant category
-   fraud by location
-   device-related anomalies
-   top fraud reasons

------------------------------------------------------------------------

# 🔄 Real-Time Detection Workflow

![Detection Workflow](docs/images/detection-workflow.png)

The transaction follows a simple analytical sequence:

``` text
Payment Event
     ↓
Validate
     ↓
Create Features
     ↓
Behavioral Analysis
     ↓
Rules + ML / Anomaly Score
     ↓
Risk Score
     ↓
Allow / Review / Block
     ↓
Store Outcome
     ↓
Dashboard + Feedback
```

The important design principle is **context**.

For example:

``` text
Transaction A
Amount: ₹18,000
User average: ₹16,500
Device: Known
Time: Normal
Beneficiary: Known
Velocity: Normal
→ Lower risk

Transaction B
Amount: ₹18,000
User average: ₹1,800
Device: New
Time: 2:13 AM
Beneficiary: New
Previous 10 minutes: 5 transactions
→ High risk
```

The amount is identical, but the behavioral context is very different.

------------------------------------------------------------------------

# 🧠 Behavioral Analytics

![Behavioral Analytics](docs/images/behavioral-analytics.png)

Behavioral analytics is one of the core ideas behind UPISHIELD.

Instead of asking only:

> "Is this transaction fraudulent?"

the system asks:

> "How different is this transaction from the customer's normal
> behavior?"

## Important Behavioral Features

### 1. Amount Deviation

Measures how far the current transaction is from a user's normal
transaction amount.

A simple standardized signal can be represented as:

``` text
amount_z_score =
(current_amount - user_mean_amount)
/
user_std_amount
```

A high positive deviation can indicate unusual spending.

### 2. Transaction Velocity

Measures the number of transactions within a short time window.

Example:

``` text
transactions_last_5_min
transactions_last_15_min
transactions_last_60_min
```

A sudden burst can indicate automated activity, account takeover or
coordinated fraud.

### 3. New Device

A transaction from a device never previously associated with the user
can increase risk.

``` text
new_device_flag = 1
```

This signal should not automatically mean fraud. It becomes more useful
when combined with other anomalies.

### 4. New Beneficiary

A new recipient can be legitimate, but a newly added beneficiary
followed immediately by a large transfer deserves additional attention.

### 5. Unusual Time

Users usually have recurring payment patterns.

For example:

``` text
normal_active_hours = 07:00–23:00
transaction_time = 02:30
```

The system can convert this into an `unusual_hour_flag`.

### 6. Location Inconsistency

If the user's recent transactions are geographically concentrated but
the next transaction occurs far away within an unrealistic time
interval, the event may be suspicious.

### 7. Failed Attempt Behavior

Multiple authentication failures followed by a successful transaction
can be treated as a risk signal.

------------------------------------------------------------------------

# 📊 Fraud Detection Methodology

UPISHIELD can support multiple detection strategies.

## 1. Rule-Based Detection

Rules are transparent and easy for fraud teams to understand.

Example:

``` text
IF
    amount > user_average * 5
AND new_device = TRUE
AND new_beneficiary = TRUE
THEN
    risk_level = HIGH
```

### Advantages

-   Easy to explain
-   Easy to deploy
-   Useful for known fraud patterns

### Limitations

-   Static
-   Requires manual maintenance
-   Can miss unknown patterns

------------------------------------------------------------------------

## 2. Statistical Detection

Statistical techniques identify transactions that deviate from a
customer's baseline.

Examples:

-   Z-score
-   percentile thresholds
-   rolling averages
-   standard deviation
-   moving-window velocity

This approach is useful when labeled fraud data is limited.

------------------------------------------------------------------------

## 3. Machine Learning

Depending on the available dataset, UPISHIELD can use:

-   Logistic Regression
-   Random Forest
-   XGBoost
-   LightGBM
-   Isolation Forest
-   Autoencoders

### Supervised Learning

If historical transactions have a reliable fraud label:

``` text
Features → ML Model → Fraud Probability
```

### Unsupervised Learning

If labels are limited:

``` text
Normal Behavior → Learn Pattern → Detect Outliers
```

------------------------------------------------------------------------

# ⚙️ Risk Scoring

A practical fraud system should produce more than a simple `0/1`.

Example:

``` text
Risk Score: 87 / 100
Risk Level: HIGH

Reasons:
✓ New device
✓ New beneficiary
✓ 6 transactions in 5 minutes
✓ Amount 4.8× user average
✓ Unusual transaction hour
```

A conceptual ensemble score can be represented as:

``` text
Final Risk Score =
    Rule Score × Rule Weight
  + ML Probability × ML Weight
  + Behavioral Anomaly × Anomaly Weight
```

The exact weights should be tuned using validation data and business
costs.

------------------------------------------------------------------------

# 🗄️ Data Model

A typical transaction table can contain:

  Column              Description
  ------------------- -------------------------------
  transaction_id      Unique transaction identifier
  user_id             Customer identifier
  timestamp           Transaction time
  amount              Transaction value
  merchant_id         Merchant identifier
  merchant_category   Merchant category
  transaction_type    P2P / P2M / other
  device_id           Device identifier
  beneficiary_id      Recipient identifier
  location            Transaction location
  status              Success / failed / reversed
  fraud_label         Target label where available

### Derived Features

  Feature              Meaning
  -------------------- -----------------------------
  avg_amount_30d       User's historical average
  amount_deviation     Difference from baseline
  tx_count_5m          Recent transaction velocity
  tx_count_1h          Hourly velocity
  new_device           Device novelty
  new_beneficiary      Recipient novelty
  unusual_hour         Time anomaly
  location_deviation   Geographic anomaly
  failed_attempts      Recent failed attempts
  risk_score           Combined risk estimate

------------------------------------------------------------------------

# 🧪 Exploratory Data Analysis

Before training a model, the dataset should be explored carefully.

Recommended analysis:

### Transaction Volume

``` sql
SELECT
    DATE(timestamp) AS transaction_date,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY transaction_date;
```

### Fraud Rate

``` sql
SELECT
    AVG(CASE WHEN fraud_label = 1 THEN 1.0 ELSE 0.0 END) AS fraud_rate
FROM transactions;
```

### Fraud by Hour

``` sql
SELECT
    EXTRACT(HOUR FROM timestamp) AS hour,
    COUNT(*) AS transactions,
    SUM(fraud_label) AS fraud_transactions
FROM transactions
GROUP BY EXTRACT(HOUR FROM timestamp)
ORDER BY hour;
```

### Fraud by Merchant Category

``` sql
SELECT
    merchant_category,
    COUNT(*) AS transactions,
    SUM(fraud_label) AS fraud_count
FROM transactions
GROUP BY merchant_category
ORDER BY fraud_count DESC;
```

------------------------------------------------------------------------

# 📈 Dashboard

![Dashboard Concept](docs/images/dashboard-concept.png)

The dashboard should be designed for both technical and non-technical
users.

## Page 1 --- Executive Overview

Recommended KPIs:

-   Total transactions
-   Total transaction value
-   Fraud alerts
-   High-risk transactions
-   Fraud rate
-   Average transaction amount

Recommended visuals:

-   transaction volume trend
-   fraud trend
-   risk distribution
-   successful vs failed transactions

## Page 2 --- Fraud Intelligence

Focus on:

-   fraud by hour
-   fraud by merchant category
-   fraud by location
-   top risk reasons
-   high-risk users/devices
-   transaction velocity

## Page 3 --- Transaction Investigation

A searchable transaction-level table can display:

``` text
Transaction ID
Timestamp
User
Amount
Merchant
Risk Score
Risk Level
Reason Codes
Status
```

This page turns the dashboard into an analyst investigation tool.

------------------------------------------------------------------------

# 🧮 Model Evaluation

Fraud datasets are usually imbalanced. Therefore, accuracy alone can be
misleading.

For example:

``` text
99.5% legitimate
0.5% fraud
```

A model predicting every transaction as legitimate could achieve very
high accuracy while detecting zero fraud.

Use these metrics instead:

  Metric                Why it matters
  --------------------- --------------------------------------------------
  Precision             How many flagged transactions are actually fraud
  Recall                How much fraud the system catches
  F1-score              Balance between precision and recall
  PR-AUC                Useful for imbalanced classification
  ROC-AUC               Overall ranking quality
  False Positive Rate   Customer friction
  False Negative Rate   Missed fraud

### Business Trade-off

A fraud system must balance:

``` text
More Recall
    ↓
More fraud detected
    ↓
Potentially more false positives
    ↓
More customer friction
```

The optimal threshold should therefore be selected using business costs,
not only mathematical performance.

------------------------------------------------------------------------

# 🔍 Explainability

A fraud alert should be understandable.

Instead of:

``` text
Fraud = 1
```

UPISHIELD should provide:

``` text
Risk Score: 91
Risk Level: Critical

Primary Reasons:
1. Transaction amount is significantly above user baseline.
2. Device was not previously observed.
3. Beneficiary is new.
4. Transaction velocity is unusually high.
5. Activity occurred outside the user's normal time window.
```

For tree-based ML models, SHAP or feature-importance techniques can help
explain which features contributed most strongly to the prediction.

------------------------------------------------------------------------

# 🛠️ Technology Stack

The exact stack can be adapted to the implementation.

### Data & Analytics

-   Python
-   Pandas
-   NumPy
-   SQL
-   Jupyter Notebook

### Machine Learning

-   Scikit-learn
-   XGBoost / LightGBM
-   Isolation Forest
-   SHAP

### Database

-   MySQL / PostgreSQL / SQLite

### Dashboard

-   Power BI
-   Tableau
-   Streamlit

### Engineering

-   FastAPI / Flask
-   Docker
-   Git & GitHub

------------------------------------------------------------------------

# 📁 Recommended Repository Structure

``` text
UPISHIELD-FRAUD-DETECTION-AND-BEHAVIOR-ANALYTICS-IN-REAL-TIME-PAYMENT-SYSTEMS/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_training.ipynb
│
├── sql/
│   ├── schema.sql
│   ├── fraud_analysis.sql
│   └── business_queries.sql
│
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   ├── fraud_model.py
│   └── scoring.py
│
├── dashboard/
│   └── dashboard.pbix
│
├── models/
│   └── model.pkl
│
├── docs/
│   └── images/
│       ├── architecture.png
│       ├── detection-workflow.png
│       ├── behavioral-analytics.png
│       └── dashboard-concept.png
│
├── requirements.txt
├── README.md
└── LICENSE
```

------------------------------------------------------------------------

# 🚀 Installation

Clone the repository:

``` bash
git clone https://github.com/<your-username>/UPISHIELD-FRAUD-DETECTION-AND-BEHAVIOR-ANALYTICS-IN-REAL-TIME-PAYMENT-SYSTEMS.git
cd UPISHIELD-FRAUD-DETECTION-AND-BEHAVIOR-ANALYTICS-IN-REAL-TIME-PAYMENT-SYSTEMS
```

Create a virtual environment:

``` bash
python -m venv venv
```

Activate it on Windows:

``` bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

``` bash
source venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the analysis notebooks:

``` bash
jupyter notebook
```

If a Streamlit dashboard is included:

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

# 🔐 Data Privacy & Security

This project is intended for portfolio, research and educational use.

Do **not** commit:

-   real customer information
-   UPI IDs
-   bank account numbers
-   phone numbers
-   authentication credentials
-   payment secrets
-   production transaction logs
-   API keys

Use `.gitignore` to prevent accidental uploads.

Example:

``` gitignore
.env
*.key
*.pem
data/raw/private/
__pycache__/
.venv/
```

------------------------------------------------------------------------

# ⚠️ Important Limitations

UPISHIELD is a portfolio/research implementation and should not be
treated as a production payment-security system without extensive
validation.

Important limitations include:

1.  Synthetic or anonymized data may not represent real-world fraud.
2.  Fraud patterns evolve continuously.
3.  Model performance can degrade after deployment.
4.  False positives can affect legitimate customers.
5.  Fraud labels may contain delays or inaccuracies.
6.  Real-time systems require strict latency and availability
    engineering.
7.  Production deployment requires privacy, security, compliance and
    operational controls.

------------------------------------------------------------------------

# 🔮 Future Enhancements

### 1. Real-Time Streaming

Integrate:

``` text
Kafka → Stream Processor → Feature Store → Fraud Model → Alert Service
```

### 2. Graph-Based Fraud Detection

Represent:

``` text
User → Device → Beneficiary → Merchant → Account
```

as a graph.

This can help identify connected fraud rings and mule-account networks.

### 3. Adaptive Risk Thresholds

Instead of one global threshold:

``` text
threshold = f(user_segment, transaction_type, risk_context)
```

### 4. Model Monitoring

Track:

-   data drift
-   feature drift
-   prediction drift
-   precision/recall
-   alert volume
-   false-positive rate

### 5. Analyst Feedback Loop

Allow investigators to mark:

``` text
Confirmed Fraud
False Positive
Needs Review
```

These outcomes can later support model retraining.

### 6. Explainable AI

Add SHAP-based reason codes to the investigation dashboard.

------------------------------------------------------------------------

# 💼 Business Impact

A successful fraud-monitoring platform can create value in several ways:

### Reduce Financial Loss

Earlier identification can reduce exposure to suspicious activity.

### Reduce Manual Investigation

Risk-ranking allows analysts to focus on the highest-priority alerts.

### Improve Customer Experience

Better precision can reduce unnecessary transaction blocks.

### Improve Decision Making

Dashboards provide visibility into:

-   when fraud occurs
-   where it occurs
-   how it occurs
-   which behaviors are changing
-   which risk signals are most useful

### Support Scalable Monitoring

Automation allows payment platforms to analyze large transaction volumes
consistently.

------------------------------------------------------------------------

# 📌 Key Insights to Present in an Interview

If this project is being used for a **Data Analyst / Business Analyst /
Data Science portfolio**, emphasize the analytical thinking rather than
only the model.

### Interview Story

> "I built UPISHIELD to analyze suspicious behavior in real-time payment
> transactions. I started by understanding transaction patterns through
> SQL and exploratory analysis, then engineered behavioral features such
> as transaction velocity, amount deviation, device novelty and
> unusual-hour activity. I combined rule-based signals with
> machine-learning/anomaly detection and created risk scores that could
> be consumed by a fraud-monitoring dashboard. The key focus was not
> just model accuracy, but reducing false positives and explaining why a
> transaction was considered risky."

### Skills Demonstrated

``` text
SQL
Python
Pandas
Data Cleaning
EDA
Feature Engineering
Statistics
Machine Learning
Fraud Analytics
Behavioral Analytics
Dashboard Development
Business Intelligence
Data Visualization
Git/GitHub
```

------------------------------------------------------------------------

# 📊 Recommended Project KPIs

When you have your final model results, add them here:

  KPI                                     Result
  ------------------------ ---------------------
  Total Transactions                `YOUR_VALUE`
  Fraud Transactions                `YOUR_VALUE`
  Fraud Rate                       `YOUR_VALUE%`
  Precision                        `YOUR_VALUE%`
  Recall                           `YOUR_VALUE%`
  F1 Score                         `YOUR_VALUE%`
  PR-AUC                            `YOUR_VALUE`
  False Positive Rate              `YOUR_VALUE%`
  Average Detection Time     `YOUR_VALUE ms/sec`

> **Do not invent these numbers.** Replace the placeholders with results
> calculated from your actual dataset and test set.

------------------------------------------------------------------------

# 🏆 Why This Project Is Portfolio-Strong

UPISHIELD demonstrates more than a simple machine-learning notebook.

It combines:

``` text
Business Problem
      ↓
Data Engineering
      ↓
SQL Analytics
      ↓
Behavioral Features
      ↓
Fraud Detection
      ↓
Model Evaluation
      ↓
Explainability
      ↓
Dashboard
      ↓
Business Recommendations
```

That makes it particularly suitable for demonstrating **Data Analyst,
Business Analyst, Fraud Analyst, FinTech Analytics and Junior Data
Scientist** skills.

------------------------------------------------------------------------

# 📚 References & Further Reading

-   GitHub documentation recommends a README for repositories so
    visitors can understand and navigate a project.
-   GitHub supports Mermaid diagrams directly in repositories, which can
    also be used for maintainable architecture and workflow
    documentation.
-   Current industry discussions increasingly emphasize real-time
    behavioral monitoring for instant-payment fraud because traditional
    delayed detection windows can be too slow.

For production implementations, consult official payment-network,
banking and regulatory guidance before making security or compliance
claims.

------------------------------------------------------------------------

# 👨‍💻 Author

**Syed Ziauddin**

Data Analyst / Business Analyst Aspirant

### Areas of Interest

-   Data Analytics
-   Business Intelligence
-   SQL
-   Python
-   Power BI
-   Fraud Analytics
-   FinTech
-   Machine Learning

------------------------------------------------------------------------

# ⭐ If You Find This Project Useful

If this repository helped you understand payment fraud analytics, feel
free to:

⭐ Star the repository\
🍴 Fork the project\
💬 Open an issue or discussion\
🔗 Connect with the author

------------------------------------------------------------------------

## 📄 License

This project is provided for educational and portfolio purposes. Add an
appropriate open-source license if you plan to distribute or modify the
project publicly.
