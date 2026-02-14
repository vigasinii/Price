import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from plotly.subplots import make_subplots
import random

# Page configuration
st.set_page_config(
    page_title="PriceIQ - Advanced Price Monitoring Platform",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alert-card {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 5px solid;
        color: #000000;
    }
    .alert-critical {
        background-color: #fee;
        border-color: #f44;
    }
    .alert-warning {
        background-color: #ffc;
        border-color: #fa0;
    }
    .alert-info {
        background-color: #eff;
        border-color: #4af;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    /* Sidebar button styling */
    .stButton > button {
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    /* Make sidebar nav buttons full width with proper spacing */
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

def _init_sample_data():
    """Initialize sample data for demonstration"""
    # Sample products
    st.session_state.products = [
        {"id": 1, "name": "Wireless Headphones Pro", "sku": "WHP-001", "current_price": 299.99, "cost": 150.00, "category": "Electronics"},
        {"id": 2, "name": "Smart Watch X200", "sku": "SWX-200", "current_price": 499.99, "cost": 250.00, "category": "Electronics"},
        {"id": 3, "name": "Bluetooth Speaker Max", "sku": "BSM-300", "current_price": 149.99, "cost": 75.00, "category": "Audio"},
        {"id": 4, "name": "USB-C Hub Elite", "sku": "UCH-400", "current_price": 79.99, "cost": 40.00, "category": "Accessories"},
        {"id": 5, "name": "Laptop Stand Pro", "sku": "LSP-500", "current_price": 129.99, "cost": 65.00, "category": "Accessories"},
    ]
    
    # Sample competitors
    st.session_state.competitors = [
        {"name": "Amazon", "url": "amazon.com", "status": "Active"},
        {"name": "Best Buy", "url": "bestbuy.com", "status": "Active"},
        {"name": "Walmart", "url": "walmart.com", "status": "Active"},
        {"name": "Target", "url": "target.com", "status": "Active"},
        {"name": "Newegg", "url": "newegg.com", "status": "Active"},
    ]
    
    # Generate sample price history
    _generate_sample_price_history()
    
    # Sample alerts
    st.session_state.alerts = [
        {"time": datetime.now() - timedelta(minutes=5), "type": "critical", "message": "Competitor dropped price by 15% on Wireless Headphones Pro", "product": "WHP-001"},
        {"time": datetime.now() - timedelta(minutes=30), "type": "warning", "message": "MAP violation detected on Smart Watch X200", "product": "SWX-200"},
        {"time": datetime.now() - timedelta(hours=1), "type": "info", "message": "New competitor detected for Bluetooth Speaker Max", "product": "BSM-300"},
        {"time": datetime.now() - timedelta(hours=2), "type": "critical", "message": "Stock-out detected at Amazon for USB-C Hub Elite", "product": "UCH-400"},
        {"time": datetime.now() - timedelta(hours=3), "type": "warning", "message": "Price volatility increased for Laptop Stand Pro", "product": "LSP-500"},
    ]
    
    # Sample dynamic pricing rules
    st.session_state.dynamic_pricing_rules = [
        {"id": 1, "product_sku": "WHP-001", "rule_type": "Match Lowest", "floor_price": 249.99, "ceiling_price": 349.99, "margin_min": 30, "active": True},
        {"id": 2, "product_sku": "SWX-200", "rule_type": "Beat by %", "beat_by": 5, "floor_price": 449.99, "ceiling_price": 599.99, "margin_min": 35, "active": True},
        {"id": 3, "product_sku": "BSM-300", "rule_type": "Fixed Margin", "target_margin": 40, "floor_price": 129.99, "ceiling_price": 199.99, "active": False},
    ]

def _generate_sample_price_history():
    """Generate realistic sample price history"""
    days = 30
    base_date = datetime.now() - timedelta(days=days)
    
    for product in st.session_state.products:
        base_price = product['current_price']
        
        for day in range(days):
            current_date = base_date + timedelta(days=day)
            
            # Your price (slight variations)
            your_price = base_price + np.random.normal(0, 5)
            
            # Competitor prices (more variation)
            for competitor in st.session_state.competitors[:3]:  # Top 3 competitors
                comp_price = base_price * np.random.uniform(0.85, 1.15)
                
                st.session_state.price_history.append({
                    "date": current_date,
                    "product_id": product['id'],
                    "product_name": product['name'],
                    "sku": product['sku'],
                    "source": competitor['name'],
                    "price": round(comp_price, 2),
                    "availability": np.random.choice([True, False], p=[0.95, 0.05]),
                    "shipping_cost": round(np.random.uniform(0, 15), 2)
                })
            
            # Add your own price
            st.session_state.price_history.append({
                "date": current_date,
                "product_id": product['id'],
                "product_name": product['name'],
                "sku": product['sku'],
                "source": "Your Store",
                "price": round(your_price, 2),
                "availability": True,
                "shipping_cost": 0
            })

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.products = []
    st.session_state.competitors = []
    st.session_state.price_history = []
    st.session_state.alerts = []
    st.session_state.dynamic_pricing_rules = []
    st.session_state.tracked_urls = []
    
    # Sample data for demonstration
    _init_sample_data()
# Sidebar Navigation
with st.sidebar:
    st.markdown('<p class="main-header" style="font-size: 1.5rem;">🎯 PriceIQ</p>', unsafe_allow_html=True)
    st.markdown("### Advanced Price Intelligence")
    st.markdown("---")
    
    # Navigation buttons with better styling
    st.markdown("#### 🧭 Navigation")
    
    # Initialize selected page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📊 Dashboard"
    
    nav_options = [
        ("📊", "Dashboard"),
        ("🔍", "Competitor Tracking"),
        ("⚡", "Dynamic Pricing"),
        ("📈", "Analytics & Reports"),
        ("🚨", "Alerts & Monitoring"),
        ("🛠️", "Settings & Integration"),
        ("📦", "Product Management")
    ]
    
    for icon, label in nav_options:
        full_label = f"{icon} {label}"
        if st.button(full_label, key=f"nav_{label}", use_container_width=True, 
                    type="primary" if st.session_state.current_page == full_label else "secondary"):
            st.session_state.current_page = full_label
            st.rerun()
    
    page = st.session_state.current_page
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("#### Quick Stats")
    st.metric("Products Tracked", len(st.session_state.products))
    st.metric("Active Competitors", len([c for c in st.session_state.competitors if c['status'] == 'Active']))
    st.metric("Active Alerts", len([a for a in st.session_state.alerts if (datetime.now() - a['time']).total_seconds() < 86400]))
    
    st.markdown("---")
    st.markdown("#### Last Crawl")
    st.info(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
    st.success("✅ All systems operational")

def show_dashboard():
    """Main dashboard with comprehensive overview"""
    st.markdown('<p class="main-header">📊 Real-Time Pricing Dashboard</p>', unsafe_allow_html=True)
    
    # Time filter
    col_time1, col_time2, col_time3 = st.columns([2, 2, 1])
    with col_time1:
        time_range = st.selectbox("Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"])
    with col_time2:
        if time_range == "Custom":
            date_range = st.date_input("Select Date Range", [datetime.now() - timedelta(days=30), datetime.now()])
    with col_time3:
        auto_refresh = st.checkbox("Auto Refresh", value=True)
    
    # Key metrics row
    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_margin = np.mean([(p['current_price'] - p['cost']) / p['current_price'] * 100 for p in st.session_state.products])
        st.metric(
            "Avg Margin",
            f"{avg_margin:.1f}%",
            delta="2.3%",
            delta_color="normal"
        )
    
    with col2:
        competitive_index = 87.5
        st.metric(
            "Competitive Index",
            f"{competitive_index:.1f}",
            delta="-1.2",
            delta_color="inverse"
        )
    
    with col3:
        price_changes = 24
        st.metric(
            "Price Changes (24h)",
            price_changes,
            delta="3",
            delta_color="off"
        )
    
    with col4:
        map_violations = 2
        st.metric(
            "MAP Violations",
            map_violations,
            delta="-1",
            delta_color="normal"
        )
    
    with col5:
        winning_position = 68
        st.metric(
            "Winning Position",
            f"{winning_position}%",
            delta="5%",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Main charts row
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### 💹 Price Position vs Competitors")
        show_price_position_chart()
    
    with col_chart2:
        st.markdown("#### 📊 Market Share by Price Point")
        show_market_share_chart()
    
    # Second row of charts
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.markdown("#### 📊 Category Performance")
        show_category_performance()
    
    with col_chart4:
        st.markdown("#### 🎯 Margin Distribution")
        show_margin_distribution()
    
    # Product performance table
    st.markdown("### 🏆 Product Performance Overview")
    show_product_performance_table()
    
    # Recent activity feed
    st.markdown("### 🔔 Recent Activity")
    show_recent_activity()

def show_price_position_chart():
    """Price position comparison chart"""
    df = pd.DataFrame(st.session_state.price_history)
    df = df[df['date'] >= datetime.now() - timedelta(days=7)]
    
    fig = go.Figure()
    
    for product in st.session_state.products[:3]:  # Top 3 products
        product_data = df[df['product_id'] == product['id']]
        
        for source in product_data['source'].unique():
            source_data = product_data[product_data['source'] == source]
            
            fig.add_trace(go.Scatter(
                x=source_data['date'],
                y=source_data['price'],
                name=f"{product['name'][:20]} - {source}",
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=6)
            ))
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_market_share_chart():
    """Market share by price point"""
    categories = ['$0-100', '$100-200', '$200-300', '$300-400', '$400+']
    your_share = [15, 25, 30, 20, 10]
    competitor_share = [20, 30, 25, 15, 10]
    
    fig = go.Figure(data=[
        go.Bar(name='Your Store', x=categories, y=your_share, marker_color='#667eea'),
        go.Bar(name='Avg Competitor', x=categories, y=competitor_share, marker_color='#764ba2')
    ])
    
    fig.update_layout(
        barmode='group',
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_category_performance():
    """Category performance chart"""
    categories = list(set([p['category'] for p in st.session_state.products]))
    revenue = [random.randint(50000, 200000) for _ in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=revenue,
            marker=dict(
                color=revenue,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Revenue")
            ),
            text=[f"${r:,.0f}" for r in revenue],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis_title="Revenue ($)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_margin_distribution():
    """Margin distribution chart"""
    margins = [(p['current_price'] - p['cost']) / p['current_price'] * 100 for p in st.session_state.products]
    
    fig = go.Figure(data=[go.Histogram(
        x=margins,
        nbinsx=20,
        marker_color='#667eea',
        opacity=0.75
    )])
    
    fig.add_vline(x=np.mean(margins), line_dash="dash", line_color="red", 
                  annotation_text=f"Avg: {np.mean(margins):.1f}%")
    
    fig.update_layout(
        xaxis_title="Margin %",
        yaxis_title="Number of Products",
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_product_performance_table():
    """Product performance comparison table"""
    df = pd.DataFrame(st.session_state.price_history)
    
    performance_data = []
    for product in st.session_state.products:
        product_df = df[df['product_id'] == product['id']]
        
        your_price = product['current_price']
        competitor_prices = product_df[product_df['source'] != 'Your Store']['price']
        
        if len(competitor_prices) > 0:
            min_comp = competitor_prices.min()
            avg_comp = competitor_prices.mean()
            max_comp = competitor_prices.max()
            
            price_diff = ((your_price - avg_comp) / avg_comp * 100)
            position = "🥇 Lowest" if your_price <= min_comp else ("🥈 Competitive" if your_price <= avg_comp else "🥉 Higher")
        else:
            min_comp = avg_comp = max_comp = 0
            price_diff = 0
            position = "➖ No Data"
        
        margin = (your_price - product['cost']) / your_price * 100
        
        performance_data.append({
            "Product": product['name'],
            "SKU": product['sku'],
            "Your Price": f"${your_price:.2f}",
            "Comp Min": f"${min_comp:.2f}" if min_comp > 0 else "N/A",
            "Comp Avg": f"${avg_comp:.2f}" if avg_comp > 0 else "N/A",
            "Comp Max": f"${max_comp:.2f}" if max_comp > 0 else "N/A",
            "Diff %": f"{price_diff:+.1f}%",
            "Margin %": f"{margin:.1f}%",
            "Position": position
        })
    
    performance_df = pd.DataFrame(performance_data)
    st.dataframe(performance_df, use_container_width=True, hide_index=True)

def show_recent_activity():
    """Recent activity feed"""
    for alert in st.session_state.alerts[:5]:
        alert_class = f"alert-{alert['type']}"
        time_ago = (datetime.now() - alert['time']).seconds // 60
        
        icon = "🔴" if alert['type'] == "critical" else ("⚠️" if alert['type'] == "warning" else "ℹ️")
        
        st.markdown(f"""
        <div class="alert-card {alert_class}">
            {icon} <strong>{alert['message']}</strong><br>
            <small>{time_ago} minutes ago • Product: {alert['product']}</small>
        </div>
        """, unsafe_allow_html=True)

def show_competitor_tracking():
    """Competitor tracking interface"""
    st.markdown('<p class="main-header">🔍 Competitor Price Tracking</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🎯 Active Tracking", "➕ Add Competitors", "🌐 Crawl Settings", "🤖 Auto-Matching"])
    
    with tabs[0]:
        show_active_competitor_tracking()
    
    with tabs[1]:
        show_add_competitors()
    
    with tabs[2]:
        show_crawl_settings()
    
    with tabs[3]:
        show_auto_matching()

def show_active_competitor_tracking():
    """Active competitor tracking view"""
    st.markdown("### Currently Tracked Competitors")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_product = st.selectbox("Filter by Product", ["All Products"] + [p['name'] for p in st.session_state.products])
    with col2:
        selected_competitor = st.selectbox("Filter by Competitor", ["All Competitors"] + [c['name'] for c in st.session_state.competitors])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Out of Stock", "Price Changed"])
    
    # Competitor comparison table
    st.markdown("#### 📊 Price Comparison Matrix")
    
    df = pd.DataFrame(st.session_state.price_history)
    latest_df = df.sort_values('date').groupby(['product_id', 'source']).tail(1)
    
    # Create pivot table
    pivot_data = []
    for product in st.session_state.products:
        product_data = latest_df[latest_df['product_id'] == product['id']]
        row = {"Product": product['name'], "SKU": product['sku']}
        
        for source in product_data['source'].unique():
            source_price = product_data[product_data['source'] == source]['price'].values[0]
            row[source] = f"${source_price:.2f}"
        
        pivot_data.append(row)
    
    pivot_df = pd.DataFrame(pivot_data)
    st.dataframe(pivot_df, use_container_width=True, hide_index=True)
    
    # Detailed tracking list
    st.markdown("#### 🔗 Tracked URLs")
    
    for i, product in enumerate(st.session_state.products[:3]):
        with st.expander(f"📦 {product['name']} ({product['sku']})"):
            for competitor in st.session_state.competitors[:3]:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.text(f"🔗 {competitor['name']}")
                    st.caption(f"https://{competitor['url']}/product/{product['sku'].lower()}")
                
                with col2:
                    last_crawl = datetime.now() - timedelta(minutes=random.randint(5, 60))
                    st.caption(f"Last crawled: {last_crawl.strftime('%H:%M')}")
                
                with col3:
                    price = round(product['current_price'] * random.uniform(0.9, 1.1), 2)
                    st.metric("Price", f"${price}")
                
                with col4:
                    if st.button("🔄", key=f"refresh_{i}_{competitor['name']}"):
                        st.success("Crawling...")

def show_add_competitors():
    """Add new competitors interface"""
    st.markdown("### ➕ Add New Competitor Tracking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Manual URL Entry")
        
        with st.form("add_competitor_form"):
            product_select = st.selectbox("Select Product", [p['name'] for p in st.session_state.products])
            competitor_url = st.text_input("Competitor Product URL", placeholder="https://amazon.com/product/...")
            competitor_name = st.text_input("Competitor Name", placeholder="Amazon")
            
            col_a, col_b = st.columns(2)
            with col_a:
                crawl_frequency = st.selectbox("Crawl Frequency", ["Every Hour", "Every 6 Hours", "Daily", "Weekly"])
            with col_b:
                geo_location = st.selectbox("Geo Location", ["US", "UK", "EU", "Asia-Pacific"])
            
            if st.form_submit_button("🎯 Start Tracking", use_container_width=True):
                st.success(f"✅ Now tracking {competitor_name} for {product_select}")
    
    with col2:
        st.markdown("#### 🤖 Automatic Discovery")
        
        product_for_discovery = st.selectbox("Product for Auto-Discovery", [p['name'] for p in st.session_state.products], key="auto_discovery")
        search_marketplaces = st.multiselect(
            "Search in Marketplaces",
            ["Amazon", "eBay", "Walmart", "Best Buy", "Target", "Newegg"],
            default=["Amazon", "Walmart"]
        )
        
        if st.button("🔍 Auto-Discover Competitors", use_container_width=True):
            with st.spinner("Searching marketplaces..."):
                st.success(f"Found 12 competitor listings for {product_for_discovery}")
                
                # Show discovered products
                st.markdown("##### Discovered Products")
                for i in range(3):
                    col_x, col_y, col_z = st.columns([3, 2, 1])
                    with col_x:
                        st.text(f"📦 Similar product #{i+1}")
                    with col_y:
                        st.text(f"Match: {random.randint(85, 99)}%")
                    with col_z:
                        st.checkbox("Track", key=f"track_{i}")

def show_crawl_settings():
    """Crawl configuration settings"""
    st.markdown("### 🌐 Web Crawling Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Crawl Infrastructure")
        
        use_proxies = st.checkbox("Use Rotating Proxies", value=True)
        if use_proxies:
            proxy_pool_size = st.slider("Proxy Pool Size", 10, 1000, 100)
            st.info(f"Using {proxy_pool_size} rotating proxy IPs")
        
        anti_bot_level = st.select_slider(
            "Anti-Bot Protection Level",
            options=["Basic", "Standard", "Advanced", "Maximum"],
            value="Advanced"
        )
        
        headless_browser = st.checkbox("Use Headless Browser (for JS sites)", value=True)
        
        st.markdown("#### Geographic Routing")
        geo_regions = st.multiselect(
            "Crawl from Regions",
            ["North America", "Europe", "Asia", "South America", "Australia"],
            default=["North America"]
        )
        
    with col2:
        st.markdown("#### Crawl Scheduling")
        
        default_frequency = st.selectbox(
            "Default Crawl Frequency",
            ["Every 15 minutes", "Every Hour", "Every 6 Hours", "Daily", "Weekly"]
        )
        
        peak_hours = st.checkbox("Increase frequency during peak hours (9AM-5PM)")
        
        rate_limit = st.number_input("Requests per minute (per competitor)", 1, 60, 10)
        
        st.markdown("#### Data Extraction")
        
        extract_variants = st.checkbox("Extract Product Variants (size, color)", value=True)
        extract_shipping = st.checkbox("Extract Shipping Costs", value=True)
        extract_reviews = st.checkbox("Extract Review Scores", value=False)
        extract_availability = st.checkbox("Track Stock Availability", value=True)
        
    if st.button("💾 Save Crawl Settings", use_container_width=True, type="primary"):
        st.success("✅ Crawl settings updated successfully!")

def show_auto_matching():
    """AI-based product matching configuration"""
    st.markdown("### 🤖 AI Product Auto-Matching")
    
    st.info("🧠 AI Auto-Matching uses ML algorithms to identify the same product across different competitor sites, even with different titles and SKUs.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Matching Algorithm Configuration")
        
        matching_method = st.radio(
            "Primary Matching Method",
            ["AI Similarity Scoring (Recommended)", "SKU/UPC/GTIN Matching", "Hybrid Approach"]
        )
        
        confidence_threshold = st.slider("Minimum Match Confidence %", 50, 100, 85)
        
        st.markdown("#### Matching Attributes")
        use_brand = st.checkbox("Brand Name", value=True)
        use_model = st.checkbox("Model Number", value=True)
        use_upc = st.checkbox("UPC/EAN/GTIN", value=True)
        use_sku = st.checkbox("SKU", value=True)
        use_attributes = st.checkbox("Product Attributes (size, color, etc.)", value=True)
        use_image = st.checkbox("Image Similarity (slower)", value=False)
        
    with col2:
        st.markdown("#### Match Review Queue")
        
        auto_approve_high_confidence = st.checkbox("Auto-approve matches >95% confidence", value=True)
        
        st.markdown("##### Pending Matches for Review")
        
        for i in range(3):
            with st.expander(f"Match #{i+1} - {random.randint(75, 94)}% confidence"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.text("Your Product:")
                    st.caption(st.session_state.products[i]['name'])
                    st.caption(f"SKU: {st.session_state.products[i]['sku']}")
                
                with col_b:
                    st.text("Competitor Product:")
                    st.caption(f"{st.session_state.products[i]['name']} - Similar")
                    st.caption(f"Competitor SKU: COMP-{i+1}-XXX")
                
                col_x, col_y = st.columns(2)
                with col_x:
                    if st.button("✅ Approve Match", key=f"approve_{i}"):
                        st.success("Match approved!")
                with col_y:
                    if st.button("❌ Reject Match", key=f"reject_{i}"):
                        st.error("Match rejected")
    
    if st.button("🔄 Run Auto-Matching Now", use_container_width=True, type="primary"):
        with st.spinner("Running AI matching algorithm..."):
            st.success("✅ Found 47 new matches. 38 auto-approved, 9 pending review.")

def show_dynamic_pricing():
    """Dynamic pricing configuration and management"""
    st.markdown('<p class="main-header">⚡ Dynamic Pricing Engine</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📋 Active Rules", "➕ Create Rule", "📊 Impact Analysis", "⚙️ Settings"])
    
    with tabs[0]:
        show_active_pricing_rules()
    
    with tabs[1]:
        show_create_pricing_rule()
    
    with tabs[2]:
        show_pricing_impact_analysis()
    
    with tabs[3]:
        show_pricing_settings()

def show_active_pricing_rules():
    """Display and manage active pricing rules"""
    st.markdown("### 📋 Active Dynamic Pricing Rules")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Rules", len([r for r in st.session_state.dynamic_pricing_rules if r['active']]))
    with col2:
        st.metric("Products with Rules", len(set([r['product_sku'] for r in st.session_state.dynamic_pricing_rules])))
    with col3:
        st.metric("Price Changes (24h)", 18)
    with col4:
        st.metric("Avg Response Time", "12 min")
    
    # Rules table
    st.markdown("#### Current Rules")
    
    for i, rule in enumerate(st.session_state.dynamic_pricing_rules):
        product = next((p for p in st.session_state.products if p['sku'] == rule['product_sku']), None)
        
        with st.expander(f"{'✅' if rule['active'] else '⏸️'} Rule #{rule['id']}: {product['name'] if product else rule['product_sku']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Rule Configuration**")
                st.text(f"Type: {rule['rule_type']}")
                if 'beat_by' in rule:
                    st.text(f"Beat competitors by: {rule['beat_by']}%")
                if 'target_margin' in rule:
                    st.text(f"Target margin: {rule['target_margin']}%")
                if 'margin_min' in rule:
                    st.text(f"Min Margin: {rule['margin_min']}%")
            
            with col2:
                st.markdown("**Price Constraints**")
                st.text(f"Floor Price: ${rule['floor_price']}")
                st.text(f"Ceiling Price: ${rule['ceiling_price']}")
                if product:
                    current_margin = (product['current_price'] - product['cost']) / product['current_price'] * 100
                    st.text(f"Current Margin: {current_margin:.1f}%")
            
            with col3:
                st.markdown("**Actions**")
                new_status = st.toggle("Active", value=rule['active'], key=f"rule_status_{i}")
                if new_status != rule['active']:
                    rule['active'] = new_status
                    st.success("Status updated!")
                
                if st.button("Edit Rule", key=f"edit_rule_{i}"):
                    st.info("Edit mode enabled")
                
                if st.button("Delete Rule", key=f"delete_rule_{i}", type="secondary"):
                    st.warning("Rule deleted")

def show_create_pricing_rule():
    """Create new pricing rule interface"""
    st.markdown("### ➕ Create New Dynamic Pricing Rule")
    
    with st.form("create_pricing_rule"):
        st.markdown("#### 1️⃣ Select Product")
        product_sku = st.selectbox("Product", [f"{p['name']} ({p['sku']})" for p in st.session_state.products])
        
        st.markdown("#### 2️⃣ Choose Pricing Strategy")
        
        strategy = st.radio(
            "Pricing Strategy",
            ["Match Lowest Competitor", "Beat Lowest by %", "Fixed Margin %", "Dynamic Market Position", "Custom Algorithm"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if "Beat Lowest" in strategy:
                beat_percentage = st.number_input("Beat competitor by %", 1, 50, 5)
            elif "Fixed Margin" in strategy:
                target_margin = st.number_input("Target Margin %", 10, 80, 40)
            elif "Dynamic Market" in strategy:
                market_position = st.select_slider("Market Position", ["Aggressive", "Competitive", "Premium"], value="Competitive")
        
        with col2:
            st.markdown("**Competitor Selection**")
            consider_all = st.checkbox("Consider all competitors", value=True)
            
            if not consider_all:
                selected_competitors = st.multiselect("Select competitors", [c['name'] for c in st.session_state.competitors])
        
        st.markdown("#### 3️⃣ Set Constraints & Guardrails")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            floor_price = st.number_input("Floor Price ($)", 0.0, 10000.0, 100.0, step=10.0)
        
        with col4:
            ceiling_price = st.number_input("Ceiling Price ($)", 0.0, 10000.0, 500.0, step=10.0)
        
        with col5:
            min_margin = st.number_input("Minimum Margin %", 0, 100, 25)
        
        st.markdown("#### 4️⃣ Advanced Options")
        
        col6, col7 = st.columns(2)
        
        with col6:
            consider_inventory = st.checkbox("Consider inventory levels", value=True)
            if consider_inventory:
                low_stock_threshold = st.number_input("Low stock threshold", 1, 100, 10)
                low_stock_action = st.selectbox("Action on low stock", ["Increase price", "Maintain price", "Decrease price"])
        
        with col7:
            time_based = st.checkbox("Time-based pricing", value=False)
            if time_based:
                peak_hours_multiplier = st.slider("Peak hours price multiplier", 0.8, 1.5, 1.1, 0.05)
        
        st.markdown("#### 5️⃣ Execution Settings")
        
        col8, col9 = st.columns(2)
        
        with col8:
            update_frequency = st.selectbox("Update Frequency", ["Real-time", "Every 15 minutes", "Hourly", "Daily"])
        
        with col9:
            max_change_per_update = st.number_input("Max price change per update %", 1, 50, 10)
        
        if st.form_submit_button("🚀 Create Pricing Rule", use_container_width=True, type="primary"):
            st.success("✅ Dynamic pricing rule created successfully!")
            st.balloons()

def show_pricing_impact_analysis():
    """Analyze pricing rule impact"""
    st.markdown("### 📊 Pricing Impact Analysis")
    
    # Impact simulation
    st.markdown("#### 💡 What-If Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        simulation_product = st.selectbox("Select Product for Simulation", [p['name'] for p in st.session_state.products])
        price_change = st.slider("Simulated Price Change %", -30, 30, 0)
    
    with col2:
        st.markdown("**Projected Impact**")
        
        current_price = 299.99
        new_price = current_price * (1 + price_change/100)
        
        st.metric("New Price", f"${new_price:.2f}", f"{price_change:+.1f}%")
        
        # Estimated demand change
        demand_elasticity = -1.5
        demand_change = demand_elasticity * price_change
        st.metric("Estimated Demand Change", f"{demand_change:+.1f}%", delta_color="inverse" if demand_change < 0 else "normal")
        
        # Revenue impact
        revenue_change = (1 + price_change/100) * (1 + demand_change/100) - 1
        st.metric("Projected Revenue Impact", f"{revenue_change*100:+.1f}%", delta_color="normal" if revenue_change > 0 else "inverse")
    
    # Historical impact
    st.markdown("#### 📈 Historical Rule Performance")
    
    performance_data = {
        "Rule": ["Match Lowest", "Beat by 5%", "Fixed Margin 40%"],
        "Products": [15, 8, 12],
        "Avg Margin Change": ["+2.3%", "+5.1%", "+3.8%"],
        "Revenue Impact": ["+8.5%", "+12.3%", "+6.7%"],
        "Win Rate": ["68%", "45%", "72%"]
    }
    
    st.dataframe(pd.DataFrame(performance_data), use_container_width=True, hide_index=True)
    
    # Price change timeline
    st.markdown("#### 📉 Price Change History")
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    your_prices = [299.99 + np.random.normal(0, 10) for _ in range(30)]
    competitor_avg = [295 + np.random.normal(0, 15) for _ in range(30)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=your_prices, name="Your Price", line=dict(color='#667eea', width=3)))
    fig.add_trace(go.Scatter(x=dates, y=competitor_avg, name="Competitor Avg", line=dict(color='#764ba2', width=2, dash='dash')))
    
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

def show_pricing_settings():
    """Global pricing settings"""
    st.markdown("### ⚙️ Dynamic Pricing Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Global Constraints")
        
        global_floor_margin = st.number_input("Global Minimum Margin %", 0, 100, 20)
        max_price_drop_24h = st.number_input("Max Price Drop in 24h %", 0, 50, 15)
        max_price_increase_24h = st.number_input("Max Price Increase in 24h %", 0, 50, 20)
        
        st.markdown("#### Automation Controls")
        
        require_approval = st.checkbox("Require approval for price changes >10%", value=True)
        pause_on_stockout = st.checkbox("Pause pricing rules on stockout", value=True)
        notify_on_change = st.checkbox("Email notification on price changes", value=True)
    
    with col2:
        st.markdown("#### Market Conditions")
        
        competitor_response_delay = st.slider("Competitor response delay (minutes)", 0, 60, 15)
        market_volatility_threshold = st.slider("High volatility threshold %", 5, 50, 20)
        
        st.markdown("#### Safety Features")
        
        enable_circuit_breaker = st.checkbox("Enable circuit breaker (pause on anomalies)", value=True)
        if enable_circuit_breaker:
            circuit_breaker_threshold = st.number_input("Circuit breaker trigger (changes/hour)", 1, 100, 10)
        
        rollback_enabled = st.checkbox("Enable automatic rollback on negative impact", value=True)
    
    if st.button("💾 Save Global Settings", use_container_width=True, type="primary"):
        st.success("✅ Settings saved successfully!")

def show_analytics():
    """Analytics and reporting interface"""
    st.markdown('<p class="main-header">📈 Analytics & Reports</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📊 Overview", "🎯 Competitive Analysis", "💰 Revenue Impact", "📉 Trend Analysis", "📄 Export Reports"])
    
    with tabs[0]:
        show_analytics_overview()
    
    with tabs[1]:
        show_competitive_analysis()
    
    with tabs[2]:
        show_revenue_impact()
    
    with tabs[3]:
        show_trend_analysis()
    
    with tabs[4]:
        show_export_reports()

def show_analytics_overview():
    """Analytics overview dashboard"""
    st.markdown("### 📊 Analytics Overview")
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input("From", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("To", datetime.now())
    with col3:
        st.markdown("####")
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", "$458,293", "+12.3%")
    with col2:
        st.metric("Avg Margin", "42.3%", "+3.1%")
    with col3:
        st.metric("Market Share", "23.8%", "+1.2%")
    with col4:
        st.metric("Price Optimality", "87%", "+5%")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 💹 Revenue Trend")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        revenue = [15000 + np.random.normal(0, 2000) + i*100 for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=revenue, fill='tozeroy', line=dict(color='#667eea', width=2)))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("#### 🎯 Win Rate by Category")
        
        categories = ['Electronics', 'Audio', 'Accessories']
        win_rates = [68, 72, 65]
        
        fig = go.Figure(data=[go.Bar(x=categories, y=win_rates, marker_color='#764ba2')])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="Win Rate %")
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed metrics table
    st.markdown("#### 📋 Detailed Product Metrics")
    
    metrics_data = []
    for product in st.session_state.products:
        metrics_data.append({
            "Product": product['name'],
            "Revenue (30d)": f"${random.randint(20000, 100000):,}",
            "Units Sold": random.randint(100, 500),
            "Avg Price": f"${product['current_price']:.2f}",
            "Margin %": f"{((product['current_price'] - product['cost']) / product['current_price'] * 100):.1f}%",
            "Win Rate": f"{random.randint(60, 85)}%",
            "Price Changes": random.randint(5, 25)
        })
    
    st.dataframe(pd.DataFrame(metrics_data), use_container_width=True, hide_index=True)

def show_competitive_analysis():
    """Competitive analysis view"""
    st.markdown("### 🎯 Competitive Analysis")
    
    # Competitor comparison
    st.markdown("#### Market Position Analysis")
    
    competitors = [c['name'] for c in st.session_state.competitors]
    your_position = [23.8, 42.3, 87, 68]
    comp_avg = [21.5, 38.7, 82, 63]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Market Share %', 'Avg Margin %', 'Price Competitiveness', 'Win Rate %')
    )
    
    metrics = ['Market Share', 'Avg Margin', 'Competitiveness', 'Win Rate']
    
    for i, (your_val, comp_val, metric) in enumerate(zip(your_position, comp_avg, metrics)):
        row = i // 2 + 1
        col = i % 2 + 1
        
        fig.add_trace(
            go.Bar(name='You', x=['You'], y=[your_val], marker_color='#667eea', showlegend=(i==0)),
            row=row, col=col
        )
        fig.add_trace(
            go.Bar(name='Competitor Avg', x=['Comp Avg'], y=[comp_val], marker_color='#764ba2', showlegend=(i==0)),
            row=row, col=col
        )
    
    fig.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Competitor price distribution
    st.markdown("#### 📊 Price Distribution vs Competitors")
    
    price_ranges = ['$0-100', '$100-200', '$200-300', '$300-400', '$400+']
    your_distribution = [15, 25, 30, 20, 10]
    comp_distribution = [20, 30, 25, 15, 10]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price_ranges, y=your_distribution, name='Your Store', 
                             fill='tozeroy', line=dict(color='#667eea', width=3)))
    fig.add_trace(go.Scatter(x=price_ranges, y=comp_distribution, name='Competitor Avg',
                             fill='tozeroy', line=dict(color='#764ba2', width=3)))
    
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

def show_revenue_impact():
    """Revenue impact analysis"""
    st.markdown("### 💰 Revenue Impact Analysis")
    
    st.markdown("#### Price Optimization Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Revenue with Dynamic Pricing", "$458,293", "+12.3%")
        st.caption("vs. static pricing baseline")
    
    with col2:
        st.metric("Additional Margin Captured", "$45,820", "+8.5%")
        st.caption("from optimization")
    
    with col3:
        st.metric("ROI on Price Monitoring", "780%", "")
        st.caption("annual return")
    
    # Attribution analysis
    st.markdown("#### 📈 Revenue Attribution by Strategy")
    
    strategies = ['Match Lowest', 'Beat by %', 'Fixed Margin', 'Dynamic Position']
    revenue_contribution = [125000, 180000, 95000, 58293]
    
    fig = go.Figure(data=[go.Pie(labels=strategies, values=revenue_contribution, hole=0.4)])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Time-based impact
    st.markdown("#### ⏰ Revenue Impact Over Time")
    
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    baseline_revenue = [14000 + np.random.normal(0, 1000) for _ in range(90)]
    optimized_revenue = [15500 + np.random.normal(0, 1000) + i*20 for i in range(90)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=baseline_revenue, name='Baseline (Static Pricing)', 
                             line=dict(color='gray', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=dates, y=optimized_revenue, name='With Dynamic Pricing',
                             line=dict(color='#667eea', width=3), fill='tonexty'))
    
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

def show_trend_analysis():
    """Trend analysis view"""
    st.markdown("### 📉 Trend Analysis")
    
    # Price trends
    st.markdown("#### 💹 Price Trends by Category")
    
    selected_category = st.selectbox("Select Category", ["All Categories", "Electronics", "Audio", "Accessories"])
    
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    fig = go.Figure()
    
    for product in st.session_state.products[:3]:
        prices = [product['current_price'] + np.random.normal(0, product['current_price']*0.05) for _ in range(90)]
        fig.add_trace(go.Scatter(x=dates, y=prices, name=product['name'], mode='lines'))
    
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0), hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal patterns
    st.markdown("#### 📅 Seasonal Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        demand_index = [95, 85, 90, 100, 105, 110, 115, 120, 110, 105, 130, 140]
        
        fig = go.Figure(data=[go.Bar(x=months, y=demand_index, marker_color='#667eea')])
        fig.update_layout(title="Demand Seasonality Index", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        price_volatility = [12, 10, 8, 15, 18, 20, 22, 25, 20, 18, 28, 35]
        
        fig = go.Figure(data=[go.Scatter(x=months, y=price_volatility, mode='lines+markers',
                                         line=dict(color='#764ba2', width=3))])
        fig.update_layout(title="Price Volatility %", height=300)
        st.plotly_chart(fig, use_container_width=True)

def show_export_reports():
    """Export and reporting interface"""
    st.markdown("### 📄 Export Reports")
    
    st.markdown("#### 📊 Generate Custom Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Comprehensive Analytics", "Competitor Pricing", "Dynamic Pricing Performance", 
             "Revenue Analysis", "Product Performance", "Custom Report"]
        )
        
        date_range = st.date_input("Date Range", [datetime.now() - timedelta(days=30), datetime.now()])
        
        products_to_include = st.multiselect("Products", [p['name'] for p in st.session_state.products], 
                                             default=[p['name'] for p in st.session_state.products])
    
    with col2:
        format_type = st.selectbox("Export Format", ["PDF", "Excel (XLSX)", "CSV", "JSON"])
        
        include_charts = st.checkbox("Include visualizations", value=True)
        include_raw_data = st.checkbox("Include raw data", value=False)
        
        schedule_report = st.checkbox("Schedule recurring report", value=False)
        
        if schedule_report:
            frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
            email_to = st.text_input("Email to", "your@email.com")
    
    if st.button("📥 Generate & Download Report", use_container_width=True, type="primary"):
        with st.spinner("Generating report..."):
            st.success(f"✅ Report generated! Click below to download.")
            st.download_button(
                label="⬇️ Download Report",
                data="Sample report data",
                file_name=f"price_analytics_{datetime.now().strftime('%Y%m%d')}.{format_type.lower()}",
                mime="application/octet-stream",
                use_container_width=True
            )
    
    # Quick export buttons
    st.markdown("#### ⚡ Quick Exports")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Current Prices (CSV)", use_container_width=True):
            st.info("Downloading current prices...")
    
    with col2:
        if st.button("📈 Price History (Excel)", use_container_width=True):
            st.info("Downloading price history...")
    
    with col3:
        if st.button("🎯 Competitor Data (CSV)", use_container_width=True):
            st.info("Downloading competitor data...")
    
    with col4:
        if st.button("📄 Full Analytics (PDF)", use_container_width=True):
            st.info("Generating PDF report...")

def show_alerts():
    """Alerts and monitoring interface"""
    st.markdown('<p class="main-header">🚨 Alerts & Monitoring</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🔔 Active Alerts", "⚙️ Alert Rules", "📊 Alert Analytics", "📧 Notifications"])
    
    with tabs[0]:
        show_active_alerts()
    
    with tabs[1]:
        show_alert_rules()
    
    with tabs[2]:
        show_alert_analytics()
    
    with tabs[3]:
        show_notification_settings()

def show_active_alerts():
    """Active alerts view"""
    st.markdown("### 🔔 Active Alerts")
    
    # Alert summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Critical Alerts", len([a for a in st.session_state.alerts if a['type'] == 'critical']))
    with col2:
        st.metric("Warnings", len([a for a in st.session_state.alerts if a['type'] == 'warning']))
    with col3:
        st.metric("Info", len([a for a in st.session_state.alerts if a['type'] == 'info']))
    with col4:
        st.metric("Resolved Today", 12)
    
    # Filter controls
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        alert_filter = st.selectbox("Filter by Type", ["All", "Critical", "Warning", "Info"])
    with col_f2:
        time_filter = st.selectbox("Time Range", ["Last Hour", "Last 24 Hours", "Last Week", "All Time"])
    with col_f3:
        product_filter = st.selectbox("Product", ["All Products"] + [p['name'] for p in st.session_state.products])
    
    # Alert list
    st.markdown("#### Recent Alerts")
    
    for alert in st.session_state.alerts:
        alert_class = f"alert-{alert['type']}"
        icon = "🔴" if alert['type'] == "critical" else ("⚠️" if alert['type'] == "warning" else "ℹ️")
        
        time_diff = datetime.now() - alert['time']
        if time_diff.days > 0:
            time_ago = f"{time_diff.days} days ago"
        elif time_diff.seconds // 3600 > 0:
            time_ago = f"{time_diff.seconds // 3600} hours ago"
        else:
            time_ago = f"{time_diff.seconds // 60} minutes ago"
        
        with st.container():
            col_alert1, col_alert2, col_alert3 = st.columns([6, 2, 2])
            
            with col_alert1:
                st.markdown(f"""
                <div class="alert-card {alert_class}">
                    {icon} <strong>{alert['message']}</strong><br>
                    <small>{time_ago} • Product: {alert['product']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_alert2:
                if st.button("View Details", key=f"view_{alert['time']}"):
                    st.info("Alert details opened")
            
            with col_alert3:
                if st.button("Dismiss", key=f"dismiss_{alert['time']}"):
                    st.success("Alert dismissed")

def show_alert_rules():
    """Alert rules configuration"""
    st.markdown("### ⚙️ Alert Rules Configuration")
    
    st.markdown("#### Create New Alert Rule")
    
    with st.form("create_alert_rule"):
        col1, col2 = st.columns(2)
        
        with col1:
            rule_name = st.text_input("Rule Name", "Price Drop Alert")
            
            trigger_type = st.selectbox(
                "Trigger Type",
                ["Price Change", "MAP Violation", "Stock Status", "Competitor Price", 
                 "Margin Threshold", "Market Position", "Custom Condition"]
            )
            
            if trigger_type == "Price Change":
                threshold = st.number_input("Price change threshold %", 1, 100, 10)
                direction = st.radio("Direction", ["Increase", "Decrease", "Either"])
            
            elif trigger_type == "MAP Violation":
                map_price = st.number_input("MAP Price $", 0.0, 10000.0, 299.99)
            
            elif trigger_type == "Margin Threshold":
                margin_threshold = st.number_input("Minimum Margin %", 0, 100, 30)
        
        with col2:
            severity = st.select_slider("Alert Severity", ["Info", "Warning", "Critical"])
            
            notify_channels = st.multiselect(
                "Notification Channels",
                ["Email", "SMS", "Slack", "Dashboard", "Webhook"],
                default=["Email", "Dashboard"]
            )
            
            products_for_rule = st.multiselect(
                "Apply to Products",
                [p['name'] for p in st.session_state.products],
                default=[st.session_state.products[0]['name']]
            )
            
            active = st.checkbox("Activate immediately", value=True)
        
        if st.form_submit_button("✅ Create Alert Rule", use_container_width=True):
            st.success("Alert rule created successfully!")
    
    # Existing rules
    st.markdown("#### Existing Alert Rules")
    
    existing_rules = [
        {"name": "Competitor Price Drop >10%", "type": "Critical", "active": True, "triggers": 24},
        {"name": "MAP Violation Detection", "type": "Critical", "active": True, "triggers": 5},
        {"name": "Low Margin Alert <25%", "type": "Warning", "active": True, "triggers": 12},
        {"name": "Stock-Out Detection", "type": "Warning", "active": True, "triggers": 8},
        {"name": "Price Volatility High", "type": "Info", "active": False, "triggers": 0},
    ]
    
    for rule in existing_rules:
        with st.expander(f"{'✅' if rule['active'] else '⏸️'} {rule['name']} - {rule['type']}"):
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                st.text(f"Status: {'Active' if rule['active'] else 'Paused'}")
                st.text(f"Triggers (7d): {rule['triggers']}")
            
            with col_r2:
                if st.button("Edit", key=f"edit_{rule['name']}"):
                    st.info("Edit mode")
            
            with col_r3:
                if st.button("Delete", key=f"delete_{rule['name']}"):
                    st.warning("Deleted")

def show_alert_analytics():
    """Alert analytics"""
    st.markdown("### 📊 Alert Analytics")
    
    # Alert trends
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    critical_alerts = [random.randint(0, 5) for _ in range(30)]
    warning_alerts = [random.randint(2, 10) for _ in range(30)]
    info_alerts = [random.randint(5, 15) for _ in range(30)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=critical_alerts, name='Critical', 
                             stackgroup='one', fillcolor='#f44', line=dict(width=0)))
    fig.add_trace(go.Scatter(x=dates, y=warning_alerts, name='Warning',
                             stackgroup='one', fillcolor='#fa0', line=dict(width=0)))
    fig.add_trace(go.Scatter(x=dates, y=info_alerts, name='Info',
                             stackgroup='one', fillcolor='#4af', line=dict(width=0)))
    
    fig.update_layout(height=300, title="Alert Volume Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Alert distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Alerts by Type")
        
        alert_types = ['Price Drop', 'MAP Violation', 'Stock-Out', 'High Volatility', 'Margin Low']
        alert_counts = [45, 12, 18, 28, 15]
        
        fig = go.Figure(data=[go.Pie(labels=alert_types, values=alert_counts)])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏱️ Response Time")
        
        response_times = ['<5 min', '5-15 min', '15-30 min', '30-60 min', '>1 hour']
        response_counts = [35, 42, 18, 8, 3]
        
        fig = go.Figure(data=[go.Bar(x=response_times, y=response_counts, marker_color='#667eea')])
        fig.update_layout(height=300, yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

def show_notification_settings():
    """Notification settings"""
    st.markdown("### 📧 Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Email Notifications")
        
        email_enabled = st.checkbox("Enable email notifications", value=True)
        
        if email_enabled:
            email_address = st.text_input("Email Address", "your@email.com")
            
            st.markdown("**Alert Levels to Email**")
            email_critical = st.checkbox("Critical alerts", value=True, key="email_crit")
            email_warning = st.checkbox("Warning alerts", value=True, key="email_warn")
            email_info = st.checkbox("Info alerts", value=False, key="email_info")
            
            digest_mode = st.checkbox("Send daily digest instead of real-time", value=False)
            
            if digest_mode:
                digest_time = st.time_input("Digest delivery time", datetime.now().time())
    
    with col2:
        st.markdown("#### Other Notification Channels")
        
        slack_enabled = st.checkbox("Slack notifications", value=False)
        if slack_enabled:
            slack_webhook = st.text_input("Slack Webhook URL", type="password")
            slack_channel = st.text_input("Channel", "#price-alerts")
        
        sms_enabled = st.checkbox("SMS notifications (critical only)", value=False)
        if sms_enabled:
            phone_number = st.text_input("Phone Number", "+1 (555) 000-0000")
        
        webhook_enabled = st.checkbox("Custom webhook", value=False)
        if webhook_enabled:
            webhook_url = st.text_input("Webhook URL", "https://your-api.com/alerts")
    
    if st.button("💾 Save Notification Settings", use_container_width=True, type="primary"):
        st.success("✅ Notification settings saved!")

def show_settings():
    """Settings and integration interface"""
    st.markdown('<p class="main-header">🛠️ Settings & Integration</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🔌 Integrations", "👤 Account", "🔐 API Keys", "⚙️ General Settings"])
    
    with tabs[0]:
        show_integrations()
    
    with tabs[1]:
        show_account_settings()
    
    with tabs[2]:
        show_api_keys()
    
    with tabs[3]:
        show_general_settings()

def show_integrations():
    """Integration settings"""
    st.markdown("### 🔌 Platform Integrations")
    
    # Shopify integration
    with st.expander("🛍️ Shopify", expanded=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**Shopify Store Integration**")
            st.caption("Sync products, prices, and inventory with your Shopify store")
            
            shopify_connected = st.checkbox("Connected", value=True, disabled=True)
            
            if shopify_connected:
                store_url = st.text_input("Store URL", "your-store.myshopify.com", disabled=True)
                st.success("✅ Connected and syncing")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Products Synced", "847")
                with col_b:
                    st.metric("Last Sync", "2 minutes ago")
        
        with col2:
            st.markdown("####")
            st.markdown("####")
            if st.button("Configure", use_container_width=True):
                st.info("Opening Shopify settings...")
            
            if st.button("Sync Now", use_container_width=True, type="primary"):
                st.success("Syncing...")
    
    # Other integrations
    integrations = [
        {"name": "WooCommerce", "icon": "🛒", "status": False},
        {"name": "Amazon Seller Central", "icon": "📦", "status": False},
        {"name": "eBay", "icon": "🏷️", "status": False},
        {"name": "BigCommerce", "icon": "🏪", "status": False},
        {"name": "Magento", "icon": "🎪", "status": False},
        {"name": "Google Shopping", "icon": "🔍", "status": True},
    ]
    
    for integration in integrations:
        with st.expander(f"{integration['icon']} {integration['name']}"):
            if integration['status']:
                st.success("✅ Connected")
                if st.button(f"Disconnect {integration['name']}", key=f"disconnect_{integration['name']}"):
                    st.warning("Disconnected")
            else:
                st.info("Not connected")
                if st.button(f"Connect {integration['name']}", key=f"connect_{integration['name']}", type="primary"):
                    st.success("Connection initiated...")

def show_account_settings():
    """Account settings"""
    st.markdown("### 👤 Account Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Profile Information")
        
        company_name = st.text_input("Company Name", "Your Company")
        contact_name = st.text_input("Contact Name", "John Doe")
        email = st.text_input("Email", "john@yourcompany.com")
        phone = st.text_input("Phone", "+1 (555) 123-4567")
    
    with col2:
        st.markdown("#### Plan & Billing")
        
        st.info("**Current Plan:** Professional")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Products", "847 / 1,000")
        with col_m2:
            st.metric("API Calls", "125K / 200K")
        
        if st.button("⬆️ Upgrade Plan", use_container_width=True):
            st.info("Opening upgrade page...")
        
        st.markdown("####")
        st.markdown("**Billing Information**")
        st.text("Next billing date: March 15, 2026")
        st.text("Amount: $199/month")
    
    if st.button("💾 Save Account Settings", use_container_width=True, type="primary"):
        st.success("✅ Settings saved!")

def show_api_keys():
    """API keys management"""
    st.markdown("### 🔐 API Keys & Webhooks")
    
    st.info("🔒 API keys allow you to integrate PriceIQ with your own applications and systems.")
    
    # Existing API keys
    st.markdown("#### Active API Keys")
    
    api_keys = [
        {"name": "Production Key", "key": "pk_live_abc123...xyz789", "created": "2025-01-15", "last_used": "2 hours ago"},
        {"name": "Development Key", "key": "pk_test_def456...uvw012", "created": "2025-02-01", "last_used": "Never"},
    ]
    
    for key_data in api_keys:
        with st.expander(f"🔑 {key_data['name']}"):
            col_k1, col_k2, col_k3 = st.columns(3)
            
            with col_k1:
                st.text(f"Key: {key_data['key']}")
                st.caption(f"Created: {key_data['created']}")
            
            with col_k2:
                st.text(f"Last used: {key_data['last_used']}")
            
            with col_k3:
                if st.button("Revoke", key=f"revoke_{key_data['name']}", type="secondary"):
                    st.warning("Key revoked")
    
    # Create new key
    st.markdown("#### Create New API Key")
    
    col_n1, col_n2 = st.columns([3, 1])
    
    with col_n1:
        new_key_name = st.text_input("Key Name", "My New Key")
        key_permissions = st.multiselect(
            "Permissions",
            ["Read Products", "Write Products", "Read Prices", "Write Prices", "Read Analytics"],
            default=["Read Products", "Read Prices"]
        )
    
    with col_n2:
        st.markdown("###")
        if st.button("🔑 Generate Key", use_container_width=True, type="primary"):
            st.success("New API key generated!")
            st.code("pk_live_new123...abc789")

def show_general_settings():
    """General application settings"""
    st.markdown("### ⚙️ General Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Display Preferences")
        
        timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT"])
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY"])
        date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        
        st.markdown("#### Dashboard Settings")
        
        default_time_range = st.selectbox("Default Time Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
        dashboard_refresh = st.selectbox("Auto-refresh interval", ["Off", "30 seconds", "1 minute", "5 minutes"])
    
    with col2:
        st.markdown("#### Data Retention")
        
        price_history_retention = st.selectbox("Price History Retention", ["30 days", "90 days", "1 year", "Forever"])
        alert_retention = st.selectbox("Alert History Retention", ["7 days", "30 days", "90 days", "1 year"])
        
        st.markdown("#### Privacy & Data")
        
        anonymize_data = st.checkbox("Anonymize exported data", value=False)
        share_analytics = st.checkbox("Share anonymized analytics with PriceIQ (helps improve service)", value=True)
    
    if st.button("💾 Save General Settings", use_container_width=True, type="primary"):
        st.success("✅ Settings saved!")

def show_product_management():
    """Product management interface"""
    st.markdown('<p class="main-header">📦 Product Management</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📋 All Products", "➕ Add Products", "🏷️ Categories", "📊 Bulk Actions"])
    
    with tabs[0]:
        show_all_products()
    
    with tabs[1]:
        show_add_products()
    
    with tabs[2]:
        show_categories()
    
    with tabs[3]:
        show_bulk_actions()

def show_all_products():
    """All products view"""
    st.markdown("### 📋 All Products")
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search products", "")
    with col2:
        category_filter = st.selectbox("Category", ["All"] + list(set([p['category'] for p in st.session_state.products])))
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Out of Stock"])
    
    # Products table
    products_data = []
    for product in st.session_state.products:
        margin = (product['current_price'] - product['cost']) / product['current_price'] * 100
        
        products_data.append({
            "SKU": product['sku'],
            "Name": product['name'],
            "Category": product['category'],
            "Price": f"${product['current_price']:.2f}",
            "Cost": f"${product['cost']:.2f}",
            "Margin": f"{margin:.1f}%",
            "Tracked": "✅",
            "Rules": random.randint(0, 3)
        })
    
    df = pd.DataFrame(products_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Bulk actions
    st.markdown("#### Quick Actions")
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        if st.button("📥 Export Products"):
            st.success("Exporting...")
    with col_b:
        if st.button("🔄 Sync from Shopify"):
            st.success("Syncing...")
    with col_c:
        if st.button("📊 Analyze All"):
            st.info("Running analysis...")
    with col_d:
        if st.button("🏷️ Edit Categories"):
            st.info("Opening editor...")

def show_add_products():
    """Add products interface"""
    st.markdown("### ➕ Add Products")
    
    method = st.radio("Add Method", ["Manual Entry", "CSV Import", "Sync from Shopify"])
    
    if method == "Manual Entry":
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input("Product Name *")
                sku = st.text_input("SKU *")
                category = st.selectbox("Category", ["Electronics", "Audio", "Accessories", "Other"])
            
            with col2:
                current_price = st.number_input("Current Price *", 0.0, 100000.0, 0.0, step=10.0)
                cost = st.number_input("Cost *", 0.0, 100000.0, 0.0, step=10.0)
                
            start_tracking = st.checkbox("Start tracking competitors immediately", value=True)
            
            if st.form_submit_button("➕ Add Product", use_container_width=True, type="primary"):
                st.success(f"✅ Product '{product_name}' added successfully!")
    
    elif method == "CSV Import":
        st.markdown("#### 📄 CSV Import")
        
        st.info("Upload a CSV file with columns: name, sku, category, current_price, cost")
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
        
        if uploaded_file:
            st.success("File uploaded! Preview:")
            # Would show CSV preview here
            
            if st.button("📥 Import Products", use_container_width=True, type="primary"):
                st.success("✅ Imported 25 products successfully!")
    
    else:  # Sync from Shopify
        st.markdown("#### 🛍️ Sync from Shopify")
        
        if st.button("🔄 Sync All Products from Shopify", use_container_width=True, type="primary"):
            with st.spinner("Syncing from Shopify..."):
                st.success("✅ Synced 847 products from Shopify!")

def show_categories():
    """Categories management"""
    st.markdown("### 🏷️ Product Categories")
    
    categories = list(set([p['category'] for p in st.session_state.products]))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Current Categories")
        
        for category in categories:
            count = len([p for p in st.session_state.products if p['category'] == category])
            
            col_c1, col_c2, col_c3 = st.columns([3, 1, 1])
            
            with col_c1:
                st.text(f"📁 {category}")
            with col_c2:
                st.caption(f"{count} products")
            with col_c3:
                if st.button("Edit", key=f"edit_cat_{category}"):
                    st.info("Editing...")
    
    with col2:
        st.markdown("#### Add Category")
        
        new_category = st.text_input("Category Name")
        
        if st.button("➕ Add Category", use_container_width=True):
            st.success(f"Category '{new_category}' added!")

def show_bulk_actions():
    """Bulk actions on products"""
    st.markdown("### 📊 Bulk Actions")
    
    st.markdown("#### Select Products")
    
    all_products = st.checkbox("Select all products")
    
    if not all_products:
        selected_products = st.multiselect("Choose products", [p['name'] for p in st.session_state.products])
    else:
        selected_products = [p['name'] for p in st.session_state.products]
    
    st.info(f"Selected: {len(selected_products)} products")
    
    # Bulk actions
    st.markdown("#### Choose Action")
    
    action = st.selectbox("Bulk Action", [
        "Update Prices",
        "Apply Pricing Rule",
        "Change Category",
        "Enable/Disable Tracking",
        "Export Selection",
        "Delete Products"
    ])
    
    if action == "Update Prices":
        col_u1, col_u2 = st.columns(2)
        
        with col_u1:
            update_type = st.radio("Update Type", ["Increase by %", "Decrease by %", "Set to value"])
        
        with col_u2:
            if "by %" in update_type:
                percentage = st.number_input("Percentage", 1, 100, 10)
            else:
                new_price = st.number_input("New Price", 0.0, 10000.0, 100.0)
    
    elif action == "Apply Pricing Rule":
        rule_to_apply = st.selectbox("Select Rule", [f"Rule #{r['id']}" for r in st.session_state.dynamic_pricing_rules])
    
    elif action == "Change Category":
        new_category = st.selectbox("New Category", ["Electronics", "Audio", "Accessories"])
    
    if st.button("🚀 Execute Bulk Action", use_container_width=True, type="primary"):
        with st.spinner("Processing..."):
            st.success(f"✅ Bulk action completed on {len(selected_products)} products!")

# Main content area - Navigation logic
if page == "📊 Dashboard":
    show_dashboard()
elif page == "🔍 Competitor Tracking":
    show_competitor_tracking()
elif page == "⚡ Dynamic Pricing":
    show_dynamic_pricing()
elif page == "📈 Analytics & Reports":
    show_analytics()
elif page == "🚨 Alerts & Monitoring":
    show_alerts()
elif page == "🛠️ Settings & Integration":
    show_settings()
elif page == "📦 Product Management":
    show_product_management()

# Run the app
if __name__ == "__main__":
    pass