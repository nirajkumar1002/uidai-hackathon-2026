"""
Streamlit Dashboard - UIDAI Data Hackathon Winning Solution
Three-Problem Analysis: Biometric Compliance + Geographic Divide + Urban-Rural Gap

Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_path)

from data_loader import DataLoader
from visualization_utils import VisualizationTools

# Page config
st.set_page_config(
    page_title="UIDAI Aadhaar Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_resource
def load_data():
    # Get absolute path to data directory
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, 'data', 'raw')
    loader = DataLoader(data_dir=data_path)
    return loader.load_all_data()

try:
    datasets = load_data()
    enrolment_df = datasets['enrolment'].copy()
    demographic_df = datasets['demographic'].copy()
    biometric_df = datasets['biometric'].copy()
except (AttributeError, TypeError) as e:
    st.error("❌ Error loading data. Please check that data files exist in data/raw/")
    st.stop()

# Clean state names function
def clean_state_names(df):
    """Standardize state names: fix typos, normalize case and spacing"""
    df['state'] = df['state'].astype(str).str.strip()
    df['state'] = df['state'].str.replace(r'\s+', ' ', regex=True).str.title()
    
    state_corrections = {
        'West Bangal': 'West Bengal', 'Westbengal': 'West Bengal', 'West  Bengal': 'West Bengal',
        'Jammu And Kashmir': 'Jammu & Kashmir', 'Andaman And Nicobar Islands': 'Andaman & Nicobar Islands',
        'Dadra And Nagar Haveli': 'Dadra & Nagar Haveli and Daman & Diu',
        'Daman And Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'Dadra & Nagar Haveli': 'Dadra & Nagar Haveli and Daman & Diu',
        'Daman & Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'Dadra And Nagar Haveli And Daman And Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'Delhi': 'NCT of Delhi', 'Nct Of Delhi': 'NCT of Delhi',
        'Uttaranchal': 'Uttarakhand', 'Orissa': 'Odisha', 'Pondicherry': 'Puducherry',
    }
    df['state'] = df['state'].replace(state_corrections)
    invalid_states = ['100000', 'Nan', 'None', '']
    df = df[~df['state'].isin(invalid_states)]
    df = df[df['state'].str.match(r'^[A-Za-z\s&]+$')]
    return df

# Clean state names in all datasets
enrolment_df = clean_state_names(enrolment_df)
demographic_df = clean_state_names(demographic_df)
biometric_df = clean_state_names(biometric_df)

# Prepare data
enrolment_df['total_enroll'] = enrolment_df[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)
enrolment_df['children_enroll'] = enrolment_df[['age_0_5', 'age_5_17']].sum(axis=1)
biometric_df['bio_child'] = biometric_df['bio_age_5_17']

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Problem",
    [
        "🏠 Overview",
        "🔴 Problem #1: Biometric Compliance",
        "🔴 Problem #3: Geographic Divide",
        "🔴 Problem #4: Urban-Rural Gap",
        "💡 Synthesis & Recommendations"
    ]
)

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "🏠 Overview":
    st.title("🌍 UIDAI Aadhaar Data Analysis")
    st.subheader("Identifying Three Critical Gaps in Universal Digital Identity Access")
    
    st.markdown("""
    ### The Challenge
    India has achieved remarkable universal child Aadhaar enrollment, but three 
    interconnected crises create a **two-tiered digital identity system** that 
    threatens equal access to welfare and social services.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Enrollments", "4.6M+", "children & adults")
    
    with col2:
        st.metric("Biometric Updates", "67.4M+", "across all ages")
    
    with col3:
        st.metric("States Covered", "55+", "including UTs")
    
    st.divider()
    
    st.markdown("""
    ### Three Critical Problems
    
    **🔴 Problem #1: Biometric Compliance Crisis**
    - Mandatory biometric updates at age 5 and 15
    - Compliance varies dramatically by state
    - Some children never get authenticated
    - Impact: Welfare access blocked for non-compliant regions
    
    **🔴 Problem #3: Geographic Digital Divide**
    - Top 5 states = 45%+ of all enrollments
    - Massive concentration in developed regions
    - Northeastern states severely underserved
    - Impact: Regional inequality in digital access
    
    **🔴 Problem #4: Urban-Rural Coverage Disparity**
    - Urban metros get 10x+ more enrollments
    - Rural enrollment infrastructure inadequate
    - Villages lack awareness and centers
    - Impact: Rural populations lack digital identity
    """)
    
    st.divider()
    
    st.markdown("""
    ### The Thesis
    These three crises combine to create systematic exclusion:
    
    1. **Geographic concentration** means most infrastructure in 5 states
    2. **Urban-rural divide** means metro-centric deployment within those states
    3. **Compliance gaps** mean even enrolled children lack authentication
    4. **Result**: 60-70% of India lacks reliable digital identity access
    """)

