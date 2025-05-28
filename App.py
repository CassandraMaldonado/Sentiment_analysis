import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
        'Tech': {'mentions': 1392510, 'rank': 1, 'impact_level': 'Transformational'},
        'Finance': {'mentions': 256215, 'rank': 2, 'impact_level': 'High'},
        'Healthcare': {'mentions': 249801, 'rank': 3, 'impact_level': 'High'},
        'Media': {'mentions': 244143, 'rank': 4, 'impact_level': 'High'},
        'Retail': {'mentions': 130249, 'rank': 5, 'impact_level': 'Medium-High'},
        'Government': {'mentions': 121871, 'rank': 6, 'impact_level': 'Medium'},
        'Education': {'mentions': 119335, 'rank': 7, 'impact_level': 'Medium'},
        'Energy': {'mentions': 33252, 'rank': 8, 'impact_level': 'Emerging'},
        'Transport': {'mentions': 29474, 'rank': 9, 'impact_level': 'Emerging'}
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
            'Software Developer': 28200,
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
                    # Convert to pandas datetime
                    date = pd.to_datetime(date_str + '-01')  # Add day to make it a valid date
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

# Load all data
industry_data = load_industry_data()
tech_mentions = load_technology_data()
use_cases = load_use_case_data()
job_impact = load_job_impact_data()
time_series_data = load_real_time_series_data()
detailed_recommendations = load_detailed_recommendations()

# Convert industry data to DataFrame for easier handling
industry_df = pd.DataFrame([
    {
        'industry': industry,
        'ai_mentions': data['mentions'],
        'impact_level': data['impact_level'],
        'rank': data['rank'],
        **data  # Include all other data
    }
    for industry, data in industry_data.items()
])

# ------------------------------
# Main App
# ------------------------------
st.title("AI Readiness Navigator")
st.markdown("**Identify industries most impacted by AI and develop actionable adoption strategies**")
st.markdown("*Analysis based on 184,388+ news articles covering paradigm-shifting AI technologies*")

# Show key paradigm shift technologies
st.markdown("""
<div class="paradigm-shift">
<h4>Paradigm Shift Technologies Driving AI Adoption:</h4>
<p><strong>Generative AI:</strong> 109,424 mentions | <strong>Conversational AI (ChatGPT):</strong> 57,722 mentions | <strong>Computer Vision:</strong> 27,004 mentions</p>
<p>These represent fundamental shifts in how AI technologies are being adopted across industries</p>
</div>
""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio("Navigate", ["Industry Dashboard", "Recommendation Engine", "Rollout Simulator", "Technology Trends"])

# ------------------------------
# 1. Industry Dashboard
# ------------------------------
if page == "Industry Dashboard":
    st.header("Industry Impact Dashboard")
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
    st.subheader("📈 Industry AI Impact Comparison")
    
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
        <br>• Discussion volume: {data['mentions']:,} mentions
        <br>• Gradual adoption expected over 3-5 years
        <br>• Focus on specific use cases rather than broad transformation
        </div>
        """, unsafe_allow_html=True)

