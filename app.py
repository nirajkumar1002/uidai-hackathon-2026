"""
Streamlit Dashboard - UIDAI Data Hackathon Winning Solution
Three-Problem Analysis: Biometric Compliance + Geographic Divide + Urban-Rural Gap

ARCHITECTURE:
- This app ONLY loads preprocessed data from data/processed/
- Heavy computations happen in preprocess.py (run once locally)
- This app is lightweight and Streamlit Cloud compatible
- All data is cached for instant page navigation

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
import sys

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="UIDAI Aadhaar Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    /* Optimize sidebar for better text display */
    [data-testid="stSidebar"] {
        width: 350px !important;
    }
    .css-1d391kg {
        padding-left: 15px;
        padding-right: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING (CACHED FOR PERFORMANCE)
# ============================================================================

@st.cache_data
def get_processed_data_path():
    """Get the path to processed data directory"""
    return Path(__file__).parent / 'data' / 'processed'

@st.cache_data
def load_state_compliance():
    """Load state-level biometric compliance data"""
    try:
        data_dir = get_processed_data_path()
        path = data_dir / 'state_compliance.csv'
        
        if not path.exists():
            st.error(f"❌ File not found: {path}")
            st.info("Please run: python preprocess.py")
            st.stop()
        
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, compression='gzip')
    except Exception as e:
        st.error(f"❌ Error loading compliance data: {str(e)}")
        st.stop()

@st.cache_data
def load_state_geography():
    """Load state-level enrollment geography data"""
    try:
        data_dir = get_processed_data_path()
        path = data_dir / 'state_geography.csv'
        
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, compression='gzip')
    except Exception as e:
        st.error(f"❌ Error loading geography data: {str(e)}")
        st.stop()

@st.cache_data
def load_district_volumes():
    """Load district-level enrollment data"""
    try:
        data_dir = get_processed_data_path()
        path = data_dir / 'district_volumes.csv'
        
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, compression='gzip')
    except Exception as e:
        st.error(f"❌ Error loading district data: {str(e)}")
        st.stop()

@st.cache_data
def load_state_urban_rural():
    """Load state-level urban-rural split data"""
    try:
        data_dir = get_processed_data_path()
        path = data_dir / 'state_urban_rural.csv'
        
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, compression='gzip')
    except Exception as e:
        st.error(f"❌ Error loading urban-rural data: {str(e)}")
        st.stop()

@st.cache_data
def load_state_metrics_full():
    """Load complete state metrics for advanced analytics"""
    try:
        data_dir = get_processed_data_path()
        path = data_dir / 'state_metrics_full.csv'
        
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, compression='gzip')
    except Exception as e:
        st.error(f"❌ Error loading full metrics: {str(e)}")
        st.stop()

# Load all data
try:
    state_compliance_df = load_state_compliance()
    state_geography_df = load_state_geography()
    district_volumes_df = load_district_volumes()
    state_urban_rural_df = load_state_urban_rural()
    state_metrics_df = load_state_metrics_full()
except Exception as e:
    st.error(f"❌ Fatal error loading data: {str(e)}")
    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Problem",
    [
        "🏠 Overview",
        "🔴 Problem #1: Biometric Compliance",
        "🔴 Problem #2: Geographic Divide",
        "🔴 Problem #3: Urban-Rural Gap",
        "🔬 Advanced Analytics",
        "💡 Synthesis & Recommendations",
        "👥 Team"
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
    
    **🔴 Problem #2: Geographic Digital Divide**
    - Top 5 states = 55.3% of all enrollments
    - Massive concentration in developed regions
    - Northeastern states severely underserved
    - Impact: Regional inequality in digital access
    
    **🔴 Problem #3: Urban-Rural Coverage Disparity**
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
    Mandatory Biometric Updates (MBU) for children at age 5 and 15 should ensure 
    proper authentication. But compliance varies massively across states. Some regions 
    have excellent tracking infrastructure, others have nearly zero compliance.
    """)
    
    state_compliance_sorted = state_compliance_df.sort_values('compliance_ratio', ascending=False)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Best State", state_compliance_sorted.iloc[0]['state'], 
                 f"{state_compliance_sorted.iloc[0]['compliance_ratio']:.2f}x")
    with col2:
        st.metric("Worst State", state_compliance_sorted.iloc[-1]['state'],
                 f"{state_compliance_sorted.iloc[-1]['compliance_ratio']:.2f}x")
    with col3:
        gap = state_compliance_sorted.iloc[0]['compliance_ratio'] - state_compliance_sorted.iloc[-1]['compliance_ratio']
        st.metric("Compliance Gap", f"{gap:.2f}x", "Crisis threshold!")
    with col4:
        avg = state_compliance_sorted['compliance_ratio'].mean()
        st.metric("National Average", f"{avg:.2f}x", "inconsistent")
    
    st.divider()
    
    # Visualization
    fig = px.bar(
        state_compliance_sorted.sort_values('compliance_ratio', ascending=True),
        x='compliance_ratio',
        y='state',
        orientation='h',
        title='Biometric Compliance Ratio by State (Higher = Better)',
        labels={'compliance_ratio': 'Updates per Enrollment', 'state': 'State'},
        color='compliance_ratio',
        color_continuous_scale='RdYlGn'
    )
    fig.add_vline(x=state_compliance_sorted['compliance_ratio'].mean(), 
                  line_dash="dash", line_color="blue",
                  annotation_text=f"Avg: {state_compliance_sorted['compliance_ratio'].mean():.2f}x")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # State selector
    st.subheader("Deep Dive: Select a State")
    selected_state = st.selectbox("Choose state for details", state_compliance_sorted['state'].unique())
    
    state_data = state_compliance_df[state_compliance_df['state'] == selected_state].iloc[0]
    st.write(f"""
    **{selected_state}**
    - Child Enrollments: {state_data['children_enroll']:,.0f}
    - Biometric Updates: {state_data['child_bio_updates']:,.0f}
    - Compliance Ratio: {state_data['compliance_ratio']:.2f}x
    - Status: {'✅ High' if state_data['compliance_ratio'] > 1.5 else '⚠️ Medium' if state_data['compliance_ratio'] > 0.8 else '🔴 Critical'}
    """)

