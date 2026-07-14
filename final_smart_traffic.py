import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# 2x2 Grid Intersections
grid = {
    "A": {"NS": 0, "EW": 0},
    "B": {"NS": 0, "EW": 0},
    "C": {"NS": 0, "EW": 0},
    "D": {"NS": 0, "EW": 0}
}

base_green = 5
max_green = 15

# Store data for CSV
data = []

# Simulation cycles
for cycle in range(20):

    print("\n===============================")
    print("FINAL SMART TRAFFIC CYCLE:", cycle + 1)
    print("===============================")

    # Step 1: Generate random traffic
    for inter in grid:
        ns_new = random.randint(0, 6)
        ew_new = random.randint(0, 6)

        grid[inter]["NS"] += ns_new
        grid[inter]["EW"] += ew_new

    # Step 2: Emergency Detection
    emergency_intersection = random.choice(["NONE", "A", "B", "C", "D", "NONE", "NONE"])

    if emergency_intersection != "NONE":
        emergency_lane = random.choice(["NS", "EW"])
    else:
        emergency_lane = "NONE"

    print("🚑 Emergency Intersection:", emergency_intersection, " Lane:", emergency_lane)

    # Step 3: Green Wave Synchronization
    if cycle % 2 == 0:
        green_wave_group = ["A", "B"]
    else:
        green_wave_group = ["C", "D"]

    print("🌊 Green Wave Group:", green_wave_group)

    # Step 4: Signal Timing + Vehicle Passing
    for inter in grid:

        ns_cars = grid[inter]["NS"]
        ew_cars = grid[inter]["EW"]

        # Emergency Priority
        if inter == emergency_intersection:
            if emergency_lane == "NS":
                ns_green = 20
                ew_green = 3
            else:
                ns_green = 3
                ew_green = 20

        # Green Wave Priority
        elif inter in green_wave_group:
            ns_green = max_green
            ew_green = base_green

        # Normal Density Based Timing
        else:
            total = ns_cars + ew_cars
            if total == 0:
                ns_green = base_green
                ew_green = base_green
            else:
                ns_green = int((ns_cars / total) * max_green)
                ew_green = int((ew_cars / total) * max_green)

                if ns_green < base_green:
                    ns_green = base_green
                if ew_green < base_green:
                    ew_green = base_green

        # Cars Passing
        ns_passed = min(ns_cars, ns_green)
        ew_passed = min(ew_cars, ew_green)

        grid[inter]["NS"] -= ns_passed
        grid[inter]["EW"] -= ew_passed

        # Print status
        print(f"\nIntersection {inter}")
        print(f"Waiting Cars -> NS:{ns_cars} EW:{ew_cars}")
        print(f"Green Time -> NS:{ns_green}s EW:{ew_green}s")
        print(f"Cars Passed -> NS:{ns_passed} EW:{ew_passed}")
        print(f"Remaining -> NS:{grid[inter]['NS']} EW:{grid[inter]['EW']}")

        # Save data
        data.append([
            cycle + 1,
            inter,
            ns_cars,
            ew_cars,
            ns_green,
            ew_green,
            emergency_intersection,
            emergency_lane
        ])

    time.sleep(1)

print("\n✅ Simulation Finished! Saving CSV...")

# Save to CSV
df = pd.DataFrame(data, columns=[
    "Cycle", "Intersection", "NS_Density", "EW_Density",
    "NS_Green", "EW_Green", "Emergency_Intersection", "Emergency_Lane"
])

df.to_csv("final_traffic_report.csv", index=False)

print("✅ Data saved as final_traffic_report.csv")

# Visualization (Average density per cycle)
avg_ns = df.groupby("Cycle")["NS_Density"].mean()
avg_ew = df.groupby("Cycle")["EW_Density"].mean()

plt.plot(avg_ns.index, avg_ns.values, label="Average NS Density")
plt.plot(avg_ew.index, avg_ew.values, label="Average EW Density")

plt.title("Average Traffic Density Over Time (Grid System)")
plt.xlabel("Cycle")
plt.ylabel("Average Density")
plt.legend()
plt.grid(True)

plt.show()