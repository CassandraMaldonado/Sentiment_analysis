import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="AI Readiness Navigator", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #ff6b6b;
}
.recommendation-box {
    background-color: #e8f5e8;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #4caf50;
}
.warning-box {
    background-color: #fff3cd;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #ffc107;
}
.impact-high { color: #dc3545; font-weight: bold; }
.impact-medium { color: #fd7e14; font-weight: bold; }
.impact-low { color: #28a745; font-weight: bold; }
.paradigm-shift { 
    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Real Data from Analysis Charts
# ------------------------------
def load_industry_data():
    # From Chart 3: Total AI Mentions of Top Industries
    industry_data = {
        'Tech': {'mentions': 31665, 'rank': 1, 'impact_level': 'High'},
        'Finance': {'mentions': 5330, 'rank': 5, 'impact_level': 'Medium'},
        'Healthcare': {'mentions': 7300, 'rank': 3, 'impact_level': 'High'},
        'Media': {'mentions': 4592, 'rank': 7, 'impact_level': 'Emerging'},
        'Retail': {'mentions': 8147, 'rank': 2, 'impact_level': 'High'},
        'Government': {'mentions': 2816, 'rank': 8, 'impact_level': 'Low'},
        'Education': {'mentions': 6765, 'rank': 4, 'impact_level': 'Medium'},
        'Energy': {'mentions': 4788, 'rank': 6, 'impact_level': 'Emerging'},
        'Manufacturing': {'mentions': 1611, 'rank': 9, 'impact_level': 'Low'},
        'Transport': {'mentions': 710, 'rank': 10, 'impact_level': 'Emerging'}
    }
    
    # Topic relevance from Chart 4 heatmap (key paradigm shift areas)
    topic_relevance = {
        'Tech': {
            'Consumer Tech & AI': 0.095,
            'Digital Trading': 0.083, 
            'Corporate Finance': 0.218,
            'paradigm_technologies': ['Generative Models', 'ChatGPT', 'Computer Vision']
        },
        'Finance': {
            'Consumer Services': 0.477,
            'Financial Markets': 0.051,
            'Digital Trading': 0.103,
            'paradigm_technologies': ['ChatGPT', 'Automation', 'AI Systems']
        },
        'Healthcare': {
            'Corporate Finance': 0.364,
            'Medical & Scientific': 0.101,
            'Consumer Tech': 0.065,
            'paradigm_technologies': ['Medical AI', 'Computer Vision', 'NLP']
        },
        'Media': {
            'Services & Digital Trading': 0.165,
            'Consumer Tech': 0.148,
            'Online Services': 0.115,
            'paradigm_technologies': ['Generative Models', 'AI Safety', 'Computer Vision']
        },
        'Education': {
            'Consumer Tech & AI': 0.233,
            'Digital Trends': 0.149,
            'Online Services': 0.117,
            'paradigm_technologies': ['ChatGPT', 'NLP', 'Educational AI']
        },
        'Retail': {
            'Corporate Finance': 0.214,
            'IT Hardware': 0.204,
            'Digital Trading': 0.075,
            'paradigm_technologies': ['Recommendation Systems', 'Computer Vision', 'Automation']
        },
        'Government': {
            'Consumer Tech & AI': 0.194,
            'Digital Trends': 0.183,
            'Online Services': 0.100,
            'paradigm_technologies': ['AI Systems', 'Automation', 'NLP']
        },
        'Energy': {
            'Corporate Finance': 0.232,
            'IT Hardware': 0.135,
            'Digital Trading': 0.089,
            'paradigm_technologies': ['Predictive AI', 'IoT Integration', 'Automation']
        },
        'Manufacturing': {
            'Consumer Tech & AI': 0.130,
            'Corporate Finance': 0.127,
            'Digital Trading': 0.120,
            'paradigm_technologies': ['Predictive AI', 'IoT Integration', 'Automation']
        },
        'Transport': {
            'Corporate Finance': 0.261,
            'IT Hardware': 0.156,
            'Digital Trading': 0.067,
            'paradigm_technologies': ['Autonomous Systems', 'Computer Vision', 'IoT']
        }
    }
    
    # Combine data
    for industry in industry_data:
        industry_data[industry].update(topic_relevance.get(industry, {}))
    
    return industry_data

def load_technology_data():
    # From Chart 7: AI Technology Mentions
    return {
        'AI': 177335,
        'NLP': 165047,
        'Generative Models': 109424,
        'ChatGPT': 57722,
        'Automation': 49849,
        'Machine Learning': 35037,
        'Foundation Models': 31374,
        'Computer Vision': 27004,
        'Algorithm': 26108,
        'AI Safety': 23968,
        'Robotics': 23224,
        'Speech AI': 21053,
        'GPT': 17401,
        'Deep Learning': 15256
    }

def load_use_case_data():
    # From Chart 5: AI Use Cases by Category Breakdown
    return {
        'Conversational AI': {
            'Customer Service': 44700,
            'HR Systems': 150194,
            'Technical Support': 11526,
            'Educational Support': 7760,
            'Healthcare Support': 350
        },
        'Generative Vision': {
            'Marketing Content': 79870,
            'Product Design': 50410,
            'Fashion Design': 441,
            'Media Production': 5676
        },
        'Workflow Automation': {
            'CRM Integration': 4396,
            'Task Automation': 32007,
            'Financial Operations': 1500,
            'Supply Chain': 409,
            'Legal Operations': 490
        }
    }

def load_job_impact_data():
    # From Chart 6: Job automation risk data
    return {
        'High Impact (80-100% automation potential)': {
            'Delivery Driver': 204,
            'Receptionist': 119, 
            'Truck Driver': 281,
            'Cashier': 245
        },
        'Medium-High Impact (60-79% automation potential)': {
            'Data Analyst': 1104,
            'Customer Service Rep': 10338,
            'Accountant': 857,
            'Financial Analyst': 375
        },
        'Medium Impact (40-59% augmentation potential)': {
            'Developer': 28200,
            'Software Engineer': 4991,
            'ML Engineer': 643,
            'AI Engineer': 1338,
            'Nurse': 3096,
            'Teacher': 11015,
            'Lawyer': 6651
        }
    }

def load_real_time_series_data():
    """Load actual time series data from analysis"""
    # Real data from your analysis
    raw_data = {
        'AI': [(('2023-01', 'M'), 65615), (('2017-01', 'M'), 930), (('2022-01', 'M'), 22068), (('2019-01', 'M'), 1784), (('2024-01', 'M'), 38851), (('2025-01', 'M'), 11946), (('2002-01', 'M'), 320), (('2021-01', 'M'), 4080), (('2000-01', 'M'), 1716), (('2003-01', 'M'), 155), (('2020-01', 'M'), 2561), (('2011-01', 'M'), 212), (('2010-01', 'M'), 337), (('2023-02', 'M'), 162), (('2018-01', 'M'), 1439), (('2025-11', 'M'), 22), (('2025-03', 'M'), 63), (('2031-01', 'M'), 181), (('2024-02', 'M'), 287), (('2029-01', 'M'), 180), (('2013-01', 'M'), 469), (('2024-04', 'M'), 214), (('2024-03', 'M'), 221), (('2030-01', 'M'), 1262), (('2022-10', 'M'), 32), (('2016-01', 'M'), 833), (('2023-11', 'M'), 270), (('2050-01', 'M'), 120), (('2022-04', 'M'), 50), (('2008-01', 'M'), 361), (('2007-01', 'M'), 295), (('2027-01', 'M'), 473), (('2024-07', 'M'), 117), (('2015-01', 'M'), 844), (('2024-06', 'M'), 177), (('2026-01', 'M'), 632), (('2005-01', 'M'), 278), (('2082-01', 'M'), 18), (('2022-12', 'M'), 64), (('2023-03', 'M'), 195), (('2077-01', 'M'), 75), (('2009-01', 'M'), 197), (('2012-01', 'M'), 664), (('2028-01', 'M'), 421), (('2049-01', 'M'), 42), (('2001-01', 'M'), 354), (('2023-07', 'M'), 260), (('2040-01', 'M'), 118), (('2032-01', 'M'), 366), (('2024-11', 'M'), 85), (('2024-05', 'M'), 261), (('2043-01', 'M'), 9), (('2036-01', 'M'), 13), (('2014-01', 'M'), 405), (('2024-09', 'M'), 108), (('2055-01', 'M'), 10), (('2024-10', 'M'), 105), (('2023-10', 'M'), 175), (('2023-05', 'M'), 327), (('2023-12', 'M'), 204), (('2024-08', 'M'), 78), (('2042-01', 'M'), 34), (('2025-04', 'M'), 314), (('2097-01', 'M'), 8), (('2006-01', 'M'), 154), (('2023-09', 'M'), 177), (('2022-06', 'M'), 22), (('2073-01', 'M'), 8), (('2023-06', 'M'), 196), (('2023-08', 'M'), 222), (('2025-06', 'M'), 6), (('2023-04', 'M'), 193), (('2035-01', 'M'), 125), (('2022-03', 'M'), 34), (('2054-01', 'M'), 4), (('2025-02', 'M'), 93), (('2034-01', 'M'), 63), (('2099-01', 'M'), 7), (('2045-01', 'M'), 16), (('2047-01', 'M'), 27), (('2081-01', 'M'), 16), (('2070-01', 'M'), 31), (('2022-07', 'M'), 28), (('2022-05', 'M'), 34), (('2004-01', 'M'), 209), (('2024-12', 'M'), 78), (('2033-01', 'M'), 150), (('2025-07', 'M'), 8), (('2038-01', 'M'), 6), (('2025-05', 'M'), 13), (('2059-01', 'M'), 12), (('2061-01', 'M'), 15), (('2062-01', 'M'), 21), (('2022-09', 'M'), 40), (('2089-01', 'M'), 11), (('2063-01', 'M'), 10), (('2091-01', 'M'), 13), (('2048-01', 'M'), 13), (('2022-11', 'M'), 40), (('2068-01', 'M'), 10), (('2090-01', 'M'), 6), (('2092-01', 'M'), 11), (('2078-01', 'M'), 2), (('2014-02', 'M'), 1), (('2083-01', 'M'), 8), (('2087-01', 'M'), 6), (('2094-01', 'M'), 2), (('2052-01', 'M'), 18), (('2044-01', 'M'), 9), (('2053-01', 'M'), 5), (('2022-02', 'M'), 15), (('2098-01', 'M'), 6), (('2037-01', 'M'), 8), (('2060-01', 'M'), 14), (('2051-01', 'M'), 4), (('2022-08', 'M'), 28), (('2057-01', 'M'), 4), (('2041-01', 'M'), 8), (('2080-01', 'M'), 11), (('2064-01', 'M'), 4), (('2019-12', 'M'), 1), (('2071-01', 'M'), 5), (('2096-01', 'M'), 10), (('2072-01', 'M'), 13), (('2039-01', 'M'), 4), (('2084-01', 'M'), 5), (('2046-01', 'M'), 5), (('2025-08', 'M'), 4), (('2025-10', 'M'), 6), (('2021-10', 'M'), 2), (('2088-01', 'M'), 10), (('2069-01', 'M'), 4), (('2067-01', 'M'), 9), (('2095-01', 'M'), 4), (('2074-01', 'M'), 5), (('2065-01', 'M'), 4), (('2058-01', 'M'), 8), (('2086-01', 'M'), 5), (('2021-12', 'M'), 4), (('2093-01', 'M'), 7), (('2012-10', 'M'), 2), (('2056-01', 'M'), 15), (('2017-02', 'M'), 2), (('2020-05', 'M'), 1), (('2079-01', 'M'), 2), (('2076-01', 'M'), 5), (('2021-08', 'M'), 1), (('2025-09', 'M'), 1), (('2085-01', 'M'), 5), (('2021-11', 'M'), 1), (('2075-01', 'M'), 5), (('2019-05', 'M'), 1), (('2066-01', 'M'), 1), (('2020-08', 'M'), 1), (('2029-09', 'M'), 1), (('2021-04', 'M'), 1)],
        'Artificial Intelligence': [(('2023-01', 'M'), 50123), (('2017-01', 'M'), 578), (('2022-01', 'M'), 14752), (('2019-01', 'M'), 1304), (('2024-01', 'M'), 25489), (('2025-01', 'M'), 6851), (('2002-01', 'M'), 203), (('2021-01', 'M'), 3014), (('2000-01', 'M'), 1113), (('2003-01', 'M'), 89), (('2020-01', 'M'), 1810), (('2011-01', 'M'), 125), (('2010-01', 'M'), 241), (('2023-02', 'M'), 112), (('2018-01', 'M'), 1015), (('2025-11', 'M'), 14), (('2025-03', 'M'), 37), (('2031-01', 'M'), 141), (('2024-02', 'M'), 203), (('2029-01', 'M'), 130), (('2013-01', 'M'), 330), (('2024-04', 'M'), 147), (('2024-03', 'M'), 147), (('2030-01', 'M'), 1015), (('2022-10', 'M'), 21), (('2016-01', 'M'), 579), (('2023-11', 'M'), 194), (('2050-01', 'M'), 88), (('2022-04', 'M'), 38), (('2008-01', 'M'), 239), (('2007-01', 'M'), 202), (('2027-01', 'M'), 355), (('2024-07', 'M'), 71), (('2015-01', 'M'), 599), (('2024-06', 'M'), 108), (('2026-01', 'M'), 472), (('2005-01', 'M'), 192), (('2082-01', 'M'), 10), (('2022-12', 'M'), 50), (('2023-03', 'M'), 135), (('2077-01', 'M'), 30), (('2009-01', 'M'), 141), (('2012-01', 'M'), 487), (('2028-01', 'M'), 315), (('2049-01', 'M'), 27), (('2001-01', 'M'), 260), (('2023-07', 'M'), 205), (('2040-01', 'M'), 88), (('2032-01', 'M'), 268), (('2024-11', 'M'), 39), (('2024-05', 'M'), 193), (('2043-01', 'M'), 3), (('2036-01', 'M'), 8), (('2014-01', 'M'), 298), (('2024-09', 'M'), 45), (('2055-01', 'M'), 8), (('2024-10', 'M'), 48), (('2023-10', 'M'), 135), (('2023-05', 'M'), 236), (('2023-12', 'M'), 142), (('2024-08', 'M'), 50), (('2042-01', 'M'), 24), (('2025-04', 'M'), 119), (('2097-01', 'M'), 5), (('2006-01', 'M'), 112), (('2023-09', 'M'), 123), (('2022-06', 'M'), 14), (('2073-01', 'M'), 5), (('2023-06', 'M'), 145), (('2023-08', 'M'), 141), (('2025-06', 'M'), 4), (('2023-04', 'M'), 111), (('2035-01', 'M'), 89), (('2022-03', 'M'), 27), (('2054-01', 'M'), 2), (('2025-02', 'M'), 63), (('2034-01', 'M'), 46), (('2099-01', 'M'), 3), (('2045-01', 'M'), 6), (('2047-01', 'M'), 18), (('2081-01', 'M'), 2), (('2070-01', 'M'), 11), (('2022-07', 'M'), 18), (('2022-05', 'M'), 18), (('2004-01', 'M'), 151), (('2024-12', 'M'), 42), (('2033-01', 'M'), 103), (('2025-07', 'M'), 3), (('2038-01', 'M'), 3), (('2025-05', 'M'), 8), (('2059-01', 'M'), 5), (('2061-01', 'M'), 4), (('2062-01', 'M'), 15), (('2022-09', 'M'), 34), (('2089-01', 'M'), 9), (('2063-01', 'M'), 2), (('2091-01', 'M'), 9), (('2048-01', 'M'), 8), (('2022-11', 'M'), 31), (('2068-01', 'M'), 1), (('2090-01', 'M'), 3), (('2092-01', 'M'), 5), (('2078-01', 'M'), 1), (('2014-02', 'M'), 1), (('2083-01', 'M'), 4), (('2087-01', 'M'), 2), (('2094-01', 'M'), 1), (('2052-01', 'M'), 13), (('2044-01', 'M'), 3), (('2053-01', 'M'), 1), (('2022-02', 'M'), 12), (('2098-01', 'M'), 5), (('2037-01', 'M'), 6), (('2060-01', 'M'), 4), (('2051-01', 'M'), 3), (('2022-08', 'M'), 18), (('2057-01', 'M'), 1), (('2041-01', 'M'), 2), (('2080-01', 'M'), 4), (('2064-01', 'M'), 0), (('2019-12', 'M'), 0), (('2071-01', 'M'), 5), (('2096-01', 'M'), 4), (('2072-01', 'M'), 8), (('2039-01', 'M'), 3), (('2084-01', 'M'), 2), (('2046-01', 'M'), 3), (('2025-08', 'M'), 2), (('2025-10', 'M'), 4), (('2021-10', 'M'), 1), (('2088-01', 'M'), 0), (('2069-01', 'M'), 2), (('2067-01', 'M'), 0), (('2095-01', 'M'), 1), (('2074-01', 'M'), 2), (('2065-01', 'M'), 2), (('2058-01', 'M'), 0), (('2086-01', 'M'), 2), (('2021-12', 'M'), 3), (('2093-01', 'M'), 5), (('2012-10', 'M'), 0), (('2056-01', 'M'), 13), (('2017-02', 'M'), 2), (('2020-05', 'M'), 1), (('2079-01', 'M'), 0), (('2076-01', 'M'), 0), (('2021-08', 'M'), 1), (('2025-09', 'M'), 0), (('2085-01', 'M'), 3), (('2021-11', 'M'), 0), (('2075-01', 'M'), 3), (('2019-05', 'M'), 1), (('2066-01', 'M'), 0), (('2020-08', 'M'), 1), (('2029-09', 'M'), 1), (('2021-04', 'M'), 1)],
        'GPT': [(('2023-01', 'M'), 7469), (('2017-01', 'M'), 125), (('2022-01', 'M'), 1359), (('2019-01', 'M'), 229), (('2024-01', 'M'), 3422), (('2025-01', 'M'), 886), (('2002-01', 'M'), 14), (('2021-01', 'M'), 462), (('2000-01', 'M'), 179), (('2003-01', 'M'), 11), (('2020-01', 'M'), 268), (('2011-01', 'M'), 20), (('2010-01', 'M'), 62), (('2023-02', 'M'), 25), (('2018-01', 'M'), 194), (('2025-11', 'M'), 1), (('2025-03', 'M'), 6), (('2031-01', 'M'), 6), (('2024-02', 'M'), 12), (('2029-01', 'M'), 10), (('2013-01', 'M'), 66), (('2024-04', 'M'), 26), (('2024-03', 'M'), 18), (('2030-01', 'M'), 79), (('2022-10', 'M'), 0), (('2016-01', 'M'), 145), (('2023-11', 'M'), 30), (('2050-01', 'M'), 6), (('2022-04', 'M'), 0), (('2008-01', 'M'), 48), (('2007-01', 'M'), 38), (('2027-01', 'M'), 36), (('2024-07', 'M'), 6), (('2015-01', 'M'), 212), (('2024-06', 'M'), 11), (('2026-01', 'M'), 45), (('2005-01', 'M'), 30), (('2082-01', 'M'), 4), (('2022-12', 'M'), 6), (('2023-03', 'M'), 58), (('2077-01', 'M'), 7), (('2009-01', 'M'), 24), (('2012-01', 'M'), 65), (('2028-01', 'M'), 16), (('2049-01', 'M'), 3), (('2001-01', 'M'), 37), (('2023-07', 'M'), 16), (('2040-01', 'M'), 12), (('2032-01', 'M'), 27), (('2024-11', 'M'), 4), (('2024-05', 'M'), 48), (('2043-01', 'M'), 1), (('2036-01', 'M'), 0), (('2014-01', 'M'), 46), (('2024-09', 'M'), 9), (('2055-01', 'M'), 2), (('2024-10', 'M'), 20), (('2023-10', 'M'), 6), (('2023-05', 'M'), 49), (('2023-12', 'M'), 34), (('2024-08', 'M'), 15), (('2042-01', 'M'), 2), (('2025-04', 'M'), 13), (('2097-01', 'M'), 1), (('2006-01', 'M'), 16), (('2023-09', 'M'), 16), (('2022-06', 'M'), 0), (('2073-01', 'M'), 0), (('2023-06', 'M'), 17), (('2023-08', 'M'), 32), (('2025-06', 'M'), 0), (('2023-04', 'M'), 53), (('2035-01', 'M'), 10), (('2022-03', 'M'), 2), (('2054-01', 'M'), 0), (('2025-02', 'M'), 4), (('2034-01', 'M'), 5), (('2099-01', 'M'), 0), (('2045-01', 'M'), 0), (('2047-01', 'M'), 2), (('2081-01', 'M'), 0), (('2070-01', 'M'), 2), (('2022-07', 'M'), 3), (('2022-05', 'M'), 1), (('2004-01', 'M'), 9), (('2024-12', 'M'), 3), (('2033-01', 'M'), 8), (('2025-07', 'M'), 0), (('2038-01', 'M'), 0), (('2025-05', 'M'), 0), (('2059-01', 'M'), 0), (('2061-01', 'M'), 0), (('2062-01', 'M'), 3), (('2022-09', 'M'), 2), (('2089-01', 'M'), 3), (('2063-01', 'M'), 0), (('2091-01', 'M'), 0), (('2048-01', 'M'), 3), (('2022-11', 'M'), 1), (('2068-01', 'M'), 0), (('2090-01', 'M'), 1), (('2092-01', 'M'), 1), (('2078-01', 'M'), 0), (('2014-02', 'M'), 0), (('2083-01', 'M'), 2), (('2087-01', 'M'), 0), (('2094-01', 'M'), 0), (('2052-01', 'M'), 4), (('2044-01', 'M'), 0), (('2053-01', 'M'), 0), (('2022-02', 'M'), 1), (('2098-01', 'M'), 0), (('2037-01', 'M'), 2), (('2060-01', 'M'), 3), (('2051-01', 'M'), 0), (('2022-08', 'M'), 0), (('2057-01', 'M'), 0), (('2041-01', 'M'), 0), (('2080-01', 'M'), 1), (('2064-01', 'M'), 1), (('2019-12', 'M'), 1), (('2071-01', 'M'), 1), (('2096-01', 'M'), 0), (('2072-01', 'M'), 0), (('2039-01', 'M'), 1), (('2084-01', 'M'), 0), (('2046-01', 'M'), 0), (('2025-08', 'M'), 0), (('2025-10', 'M'), 0), (('2021-10', 'M'), 1), (('2088-01', 'M'), 0), (('2069-01', 'M'), 0), (('2067-01', 'M'), 0), (('2095-01', 'M'), 0), (('2074-01', 'M'), 0), (('2065-01', 'M'), 0), (('2058-01', 'M'), 0), (('2086-01', 'M'), 0), (('2021-12', 'M'), 0), (('2093-01', 'M'), 0), (('2012-10', 'M'), 0), (('2056-01', 'M'), 0), (('2017-02', 'M'), 0), (('2020-05', 'M'), 0), (('2079-01', 'M'), 0), (('2076-01', 'M'), 0), (('2021-08', 'M'), 0), (('2025-09', 'M'), 0), (('2085-01', 'M'), 0), (('2021-11', 'M'), 0), (('2075-01', 'M'), 0), (('2019-05', 'M'), 0), (('2066-01', 'M'), 0), (('2020-08', 'M'), 0), (('2029-09', 'M'), 0), (('2021-04', 'M'), 0)],
        'Machine Learning': [(('2023-01', 'M'), 13067), (('2017-01', 'M'), 182), (('2022-01', 'M'), 6439), (('2019-01', 'M'), 392), (('2024-01', 'M'), 5443), (('2025-01', 'M'), 1522), (('2002-01', 'M'), 34), (('2021-01', 'M'), 902), (('2000-01', 'M'), 239), (('2003-01', 'M'), 25), (('2020-01', 'M'), 630), (('2011-01', 'M'), 44), (('2010-01', 'M'), 92), (('2023-02', 'M'), 26), (('2018-01', 'M'), 264), (('2025-11', 'M'), 0), (('2025-03', 'M'), 12), (('2031-01', 'M'), 84), (('2024-02', 'M'), 31), (('2029-01', 'M'), 50), (('2013-01', 'M'), 114), (('2024-04', 'M'), 22), (('2024-03', 'M'), 29), (('2030-01', 'M'), 383), (('2022-10', 'M'), 5), (('2016-01', 'M'), 157), (('2023-11', 'M'), 45), (('2050-01', 'M'), 18), (('2022-04', 'M'), 11), (('2008-01', 'M'), 64), (('2007-01', 'M'), 38), (('2027-01', 'M'), 131), (('2024-07', 'M'), 21), (('2015-01', 'M'), 120), (('2024-06', 'M'), 22), (('2026-01', 'M'), 122), (('2005-01', 'M'), 70), (('2082-01', 'M'), 1), (('2022-12', 'M'), 14), (('2023-03', 'M'), 29), (('2077-01', 'M'), 10), (('2009-01', 'M'), 39), (('2012-01', 'M'), 165), (('2028-01', 'M'), 143), (('2049-01', 'M'), 4), (('2001-01', 'M'), 50), (('2023-07', 'M'), 41), (('2040-01', 'M'), 10), (('2032-01', 'M'), 185), (('2024-11', 'M'), 37), (('2024-05', 'M'), 25), (('2043-01', 'M'), 0), (('2036-01', 'M'), 2), (('2014-01', 'M'), 77), (('2024-09', 'M'), 19), (('2055-01', 'M'), 2), (('2024-10', 'M'), 13), (('2023-10', 'M'), 17), (('2023-05', 'M'), 21), (('2023-12', 'M'), 20), (('2024-08', 'M'), 16), (('2042-01', 'M'), 6), (('2025-04', 'M'), 39), (('2097-01', 'M'), 1), (('2006-01', 'M'), 26), (('2023-09', 'M'), 15), (('2022-06', 'M'), 7), (('2073-01', 'M'), 0), (('2023-06', 'M'), 22), (('2023-08', 'M'), 18), (('2025-06', 'M'), 2), (('2023-04', 'M'), 19), (('2035-01', 'M'), 26), (('2022-03', 'M'), 9), (('2054-01', 'M'), 1), (('2025-02', 'M'), 3), (('2034-01', 'M'), 24), (('2099-01', 'M'), 2), (('2045-01', 'M'), 1), (('2047-01', 'M'), 5), (('2081-01', 'M'), 0), (('2070-01', 'M'), 3), (('2022-07', 'M'), 8), (('2022-05', 'M'), 12), (('2004-01', 'M'), 33), (('2024-12', 'M'), 17), (('2033-01', 'M'), 69), (('2025-07', 'M'), 0), (('2038-01', 'M'), 0), (('2025-05', 'M'), 7), (('2059-01', 'M'), 1), (('2061-01', 'M'), 1), (('2062-01', 'M'), 0), (('2022-09', 'M'), 14), (('2089-01', 'M'), 4), (('2063-01', 'M'), 0), (('2091-01', 'M'), 2), (('2048-01', 'M'), 4), (('2022-11', 'M'), 8), (('2068-01', 'M'), 0), (('2090-01', 'M'), 1), (('2092-01', 'M'), 2), (('2078-01', 'M'), 0), (('2014-02', 'M'), 1), (('2083-01', 'M'), 0), (('2087-01', 'M'), 1), (('2094-01', 'M'), 0), (('2052-01', 'M'), 1), (('2044-01', 'M'), 1), (('2053-01', 'M'), 0), (('2022-02', 'M'), 8), (('2098-01', 'M'), 1), (('2037-01', 'M'), 0), (('2060-01', 'M'), 2), (('2051-01', 'M'), 0), (('2022-08', 'M'), 5), (('2057-01', 'M'), 0), (('2041-01', 'M'), 1), (('2080-01', 'M'), 0), (('2064-01', 'M'), 0), (('2019-12', 'M'), 1), (('2071-01', 'M'), 1), (('2096-01', 'M'), 1), (('2072-01', 'M'), 2), (('2039-01', 'M'), 0), (('2084-01', 'M'), 1), (('2046-01', 'M'), 0), (('2025-08', 'M'), 0), (('2025-10', 'M'), 0), (('2021-10', 'M'), 0), (('2088-01', 'M'), 1), (('2069-01', 'M'), 1), (('2067-01', 'M'), 0), (('2095-01', 'M'), 0), (('2074-01', 'M'), 1), (('2065-01', 'M'), 0), (('2058-01', 'M'), 0), (('2086-01', 'M'), 1), (('2021-12', 'M'), 1), (('2093-01', 'M'), 0), (('2012-10', 'M'), 1), (('2056-01', 'M'), 1), (('2017-02', 'M'), 1), (('2020-05', 'M'), 0), (('2079-01', 'M'), 0), (('2076-01', 'M'), 0), (('2021-08', 'M'), 0), (('2025-09', 'M'), 0), (('2085-01', 'M'), 0), (('2021-11', 'M'), 1), (('2075-01', 'M'), 1), (('2019-05', 'M'), 0), (('2066-01', 'M'), 0), (('2020-08', 'M'), 0), (('2029-09', 'M'), 0), (('2021-04', 'M'), 0)],
        'ChatGPT': [(('2023-01', 'M'), 22698), (('2017-01', 'M'), 283), (('2022-01', 'M'), 3636), (('2019-01', 'M'), 807), (('2024-01', 'M'), 10841), (('2025-01', 'M'), 3296), (('2002-01', 'M'), 81), (('2021-01', 'M'), 1413), (('2000-01', 'M'), 609), (('2003-01', 'M'), 32), (('2020-01', 'M'), 668), (('2011-01', 'M'), 78), (('2010-01', 'M'), 144), (('2023-02', 'M'), 114), (('2018-01', 'M'), 586), (('2025-11', 'M'), 4), (('2025-03', 'M'), 14), (('2031-01', 'M'), 11), (('2024-02', 'M'), 92), (('2029-01', 'M'), 25), (('2013-01', 'M'), 207), (('2024-04', 'M'), 62), (('2024-03', 'M'), 46), (('2030-01', 'M'), 316), (('2022-10', 'M'), 1), (('2016-01', 'M'), 337), (('2023-11', 'M'), 133), (('2050-01', 'M'), 25), (('2022-04', 'M'), 0), (('2008-01', 'M'), 137), (('2007-01', 'M'), 136), (('2027-01', 'M'), 139), (('2024-07', 'M'), 14), (('2015-01', 'M'), 468), (('2024-06', 'M'), 43), (('2026-01', 'M'), 212), (('2005-01', 'M'), 94), (('2082-01', 'M'), 8), (('2022-12', 'M'), 28), (('2023-03', 'M'), 114), (('2077-01', 'M'), 24), (('2009-01', 'M'), 60), (('2012-01', 'M'), 160), (('2028-01', 'M'), 67), (('2049-01', 'M'), 5), (('2001-01', 'M'), 123), (('2023-07', 'M'), 126), (('2040-01', 'M'), 48), (('2032-01', 'M'), 39), (('2024-11', 'M'), 14), (('2024-05', 'M'), 101), (('2043-01', 'M'), 1), (('2036-01', 'M'), 3), (('2014-01', 'M'), 146), (('2024-09', 'M'), 15), (('2055-01', 'M'), 5), (('2024-10', 'M'), 19), (('2023-10', 'M'), 61), (('2023-05', 'M'), 189), (('2023-12', 'M'), 81), (('2024-08', 'M'), 24), (('2042-01', 'M'), 11), (('2025-04', 'M'), 28), (('2097-01', 'M'), 3), (('2006-01', 'M'), 60), (('2023-09', 'M'), 71), (('2022-06', 'M'), 1), (('2073-01', 'M'), 0), (('2023-06', 'M'), 86), (('2023-08', 'M'), 83), (('2025-06', 'M'), 0), (('2023-04', 'M'), 116), (('2035-01', 'M'), 31), (('2022-03', 'M'), 0), (('2054-01', 'M'), 0), (('2025-02', 'M'), 22), (('2034-01', 'M'), 14), (('2099-01', 'M'), 1), (('2045-01', 'M'), 3), (('2047-01', 'M'), 8), (('2081-01', 'M'), 1), (('2070-01', 'M'), 7), (('2022-07', 'M'), 1), (('2022-05', 'M'), 1), (('2004-01', 'M'), 87), (('2024-12', 'M'), 10), (('2033-01', 'M'), 22), (('2025-07', 'M'), 0), (('2038-01', 'M'), 1), (('2025-05', 'M'), 7), (('2059-01', 'M'), 3), (('2061-01', 'M'), 2), (('2062-01', 'M'), 9), (('2022-09', 'M'), 2), (('2089-01', 'M'), 8), (('2063-01', 'M'), 1), (('2091-01', 'M'), 5), (('2048-01', 'M'), 2), (('2022-11', 'M'), 2), (('2068-01', 'M'), 0), (('2090-01', 'M'), 2), (('2092-01', 'M'), 3), (('2078-01', 'M'), 1), (('2014-02', 'M'), 1), (('2083-01', 'M'), 3), (('2087-01', 'M'), 2), (('2094-01', 'M'), 1), (('2052-01', 'M'), 9), (('2044-01', 'M'), 0), (('2053-01', 'M'), 0), (('2022-02', 'M'), 0), (('2098-01', 'M'), 3), (('2037-01', 'M'), 4), (('2060-01', 'M'), 4), (('2051-01', 'M'), 1), (('2022-08', 'M'), 0), (('2057-01', 'M'), 1), (('2041-01', 'M'), 3), (('2080-01', 'M'), 3), (('2064-01', 'M'), 0), (('2019-12', 'M'), 1), (('2071-01', 'M'), 2), (('2096-01', 'M'), 3), (('2072-01', 'M'), 4), (('2039-01', 'M'), 1), (('2084-01', 'M'), 0), (('2046-01', 'M'), 2), (('2025-08', 'M'), 0), (('2025-10', 'M'), 1), (('2021-10', 'M'), 1), (('2088-01', 'M'), 0), (('2069-01', 'M'), 0), (('2067-01', 'M'), 0), (('2095-01', 'M'), 1), (('2074-01', 'M'), 3), (('2065-01', 'M'), 1), (('2058-01', 'M'), 0), (('2086-01', 'M'), 2), (('2021-12', 'M'), 1), (('2093-01', 'M'), 4), (('2012-10', 'M'), 0), (('2056-01', 'M'), 3), (('2017-02', 'M'), 0), (('2020-05', 'M'), 0), (('2079-01', 'M'), 1), (('2076-01', 'M'), 0), (('2021-08', 'M'), 0), (('2025-09', 'M'), 0), (('2085-01', 'M'), 0), (('2021-11', 'M'), 0), (('2075-01', 'M'), 2), (('2019-05', 'M'), 0), (('2066-01', 'M'), 0), (('2020-08', 'M'), 0), (('2029-09', 'M'), 1), (('2021-04', 'M'), 0)]
    }
    
    # Convert to clean format
    clean_data = {}
    for tech, data_list in raw_data.items():
        # Create dictionary mapping dates to values
        date_dict = {}
        for date_period_tuple, count in data_list:
            if isinstance(date_period_tuple, tuple):
                date_str = date_period_tuple[0]  # Extract the date string like '2023-01'
                try:
                    # Convert to datetime using native Python
                    year, month = date_str.split('-')
                    date = datetime(int(year), int(month), 1)
                    date_dict[date] = count
                except:
                    continue  # Skip invalid dates
        
        # Sort by date and create time series
        sorted_dates = sorted(date_dict.keys())
        # Filter to reasonable date range (2020-2025)
        filtered_dates = [d for d in sorted_dates if d.year >= 2020 and d.year <= 2025]
        
        if filtered_dates:
            clean_data[tech] = {
                'dates': filtered_dates,
                'mentions': [date_dict[d] for d in filtered_dates]
            }
    
    return clean_data

def load_detailed_recommendations():
    """Load detailed industry recommendations from analysis"""
    return {
        'Tech': {
            'automation_opportunities': [
                'Code generation, bug fixes, test case generation',
                'Log analysis, anomaly detection for cloud environments', 
                'Cybersecurity threat detection and incident response'
            ],
            'productivity_enhancements': [
                'Copilots for real-time coding and documentation',
                'Automated ticket triaging and backlog summarization',
                'AI agents for devops and deployment optimization'
            ],
            'adoption_recommendations': [
                'Create dedicated "AI enablement" teams',
                'Promote open-source AI fine-tuning internally',
                'Adopt secure, containerized model deployment pipelines'
            ],
            'description': 'The technology sector is not only the birthplace of most AI tools but also one of the first to adopt and benefit from them. AI has become integral to software development lifecycles, infrastructure management, and customer operations.'
        },
        'Healthcare': {
            'automation_opportunities': [
                'EHR transcription and coding',
                'Insurance claims routing and risk prediction',
                'Medical image classification and anomaly detection'
            ],
            'productivity_enhancements': [
                'AI scribes for clinical documentation',
                'Assistive diagnostics tools for physicians',
                'NLP for reviewing medical literature and trial results'
            ],
            'adoption_recommendations': [
                'Start in non-clinical workflows for quicker wins',
                'Use federated learning for privacy-preserving model training',
                'Partner with AI firms focused on FDA-approved solutions'
            ],
            'description': 'Healthcare is a high-stakes, high-regulation environment where AI must prove both utility and safety. AI is uniquely positioned to assist with diagnosis, administration, and personalized care.'
        },
        'Finance': {
            'automation_opportunities': [
                'Fraud pattern detection',
                'Risk model simulation and backtesting',
                'Contract review and regulatory compliance audits'
            ],
            'productivity_enhancements': [
                'Natural language querying of financial databases',
                'Client communication assistants (chatbots, summarizers)',
                'Portfolio and market insights generation'
            ],
            'adoption_recommendations': [
                'Focus first on back-office automation (KYC, audit, reporting)',
                'Use hybrid human-AI workflows for customer-facing tools',
                'Build XAI tools to support auditing, documentation, and governance'
            ],
            'description': 'Finance is data-rich, rules-based, and deeply analytical—making it fertile ground for AI applications. Financial services face strict regulation and require high transparency.'
        },
        'Education': {
            'automation_opportunities': [
                'Auto-grading and feedback generation',
                'AI-generated practice materials and quizzes',
                'Curriculum adaptation for diverse learner needs'
            ],
            'productivity_enhancements': [
                'Generative planning for lesson material',
                'AI tutors to provide 24/7 academic support',
                'NLP tools for analyzing student performance trends'
            ],
            'adoption_recommendations': [
                'Start with AI for administrative and content planning tasks',
                'Ensure inclusive access for students with disabilities',
                'Train educators on using AI without compromising academic integrity'
            ],
            'description': 'Education is undergoing rapid digitization, and AI can help tackle issues like resource constraints, personalization gaps, and administrative inefficiencies.'
        },
        'Media': {
            'automation_opportunities': [
                'Image and video generation (e.g., Midjourney, Sora)',
                'Speech-to-text for subtitling, podcast production',
                'Generative copywriting for ads, headlines, and descriptions'
            ],
            'productivity_enhancements': [
                'AI assistants for scriptwriting and idea generation',
                'Trend analysis tools based on social/news data',
                'Auto-tagging and metadata generation'
            ],
            'adoption_recommendations': [
                'Use human-in-the-loop pipelines to review AI content',
                'Set clear internal guidelines on synthetic content',
                'Experiment with multi-modal storytelling using GenAI'
            ],
            'description': 'AI is radically transforming content creation—compressing what used to take days into seconds. The best outcomes arise when humans guide the creative direction and AI provides acceleration.'
        },
        'Government': {
            'automation_opportunities': [
                'Chatbots for public Q&A and service access',
                'Translation and summarization of legal/policy documents',
                'Analysis of public sentiment and consultations'
            ],
            'productivity_enhancements': [
                'AI co-pilots for drafting reports and responses',
                'Real-time summarization of meetings and case files',
                'AI-driven trend detection from news and media'
            ],
            'adoption_recommendations': [
                'Begin with internal-use pilots to gain traction',
                'Open-source tooling helps maintain transparency',
                'Establish public advisory councils for AI ethics'
            ],
            'description': 'AI can help governments increase access to services, streamline internal processes, and make sense of vast amounts of public data. Adoption must be slow, thoughtful, and built on trust.'
        },
        'Energy': {
            'automation_opportunities': [
                'Predictive maintenance for grid infrastructure',
                'Energy demand forecasting and optimization',
                'Automated inspection of power lines and facilities'
            ],
            'productivity_enhancements': [
                'Smart grid optimization algorithms',
                'AI-powered energy trading systems',
                'Environmental impact monitoring and reporting'
            ],
            'adoption_recommendations': [
                'Start with predictive maintenance to reduce downtime',
                'Integrate AI with existing SCADA systems',
                'Focus on safety-critical applications with human oversight'
            ],
            'description': 'Energy sector can leverage AI for grid optimization, predictive maintenance, and environmental monitoring while maintaining safety and reliability standards.'
        },
        'Retail': {
            'automation_opportunities': [
                'Inventory management and demand forecasting',
                'Personalized recommendation systems',
                'Dynamic pricing optimization'
            ],
            'productivity_enhancements': [
                'Customer service chatbots and virtual assistants',
                'Supply chain optimization and logistics',
                'Visual search and product discovery'
            ],
            'adoption_recommendations': [
                'Begin with recommendation engines for immediate ROI',
                'Implement gradual personalization to build customer trust',
                'Use A/B testing to validate AI-driven decisions'
            ],
            'description': 'Retail can benefit from AI through personalized customer experiences, optimized operations, and data-driven decision making across the entire value chain.'
        },
        'Transport': {
            'automation_opportunities': [
                'Route optimization and traffic management',
                'Predictive maintenance for vehicles and infrastructure',
                'Automated logistics and warehouse operations'
            ],
            'productivity_enhancements': [
                'Fleet management and fuel optimization',
                'Real-time passenger information systems',
                'Demand forecasting for capacity planning'
            ],
            'adoption_recommendations': [
                'Prioritize safety applications with extensive testing',
                'Start with back-office optimization before customer-facing AI',
                'Collaborate with regulators on autonomous system standards'
            ],
            'description': 'Transportation industry can leverage AI for safety improvements, operational efficiency, and enhanced passenger experiences while navigating complex regulatory requirements.'
        }
    }

def load_sentiment_data():
    """Load AI sentiment analysis data from the JSON file"""
    return {
        "overall_stats": {
            "total_rows": 1186,
            "overall_sentiment_distribution": {
                "Positive": 749,
                "Neutral": 429,
                "Negative": 7
            },
            "workplace_sentiment_distribution": {
                "Neutral": 995,
                "Positive": 147,
                "Negative": 43
            },
            "average_entities_per_row": 120.97,
            "total_unique_organizations": 21430,
            "total_unique_persons": 12448,
            "total_unique_locations": 3256
        },
        "ai_technologies": [
            {"entity": "AI", "total_mentions": 1177, "positive_pct": 63.04, "neutral_pct": 36.36, "negative_pct": 0.51, "avg_sentiment": 0.626, "workplace_sentiment": 0.087},
            {"entity": "Artificial Intelligence", "total_mentions": 806, "positive_pct": 58.44, "neutral_pct": 40.82, "negative_pct": 0.74, "avg_sentiment": 0.577, "workplace_sentiment": 0.097},
            {"entity": "ChatGPT", "total_mentions": 352, "positive_pct": 65.91, "neutral_pct": 34.09, "negative_pct": 0.0, "avg_sentiment": 0.659, "workplace_sentiment": 0.054},
            {"entity": "OpenAI", "total_mentions": 305, "positive_pct": 62.30, "neutral_pct": 37.70, "negative_pct": 0.0, "avg_sentiment": 0.623, "workplace_sentiment": 0.039},
            {"entity": "Machine Learning", "total_mentions": 199, "positive_pct": 70.85, "neutral_pct": 28.64, "negative_pct": 0.50, "avg_sentiment": 0.704, "workplace_sentiment": 0.141},
            {"entity": "Bard", "total_mentions": 82, "positive_pct": 74.39, "neutral_pct": 25.61, "negative_pct": 0.0, "avg_sentiment": 0.744, "workplace_sentiment": -0.012},
            {"entity": "GPT-4", "total_mentions": 65, "positive_pct": 70.77, "neutral_pct": 29.23, "negative_pct": 0.0, "avg_sentiment": 0.708, "workplace_sentiment": 0.062},
            {"entity": "Gemini", "total_mentions": 63, "positive_pct": 76.19, "neutral_pct": 23.81, "negative_pct": 0.0, "avg_sentiment": 0.762, "workplace_sentiment": 0.190},
            {"entity": "Copilot", "total_mentions": 38, "positive_pct": 78.95, "neutral_pct": 21.05, "negative_pct": 0.0, "avg_sentiment": 0.789, "workplace_sentiment": 0.105},
            {"entity": "Claude", "total_mentions": 19, "positive_pct": 84.21, "neutral_pct": 15.79, "negative_pct": 0.0, "avg_sentiment": 0.842, "workplace_sentiment": 0.211}
        ],
        "ai_leaders": [
            {"entity": "Sam Altman", "total_mentions": 71, "positive_pct": 57.75, "neutral_pct": 42.25, "negative_pct": 0.0, "avg_sentiment": 0.577, "workplace_sentiment": 0.014},
            {"entity": "Elon Musk", "total_mentions": 60, "positive_pct": 45.0, "neutral_pct": 55.0, "negative_pct": 0.0, "avg_sentiment": 0.450, "workplace_sentiment": 0.0},
            {"entity": "Sundar Pichai", "total_mentions": 31, "positive_pct": 67.74, "neutral_pct": 32.26, "negative_pct": 0.0, "avg_sentiment": 0.677, "workplace_sentiment": -0.065},
            {"entity": "Satya Nadella", "total_mentions": 23, "positive_pct": 65.22, "neutral_pct": 34.78, "negative_pct": 0.0, "avg_sentiment": 0.652, "workplace_sentiment": 0.0},
            {"entity": "Geoffrey Hinton", "total_mentions": 7, "positive_pct": 57.14, "neutral_pct": 42.86, "negative_pct": 0.0, "avg_sentiment": 0.571, "workplace_sentiment": 0.0},
            {"entity": "Ilya Sutskever", "total_mentions": 6, "positive_pct": 66.67, "neutral_pct": 33.33, "negative_pct": 0.0, "avg_sentiment": 0.667, "workplace_sentiment": 0.167},
            {"entity": "Andrew Ng", "total_mentions": 5, "positive_pct": 60.0, "neutral_pct": 40.0, "negative_pct": 0.0, "avg_sentiment": 0.600, "workplace_sentiment": 0.0},
            {"entity": "Dario Amodei", "total_mentions": 2, "positive_pct": 50.0, "neutral_pct": 50.0, "negative_pct": 0.0, "avg_sentiment": 0.500, "workplace_sentiment": 0.0}
        ],
        "ai_companies": [
            {"entity": "Google", "total_mentions": 308, "positive_pct": 66.23, "neutral_pct": 33.44, "negative_pct": 0.32, "avg_sentiment": 0.659, "workplace_sentiment": 0.084},
            {"entity": "Microsoft", "total_mentions": 264, "positive_pct": 67.80, "neutral_pct": 32.20, "negative_pct": 0.0, "avg_sentiment": 0.678, "workplace_sentiment": 0.061},
            {"entity": "Apple", "total_mentions": 159, "positive_pct": 74.21, "neutral_pct": 25.79, "negative_pct": 0.0, "avg_sentiment": 0.742, "workplace_sentiment": 0.044},
            {"entity": "Meta", "total_mentions": 125, "positive_pct": 58.40, "neutral_pct": 40.80, "negative_pct": 0.80, "avg_sentiment": 0.576, "workplace_sentiment": 0.008},
            {"entity": "NVIDIA", "total_mentions": 90, "positive_pct": 71.11, "neutral_pct": 28.89, "negative_pct": 0.0, "avg_sentiment": 0.711, "workplace_sentiment": 0.011},
            {"entity": "OpenAI", "total_mentions": 45, "positive_pct": 62.22, "neutral_pct": 37.78, "negative_pct": 0.0, "avg_sentiment": 0.622, "workplace_sentiment": 0.089},
            {"entity": "IBM", "total_mentions": 30, "positive_pct": 66.67, "neutral_pct": 33.33, "negative_pct": 0.0, "avg_sentiment": 0.667, "workplace_sentiment": 0.200},
            {"entity": "Anthropic", "total_mentions": 12, "positive_pct": 58.33, "neutral_pct": 33.33, "negative_pct": 0.0, "avg_sentiment": 0.636, "workplace_sentiment": 0.0}
        ]
    }

# Load all data
industry_data = load_industry_data()
tech_mentions = load_technology_data()
use_cases = load_use_case_data()
job_impact = load_job_impact_data()
time_series_data = load_real_time_series_data()
detailed_recommendations = load_detailed_recommendations()
sentiment_data = load_sentiment_data()

# Convert industry data to list of dictionaries for easier handling
industry_list = []
for industry, data in industry_data.items():
    industry_record = {
        'industry': industry,
        'ai_mentions': data['mentions'],
        'impact_level': data['impact_level'],
        'rank': data['rank']
    }
    industry_record.update(data)  # Include all other data
    industry_list.append(industry_record)

# ------------------------------
# Main App
# ------------------------------
st.title("AI Job Impact Readiness Navigator")
st.markdown("*Analysis based on 184,388 news articles covering paradigm shifting AI technologies*")

# Why This Matters section
st.markdown("""
<div class="warning-box">
<h4> Why This Matters</h4>
<p> AI adoption is not just a technological issue, it's a social and economic inflection point. When implemented without foresight, automation can displace vulnerable workers and fracture public trust in innovation.</p>

<p><strong>Key Risks:</strong></p>
<ul>
<li><strong>Digital Divide:</strong> Those with access to capital, computing resources and technical talent are mostly benefited from AI, while low-wage, routine-task workers may face disruption without support systems. This could exacerbate societal divides.</li>
<li><strong>Job Displacement:</strong> Job displacement isn't theoretical, it's happening right now. Without upskilling and reskilling programs a large portions of the workforce risk falling behind. Education and training must be provided.</li>
<li><strong>Window of Influence:</strong> Industry leaders have a window of influence to shape AI adoption responsibly. By acting early, they can ensure AI augments human capabilities rather than replace them, while boosting productivity and protecting livelihoods.</li>
<li><strong>Need for Coordination:</strong> Government regulation, academic research and corporate innovation must work together to build trustworthy AI ecosystems that are fair, transparent and aligned with social values.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Show key paradigm shift technologies
st.markdown("""
<div class="paradigm-shift">
<h4>Paradigm Shift Technologies Driving AI Adoption:</h4>
<p><strong>Generative AI:</strong> 109,424 mentions | <strong>Conversational AI (ChatGPT):</strong> 57,722 mentions | <strong>Computer Vision:</strong> 27,004 mentions</p>
<p>These represent fundamental shifts in how AI technologies are being adopted across industries.</p>
</div>
""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio("Navigate", ["Industry Dashboard", "Recommendation Engine", "Rollout Simulator", "Technology Trends", "AI Players & Organizations"])

# ------------------------------
# 1. Industry Dashboard
# ------------------------------
if page == "Industry Dashboard":
    st.header("📊 Industry Impact Dashboard")
    st.markdown("*Ranking industries by AI impact potential based on discussion volume and technology adoption patterns*")
    
    # Industry selection
    selected_industry = st.selectbox("Select Industry", list(industry_data.keys()))
    data = industry_data[selected_industry]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("AI Mentions", f"{data['mentions']:,}")
    with col2:
        st.metric("Industry Rank", f"#{data['rank']}")
    with col3:
        st.metric("Impact Level", data['impact_level'])
    with col4:
        impact_score = (10 - data['rank']) / 9 * 100
        st.metric("Impact Score", f"{impact_score:.0f}%")
    
    # Paradigm shift technologies for this industry
    st.subheader("Key Paradigm Shift Technologies")
    if 'paradigm_technologies' in data:
        tech_cols = st.columns(len(data['paradigm_technologies']))
        for i, tech in enumerate(data['paradigm_technologies']):
            with tech_cols[i]:
                # Get mention count from tech_mentions if available
                mentions = tech_mentions.get(tech, 0)
                if mentions == 0:
                    # Try to find similar tech names
                    for key, value in tech_mentions.items():
                        if tech.lower() in key.lower() or key.lower() in tech.lower():
                            mentions = value
                            break
                st.markdown(f"**{tech}**")
                if mentions > 0:
                    st.write(f"{mentions:,} mentions")
    
    # Industry comparison chart
    st.subheader(" Industry AI Impact Comparison")
    
    # Create comparison dataframe
    comparison_data = []
    for industry, data in industry_data.items():
        comparison_data.append({
            'Industry': industry,
            'AI Mentions': data['mentions'],
            'Impact Level': data['impact_level'],
            'Rank': data['rank']
        })
    
    comp_df = pd.DataFrame(comparison_data).sort_values('AI Mentions', ascending=True)
    
    # Use streamlit's built-in bar chart
    chart_data = comp_df.set_index('Industry')['AI Mentions']
    st.bar_chart(chart_data, height=500)
    
    # Analysis insights
    st.subheader("Impact Analysis")
    
    if data['impact_level'] == 'Transformational':
        st.markdown(f"""
        <div class="metric-card">
        <strong>{selected_industry}</strong> shows <strong>transformational AI impact potential</strong>:
        <br>• Highest discussion volume ({data['mentions']:,} mentions)
        <br>• Multiple paradigm-shift technologies being adopted
        <br>• Leading innovation in AI applications
        <br>• Expected to drive industry-wide changes in the next 2-3 years
        </div>
        """, unsafe_allow_html=True)
    elif data['impact_level'] == 'High':
        st.markdown(f"""
        <div class="metric-card">
        <strong>{selected_industry}</strong> shows <strong>high AI impact potential</strong>:
        <br>• Significant discussion volume ({data['mentions']:,} mentions)
        <br>• Active adoption of conversational AI and automation
        <br>• Major productivity improvements expected within 2-4 years
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
        <strong>{selected_industry}</strong> shows <strong>{data['impact_level'].lower()} AI impact</strong>:
        <br>• Discussion volume: {data['mentions']:,} mentions.
        <br>• Gradual adoption expected over 3-5 years.
        <br>• Focus on specific use cases rather than broad transformation.
        </div>
        """, unsafe_allow_html=True)

# ------------------------------
# 2. Recommendation Engine
# ------------------------------
elif page == "Recommendation Engine":
    st.header("Actionable AI Adoption Recommendations")
    st.markdown("*Strategic guidance for successful AI implementation based on industry impact analysis.*")
    
    selected_industry = st.selectbox("Select Industry for Recommendations", list(industry_data.keys()), key="rec")
    data = industry_data[selected_industry]
    
    # High-impact recommendations based on analysis
    st.subheader("Priority Automation Opportunities")
    
    if selected_industry == 'Tech':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Generative AI Integration</h4>
        • <strong>Automate</strong>: Code generation, documentation, testing.
        • <strong>Productivity Boost</strong>: 40-60% reduction in development time.
        • <strong>Implementation</strong>: Integrate GPT-4/GitHub Copilot into development workflows.
        • <strong>Success Factor</strong>: Start with non-critical code, build developer confidence.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Conversational AI for Customer Support (44,700 use case mentions)</h4>
        • <strong>Automate</strong>: 70% of support tickets, documentation queries.
        • <strong>Productivity Boost</strong>: 3x faster response times, 24/7 availability.
        • <strong>Implementation</strong>: Deploy ChatGPT-powered chatbots.
        • <strong>Success Factor</strong>: Train on company-specific knowledge base.
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Finance':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Automated Risk Assessment & Compliance. </h4>
        • <strong>Automate</strong>: Document review and regulatory compliance checking.
        • <strong>Productivity Boost</strong>: 80% faster compliance reviews.
        • <strong>Implementation</strong>: Deploy NLP models for document analysis.
        • <strong>Success Factor</strong>: Maintain human oversight for final decisions.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Conversational Financial Advisory (ChatGPT applications).</h4>
        • <strong>Automate</strong>: Basic financial planning and portfolio queries.
        • <strong>Productivity Boost</strong>: Handle 5x more client interactions.
        • <strong>Implementation</strong>: Integrate AI advisors with human oversight.
        • <strong>Success Factor</strong>: Ensure regulatory compliance and transparency.
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Healthcare':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Medical Image Analysis (Computer Vision: 27,004 mentions).</h4>
        • <strong>Automate</strong>: Radiology screening and diagnosis.
        • <strong>Productivity Boost</strong>: 50% faster image analysis.
        • <strong>Implementation</strong>: Deploy AI-assisted diagnostic tools.
        • <strong>Success Factor</strong>: Always require a physician final approval.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Clinical Documentation Automation.</h4>
        • <strong>Automate</strong>: Note transcription and summary generation.
        • <strong>Productivity Boost</strong>: Over 2 hours saved per day per physician.
        • <strong>Implementation</strong>: Voice-to-text with medical terminology.
        • <strong>Success Factor</strong>: Integrate with existing EHR systems.
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Media':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Generative Content Creation.</h4>
        • <strong>Automate</strong>: Social media content, basic articles and image generation.
        • <strong>Productivity Boost</strong>: 10x faster content production.
        • <strong>Implementation</strong>: Use DALL-E for images and GPT for content.
        • <strong>Success Factor</strong>: Maintain editorial oversight for brand voice.
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Retail':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Personalized Recommendation Systems</h4>
        • <strong>Automate</strong>: Product recommendations and inventory optimization.
        • <strong>Productivity Boost</strong>: 25% increase in conversion rates.
        • <strong>Implementation</strong>: ML-powered recommendation engines.
        • <strong>Success Factor</strong>: Balance personalization with privacy.
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Education':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. AI-Powered Tutoring Systems (ChatGPT in education)</h4>
        • <strong>Automate</strong>: Homework problems and personalized learning paths.
        • <strong>Productivity Boost</strong>: 24/7 student support availability.
        • <strong>Implementation</strong>: Deploy educational AI assistants.
        • <strong>Success Factor</strong>: Maintain academic integrity guidelines.
        </div>
        """, unsafe_allow_html=True)

    else:
        # Generic recommendations for other industries
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Process Automation (32,007 task automation mentions). </h4>
        • <strong>Automate</strong>: Data entry, document processing and scheduling.
        • <strong>Productivity Boost</strong>: 50-70% time savings on routine tasks.
        • <strong>Implementation</strong>: Start with repetitive and rule-based processes.
        • <strong>Success Factor</strong>: Identify clear ROI metrics before implementation.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Customer Service Enhancement (44,700 mentions).</h4>
        • <strong>Automate</strong>: FAQ responses and appointment scheduling.
        • <strong>Productivity Boost</strong>: Handle 3x more customer inquiries.
        • <strong>Implementation</strong>: Conversational AI with human escalation.
        • <strong>Success Factor</strong>: Train AI on industry-specific terminology.
        </div>
        """, unsafe_allow_html=True)
    
    # Success factors for AI adoption
    st.subheader("Critical Success Factors")
    
    success_factors = {
        'Tech': "Focus on developer productivity tools first, since they show fastest ROI and build internal AI confidence.",
        'Finance': "Prioritize explainable AI for regulatory compliance, transparency is key for adoption success.", 
        'Healthcare': "Always maintain physician oversight AI should augment, never replace medical judgment.",
        'Media': "Balance automation with creative control. Use AI for efficiency and humans for strategy.",
        'Retail': "Start with recommendation systems, they provide immediate customer value and measurable ROI.",
        'Education': "Address academic integrity concerns proactively, establish clear AI usage guidelines.",
        'Government': "Focus on citizen service improvements, to show tangible public benefits from AI adoption.",
        'Energy': "Emphasize predictive maintenance, AI prevents costly downtime and improves safety.",
        'Transport': "Prioritize safety applications, use AI for risk reduction and efficiency optimization."
    }
    
    st.markdown(f"""
    <div class="warning-box">
    <strong>Key Success Factor for {selected_industry}:</strong><br>
    {success_factors.get(selected_industry, "Start with pilot programs to build confidence and demonstrate ROI before scaling AI initiatives")}
    </div>
    """, unsafe_allow_html=True)
    
    # Employee productivity recommendations
    st.subheader("⚡ Employee Productivity Enhancement")
    
    productivity_recommendations = [
        "**Training Programs**: Invest 20% of implementation budget in AI training.",
        "**Gradual Rollout**: Start with 1-2 departments, scale based on success metrics.",
        "**Human-AI Collaboration**: Position AI as intelligent assistants not replacements.",
        "**Feedback Loops**: Collect user feedback weekly during the first 3 months.",
        "**Success Metrics**: Track time savings, error reduction and employee satisfaction."
    ]
    
    for rec in productivity_recommendations:
        st.markdown(f"• {rec}")

# ------------------------------
# 3. Rollout Simulator
# ------------------------------
elif page == "Rollout Simulator":
    st.header("🔄 AI Rollout Risk Simulator")
    st.markdown("*Simulate different rollout approaches and predict success likelihood*")
    
    # User inputs
    col1, col2 = st.columns(2)
    
    with col1:
        sim_industry = st.selectbox("Industry", list(industry_data.keys()), key="sim")
        rollout_speed = st.selectbox("Rollout Speed", ["Pilot (3 months)", "Gradual (6-12 months)", "Aggressive (1-3 months)", "Enterprise-wide (immediate)"])
        staff_percentage = st.slider("Percentage of Staff Affected", 0, 100, 30)
    
    with col2:
        ai_approach = st.selectbox("AI Implementation Approach", [
            "Human-AI Collaboration (Augmentation)", 
            "Partial Automation (50% AI, 50% Human)",
            "High Automation (80% AI, 20% Human Oversight)",
            "Full Automation (95% AI)"
        ])
        change_management = st.selectbox("Change Management Investment", ["Minimal", "Standard", "Comprehensive", "Extensive"])
    
    # Calculate success probability
    def calculate_success_probability(industry, speed, percentage, approach, change_mgmt):
        base_score = 70  # Start with 70% base success rate
        
        # Industry factor (based on AI readiness from mentions)
        industry_item = next((item for item in industry_list if item['industry'] == industry), None)
        if industry_item:
            industry_mentions = industry_item['ai_mentions']
            max_mentions = max(item['ai_mentions'] for item in industry_list)
            if industry_mentions > 500000:
                base_score += 15  # High AI readiness
            elif industry_mentions > 200000:
                base_score += 10  # Medium-high readiness
            elif industry_mentions > 100000:
                base_score += 5   # Medium readiness
            else:
                base_score -= 10  # Low readiness
        else:
            base_score -= 5  # Unknown industry
        
        # Speed factor
        speed_adjustments = {
            "Pilot (3 months)": +20,
            "Gradual (6-12 months)": +10,
            "Aggressive (1-3 months)": -15,
            "Enterprise-wide (immediate)": -25
        }
        base_score += speed_adjustments.get(speed, 0)
        
        # Staff percentage impact
        if percentage > 75:
            base_score -= 20
        elif percentage > 50:
            base_score -= 10
        elif percentage < 25:
            base_score += 10
        
        # Approach factor
        approach_adjustments = {
            "Human-AI Collaboration (Augmentation)": +15,
            "Partial Automation (50% AI, 50% Human)": +5,
            "High Automation (80% AI, 20% Human Oversight)": -10,
            "Full Automation (95% AI)": -20
        }
        base_score += approach_adjustments.get(approach, 0)
        
        # Change management factor
        change_adjustments = {
            "Minimal": -15,
            "Standard": 0,
            "Comprehensive": +10,
            "Extensive": +20
        }
        base_score += change_adjustments.get(change_mgmt, 0)
        
        return max(10, min(95, base_score))  # Cap between 10-95%
    
    success_prob = calculate_success_probability(sim_industry, rollout_speed, staff_percentage, ai_approach, change_management)
    
    # Display results
    st.subheader(" Rollout Success Prediction")
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = success_prob,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Success Probability (%)"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightcoral"},
                {'range': [40, 70], 'color': "lightyellow"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis
    if success_prob >= 80:
        st.success(f"**HIGH SUCCESS PROBABILITY ({success_prob}%)**")
        st.markdown("""
        **Your rollout plan shows strong success indicators:**
        1. Well-balanced approach to AI implementation.
        2. Appropriate timeline for organizational change.  
        3. Good management planning.  
        
        **Recommendations to maintain success:**
        • Continue with current plan.
        • Monitor key metrics weekly.
        • Prepare contingency plans for unexpected challenges.
        """)
    elif success_prob >= 60:
        st.warning(f"**MODERATE SUCCESS PROBABILITY ({success_prob}%)**")
        st.markdown("""
        **⚠️ Your rollout plan has some risk factors to address:**
        1. Consider adjusting your timeline or scope.  
        2. May need additional management support. 
        
        **Recommendations to improve success:**
        • Extend timeline if currently aggressive.
        • Increase management investment.
        • Consider starting with smaller pilot group.
        """)
    else:
        st.error(f"**LOW SUCCESS PROBABILITY ({success_prob}%)**")
        st.markdown("""
        **❌ Your rollout plan has significant risk factors:**
        1. High risk of employee resistance or project failure.  
        2. Timeline or scope may be too aggressive. 
        3. Insufficient management planning.  
        
        **Critical recommendations:**
        • Extend rollout timeline significantly.
        • Reduce the initial scope to a pilot program.
        • Invest heavily in management and training.
        • Focus on augmentation rather than automation.
        """)
    
    # What AI Still Can't Do section
    st.subheader("🤔 What AI Still Can't Do")
    st.markdown("""
    <div class="recommendation-box">
    <h4>Understanding AI Limitations is Critical for a Successful Implementation</h4>
    
    <p><strong>🧠 Empathy and emotional intelligence:</strong> While AI can mimic emotion through tone and language, it doesn't truly understand feelings. Roles that rely on compassion like therapists, nurses and conflict mediators, still require that human touch.</p>
    
    <p><strong>⚖️ Human judgment in complex contexts:</strong> AI can follow patterns and rules, but it struggles with ambiguity and moral gray areas. Decision-making that depends on values, ethics or long-term social consequences like in law, policy or leadership still needs people.</p>
    
    <p><strong>🔧 Skilled movement and physical adaptability:</strong> From fixing a leaky pipe to helping someone out of a chair, physical tasks in messy, real-world environments require dexterity and improvisation. These are incredibly difficult for robots to replicate.</p>
    
    <p><strong>🎨 Cultural awareness and original creativity:</strong> AI can remix data into something new, but true creativity like humor and storytelling, comes from experience and human context. </p>
    
    <p><em>Keep these limitations in mind when designing your AI rollout strategy.</em></p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# 4. AI Players & Organizations
# ------------------------------
elif page == "AI Players & Organizations":
    st.header("🏢 AI Players & Organizations Dashboard")
    st.markdown("*Sentiment analysis and perception tracking of key AI technologies, leaders, and companies*")
    
    # Overall Statistics
    stats = sentiment_data["overall_stats"]
    st.subheader("📊 Analysis Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Articles Analyzed", '184,388')
    with col2:
        st.metric("Unique Organizations", f"{stats['total_unique_organizations']:,}")
    with col3:
        st.metric("Unique Persons", f"{stats['total_unique_persons']:,}")
    with col4:
        st.metric("Unique Locations", f"{stats['total_unique_locations']:,}")
    
    # Overall sentiment distribution
    st.subheader("Overall Sentiment Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**General Sentiment**")
        overall_sent = stats["overall_sentiment_distribution"]
        # Create pie chart data
        sentiment_data_chart = {
            'Positive': overall_sent['Positive'],
            'Neutral': overall_sent['Neutral'], 
            'Negative': overall_sent['Negative']
        }
        
        # Display as metrics
        total_overall = sum(overall_sent.values())
        pos_pct = (overall_sent['Positive'] / total_overall) * 100
        neu_pct = (overall_sent['Neutral'] / total_overall) * 100
        neg_pct = (overall_sent['Negative'] / total_overall) * 100
        
        st.metric("Positive", f"{overall_sent['Positive']}")
        st.metric("Neutral", f"{overall_sent['Neutral']}")
        st.metric("Negative", f"{overall_sent['Negative']}")
    
    with col2:
        st.markdown("**Workplace Sentiment**")
        workplace_sent = stats["workplace_sentiment_distribution"]
        total_workplace = sum(workplace_sent.values())
        pos_pct_work = (workplace_sent['Positive'] / total_workplace) * 100
        neu_pct_work = (workplace_sent['Neutral'] / total_workplace) * 100
        neg_pct_work = (workplace_sent['Negative'] / total_workplace) * 100
        
        st.metric("Positive", f"{workplace_sent['Positive']}")
        st.metric("Neutral", f"{workplace_sent['Neutral']}")
        st.metric("Negative", f"{workplace_sent['Negative']}")
    
    # Create tabs for different categories
    tab1, tab2, tab3 = st.tabs(["🤖 AI Technologies", "👥 AI Leaders", "🏭 AI Companies"])
    
    with tab1:
        st.subheader("AI Technologies Sentiment Analysis")
        
        # Technology selector
        tech_options = [tech['entity'] for tech in sentiment_data['ai_technologies']]
        selected_tech_sentiment = st.selectbox("Select Technology", tech_options, key="tech_sentiment")
        
        # Find selected technology data
        selected_tech_data = next(tech for tech in sentiment_data['ai_technologies'] if tech['entity'] == selected_tech_sentiment)
        
        # Display technology metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Mentions", f"{selected_tech_data['total_mentions']:,}")
        with col2:
            sentiment_color = "🟢" if selected_tech_data['avg_sentiment'] > 0.7 else "🟡" if selected_tech_data['avg_sentiment'] > 0.5 else "🔴"
            st.metric("Avg Sentiment", f"{sentiment_color} {selected_tech_data['avg_sentiment']:.3f}")
        with col3:
            st.metric("Positive %", f"{selected_tech_data['positive_pct']:.1f}%")
        with col4:
            workplace_color = "🟢" if selected_tech_data['workplace_sentiment'] > 0.1 else "🟡" if selected_tech_data['workplace_sentiment'] > 0 else "🔴"
            st.metric("Workplace Sentiment", f"{workplace_color} {selected_tech_data['workplace_sentiment']:.3f}")
        
        # Sentiment breakdown for selected technology
        st.markdown("**Sentiment Breakdown**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Positive:** {selected_tech_data['positive_pct']:.1f}%")
            st.progress(selected_tech_data['positive_pct']/100)
        with col2:
            st.markdown(f"**Neutral:** {selected_tech_data['neutral_pct']:.1f}%")
            st.progress(selected_tech_data['neutral_pct']/100)
        with col3:
            st.markdown(f"**Negative:** {selected_tech_data['negative_pct']:.1f}%")
            st.progress(selected_tech_data['negative_pct']/100)
        
        # Top technologies comparison
        st.subheader("📈 Technology Sentiment Comparison")
        tech_comparison_data = {}
        for tech in sentiment_data['ai_technologies'][:8]:  # Top 8 technologies
            tech_comparison_data[tech['entity']] = tech['avg_sentiment']
        
        st.bar_chart(tech_comparison_data)
        
        # Technology insights
        st.subheader("💡 Key Insights")
        
        # Find highest sentiment technology
        highest_sentiment_tech = max(sentiment_data['ai_technologies'], key=lambda x: x['avg_sentiment'])
        most_mentioned_tech = max(sentiment_data['ai_technologies'], key=lambda x: x['total_mentions'])
        
        st.markdown(f"""
        <div class="recommendation-box">
        <h4>Technology Sentiment Highlights</h4>
        <p><strong>Highest Sentiment:</strong> {highest_sentiment_tech['entity']} ({highest_sentiment_tech['avg_sentiment']:.3f}).</p>
        <p><strong>Most Discussed:</strong> {most_mentioned_tech['entity']} ({most_mentioned_tech['total_mentions']:,} mentions).</p>
        <p><strong>Workplace Impact:</strong> Technologies with positive workplace sentiment include Claude, Gemini and Machine Learning.</p>
        <p><strong>Market Leader:</strong> AI and ChatGPT dominate discussion volume and maintain positive sentiment.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("AI Leaders Sentiment Analysis")
        
        # Leader selector
        leader_options = [leader['entity'] for leader in sentiment_data['ai_leaders']]
        selected_leader = st.selectbox("Select AI Leader", leader_options, key="leader_sentiment")
        
        # Find selected leader data
        selected_leader_data = next(leader for leader in sentiment_data['ai_leaders'] if leader['entity'] == selected_leader)
        
        # Display leader metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Mentions", f"{selected_leader_data['total_mentions']:,}")
        with col2:
            sentiment_color = "🟢" if selected_leader_data['avg_sentiment'] > 0.6 else "🟡" if selected_leader_data['avg_sentiment'] > 0.4 else "🔴"
            st.metric("Avg Sentiment", f"{sentiment_color} {selected_leader_data['avg_sentiment']:.3f}")
        with col3:
            st.metric("Positive %", f"{selected_leader_data['positive_pct']:.1f}%")
        with col4:
            workplace_color = "🟢" if selected_leader_data['workplace_sentiment'] > 0.1 else "🟡" if selected_leader_data['workplace_sentiment'] > 0 else "🔴"
            st.metric("Workplace Sentiment", f"{workplace_color} {selected_leader_data['workplace_sentiment']:.3f}")
        
        # Leaders comparison chart
        st.subheader("👥 Leaders Sentiment Comparison")
        leaders_comparison_data = {}
        for leader in sentiment_data['ai_leaders'][:6]:  # Top 6 leaders
            leaders_comparison_data[leader['entity']] = leader['avg_sentiment']
        
        st.bar_chart(leaders_comparison_data)
        
        # Leader insights
        st.subheader("💡 Leadership Insights")
        
        # Find highest sentiment leader
        highest_sentiment_leader = max(sentiment_data['ai_leaders'], key=lambda x: x['avg_sentiment'])
        most_mentioned_leader = max(sentiment_data['ai_leaders'], key=lambda x: x['total_mentions'])
        
        st.markdown(f"""
        <div class="recommendation-box">
        <h4>AI Leadership Sentiment Analysis</h4>
        <p><strong>Highest Sentiment:</strong> {highest_sentiment_leader['entity']} ({highest_sentiment_leader['avg_sentiment']:.3f}.)</p>
        <p><strong>Most Discussed:</strong> {most_mentioned_leader['entity']} ({most_mentioned_leader['total_mentions']:,} mentions).</p>
        <p><strong>Industry Dynamics:</strong> Sam Altman leads discussion volume, while technical leaders like Sundar Pichai maintain high sentiment.</p>
        <p><strong>Public Perception:</strong> Elon Musk shows mixed sentiment, reflecting polarized public opinion on his AI ventures.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("AI Companies Sentiment Analysis")
        
        # Company selector
        company_options = [company['entity'] for company in sentiment_data['ai_companies']]
        selected_company = st.selectbox("Select AI Company", company_options, key="company_sentiment")
        
        # Find selected company data
        selected_company_data = next(company for company in sentiment_data['ai_companies'] if company['entity'] == selected_company)
        
        # Display company metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Mentions", f"{selected_company_data['total_mentions']:,}")
        with col2:
            sentiment_color = "🟢" if selected_company_data['avg_sentiment'] > 0.7 else "🟡" if selected_company_data['avg_sentiment'] > 0.5 else "🔴"
            st.metric("Avg Sentiment", f"{sentiment_color} {selected_company_data['avg_sentiment']:.3f}")
        with col3:
            st.metric("Positive %", f"{selected_company_data['positive_pct']:.1f}%")
        with col4:
            workplace_color = "🟢" if selected_company_data['workplace_sentiment'] > 0.1 else "🟡" if selected_company_data['workplace_sentiment'] > 0 else "🔴"
            st.metric("Workplace Sentiment", f"{workplace_color} {selected_company_data['workplace_sentiment']:.3f}")
        
        # Companies comparison chart
        st.subheader("🏭 Companies Sentiment Comparison")
        companies_comparison_data = {}
        for company in sentiment_data['ai_companies'][:8]:  # Top 8 companies
            companies_comparison_data[company['entity']] = company['avg_sentiment']
        
        st.bar_chart(companies_comparison_data)
        
        # Company insights
        st.subheader("💡 Market Insights")
        
        # Find highest sentiment company
        highest_sentiment_company = max(sentiment_data['ai_companies'], key=lambda x: x['avg_sentiment'])
        most_mentioned_company = max(sentiment_data['ai_companies'], key=lambda x: x['total_mentions'])
        
        st.markdown(f"""
        <div class="recommendation-box">
        <h4>AI Company Market Sentiment</h4>
        <p><strong>Highest Sentiment:</strong> {highest_sentiment_company['entity']} ({highest_sentiment_company['avg_sentiment']:.3f}).</p>
        <p><strong>Most Discussed:</strong> {most_mentioned_company['entity']} ({most_mentioned_company['total_mentions']:,} mentions).</p>
        <p><strong>Market Leaders:</strong> Apple leads sentiment (0.742), while Google dominates the discussion volume.</p>
        <p><strong>Workplace Impact:</strong> IBM shows strongest workplace sentiment (0.200), indicating a positive employee perception.</p>
        <p><strong>Industry Trend:</strong> Established tech giants maintain positive sentiment while newer AI-focused companies gain traction.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cross-category insights
    st.subheader("🔄 Cross-Category Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sentiment Leaders by Category**")
        tech_leader = max(sentiment_data['ai_technologies'], key=lambda x: x['avg_sentiment'])
        person_leader = max(sentiment_data['ai_leaders'], key=lambda x: x['avg_sentiment'])
        company_leader = max(sentiment_data['ai_companies'], key=lambda x: x['avg_sentiment'])
        
        st.write(f"🤖 **Technology:** {tech_leader['entity']} ({tech_leader['avg_sentiment']:.3f})")
        st.write(f"👤 **Leader:** {person_leader['entity']} ({person_leader['avg_sentiment']:.3f})")
        st.write(f"🏢 **Company:** {company_leader['entity']} ({company_leader['avg_sentiment']:.3f})")
    
    with col2:
        st.markdown("**Discussion Volume Leaders**")
        tech_volume = max(sentiment_data['ai_technologies'], key=lambda x: x['total_mentions'])
        person_volume = max(sentiment_data['ai_leaders'], key=lambda x: x['total_mentions'])
        company_volume = max(sentiment_data['ai_companies'], key=lambda x: x['total_mentions'])
        
        st.write(f"🤖 **Technology:** {tech_volume['entity']} ({tech_volume['total_mentions']:,})")
        st.write(f"👤 **Leader:** {person_volume['entity']} ({person_volume['total_mentions']:,})")
        st.write(f"🏢 **Company:** {company_volume['entity']} ({company_volume['total_mentions']:,})")

if __name__ == "__main__":
    # Run the app
    # To run this file: streamlit run app.py
    pass