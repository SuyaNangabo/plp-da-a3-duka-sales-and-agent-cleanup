# plp-da-a3-duka-sales-and-agent-cleanup

Two client engagements for a Nairobi analytics consultancy, completed with Python (pandas and NumPy) and Google Sheets.

1. **Duka Electronics:** a half-year sales review for the Head of Sales, focused on answers rather than tables.
2. **Mobile money agent network:** an audit and clean-up of an unreliable transaction extract, followed by county and weekly summaries for the regional manager.

---

## Repository Structure

```
plp-da-a3-duka-sales-and-agent-cleanup/
├── README.md
├── requirements.txt
├── generate_data.py
├── duka_sales_exploration.ipynb
├── agent_cleanup.ipynb
├── cleaning_pipeline.py
├── excel/
│   └── duka_branch_summary.xlsx
└── outputs/
    ├── premium_online_coast_capital.csv
    └── agent_transactions_clean.csv
```

| File | Purpose |
|---|---|
| `generate_data.py` | Both dataset generators from this week, unchanged (Duka seed 2026, agent network seed 44) |
| `duka_sales_exploration.ipynb` | Engagement 1: inspection, derived columns, Tasks 3 to 7, spreadsheet check and Executive Summary |
| `excel/duka_branch_summary.xlsx` | SUMIFS branch revenue table, XLOOKUP region column and PivotTable of revenue by branch and channel |
| `outputs/premium_online_coast_capital.csv` | The 83 Premium online orders from Nairobi and Mombasa |
| `agent_cleanup.ipynb` | Engagement 2: audit table, cleaning, post-merge validation, summary tables and Data Quality Report |
| `cleaning_pipeline.py` | `clean_agent_data(txns, agents)`, which returns the clean DataFrame and a cleaning log |
| `outputs/agent_transactions_clean.csv` | 600 cleaned agent transactions with flag columns and agent county |
| `requirements.txt` | Python libraries used |

The raw generated CSVs (`duka_sales.csv`, `agents.csv` and `agent_transactions.csv`) are not committed. They can be recreated at any time with `generate_data.py`.

---

## How to Regenerate the Data

The data is synthetic and generated with fixed random seeds, so every run produces exactly the same files.

```
pip install -r requirements.txt
python generate_data.py
```

| File created | Rows | Description |
|---|---|---|
| `duka_sales.csv` | 1,000 | Duka Electronics orders, 1 January to 29 June 2026 |
| `agents.csv` | 20 | Agent register with agent ID, county and onboarding date |
| `agent_transactions.csv` | 612 | Agent transactions with deliberately injected data problems |

## How to Run the Notebooks

**In Google Colab**

1. Go to colab.research.google.com and choose **File > Upload notebook**.
2. Upload `duka_sales_exploration.ipynb`.
3. For the spreadsheet check, create a folder called `excel` in the Colab file panel and upload `duka_branch_summary.xlsx` into it.
4. Choose **Runtime > Restart session and run all**.
5. Repeat steps 1, 2 and 4 for `agent_cleanup.ipynb`.

**In Jupyter on your computer**

```
git clone https://github.com/<SuyaNangabo>/plp-da-a3-duka-sales-and-agent-cleanup.git
cd plp-da-a3-duka-sales-and-agent-cleanup
pip install -r requirements.txt
pip install notebook
jupyter notebook
```

Open each notebook and choose **Kernel > Restart & Run All**.

Each notebook writes and runs `generate_data.py` itself, so it works on its own. `agent_cleanup.ipynb` also writes `cleaning_pipeline.py` and then imports `clean_agent_data()` from it. Both notebooks save their results to the `outputs/` folder.

---

## Engagement 1: Duka Electronics

### Brief

Duka Electronics' leadership team is preparing its half-year review for January to June 2026. The Head of Sales asked for answers to a set of questions ahead of the meeting.

### Executive Summary

- Total revenue for January to June 2026 was KES 71.8M from 1,000 orders, and Nairobi contributed KES 26.1M, which is 36.4% of the total and almost double Mombasa in second place (KES 14.0M).
- Laptops generated KES 41.5M, more than double the next product (Tablets at KES 19.3M), even though Tablets sold more units (691 against 639).
- Weekend orders are worth the same as weekday orders on average (KES 71,972 against KES 71,724), so there is no case for weekend-only promotions based on basket size.
- April was the strongest month at KES 13.5M, 24.0% above June, the weakest month at KES 10.9M.
- Premium online orders from Nairobi and Mombasa came to 83 orders worth KES 10.2M, which makes them a clear target group for online marketing.

### Method

1. **First-five-minutes inspection:** loaded with `parse_dates=["order_date"]`, then checked shape, column types, missing values, date range and the main categories.
2. **Derived columns:** `revenue` (quantity × unit price), `month`, `weekday`, `is_weekend`, and `price_band` (Premium at KES 28,000 or more, otherwise Value).
3. **Analysis:** `groupby` with named aggregation, `rank`, `nlargest`, boolean filters and `isin`.
4. **Export:** Premium online orders from Nairobi and Mombasa saved with `index=False`.
5. **Spreadsheet check:** SUMIFS totals read back from the Excel file and compared with pandas.

### Inspection Findings

| Check | Result |
|---|---|
| Shape | 1,000 rows and 7 columns |
| Missing values | None |
| Date range | 1 January 2026 to 29 June 2026 |
| Orders by branch | Nairobi 376, Mombasa 186, Nakuru 162, Kisumu 159, Eldoret 117 |
| Orders by channel | In-store 57.9%, Online 32.0%, Phone order 10.1% |

### Task 3: Branch Rankings

| Branch | Total revenue (KES) | Orders | Average order (KES) | Revenue rank | Orders rank |
|---|---|---|---|---|---|
| Nairobi | 26,106,100 | 376 | 69,431 | 1 | 1 |
| Mombasa | 14,003,700 | 186 | 75,289 | 2 | 2 |
| Nakuru | 11,970,400 | 162 | 73,891 | 3 | 3 |
| Kisumu | 10,868,100 | 159 | 68,353 | 4 | 4 |
| Eldoret | 8,844,200 | 117 | 75,591 | 5 | 5 |

The two rankings are the same. Average order values are similar across branches (KES 68,353 to KES 75,591), so order volume decides revenue. Eldoret has the highest average order but the fewest orders, so it still ranks last.

### Task 4: Top Products

| Rank | By revenue (KES) | By units sold |
|---|---|---|
| 1 | Laptop, 41,535,000 | Tablet, 691 |
| 2 | Tablet, 19,348,000 | Laptop, 639 |
| 3 | Phone, 8,880,000 | Phone, 592 |

Tablets sell more units, but a laptop costs KES