# ------------------------------
# 2. Recommendation Engine
# ------------------------------
elif page == "Recommendation Engine":
    st.header("Actionable AI Adoption Recommendations")
    st.markdown("*Strategic guidance for successful AI implementation based on industry impact analysis*")
    
    selected_industry = st.selectbox("Select Industry for Recommendations", list(industry_data.keys()), key="rec")
    data = industry_data[selected_industry]
    
    # High-impact recommendations based on analysis
    st.subheader("Priority Automation Opportunities")
    
    if selected_industry == 'Tech':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Generative AI Integration (109,424 mentions - Paradigm Shift)</h4>
        • <strong>Automate</strong>: Code generation, documentation, testing
        • <strong>Productivity Boost</strong>: 40-60% reduction in development time
        • <strong>Implementation</strong>: Integrate GPT-4/GitHub Copilot into development workflows
        • <strong>Success Factor</strong>: Start with non-critical code, build developer confidence
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Conversational AI for Customer Support (44,700 use case mentions)</h4>
        • <strong>Automate</strong>: 70% of tier-1 support tickets, documentation queries
        • <strong>Productivity Boost</strong>: 3x faster response times, 24/7 availability
        • <strong>Implementation</strong>: Deploy ChatGPT-powered chatbots with human handoff
        • <strong>Success Factor</strong>: Train on company-specific knowledge base
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Finance':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Automated Risk Assessment & Compliance (256,215 mentions)</h4>
        • <strong>Automate</strong>: Document review, regulatory compliance checking
        • <strong>Productivity Boost</strong>: 80% faster compliance reviews
        • <strong>Implementation</strong>: Deploy NLP models for document analysis
        • <strong>Success Factor</strong>: Maintain human oversight for final decisions
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Conversational Financial Advisory (ChatGPT applications)</h4>
        • <strong>Automate</strong>: Basic financial planning, portfolio queries
        • <strong>Productivity Boost</strong>: Handle 5x more client interactions
        • <strong>Implementation</strong>: Integrate AI advisors with human oversight
        • <strong>Success Factor</strong>: Ensure regulatory compliance and transparency
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Healthcare':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Medical Image Analysis (Computer Vision - 27,004 mentions)</h4>
        • <strong>Automate</strong>: Radiology screening, dermatology diagnosis
        • <strong>Productivity Boost</strong>: 50% faster image analysis
        • <strong>Implementation</strong>: Deploy AI-assisted diagnostic tools
        • <strong>Success Factor</strong>: Always require physician final approval
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Clinical Documentation Automation (NLP applications)</h4>
        • <strong>Automate</strong>: Note transcription, summary generation
        • <strong>Productivity Boost</strong>: 2+ hours saved per day per physician
        • <strong>Implementation</strong>: Voice-to-text with medical terminology
        • <strong>Success Factor</strong>: Integrate with existing EHR systems
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Media':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Generative Content Creation (79,870 marketing mentions)</h4>
        • <strong>Automate</strong>: Social media content, basic articles, image generation
        • <strong>Productivity Boost</strong>: 10x faster content production
        • <strong>Implementation</strong>: DALL-E for images, GPT for copy
        • <strong>Success Factor</strong>: Maintain editorial oversight for brand voice
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Retail':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Personalized Recommendation Systems</h4>
        • <strong>Automate</strong>: Product recommendations, inventory optimization
        • <strong>Productivity Boost</strong>: 25% increase in conversion rates
        • <strong>Implementation</strong>: ML-powered recommendation engines
        • <strong>Success Factor</strong>: Balance personalization with privacy
        </div>
        """, unsafe_allow_html=True)

    elif selected_industry == 'Education':
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. AI-Powered Tutoring Systems (ChatGPT in education)</h4>
        • <strong>Automate</strong>: Homework help, personalized learning paths
        • <strong>Productivity Boost</strong>: 24/7 student support availability
        • <strong>Implementation</strong>: Deploy educational AI assistants
        • <strong>Success Factor</strong>: Maintain academic integrity guidelines
        </div>
        """, unsafe_allow_html=True)

    else:
        # Generic recommendations for other industries
        st.markdown("""
        <div class="recommendation-box">
        <h4>1. Process Automation (32,007 task automation mentions)</h4>
        • <strong>Automate</strong>: Data entry, document processing, scheduling
        • <strong>Productivity Boost</strong>: 50-70% time savings on routine tasks
        • <strong>Implementation</strong>: Start with repetitive, rule-based processes
        • <strong>Success Factor</strong>: Identify clear ROI metrics before implementation
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>2. Customer Service Enhancement (44,700 mentions)</h4>
        • <strong>Automate</strong>: FAQ responses, appointment scheduling
        • <strong>Productivity Boost</strong>: Handle 3x more customer inquiries
        • <strong>Implementation</strong>: Conversational AI with human escalation
        • <strong>Success Factor</strong>: Train AI on industry-specific terminology
        </div>
        """, unsafe_allow_html=True)
    
    # Success factors for AI adoption
    st.subheader("🎯 Critical Success Factors")
    
    success_factors = {
        'Tech': "Focus on developer productivity tools first - they show fastest ROI and build internal AI confidence",
        'Finance': "Prioritize explainable AI for regulatory compliance - transparency is key to adoption success", 
        'Healthcare': "Always maintain physician oversight - AI should augment, never replace medical judgment",
        'Media': "Balance automation with creative control - use AI for efficiency, humans for strategy",
        'Retail': "Start with recommendation systems - they provide immediate customer value and measurable ROI",
        'Education': "Address academic integrity concerns proactively - establish clear AI usage guidelines",
        'Government': "Focus on citizen service improvements - show tangible public benefits from AI adoption",
        'Energy': "Emphasize predictive maintenance - AI prevents costly downtime and improves safety",
        'Transport': "Prioritize safety applications - use AI for risk reduction and efficiency optimization"
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
        "**Training Programs**: Invest 20% of implementation budget in AI literacy training",
        "**Gradual Rollout**: Start with 1-2 departments, scale based on success metrics",
        "**Human-AI Collaboration**: Position AI as 'intelligent assistant' not 'replacement'",
        "**Feedback Loops**: Collect user feedback weekly during first 3 months",
        "**Success Metrics**: Track time savings, error reduction, and employee satisfaction"
    ]
    
    for rec in productivity_recommendations:
        st.markdown(f"• {rec}")