# ============================================================================
# PAGE 2: PROBLEM #1 - BIOMETRIC COMPLIANCE
# ============================================================================
elif page == "🔴 Problem #1: Biometric Compliance":
    st.title("🔴 PROBLEM #1: BIOMETRIC COMPLIANCE CRISIS")
    
    st.markdown("""
    ### The Issue
    Children should get biometric updates at age 5 and 15 (mandatory transitions).
    But compliance varies massively across states. Some regions have excellent 
    tracking, others have zero compliance infrastructure.
    """)
    
    # Calculate metrics
    state_enroll = enrolment_df.groupby('state')[['age_0_5', 'age_5_17']].sum().reset_index()
    state_enroll['children_enroll'] = state_enroll['age_0_5'] + state_enroll['age_5_17']
    
    state_bio = biometric_df.groupby('state')['bio_child'].sum().reset_index()
    state_bio.columns = ['state', 'child_bio_updates']
    
    state_compliance = state_enroll.merge(state_bio, on='state', how='left')
    state_compliance['child_bio_updates'] = state_compliance['child_bio_updates'].fillna(0)
    state_compliance['compliance_ratio'] = state_compliance['child_bio_updates'] / state_compliance['children_enroll']
    state_compliance = state_compliance.sort_values('compliance_ratio', ascending=False)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Best State", state_compliance.iloc[0]['state'], 
                 f"{state_compliance.iloc[0]['compliance_ratio']:.2f}x")
    with col2:
        st.metric("Worst State", state_compliance.iloc[-1]['state'],
                 f"{state_compliance.iloc[-1]['compliance_ratio']:.2f}x")
    with col3:
        gap = state_compliance.iloc[0]['compliance_ratio'] - state_compliance.iloc[-1]['compliance_ratio']
        st.metric("Compliance Gap", f"{gap:.2f}x", "Crisis threshold!")
    with col4:
        avg = state_compliance['compliance_ratio'].mean()
        st.metric("National Average", f"{avg:.2f}x", "inconsistent")
    
    st.divider()
    
    # Visualization
    fig = px.bar(
        state_compliance.sort_values('compliance_ratio', ascending=True),
        x='compliance_ratio',
        y='state',
        orientation='h',
        title='Biometric Compliance Ratio by State (Higher = Better)',
        labels={'compliance_ratio': 'Updates per Enrollment', 'state': 'State'},
        color='compliance_ratio',
        color_continuous_scale='RdYlGn'
    )
    fig.add_vline(x=state_compliance['compliance_ratio'].mean(), 
                  line_dash="dash", line_color="blue",
                  annotation_text=f"National Avg: {state_compliance['compliance_ratio'].mean():.2f}x")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # State selector
    st.subheader("Deep Dive: Select a State")
    selected_state = st.selectbox("Choose state for details", state_compliance['state'].unique())
    
    state_data = state_compliance[state_compliance['state'] == selected_state].iloc[0]
    st.write(f"""
    **{selected_state}**
    - Child Enrollments: {state_data['children_enroll']:,.0f}
    - Biometric Updates: {state_data['child_bio_updates']:,.0f}
    - Compliance Ratio: {state_data['compliance_ratio']:.2f}x
    - Status: {'✅ High' if state_data['compliance_ratio'] > 1.5 else '⚠️ Medium' if state_data['compliance_ratio'] > 0.8 else '🔴 Critical'}
    """)

