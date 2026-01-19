"""
Visualization Utilities for UIDAI Hackathon
Reusable functions for creating charts and maps
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class VisualizationTools:
    """Collection of visualization functions"""
    
    @staticmethod
    def plot_time_series(df, date_col='date', value_cols=None, title='Time Series'):
        """Plot time series for one or more columns"""
        if value_cols is None:
            value_cols = [col for col in df.columns if col != date_col]
        
        fig = go.Figure()
        
        for col in value_cols:
            if col in df.columns and col != date_col:
                fig.add_trace(go.Scatter(
                    x=df[date_col],
                    y=df[col],
                    mode='lines',
                    name=col
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Count',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def plot_state_comparison(df, state_col='state', value_col='total', top_n=20):
        """Create bar chart comparing states"""
        state_totals = df.groupby(state_col)[value_col].sum().sort_values(ascending=False).head(top_n)
        
        fig = px.bar(
            x=state_totals.index,
            y=state_totals.values,
            title=f'Top {top_n} States by {value_col}',
            labels={'x': 'State', 'y': value_col.title()},
            template='plotly_white'
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        return fig
    
    @staticmethod
    def plot_age_distribution(df, age_cols, title='Age Distribution'):
        """Plot distribution across age groups"""
        age_data = df[age_cols].sum()
        
        fig = go.Figure(data=[
            go.Bar(x=age_cols, y=age_data.values)
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title='Age Group',
            yaxis_title='Total Count',
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def plot_heatmap(df, x_col, y_col, value_col, title='Heatmap'):
        """Create a heatmap for two categorical variables"""
        pivot = df.pivot_table(index=y_col, columns=x_col, values=value_col, aggfunc='sum')
        
        fig = px.imshow(
            pivot,
            labels=dict(x=x_col, y=y_col, color=value_col),
            title=title,
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        
        return fig
    
    @staticmethod
    def plot_distribution(df, column, title=None, bins=50):
        """Plot distribution of a numeric column"""
        if title is None:
            title = f'Distribution of {column}'
        
        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=title,
            template='plotly_white'
        )
        
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title='Frequency'
        )
        
        return fig
    
    @staticmethod
    def plot_trend_with_ma(df, date_col='date', value_col='total', window=7):
        """Plot time series with moving average"""
        df_sorted = df.sort_values(date_col)
        df_sorted['MA'] = df_sorted[value_col].rolling(window=window).mean()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sorted[date_col],
            y=df_sorted[value_col],
            mode='lines',
            name='Actual',
            line=dict(color='lightblue', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_sorted[date_col],
            y=df_sorted['MA'],
            mode='lines',
            name=f'{window}-day MA',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title=f'{value_col.title()} with {window}-day Moving Average',
            xaxis_title='Date',
            yaxis_title=value_col.title(),
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def plot_correlation_matrix(df, numeric_cols=None):
        """Plot correlation matrix"""
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        corr = df[numeric_cols].corr()
        
        fig = px.imshow(
            corr,
            text_auto='.2f',
            title='Correlation Matrix',
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        
        return fig
    
    @staticmethod
    def plot_top_districts(df, district_col='district', value_col='total', top_n=20):
        """Plot top districts"""
        district_totals = df.groupby(district_col)[value_col].sum().sort_values(ascending=False).head(top_n)
        
        fig = px.bar(
            x=district_totals.values,
            y=district_totals.index,
            orientation='h',
            title=f'Top {top_n} Districts by {value_col}',
            labels={'x': value_col.title(), 'y': 'District'},
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def plot_seasonal_pattern(df, date_col='date', value_col='total'):
        """Plot seasonal patterns (monthly aggregation)"""
        df_copy = df.copy()
        df_copy['month'] = pd.to_datetime(df_copy[date_col]).dt.month
        df_copy['year'] = pd.to_datetime(df_copy[date_col]).dt.year
        
        monthly = df_copy.groupby(['year', 'month'])[value_col].sum().reset_index()
        monthly['month_name'] = pd.to_datetime(monthly['month'], format='%m').dt.strftime('%b')
        
        fig = px.line(
            monthly,
            x='month_name',
            y=value_col,
            color='year',
            title='Seasonal Pattern by Month',
            labels={'month_name': 'Month', value_col: value_col.title()},
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_summary_dashboard(df, date_col='date', numeric_cols=None):
        """Create a multi-panel summary dashboard"""
        if numeric_cols is None:
            numeric_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                           if col not in [date_col]]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Time Series', 'Distribution', 'Top States', 'Correlation'),
            specs=[[{"type": "scatter"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "heatmap"}]]
        )
        
        # Add plots (simplified version)
        # Time series
        if date_col in df.columns and len(numeric_cols) > 0:
            ts_data = df.groupby(date_col)[numeric_cols[0]].sum()
            fig.add_trace(
                go.Scatter(x=ts_data.index, y=ts_data.values, mode='lines'),
                row=1, col=1
            )
        
        fig.update_layout(height=800, showlegend=False, template='plotly_white')
        
        return fig


def save_figure(fig, filename, output_dir='../outputs/figures'):
    """Save plotly figure as HTML and PNG"""
    from pathlib import Path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as HTML
    fig.write_html(str(output_path / f"{filename}.html"))
    
    # Save as PNG
    try:
        fig.write_image(str(output_path / f"{filename}.png"), width=1200, height=600)
    except:
        print(f"   Note: PNG export requires kaleido. HTML saved successfully.")


if __name__ == "__main__":
    print("✅ Visualization utilities loaded successfully!")