# ------------------------------
# 3. Rollout Simulator
# ------------------------------
elif page == "Rollout Simulator":
    st.header("AI Rollout Risk Simulator")
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
        industry_row = industry_df[industry_df['industry'] == industry]
        if not industry_row.empty:
            industry_mentions = industry_row.iloc[0]['ai_mentions']
            max_mentions = industry_df['ai_mentions'].max()
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
    st.subheader("Rollout Success Prediction")
    
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
        - Well-balanced approach to AI implementation  
       - Appropriate timeline for organizational change  
       - Good change management planning  
        
        **Recommendations to maintain success:**
        • Continue with current plan
        • Monitor key metrics weekly
        • Prepare contingency plans for unexpected challenges
        """)
    elif success_prob >= 60:
        st.warning(f"**MODERATE SUCCESS PROBABILITY ({success_prob}%)**")
        st.markdown("""
        **Your rollout plan has some risk factors to address:**
        ⚠️ Consider adjusting timeline or scope  
        ⚠️ May need additional change management support  
        
        **Recommendations to improve success:**
        • Extend timeline if currently aggressive
        • Increase change management investment
        • Consider starting with smaller pilot group
        """)
    else:
        st.error(f"**LOW SUCCESS PROBABILITY ({success_prob}%)**")
        st.markdown("""
        **Your rollout plan has significant risk factors:**
        - High risk of employee resistance or project failure  
        - Timeline or scope may be too aggressive  
        - Insufficient change management planning  
        
        **Critical recommendations:**
        • Extend rollout timeline significantly
        • Reduce initial scope to pilot program
        • Invest heavily in change management and training
        • Focus on augmentation rather than automation
        """)

# ------------------------------
# 4. Technology Trends
# ------------------------------
elif page == "📈 Technology Trends":
    st.header("📈 AI Technology Trend Analysis")
    st.markdown("*Track technology adoption patterns and sentiment shifts over time*")
    
    # Technology selection
    selected_tech = st.selectbox("Select AI Technology", list(time_series_data.keys()))
    
    # Create tabs
    tab1, tab2 = st.tabs(["📊 Mentions Over Time", "🏭 Related Industries"])
    
    with tab1:
        st.subheader(f"Mentions Over Time: {selected_tech}")
        
        # Check if technology exists in real data
        if selected_tech in time_series_data:
            tech_data = time_series_data[selected_tech]
            
            # Create dataframe for streamlit chart
            chart_df = pd.DataFrame({
                'Date': tech_data['dates'],
                'Mentions': tech_data['mentions']
            }).set_index('Date')
            
            st.line_chart(chart_df, height=400)
            
            # Key insights from real data
            peak_idx = np.argmax(tech_data['mentions'])
            peak_date = tech_data['dates'][peak_idx]
            peak_value = tech_data['mentions'][peak_idx]
            current_value = tech_data['mentions'][-1] if tech_data['mentions'] else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Peak Mentions", f"{peak_value:,}", f"{peak_date.strftime('%b %Y')}")
            with col2:
                st.metric("Current Mentions", f"{current_value:,}")
            with col3:
                # Calculate trend (comparing last 3 months vs previous 3)
                if len(tech_data['mentions']) >= 6:
                    recent_avg = np.mean(tech_data['mentions'][-3:])
                    previous_avg = np.mean(tech_data['mentions'][-6:-3])
                    trend = "Rising" if recent_avg > previous_avg else "📉 Declining"
                else:
                    trend = "Stable"
                st.metric("Recent Trend", trend)
                
            # Show data insights
            st.subheader("Key Insights")
            total_mentions = sum(tech_data['mentions'])
            date_range = f"{tech_data['dates'][0].strftime('%Y')} - {tech_data['dates'][-1].strftime('%Y')}"
            
            st.markdown(f"""
            **Analysis Period:** {date_range}  
            **Total Mentions:** {total_mentions:,}  
            **Peak Period:** {peak_date.strftime('%B %Y')} ({peak_value:,} mentions)  
            **Data Points:** {len(tech_data['dates'])} months tracked
            """)
            
        else:
            st.warning(f"No time series data available for {selected_tech}")
            st.info("Available technologies with time series data: " + ", ".join(list(time_series_data.keys())))
    
    with tab2:
        st.subheader("Industries Using This Technology")
        
        # Map technologies to industries based on paradigm_technologies
        related_industries = []
        for industry, data in industry_data.items():
            if 'paradigm_technologies' in data:
                # Check if selected tech matches any paradigm technologies
                for paradigm_tech in data['paradigm_technologies']:
                    if (selected_tech.lower() in paradigm_tech.lower() or 
                        paradigm_tech.lower() in selected_tech.lower() or
                        selected_tech == paradigm_tech or
                        # Special matching for common variations
                        (selected_tech == 'AI' and 'ai' in paradigm_tech.lower()) or
                        (selected_tech == 'ChatGPT' and 'chatgpt' in paradigm_tech.lower()) or
                        (selected_tech == 'Machine Learning' and 'ml' in paradigm_tech.lower())):
                        related_industries.append({
                            'Industry': industry,
                            'AI Mentions': data['mentions'],
                            'Impact Level': data['impact_level'],
                            'Rank': data['rank']
                        })
                        break
        
        if related_industries:
            related_df = pd.DataFrame(related_industries)
            
            # Display table
            st.dataframe(related_df.sort_values('AI Mentions', ascending=False), use_container_width=True)
            
            # Simple bar chart visualization
            chart_data = related_df.set_index('Industry')['AI Mentions']
            st.bar_chart(chart_data)
        else:
            st.info(f"No specific industry adoption patterns found for {selected_tech} in the paradigm technologies mapping")
            
            # Show general technology impact from the real time series data
            st.subheader("Overall Technology Impact")
            if selected_tech in time_series_data:
                tech_data = time_series_data[selected_tech]
                total_mentions = sum(tech_data['mentions'])
                st.metric("Total Mentions Over Time", f"{total_mentions:,}")
                
                # Show when it peaked
                peak_idx = np.argmax(tech_data['mentions'])
                peak_date = tech_data['dates'][peak_idx]
                peak_value = tech_data['mentions'][peak_idx]
                
                st.write(f"**Peak Activity:** {peak_date.strftime('%B %Y')} with {peak_value:,} mentions")
                
                # Show adoption timeline
                st.write("**Adoption Timeline:**")
                first_significant = None
                for i, (date, mentions) in enumerate(zip(tech_data['dates'], tech_data['mentions'])):
                    if mentions > 1000 and first_significant is None:
                        first_significant = date
                        st.write(f"• First significant adoption: {date.strftime('%B %Y')} ({mentions:,} mentions)")
                        break
                
                if peak_date != first_significant:
                    st.write(f"• Peak adoption: {peak_date.strftime('%B %Y')} ({peak_value:,} mentions)")
                
                current_mentions = tech_data['mentions'][-1] if tech_data['mentions'] else 0
                st.write(f"• Current activity: {tech_data['dates'][-1].strftime('%B %Y')} ({current_mentions:,} mentions)")

# Footer
st.markdown("---")
st.markdown("*AI Readiness Navigator • Strategic guidance based on analysis of 184,388+ articles • Focus on paradigm-shifting technologies*")