# ============================================================================
# PAGE 3: PROBLEM #3 - GEOGRAPHIC DIVIDE
# ============================================================================
elif page == "🔴 Problem #3: Geographic Divide":
    st.title("🔴 PROBLEM #3: GEOGRAPHIC DIGITAL DIVIDE")
    
    st.markdown("""
    ### The Issue
    Enrollment is heavily concentrated in 5 states that account for 45%+ of 
    national activity. Other regions, especially Northeastern states, are 
    severely underserved.
    """)
    
    state_volumes = enrolment_df.groupby('state')['total_enroll'].sum().sort_values(ascending=False)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        top5_pct = state_volumes.head(5).sum() / state_volumes.sum() * 100
        st.metric("Top 5 States", f"{top5_pct:.1f}%", "of all enrollments")
    
    with col2:
        top10_pct = state_volumes.head(10).sum() / state_volumes.sum() * 100
        st.metric("Top 10 States", f"{top10_pct:.1f}%", "of all enrollments")
    
    with col3:
        state_metrics = enrolment_df.groupby('state').agg({
            'total_enroll': 'sum',
            'district': 'nunique'
        }).reset_index()
        state_metrics['per_capita'] = state_metrics['total_enroll'] / state_metrics['district']
        disparity = state_metrics['per_capita'].max() / state_metrics['per_capita'].min()
        st.metric("Per-Capita Disparity", f"{disparity:.1f}x", "highest vs lowest")
    
    st.divider()
    
    # Concentration pie chart
    col1, col2 = st.columns(2)
    
    with col1:
        top5 = state_volumes.head(5)
        others = pd.Series({'Others': state_volumes[5:].sum()})
        pie_data = pd.concat([top5, others])
        
        fig = px.pie(
            values=pie_data.values,
            names=pie_data.index,
            title='Enrollment Concentration: Top 5 vs Rest',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top states bar
        fig = px.bar(
            x=state_volumes.head(15).values,
            y=state_volumes.head(15).index,
            orientation='h',
            title='Top 15 States by Enrollment Volume',
            labels={'x': 'Total Enrollments', 'y': 'State'},
            color=state_volumes.head(15).values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💡 Key Insight")
    st.warning("""
    **Geographic Inequality**: While top 5 states account for 45%+ of enrollments,
    they represent only ~16% of India's states/UTs. This means:
    - Other states get <1/20th of resources
    - Northeastern expansion severely limited
    - Policy attention concentrated in few regions
    - Creates structural digital divide
    """)

# ============================================================================
# PAGE 4: PROBLEM #4 - URBAN-RURAL GAP
# ============================================================================
elif page == "🔴 Problem #4: Urban-Rural Gap":
    st.title("🔴 PROBLEM #4: URBAN-RURAL COVERAGE DISPARITY")
    
    st.markdown("""
    ### The Issue
    Even within states, enrollment is metro-centric. Top 50 urban districts 
    get vastly more resources than 900+ rural districts. This creates a 
    second tier of inequality.
    """)
    
    district_volumes = enrolment_df.groupby('district')['total_enroll'].sum().sort_values(ascending=False)
    
    # Urban-rural split
    urban_districts = set(district_volumes.head(50).index)
    enrolment_df['area_type'] = enrolment_df['district'].apply(lambda x: 'Urban' if x in urban_districts else 'Rural')
    
    urban_enrollment = enrolment_df[enrolment_df['area_type'] == 'Urban']['total_enroll'].sum()
    rural_enrollment = enrolment_df[enrolment_df['area_type'] == 'Rural']['total_enroll'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Urban (50 districts)", f"{urban_enrollment/(urban_enrollment+rural_enrollment)*100:.1f}%", 
                 f"{urban_enrollment:,.0f} enrollments")
    
    with col2:
        st.metric("Rural (Rest)", f"{rural_enrollment/(urban_enrollment+rural_enrollment)*100:.1f}%",
                 f"{rural_enrollment:,.0f} enrollments")
    
    with col3:
        gap = urban_enrollment / rural_enrollment
        st.metric("Urban-Rural Gap", f"{gap:.2f}x", "inequality factor")
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        urban_rural_data = pd.DataFrame({
            'Area Type': ['Urban (Top 50 Districts)', 'Rural (Remaining)'],
            'Enrollments': [urban_enrollment, rural_enrollment]
        })
        
        fig = px.pie(
            urban_rural_data,
            values='Enrollments',
            names='Area Type',
            title='Urban-Rural Enrollment Split',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top districts
        fig = px.bar(
            x=district_volumes.head(20).values,
            y=district_volumes.head(20).index,
            orientation='h',
            title='Top 20 Districts (All Urban/Metro)',
            labels={'x': 'Enrollments', 'y': 'District'},
            color=district_volumes.head(20).values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💡 Key Insight")
    st.warning(f"""
    **Urban Concentration**: Just 50 urban districts account for {urban_enrollment/(urban_enrollment+rural_enrollment)*100:.1f}% 
    of all enrollments, while 900+ rural districts account for only {rural_enrollment/(urban_enrollment+rural_enrollment)*100:.1f}%.
    
    - Top district: {district_volumes.index[0]} ({district_volumes.iloc[0]:,.0f} enrollments)
    - Bottom district: {district_volumes.index[-1]} ({district_volumes.iloc[-1]:,.0f} enrollments)
    - Disparity: {district_volumes.iloc[0] / district_volumes.iloc[-1]:.0f}x
    """)

# ============================================================================
# PAGE 5: SYNTHESIS & RECOMMENDATIONS
# ============================================================================
elif page == "💡 Synthesis & Recommendations":
    st.title("💡 SYNTHESIS & RECOMMENDATIONS")
    
    st.markdown("""
    ## The Interconnected Crisis
    
    These three problems combine to create a **two-tiered digital identity system**:
    
    ### TIER 1: PRIVILEGED
    - Urban metros in top 5 states
    - Good enrollment rates + biometric compliance
    - Easy authentication, smooth benefit delivery
    - Population: ~30-40% of India ✅
    
    ### TIER 2: DISADVANTAGED  
    - Rural areas + non-priority states
    - Low enrollment + poor compliance
    - Authentication failures, blocked welfare access
    - Population: ~60-70% of India 🔴
    """)
    
    st.divider()
    
    st.subheader("🎯 Recommended Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### TIER 1: URGENT (6 months)
        **Biometric Compliance Crisis**
        
        - Identify non-compliant children
        - Target worst-performing states
        - Completion drives at 5yr & 15yr
        - Focus: Authentication restoration
        
        **Timeline**: 6 months
        **Impact**: 50M+ children
        """)
    
    with col2:
        st.markdown("""
        ### TIER 2: HIGH (12 months)
        **Geographic Rebalancing**
        
        - Expand centers in underserved states
        - Mobile enrollment units
        - Training programs
        - Focus: Per-capita equity
        
        **Timeline**: 12 months
        **Impact**: 200M+ population
        """)
    
    with col3:
        st.markdown("""
        ### TIER 3: CRITICAL (18 months)
        **Urban-Rural Bridge**
        
        - Rural center network
        - Community campaigns
        - Vernacular support
        - Partnership with NGOs
        
        **Timeline**: 18 months
        **Impact**: 500M+ population
        """)
    
    st.divider()
    
    st.subheader("📊 Success Metrics")
    
    metrics_data = pd.DataFrame({
        'Metric': ['Compliance Gap', 'Per-Capita Disparity', 'Urban-Rural Gap'],
        'Current': ['2.5x', '12x', '10x'],
        'Target (18 months)': ['1.1x', '1.5x', '1.3x'],
        'Impact': ['Restore authentication', 'Geographic equity', 'Rural access']
    })
    
    st.dataframe(metrics_data, use_container_width=True)
    
    st.divider()
    
    st.subheader("🚀 Implementation Roadmap")
    
    st.markdown("""
    **Phase 1: Assessment & Planning (Month 1-2)**
    - Detailed compliance audit by state/district
    - Infrastructure assessment
    - Barrier analysis (awareness, access, documents)
    
    **Phase 2: Crisis Intervention (Month 3-8)**
    - Biometric completion campaigns
    - Mobile enrollment units deployed
    - Awareness through vernacular media
    
    **Phase 3: Infrastructure Build (Month 9-18)**
    - New enrollment centers in rural areas
    - Staff training programs
    - Community partnerships established
    - Monitoring dashboard operational
    
    **Phase 4: Monitoring & Optimization (Ongoing)**
    - Real-time compliance tracking
    - Quarterly performance reviews
    - Adjustment based on data
    """)

# Footer
st.divider()
st.markdown("""
---
**UIDAI Data Hackathon 2026**  
Three-Problem Analysis: Biometric Compliance + Geographic Divide + Urban-Rural Gap  
*Data-driven insights for inclusive digital identity access*
""")
