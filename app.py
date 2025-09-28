import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# Load Data
# --------------------------
@st.cache_data
def load_data():
    return pd.read_csv("OLA_DataSet.csv")  # Changed to CSV

df = load_data()

# --------------------------
# Sidebar Navigation with image on top
# --------------------------
st.sidebar.image("OLA pic.png", use_container_width=True)
page = st.sidebar.radio("Navigation", ["Home", "SQL Queries", "Visualisation", "About Creator"])

# --------------------------
# Common Title on every page
# --------------------------
st.markdown(
    """
    <div style='background-color:#7AC142; padding:10px; border-radius:5px'>
        <h1 style='color:white; text-align:center;'>OLA Rides Analysis Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Page-specific dark background colors
# --------------------------
if page == "Home":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0B2545; color: white; }
        </style>
        """, unsafe_allow_html=True
    )

elif page == "SQL Queries":
    st.markdown(
        """
        <style>
        .stApp { background-color: #1A1A2E; color: white; }
        label[for="selectbox"] { color: red; font-weight: bold; }
        div.stButton > button, div.stDownloadButton > button {
            background-color: #7AC142; color: white; font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True
    )

# --------------------------
# Home Page
# --------------------------
if page == "Home":
    st.write(
        """
        Welcome to the OLA Rides Analysis Dashboard!  

        This interactive dashboard is designed to help users analyze OLA ride data efficiently.  
        Explore insights about ride bookings, cancellations, and ratings to understand customer and driver behavior.  
        Visualize ride distances, payment methods, and vehicle usage trends.  
        Check top customers and track incomplete rides with their reasons.  
        Gain real-time understanding of cancellations by drivers and customers.  
        Evaluate the performance of drivers using ratings and other metrics.  
        Navigate through the sections using the sidebar to discover SQL-like queries, interactive visualizations, and detailed insights.
        """
    )

# --------------------------
# SQL Queries Page
# --------------------------
elif page == "SQL Queries":
    st.title("📊 Queries (Pandas Implementation)")

    query_options = {
        "1. Retrieve all successful bookings": lambda: df[df["Booking_Status"] == "Success"],
        "2. Find average ride distance per vehicle type": lambda: df.groupby("Vehicle_Type")["Ride_Distance"].mean().round(2).reset_index(),
        "3. Total number of cancelled rides by customers": lambda: pd.DataFrame({"cancelled_by_customers": [df["Canceled_Rides_by_Customer"].notna().sum()]}),
        "4. Top 5 customers with highest rides": lambda: df.groupby("Customer_ID").size().reset_index(name="total_rides").nlargest(5, "total_rides"),
        "5. Rides cancelled by drivers due to Personal & Car issues": lambda: pd.DataFrame({"total_personal_car_issues": [(df["Canceled_Rides_by_Driver"] == "Personal & Car related issue").sum()]}),
        "6. Max & Min driver ratings for Prime Sedan": lambda: df[df["Vehicle_Type"] == "Prime Sedan"]["Driver_Ratings"].agg(["max", "min"]).reset_index(),
        "7. Rides with UPI payment": lambda: df[df["Payment_Method"] == "UPI"],
        "8. Average customer rating per vehicle type": lambda: df.groupby("Vehicle_Type")["Customer_Rating"].mean().round(2).reset_index(),
        "9. Total booking value of successful rides": lambda: pd.DataFrame({"total_booking_value": [df.loc[df["Booking_Status"] == "Success", "Booking_Value"].sum()]}),
        "10. All incomplete rides with reason": lambda: df[df["Incomplete_Rides_Reason"].notna() & (df["Incomplete_Rides_Reason"] != "")]
    }

    st.markdown('<p style="color:red; font-weight:bold;">Choose a Query</p>', unsafe_allow_html=True)
    selected_query = st.selectbox("", list(query_options.keys()))

    if st.button("Generate"):
        result = query_options[selected_query]()
        st.dataframe(result)

        csv = result.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results", csv, "query_results.csv", "text/csv")

# --------------------------
# Visualisation Page
# --------------------------
elif page == "Visualisation":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0B2545; color: white; }
        div.stButton > button {
            background-color: #7AC142; color: white; font-weight: bold;
        }
        div[data-baseweb="select"] > div { color: #7AC142 !important; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True
    )

    st.title("📈 Interactive Visualisation of OLA Rides")

    # Category Selection
    st.markdown('<p style="color:red; font-weight:bold;">Category</p>', unsafe_allow_html=True)
    main_category = st.selectbox("", ["Revenue", "Cancellation", "Rating", "Vehicle Type", "Payment Method"])

    # Sub-Category Selection
    sub_options = []
    if main_category == "Revenue":
        sub_options = ["Total Revenue", "Revenue by Vehicle Type", "Revenue by Payment Method"]
    elif main_category == "Cancellation":
        sub_options = ["Driver Cancellations", "Customer Cancellations", "All Cancellations"]
    elif main_category == "Rating":
        sub_options = ["Driver Ratings", "Customer Ratings", "Average Rating by Vehicle Type"]
    elif main_category == "Vehicle Type":
        sub_options = df["Vehicle_Type"].dropna().unique().tolist()
    elif main_category == "Payment Method":
        sub_options = ["All", "Cash", "UPI", "Credit Card", "Debit Card"]

    st.markdown('<p style="color:red; font-weight:bold;">Select Analysis Filter</p>', unsafe_allow_html=True)
    sub_category = st.selectbox("", sub_options)

    if st.button("Generate"):
        driver_cancel = df["Canceled_Rides_by_Driver"].notna().sum()
        customer_cancel = df["Canceled_Rides_by_Customer"].notna().sum()

        if main_category == "Revenue":
            if sub_category == "Total Revenue":
                total_revenue = df["Booking_Value"].sum()
                st.markdown(f"<h3 style='color:red;'>Total Revenue: ₹ {total_revenue:,.2f}</h3>", unsafe_allow_html=True)

            elif sub_category == "Revenue by Vehicle Type":
                data = df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
                fig = px.bar(data, x="Vehicle_Type", y="Booking_Value", text_auto=True,
                             color="Booking_Value", color_continuous_scale="darkmint",
                             title="Revenue by Vehicle Type")
                st.plotly_chart(fig, use_container_width=True)

            elif sub_category == "Revenue by Payment Method":
                data = df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
                data = data[data["Payment_Method"].notna()]
                fig = px.pie(data, values="Booking_Value", names="Payment_Method", hole=0.4,
                             title="Revenue by Payment Method",
                             color_discrete_sequence=px.colors.qualitative.Dark2)
                fig.update_traces(textinfo="label+percent+value")
                st.plotly_chart(fig, use_container_width=True)

        elif main_category == "Cancellation":
            if sub_category == "Driver Cancellations":
                st.markdown(f"<h3 style='color:red;'>Driver Cancellations: {driver_cancel}</h3>", unsafe_allow_html=True)

            elif sub_category == "Customer Cancellations":
                st.markdown(f"<h3 style='color:red;'>Customer Cancellations: {customer_cancel}</h3>", unsafe_allow_html=True)

            elif sub_category == "All Cancellations":
                vals = [driver_cancel, customer_cancel]
                fig = px.pie(values=vals, names=["Driver", "Customer"], hole=0.3,
                             title="Overall Cancellations",
                             color_discrete_sequence=px.colors.qualitative.Dark2)
                fig.update_traces(textinfo="label+percent+value")
                st.plotly_chart(fig, use_container_width=True)

        elif main_category == "Rating":
            if sub_category == "Driver Ratings":
                fig = px.histogram(df, x="Driver_Ratings", nbins=10, text_auto=True,
                                   title="Driver Ratings Distribution",
                                   color_discrete_sequence=["#8E44AD"])
                st.plotly_chart(fig, use_container_width=True)

            elif sub_category == "Customer Ratings":
                fig = px.histogram(df, x="Customer_Rating", nbins=10, text_auto=True,
                                   title="Customer Ratings Distribution",
                                   color_discrete_sequence=["#16A085"])
                st.plotly_chart(fig, use_container_width=True)

            elif sub_category == "Average Rating by Vehicle Type":
                data = df.groupby("Vehicle_Type")["Customer_Rating"].mean().reset_index()
                fig = px.bar(data, x="Vehicle_Type", y="Customer_Rating", text_auto=True,
                             title="Average Customer Rating by Vehicle Type",
                             color="Customer_Rating", color_continuous_scale="deep")
                st.plotly_chart(fig, use_container_width=True)

        elif main_category == "Vehicle Type":
            filtered = df[df["Vehicle_Type"] == sub_category].groupby("Booking_Status").size().reset_index(name="count")
            if len(filtered) == 1:
                count = int(filtered["count"].iloc[0])
                st.markdown(f"<h3 style='color:red;'>{sub_category} - Total Count: {count}</h3>", unsafe_allow_html=True)
            else:
                fig = px.line(filtered, x="Booking_Status", y="count", markers=True,
                              title=f"{sub_category} Booking Status Trend",
                              color_discrete_sequence=px.colors.qualitative.Dark24)
                fig.update_traces(text=filtered["count"], textposition="top center")
                fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

        elif main_category == "Payment Method":
            df_payment = df.dropna(subset=["Payment_Method"])
            if sub_category != "All":
                count = df_payment[df_payment["Payment_Method"] == sub_category].shape[0]
                st.markdown(f"<h3 style='color:red;'>{sub_category} Payments: {count}</h3>", unsafe_allow_html=True)
            else:
                fig = px.pie(df_payment, names="Payment_Method", title="Payment Method Distribution",
                             color_discrete_sequence=px.colors.qualitative.Dark2)
                fig.update_traces(textinfo="label+percent+value")
                st.plotly_chart(fig, use_container_width=True)

# --------------------------
# About Creator Page
# --------------------------
elif page == "About Creator":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0B2545; color: white; }
        </style>
        """, unsafe_allow_html=True
    )

    st.write(
        """
        ## 👨‍💻 About the Creator  

        **Created by:** Nithish Rexson  
        **Current Project:** OLA Ride Data Analysis Dashboard  
        🔹 Provides real-time insights into **bookings, cancellations, revenues, and customer/driver ratings** using Streamlit, Pandas, and Plotly.  

        **Previous Projects:**  
        - ✈️ **Flight Delay Analysis (SQL + Power BI)** – Analyzed **US flight delays, cancellations, and airline performance** with KPI dashboards.  
        - 🏏 **Cricbuzz Matches Dashboard (Streamlit + Plotly)** – Built an **interactive cricket analysis tool** to visualize match insights, team stats, and player performance.  
        - 🍴 **Food Waste Management System** – Designed a **solution to track, reduce, and optimize food waste** through proper data collection and allocation.  

        These projects highlight expertise in **data preprocessing, analytics, dashboard creation, and problem-solving** across multiple domains.  
        """
    )
