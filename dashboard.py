import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# PAGE SETTINGS
# ------------------------------
st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")

st.title("🚦 SMART TRAFFIC CONTROL DASHBOARD")
st.markdown("### Fixed-Time vs Smart-Time Traffic Control Monitoring System")

# ------------------------------
# LOAD CSV FILES
# ------------------------------
fixed_df = pd.read_csv("final_fixed_time_report.csv")
smart_df = pd.read_csv("final_smart_time_report.csv")
summary_df = pd.read_csv("final_comparison_summary.csv")

# ------------------------------
# KPI VALUES
# ------------------------------
fixed_avg_wait = float(summary_df.loc[0, "Average Waiting Cars"])
smart_avg_wait = float(summary_df.loc[1, "Average Waiting Cars"])

fixed_throughput = float(summary_df.loc[0, "Throughput (Cars/Cycle)"])
smart_throughput = float(summary_df.loc[1, "Throughput (Cars/Cycle)"])

if fixed_avg_wait > 0:
    improvement = ((fixed_avg_wait - smart_avg_wait) / fixed_avg_wait) * 100
else:
    improvement = 0

# ------------------------------
# KPI CARDS
# ------------------------------
st.subheader("📌 Key Performance Indicators (KPI)")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🚗 Fixed Avg Waiting", round(fixed_avg_wait, 2))
col2.metric("🧠 Smart Avg Waiting", round(smart_avg_wait, 2))
col3.metric("🚦 Fixed Throughput", round(fixed_throughput, 2))
col4.metric("⚡ Smart Throughput", round(smart_throughput, 2))
col5.metric("✅ Improvement", f"{round(improvement, 2)}%")

st.divider()

# ------------------------------
# SELECT CYCLE
# ------------------------------
st.subheader("🔄 Live Cycle Monitoring")

max_cycle = int(fixed_df["Cycle"].max())
selected_cycle = st.slider("Select Cycle", 1, max_cycle, 1)

fixed_cycle_data = fixed_df[fixed_df["Cycle"] == selected_cycle]
smart_cycle_data = smart_df[smart_df["Cycle"] == selected_cycle]

# ------------------------------
# EMERGENCY ALERT
# ------------------------------
emergency_intersection = smart_cycle_data.iloc[0]["Emergency_Intersection"]
emergency_lane = smart_cycle_data.iloc[0]["Emergency_Lane"]

if emergency_intersection != "NONE":
    st.error(f"🚑 EMERGENCY DETECTED at Intersection {emergency_intersection} ({emergency_lane} Lane)")
else:
    st.success("✅ No Emergency Vehicle Detected in this Cycle")

st.divider()

# ------------------------------
# INTERSECTION STATUS TABLES
# ------------------------------
st.subheader("📍 Intersection Status Table (Selected Cycle)")

colA, colB = st.columns(2)

with colA:
    st.markdown("### 🚦 Fixed-Time System")
    st.dataframe(
        fixed_cycle_data[[
            "Intersection", "NS_Density", "EW_Density",
            "NS_Green", "EW_Green", "Cars_Passed", "Cars_Waiting"
        ]],
        use_container_width=True
    )

with colB:
    st.markdown("### 🧠 Smart-Time System")
    st.dataframe(
        smart_cycle_data[[
            "Intersection", "NS_Density", "EW_Density",
            "NS_Green", "EW_Green", "Cars_Passed", "Cars_Waiting"
        ]],
        use_container_width=True
    )

st.divider()

# ------------------------------
# CONGESTION WARNING SYSTEM
# ------------------------------
st.subheader("⚠ Congestion Warning System")

fixed_total_waiting = fixed_cycle_data["Cars_Waiting"].sum()
smart_total_waiting = smart_cycle_data["Cars_Waiting"].sum()

col1, col2 = st.columns(2)

with col1:
    if fixed_total_waiting > 150:
        st.warning(f"🚨 Fixed-Time Congestion HIGH ({fixed_total_waiting} waiting cars)")
    elif fixed_total_waiting > 80:
        st.info(f"⚠ Fixed-Time Congestion MEDIUM ({fixed_total_waiting} waiting cars)")
    else:
        st.success(f"✅ Fixed-Time Congestion LOW ({fixed_total_waiting} waiting cars)")

with col2:
    if smart_total_waiting > 150:
        st.warning(f"🚨 Smart-Time Congestion HIGH ({smart_total_waiting} waiting cars)")
    elif smart_total_waiting > 80:
        st.info(f"⚠ Smart-Time Congestion MEDIUM ({smart_total_waiting} waiting cars)")
    else:
        st.success(f"✅ Smart-Time Congestion LOW ({smart_total_waiting} waiting cars)")

st.divider()

# ------------------------------
# GRAPH 1: AVG WAITING TREND
# ------------------------------
st.subheader("📉 Average Waiting Cars Trend (All Cycles)")

fixed_avg_cycle = fixed_df.groupby("Cycle")["Cars_Waiting"].mean()
smart_avg_cycle = smart_df.groupby("Cycle")["Cars_Waiting"].mean()

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(fixed_avg_cycle.index, fixed_avg_cycle.values, marker="o", label="Fixed-Time")
ax1.plot(smart_avg_cycle.index, smart_avg_cycle.values, marker="s", label="Smart-Time")
ax1.axvline(selected_cycle, linestyle="--", label="Selected Cycle")

ax1.set_title("Fixed vs Smart System (Average Waiting Cars per Cycle)")
ax1.set_xlabel("Cycle")
ax1.set_ylabel("Avg Waiting Cars")
ax1.grid(True)
ax1.legend()

st.pyplot(fig1)

# ------------------------------
# GRAPH 2: THROUGHPUT TREND
# ------------------------------
st.subheader("📈 Throughput Trend (Cars Passed per Cycle)")

fixed_passed_cycle = fixed_df.groupby("Cycle")["Cars_Passed"].sum()
smart_passed_cycle = smart_df.groupby("Cycle")["Cars_Passed"].sum()

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(fixed_passed_cycle.index, fixed_passed_cycle.values, marker="o", label="Fixed-Time")
ax2.plot(smart_passed_cycle.index, smart_passed_cycle.values, marker="s", label="Smart-Time")
ax2.axvline(selected_cycle, linestyle="--", label="Selected Cycle")

ax2.set_title("Traffic Flow Efficiency (Cars Passed per Cycle)")
ax2.set_xlabel("Cycle")
ax2.set_ylabel("Cars Passed")
ax2.grid(True)
ax2.legend()

st.pyplot(fig2)

# ------------------------------
# GRAPH 3: INTERSECTION CONGESTION BAR
# ------------------------------
st.subheader("📊 Intersection Congestion Comparison (Selected Cycle)")

fixed_waiting = fixed_cycle_data.set_index("Intersection")["Cars_Waiting"]
smart_waiting = smart_cycle_data.set_index("Intersection")["Cars_Waiting"]

bar_df = pd.DataFrame({
    "Fixed-Time": fixed_waiting,
    "Smart-Time": smart_waiting
})

st.bar_chart(bar_df)

st.divider()

# ------------------------------
# EMERGENCY LOG TABLE
# ------------------------------
st.subheader("🚑 Emergency Vehicle Log")

emergency_log = smart_df[smart_df["Emergency_Intersection"] != "NONE"]

if len(emergency_log) > 0:
    st.dataframe(
        emergency_log[[
            "Cycle", "Intersection",
            "Emergency_Intersection", "Emergency_Lane",
            "NS_Green", "EW_Green"
        ]],
        use_container_width=True
    )
else:
    st.success("✅ No emergency events occurred during the simulation.")