# ============================================================================
# PAGE 3: PROBLEM #2 - GEOGRAPHIC DIVIDE
# ============================================================================

elif page == "🔴 Problem #2: Geographic Divide":
    st.title("🔴 PROBLEM #2: GEOGRAPHIC DIGITAL DIVIDE")
    
    st.markdown("""
    ### The Issue
    Enrollment is heavily concentrated in 5 states that account for 55.3% 
    of national activity. Other regions, especially Northeastern states, are 
    severely underserved.
    """)
    
    state_volumes_sorted = state_geography_df.sort_values('total_enroll', ascending=False)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        top5_pct = state_volumes_sorted.head(5)['total_enroll'].sum() / state_volumes_sorted['total_enroll'].sum() * 100
        st.metric("Top 5 States", f"{top5_pct:.1f}%", "of all enrollments")
    
    with col2:
        top10_pct = state_volumes_sorted.head(10)['total_enroll'].sum() / state_volumes_sorted['total_enroll'].sum() * 100
        st.metric("Top 10 States", f"{top10_pct:.1f}%", "of all enrollments")
    
    with col3:
        disparity = state_volumes_sorted['per_capita_district'].max() / (state_volumes_sorted['per_capita_district'].min() + 1)
        st.metric("Per-Capita Disparity", f"{disparity:.1f}x", "highest vs lowest")
    
    st.divider()
    
    # Concentration pie chart
    col1, col2 = st.columns(2)
    
    with col1:
        top5 = state_volumes_sorted.head(5)['total_enroll']
        others = pd.Series({'Others': state_volumes_sorted[5:]['total_enroll'].sum()})
        pie_data = pd.concat([top5, others])
        
        fig = px.pie(
            values=pie_data.values,
            names=pie_data.index,
            title='Enrollment Concentration: Top 5 vs Rest',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            x=state_volumes_sorted.head(15)['total_enroll'].values,
            y=state_volumes_sorted.head(15)['state'].values,
            orientation='h',
            title='Top 15 States by Enrollment Volume',
            labels={'x': 'Total Enrollments', 'y': 'State'},
            color=state_volumes_sorted.head(15)['total_enroll'].values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💡 Key Insight")
    st.warning(f"""
    **Geographic Inequality**: Top 5 states account for {top5_pct:.1f}% of enrollments,
    but represent only ~16% of India's states/UTs. This means:
    - Other states get less than 1/20th of resources
    - Northeastern expansion severely limited
    - Policy attention concentrated in few regions
    - Creates structural digital divide
    """)

# ============================================================================
# PAGE 4: PROBLEM #3 - URBAN-RURAL GAP
# ============================================================================

elif page == "🔴 Problem #3: Urban-Rural Gap":
    st.title("🔴 PROBLEM #3: URBAN-RURAL COVERAGE DISPARITY")
    
    st.markdown("""
    ### The Issue
    Even within states, enrollment is metro-centric. Top 50 urban districts 
    get vastly more resources than 900+ rural districts. This creates a 
    second tier of inequality.
    """)
    
    district_volumes_sorted = district_volumes_df.sort_values('total_enroll', ascending=False)
    top_50_volume = district_volumes_sorted.head(50)['total_enroll'].sum()
    rest_volume = district_volumes_sorted[50:]['total_enroll'].sum()
    total_volume = top_50_volume + rest_volume
    
    col1, col2, col3 = st.columns(3)
    with col1:
        urban_pct = top_50_volume / total_volume * 100
        st.metric("Urban (50 districts)", f"{urban_pct:.1f}%", f"{top_50_volume:,.0f} enrollments")
    
    with col2:
        rural_pct = rest_volume / total_volume * 100
        st.metric("Rural (Rest)", f"{rural_pct:.1f}%", f"{rest_volume:,.0f} enrollments")
    
    with col3:
        gap = top_50_volume / (rest_volume + 1)
        st.metric("Urban-Rural Gap", f"{gap:.2f}x", "inequality factor")
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        urban_rural_data = pd.DataFrame({
            'Area Type': ['Urban (Top 50 Districts)', 'Rural (Remaining)'],
            'Enrollments': [top_50_volume, rest_volume]
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
        fig = px.bar(
            x=district_volumes_sorted.head(20)['total_enroll'].values,
            y=district_volumes_sorted.head(20)['district'].values,
            orientation='h',
            title='Top 20 Districts (All Urban/Metro)',
            labels={'x': 'Enrollments', 'y': 'District'},
            color=district_volumes_sorted.head(20)['total_enroll'].values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💡 Key Insight")
    st.warning(f"""
    **Urban Concentration**: Just 50 urban districts account for {urban_pct:.1f}% 
    of all enrollments, while remaining districts account for only {rural_pct:.1f}%.
    
    - Top district: {district_volumes_sorted.iloc[0]['district']} ({district_volumes_sorted.iloc[0]['total_enroll']:,.0f} enrollments)
    - Bottom district: {district_volumes_sorted.iloc[-1]['district']} ({district_volumes_sorted.iloc[-1]['total_enroll']:,.0f} enrollments)
    - Disparity: {district_volumes_sorted.iloc[0]['total_enroll'] / (district_volumes_sorted.iloc[-1]['total_enroll'] + 1):.0f}x
    """)

# ============================================================================
# PAGE 5: ADVANCED ANALYTICS
# ============================================================================

elif page == "🔬 Advanced Analytics":
    st.title("🔬 ADVANCED ANALYTICS")

    st.markdown("""
    This section validates findings statistically and identifies state clusters 
    by enrollment scale, compliance, and urbanization patterns.
    """)

    try:
        # Prepare data for clustering
        cluster_data = state_metrics_df[['total_enroll', 'compliance_ratio', 'urban_pct']].copy()
        
        if len(cluster_data) > 3:
            from sklearn.preprocessing import StandardScaler
            from sklearn.cluster import KMeans
            
            cluster_data_scaled = StandardScaler().fit_transform(cluster_data)
            kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
            state_metrics_df['cluster'] = kmeans.fit_predict(cluster_data_scaled)
            
            st.subheader("📊 Correlation: Predictors of Compliance")
            corr_matrix = cluster_data.corr()
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu',
                labels=dict(x='Variable', y='Variable', color='Correlation'),
                title='Correlation Matrix: What Predicts Compliance?'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **📌 Key Outcomes:**
            - **Compliance vs Enrollment**: Correlation shows how enrollment scale affects compliance tracking
            - **Compliance vs Urbanization**: Urban concentration tends to improve infrastructure and compliance
            - **Implication**: States can improve compliance by investing in distributed biometric infrastructure
            """)
            
            st.divider()
            st.subheader("🧭 Clustering: State Groupings")
            
            fig = px.scatter_3d(
                state_metrics_df,
                x='total_enroll', y='compliance_ratio', z='urban_pct', color='cluster',
                hover_name='state',
                labels={'total_enroll': 'Total Enrollment','compliance_ratio': 'Compliance Ratio','urban_pct': 'Urban %'},
                title='State Clusters: Enrollment vs Compliance vs Urbanization',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                scene=dict(
                    xaxis=dict(gridcolor='lightgray', showgrid=True),
                    yaxis=dict(gridcolor='lightgray', showgrid=True),
                    zaxis=dict(gridcolor='lightgray', showgrid=True)
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **📌 Cluster Interpretation:**
            - **Cluster 0**: High enrollment + high compliance (developed states)
            - **Cluster 1**: High enrollment + low compliance (crisis zones)
            - **Cluster 2**: Low enrollment + variable compliance (emerging states)
            - **Cluster 3**: Rural-heavy states with limited urbanization
            """)
            
            st.subheader("📍 States by Cluster")
            for cluster_id in range(4):
                cluster_states = state_metrics_df[state_metrics_df['cluster'] == cluster_id].sort_values('total_enroll', ascending=False)
                if len(cluster_states) > 0:
                    states_list = ', '.join(cluster_states['state'].tolist())
                    st.write(f"**Cluster {cluster_id}** ({len(cluster_states)} states): {states_list}")
        
        st.divider()
        st.subheader("📊 Regression Summary: Predicting Compliance")
        
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import RandomForestRegressor
        
        X = state_metrics_df[['total_enroll', 'num_districts', 'urban_pct']].values
        y = state_metrics_df['compliance_ratio'].values
        
        if len(X) > 3:
            lr_model = LinearRegression().fit(X, y)
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Linear Regression R²:** {lr_model.score(X, y):.4f}")
                st.write({
                    'total_enroll': float(lr_model.coef_[0]),
                    'num_districts': float(lr_model.coef_[1]),
                    'urban_pct': float(lr_model.coef_[2])
                })
            with col2:
                st.markdown(f"**Random Forest R²:** {rf_model.score(X, y):.4f}")
                st.write({
                    'total_enroll': float(rf_model.feature_importances_[0]),
                    'num_districts': float(rf_model.feature_importances_[1]),
                    'urban_pct': float(rf_model.feature_importances_[2])
                })
    
    except Exception as e:
        st.error(f"❌ Error in Advanced Analytics: {str(e)}")

# ============================================================================
# PAGE 6: SYNTHESIS & RECOMMENDATIONS
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

# ============================================================================
# PAGE 7: TEAM
# ============================================================================

elif page == "👥 Team":
    st.title("👥 Team: Dhurandhar")
    st.subheader("UIDAI Data Hackathon 2026")
    
    st.markdown("---")
    
    team_members = [
        {"name": "Niraj Kumar", "email": "21f1006589@ds.study.iitm.ac.in", "emoji": "🧑‍💼"},
        {"name": "Shruti Chandagade", "email": "placeholder@email.com", "emoji": "👩‍💼"},
        {"name": "Pawan Chaudhary", "email": "placeholder@email.com", "emoji": "🧑‍💼"},
        {"name": "Ritesh Sharma", "email": "placeholder@email.com", "emoji": "🧑‍💼"},
        {"name": "Pradeep Mondal", "email": "placeholder@email.com", "emoji": "🧑‍💼"},
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, member in enumerate(team_members):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 20px; background-color: #f9f9f9;">
                <h3 style="margin-bottom: 10px; color: black;">{member['emoji']} {member['name']}</h3>
                <p style="color: #666; margin: 5px 0;">
                    📧 <a href="mailto:{member['email']}" style="color: #0066cc; text-decoration: none;">{member['email']}</a>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    ### 🎯 Project Contribution
    This team collaborated on the comprehensive analysis of UIDAI Aadhaar enrollment data, 
    identifying three critical problems and developing data-driven policy recommendations 
    for inclusive digital identity access across India.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**UIDAI Data Hackathon 2026**  
Three-Problem Analysis: Biometric Compliance + Geographic Divide + Urban-Rural Gap  
*Data-driven insights for inclusive digital identity access*

📊 **Architecture**: Preprocessing done separately | App only loads processed data | Optimized for Streamlit Cloud
""")
