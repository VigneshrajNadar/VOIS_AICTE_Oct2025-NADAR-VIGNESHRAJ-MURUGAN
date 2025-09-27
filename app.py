import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🏨 Airbnb Hotel Booking Analysis",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern hotel theme with animations
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated background elements */
    .hotel-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .hotel-bg::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="50" font-size="20" fill="rgba(255,255,255,0.05)">🏨</text></svg>') repeat;
        animation: float 20s linear infinite;
    }
    
    @keyframes float {
        0% { transform: translateX(-50px) translateY(-50px); }
        100% { transform: translateX(50px) translateY(50px); }
    }
    
    /* Main header with enhanced animations */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: slideInDown 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .metric-card:hover::before {
        transform: translateX(100%);
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Dark sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced form elements */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #2a2a3e 0%, #3a3a4e 100%);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        background: linear-gradient(135deg, #3a3a4e 0%, #4a4a5e 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Enhanced info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: slideInLeft 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    p, div {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Pulse animation for important elements */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Floating elements */
    .float {
        animation: floatUpDown 3s ease-in-out infinite;
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the Airbnb dataset"""
    try:
        df = pd.read_excel('1730285881-Airbnb_Open_Data.xlsx')
        
        # Data cleaning and preprocessing
        df = df.dropna(subset=['price', 'neighbourhood group', 'room type'])
        
        # Convert price to numeric and remove outliers
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]
        df = df[df['price'] < df['price'].quantile(0.99)]  # Remove extreme outliers
        
        # Clean neighbourhood group names - handle case variations and typos
        df['neighbourhood group'] = df['neighbourhood group'].str.strip().str.title()
        # Handle common variations and typos
        df['neighbourhood group'] = df['neighbourhood group'].replace({
            'Manhattan': 'Manhattan',
            'Brooklyn': 'Brooklyn', 
            'Queens': 'Queens',
            'Bronx': 'Bronx',
            'Staten Island': 'Staten Island',
            'Brookln': 'Brooklyn',  # Handle typo
            'Manhatan': 'Manhattan'  # Handle typo
        })
        
        # Convert construction year to numeric
        df['Construction year'] = pd.to_numeric(df['Construction year'], errors='coerce')
        
        # Clean room type names - handle case variations
        df['room type'] = df['room type'].str.strip().str.title()
        # Handle common variations
        df['room type'] = df['room type'].replace({
            'Entire Home/Apt': 'Entire Home/Apt',
            'Private Room': 'Private Room',
            'Shared Room': 'Shared Room',
            'Hotel Room': 'Hotel Room'
        })
        
        # Convert host identity verified to boolean - handle various formats
        df['host_identity_verified'] = df['host_identity_verified'].str.lower().str.strip()
        df['host_identity_verified'] = df['host_identity_verified'].map({
            'verified': True, 
            'unconfirmed': False,
            't': True,
            'f': False,
            'true': True,
            'false': False
        })
        
        # Convert instant bookable to boolean
        df['instant_bookable'] = df['instant_bookable'].map({'t': True, 'f': False})
        
        # Add derived columns
        df['price_per_night'] = df['price'] / df['minimum nights'].fillna(1)
        df['revenue_potential'] = df['price'] * df['availability 365'].fillna(0)
        
        # Ensure numeric columns are properly formatted
        numeric_cols = ['price', 'service fee', 'minimum nights', 'number of reviews', 
                       'reviews per month', 'review rate number', 'calculated host listings count', 
                       'availability 365']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def create_header():
    """Create the main header with animated background"""
    st.markdown("""
    <div class="hotel-bg"></div>
    <div class="main-header float">
        <h1>🏨 Airbnb Hotel Booking Analysis Dashboard</h1>
        <p>Comprehensive insights into New York City's short-term rental market</p>
        <p><em>✨ Advanced Analytics & Interactive Visualizations</em></p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_filters(df):
    """Create sidebar filters"""
    st.sidebar.markdown("## 🔍 Filter Options")
    
    # Neighbourhood group filter
    neighbourhood_groups = ['All'] + sorted(df['neighbourhood group'].unique().tolist())
    selected_neighbourhood = st.sidebar.selectbox(
        "Select Neighbourhood Group", 
        neighbourhood_groups
    )
    
    # Room type filter
    room_types = ['All'] + sorted(df['room type'].unique().tolist())
    selected_room_type = st.sidebar.selectbox(
        "Select Room Type", 
        room_types
    )
    
    # Price range filter
    price_range = st.sidebar.slider(
        "Price Range ($)",
        min_value=int(df['price'].min()),
        max_value=int(df['price'].max()),
        value=(int(df['price'].min()), int(df['price'].max()))
    )
    
    # Host verification filter
    verification_status = st.sidebar.selectbox(
        "Host Verification Status",
        ['All', 'Verified', 'Unverified']
    )
    
    return selected_neighbourhood, selected_room_type, price_range, verification_status

def filter_data(df, neighbourhood, room_type, price_range, verification):
    """Filter data based on sidebar selections with improved error handling"""
    filtered_df = df.copy()
    
    # Apply neighbourhood filter
    if neighbourhood != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood group'] == neighbourhood]
    
    # Apply room type filter
    if room_type != 'All':
        filtered_df = filtered_df[filtered_df['room type'] == room_type]
    
    # Apply price range filter
    filtered_df = filtered_df[
        (filtered_df['price'] >= price_range[0]) & 
        (filtered_df['price'] <= price_range[1])
    ]
    
    # Apply verification filter
    if verification == 'Verified':
        filtered_df = filtered_df[filtered_df['host_identity_verified'] == True]
    elif verification == 'Unverified':
        filtered_df = filtered_df[filtered_df['host_identity_verified'] == False]
    
    # If no data matches, provide helpful suggestions
    if filtered_df.empty and len(df) > 0:
        # Check what combinations might work
        suggestions = []
        
        if neighbourhood != 'All' and room_type != 'All':
            # Check if the room type exists in the neighbourhood
            room_in_neighbourhood = df[(df['neighbourhood group'] == neighbourhood) & (df['room type'] == room_type)]
            if room_in_neighbourhood.empty:
                suggestions.append(f"💡 **No {room_type} listings found in {neighbourhood}**")
                # Show available room types in this neighbourhood
                available_rooms = df[df['neighbourhood group'] == neighbourhood]['room type'].value_counts()
                if not available_rooms.empty:
                    suggestions.append(f"Available room types in {neighbourhood}: {', '.join(available_rooms.index[:3])}")
        
        if suggestions:
            for suggestion in suggestions:
                st.info(suggestion)
        
        # Try with broader criteria
        st.warning("⚠️ No exact matches found. Showing similar results...")
        filtered_df = df.copy()
        
        # Apply only price range filter
        filtered_df = filtered_df[
            (filtered_df['price'] >= price_range[0]) & 
            (filtered_df['price'] <= price_range[1])
        ]
        
        # If still empty, show all data
        if filtered_df.empty:
            st.info("💡 Showing all available data. Please adjust your price range.")
            filtered_df = df.copy()
    
    return filtered_df

def create_key_metrics(df):
    """Create key metrics cards with enhanced animations"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card pulse">
            <h3>📊 Total Listings</h3>
            <h2>{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_price = df['price'].mean()
        st.markdown(f"""
        <div class="metric-card pulse">
            <h3>💰 Avg Price</h3>
            <h2>${avg_price:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_revenue = df['revenue_potential'].sum()
        st.markdown(f"""
        <div class="metric-card pulse">
            <h3>💵 Total Revenue</h3>
            <h2>${total_revenue:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_rating = df['review rate number'].mean()
        st.markdown(f"""
        <div class="metric-card pulse">
            <h3>⭐ Avg Rating</h3>
            <h2>{avg_rating:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)

def create_price_analysis(df):
    """Create price analysis visualizations with enhanced styling"""
    st.markdown("## 💰 Price Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution by neighbourhood
        fig = px.box(df, x='neighbourhood group', y='price', 
                    title="Price Distribution by Neighbourhood Group",
                    color='neighbourhood group',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(
            showlegend=False, 
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        fig.update_xaxes(color='white')
        fig.update_yaxes(color='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price vs Room Type
        price_by_room = df.groupby('room type')['price'].mean().reset_index()
        fig = px.bar(price_by_room,
                    x='room type', y='price',
                    title="Average Price by Room Type",
                    color='price',
                    color_continuous_scale='viridis')
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        fig.update_xaxes(color='white')
        fig.update_yaxes(color='white')
        st.plotly_chart(fig, use_container_width=True)

def create_location_analysis(df):
    """Create location-based analysis with enhanced styling"""
    st.markdown("## 📍 Location Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Neighbourhood group distribution
        neighbourhood_counts = df['neighbourhood group'].value_counts()
        fig = px.pie(values=neighbourhood_counts.values, 
                    names=neighbourhood_counts.index,
                    title="Listings Distribution by Neighbourhood Group",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Map visualization
        sample_df = df.sample(min(1000, len(df)))
        fig = px.scatter_mapbox(sample_df, 
                               lat="lat", lon="long",
                               color="price", size="price",
                               hover_data=["NAME", "neighbourhood group", "room type"],
                               color_continuous_scale="viridis",
                               mapbox_style="open-street-map",
                               title="Airbnb Listings Map (Sample)")
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

def create_host_analysis(df):
    """Create host performance analysis"""
    st.markdown("## 👥 Host Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top hosts by listings count
        top_hosts = df.groupby('host name').agg({
            'calculated host listings count': 'first',
            'price': 'mean',
            'review rate number': 'mean'
        }).nlargest(10, 'calculated host listings count')
        
        fig = px.bar(top_hosts.reset_index(),
                    x='host name', y='calculated host listings count',
                    title="Top 10 Hosts by Listings Count",
                    color='calculated host listings count',
                    color_continuous_scale='blues')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Host verification vs rating
        verification_rating = df.groupby('host_identity_verified')['review rate number'].mean()
        
        # Ensure we have both verification statuses
        labels = []
        values = []
        
        if False in verification_rating.index:
            labels.append('Unverified')
            values.append(verification_rating[False])
        
        if True in verification_rating.index:
            labels.append('Verified')
            values.append(verification_rating[True])
        
        # Only create chart if we have data
        if labels and values:
            fig = px.bar(x=labels, 
                        y=values,
                        title="Average Rating by Host Verification Status",
                        color=values,
                        color_continuous_scale='greens')
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='white'
            )
            fig.update_xaxes(color='white')
            fig.update_yaxes(color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No verification data available for analysis")

def create_booking_insights(df):
    """Create booking insights and recommendations"""
    st.markdown("## 📈 Booking Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Availability analysis
        availability_stats = df.groupby('neighbourhood group')['availability 365'].mean().sort_values(ascending=False)
        fig = px.bar(x=availability_stats.index, y=availability_stats.values,
                    title="Average Availability by Neighbourhood Group",
                    color=availability_stats.values,
                    color_continuous_scale='oranges')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Service fee analysis
        fig = px.scatter(df.sample(min(2000, len(df))), 
                        x='price', y='service fee',
                        color='neighbourhood group',
                        title="Price vs Service Fee Relationship",
                        hover_data=['room type', 'neighbourhood group'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def create_recommendations(df):
    """Create data-driven recommendations"""
    st.markdown("## 💡 Data-Driven Recommendations")
    
    # Calculate insights
    avg_price_by_neighbourhood = df.groupby('neighbourhood group')['price'].mean().sort_values(ascending=False)
    best_rated_neighbourhoods = df.groupby('neighbourhood group')['review rate number'].mean().sort_values(ascending=False)
    most_available_neighbourhoods = df.groupby('neighbourhood group')['availability 365'].mean().sort_values(ascending=False)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>🏆 Premium Markets</h4>
            <p><strong>Highest Average Prices:</strong></p>
            <ul>
        """, unsafe_allow_html=True)
        for neighbourhood in avg_price_by_neighbourhood.head(3).index:
            price = avg_price_by_neighbourhood[neighbourhood]
            st.markdown(f"<li>{neighbourhood}: ${price:.0f}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>⭐ Best Rated Areas</h4>
            <p><strong>Highest Guest Satisfaction:</strong></p>
            <ul>
        """, unsafe_allow_html=True)
        for neighbourhood in best_rated_neighbourhoods.head(3).index:
            rating = best_rated_neighbourhoods[neighbourhood]
            st.markdown(f"<li>{neighbourhood}: {rating:.1f}/5</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <h4>📅 Most Available</h4>
            <p><strong>Highest Availability:</strong></p>
            <ul>
        """, unsafe_allow_html=True)
        for neighbourhood in most_available_neighbourhoods.head(3).index:
            availability = most_available_neighbourhoods[neighbourhood]
            st.markdown(f"<li>{neighbourhood}: {availability:.0f} days</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)

def main():
    """Main application function"""
    create_header()
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("Failed to load data. Please check the file path and format.")
        return
    
    # Create sidebar filters
    neighbourhood, room_type, price_range, verification = create_sidebar_filters(df)
    
    # Filter data
    filtered_df = filter_data(df, neighbourhood, room_type, price_range, verification)
    
    if filtered_df.empty:
        st.warning("No data matches your filter criteria. Please adjust your selections.")
        return
    
    # Display filtered data info with enhanced styling
    st.markdown(f"""
    <div class="info-box float">
        <h4>📊 Dataset Overview</h4>
        <p>Showing <strong>{len(filtered_df):,}</strong> listings out of <strong>{len(df):,}</strong> total listings</p>
        <p>Filters: {neighbourhood} | {room_type} | ${price_range[0]}-${price_range[1]} | {verification}</p>
        <p><em>✨ Data refreshed automatically with advanced filtering</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create visualizations
    create_key_metrics(filtered_df)
    create_price_analysis(filtered_df)
    create_location_analysis(filtered_df)
    create_host_analysis(filtered_df)
    create_booking_insights(filtered_df)
    create_recommendations(filtered_df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;">
        <p>🏨 <strong>Airbnb Hotel Booking Analysis Dashboard</strong></p>
        <p>Built with ❤️ using Advanced Analytics & Interactive Visualizations</p>
        <p><em>Data Source: Airbnb Open Data - New York City</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
