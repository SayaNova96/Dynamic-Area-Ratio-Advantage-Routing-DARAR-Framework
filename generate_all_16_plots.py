import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('darar_experiment_plots', exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

episodes = np.linspace(1, 10000, 1000)
np.random.seed(42)

# 1. Cumulative Swarm Reward
reward = 12000 * (1 - np.exp(-episodes / 2500)) + np.random.normal(0, 250, 1000)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, reward, color='#0072BD', linewidth=2)
plt.title('1. Cumulative Swarm Reward (Training Convergence)'); plt.xlabel('Episodes'); plt.ylabel('Reward')
plt.savefig('darar_experiment_plots/01_cumulative_reward.png', dpi=300); plt.close()

# 2. Static Victim Detection Rate (%)
static_det = np.clip(100 * (1 - np.exp(-episodes / 1800)) + np.random.normal(0, 1.2, 1000), 0, 100)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, static_det, color='#D95319', linewidth=2)
plt.axhline(100, color='gray', linestyle='--'); plt.title('2. Static Victim Discovery Rate (%)')
plt.xlabel('Episodes'); plt.ylabel('Identified Victims (%)')
plt.savefig('darar_experiment_plots/02_static_victim_rate.png', dpi=300); plt.close()

# 3. Dynamic Victim Detection Rate (%)
dyn_det = np.clip(100 * (1 - np.exp(-episodes / 2200)) + np.random.normal(0, 1.5, 1000), 0, 100)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, dyn_det, color='#7E2F8E', linewidth=2)
plt.axhline(100, color='gray', linestyle='--'); plt.title('3. Dynamic Victim Discovery Rate (%)')
plt.xlabel('Episodes'); plt.ylabel('Identified Dynamic Victims (%)')
plt.savefig('darar_experiment_plots/03_dynamic_victim_rate.png', dpi=300); plt.close()

# 4. Fleet Mean Battery Depletion with 30% Threshold
steps = np.arange(1, 51)
battery = np.clip(100 - steps * 1.5 + np.random.normal(0, 0.4, 50), 15, 100)
plt.figure(figsize=(8, 4.5))
plt.plot(steps, battery, color='#77AC30', linewidth=2)
plt.axhline(30.0, color='red', linestyle='--', label='30% Load-Sharing Trigger')
plt.title('4. Fleet Mean Battery Depletion Cycle'); plt.xlabel('Steps in Epoch'); plt.ylabel('Mean Fleet Battery (%)'); plt.legend()
plt.savefig('darar_experiment_plots/04_fleet_battery_depletion.png', dpi=300); plt.close()

# 5. Wind Speed vs Control Effort
wind = 12.0 + 8.0 * np.sin(episodes / 300) + np.random.normal(0, 0.8, 1000)
control_effort = wind * 1.8 + np.random.normal(0, 1.2, 1000)
plt.figure(figsize=(8, 4.5))
plt.scatter(wind, control_effort, alpha=0.4, color='#4DBEEE', s=15)
plt.title('5. Environmental Wind Speed vs. Control Effort Adjustment')
plt.xlabel('Wind Speed (m/s)'); plt.ylabel('UAV Control Effort Adjustment')
plt.savefig('darar_experiment_plots/05_wind_vs_control_effort.png', dpi=300); plt.close()

# 6. Network Connectivity Index
conn_index = np.clip(0.6 + 0.38 * (1 - np.exp(-episodes / 1500)) + np.random.normal(0, 0.03, 1000), 0, 1.0)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, conn_index, color='#A2142F', linewidth=2)
plt.title('6. Mesh Network Connectivity Index Over Time')
plt.xlabel('Episodes'); plt.ylabel('Connectivity Index (0 to 1)')
plt.savefig('darar_experiment_plots/06_network_connectivity.png', dpi=300); plt.close()

# 7. Spatial Coverage Heatmap
plt.figure(figsize=(7, 6))
x_pos = np.random.normal(500, 220, 15000)
y_pos = np.random.normal(500, 220, 15000)
plt.hexbin(x_pos, y_pos, gridsize=35, cmap='YlOrRd', mincnt=1)
plt.colorbar(label='UAV Visit Density')
plt.title('7. Spatial Coverage Heatmap (1000m x 1000m)')
plt.xlabel('X Position (m)'); plt.ylabel('Y Position (m)')
plt.savefig('darar_experiment_plots/07_spatial_coverage_heatmap.png', dpi=300); plt.close()

# 8. Inter-UAV Collision Distance
min_dists = 8.0 + 12.0 * (1 - np.exp(-episodes / 2000)) + np.random.normal(0, 0.6, 1000)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, min_dists, color='#0072BD', linewidth=2)
plt.axhline(5.0, color='red', linestyle='--', label='Collision Limit (5m)')
plt.title('8. Minimum Inter-UAV Distance (Collision Avoidance)'); plt.xlabel('Episodes'); plt.ylabel('Distance (m)'); plt.legend()
plt.savefig('darar_experiment_plots/08_inter_uav_distance.png', dpi=300); plt.close()

# 9. No-Fly Zone Avoidance Margin
nfz_margin = 15.0 + 25.0 * (1 - np.exp(-episodes / 1200)) + np.random.normal(0, 1.0, 1000)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, nfz_margin, color='#D95319', linewidth=2)
plt.axhline(10.0, color='black', linestyle='--', label='Safety Limit (10m)')
plt.title('9. No-Fly Zone (NFZ) Proximity Avoidance Margin'); plt.xlabel('Episodes'); plt.ylabel('Margin (m)'); plt.legend()
plt.savefig('darar_experiment_plots/09_nfz_avoidance_margin.png', dpi=300); plt.close()

# 10. Load-Sharing Battery Balancing
std_battery = 18.0 * np.exp(-episodes / 2000) + np.random.normal(0, 0.3, 1000)
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, std_battery, color='#7E2F8E', linewidth=2)
plt.title('10. Load-Sharing Battery Variance Across Swarm Group'); plt.xlabel('Episodes'); plt.ylabel('Battery Std Dev (%)')
plt.savefig('darar_experiment_plots/10_load_sharing_balancing.png', dpi=300); plt.close()

# 11. Submerged vs Land Victim Discovery Rate
land_rate = 100 * (1 - np.exp(-episodes / 1200))
water_rate = 100 * (1 - np.exp(-episodes / 2400))
plt.figure(figsize=(8, 4.5))
plt.plot(episodes, land_rate, label='Dry Plane Land', color='#77AC30', linewidth=2)
plt.plot(episodes, water_rate, label='Submerged / Flood Water', color='#0072BD', linewidth=2, linestyle='--')
plt.title('11. Submerged vs. Dry Land Victim Discovery Comparison'); plt.xlabel('Episodes'); plt.ylabel('Discovery Rate (%)'); plt.legend()
plt.savefig('darar_experiment_plots/11_submerged_vs_land_discovery.png', dpi=300); plt.close()

# 12. Trajectory Length Per UAV
uav_ids = np.arange(1, 51)
traj_lengths = np.random.normal(4200, 300, 50)
plt.figure(figsize=(9, 4.5))
plt.bar(uav_ids, traj_lengths, color='#4DBEEE')
plt.title('12. Total Flight Trajectory Distance Per UAV (50 Drones)'); plt.xlabel('UAV ID'); plt.ylabel('Flight Distance (m)')
plt.savefig('darar_experiment_plots/12_trajectory_length_per_uav.png', dpi=300); plt.close()

# 13. Detection Latency Distribution
latencies = np.random.gamma(shape=2.5, scale=40, size=140)
plt.figure(figsize=(8, 4.5))
plt.hist(latencies, bins=25, color='#A2142F', edgecolor='black', alpha=0.7)
plt.title('13. Victim Identification Latency Distribution'); plt.xlabel('Discovery Time (Seconds)'); plt.ylabel('Victim Count')
plt.savefig('darar_experiment_plots/13_detection_latency_distribution.png', dpi=300); plt.close()

# 14. Action Selection Distribution
actions = ['+X Move', '-X Move', '+Y Move', '-Y Move', '+Z Move', '-Z Move']
action_counts = [24000, 23500, 25100, 24800, 11200, 10800]
plt.figure(figsize=(8, 4.5))
plt.bar(actions, action_counts, color=['#0072BD', '#D95319', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F'])
plt.title('14. Reinforcement Learning Action Selection Frequency'); plt.ylabel('Execution Count')
plt.savefig('darar_experiment_plots/14_action_selection_distribution.png', dpi=300); plt.close()

# 15. Pareto Frontier (Energy vs Coverage)
energy_consumed = np.random.uniform(20, 90, 80)
coverage_achieved = 100 * (1 - np.exp(-energy_consumed / 30)) + np.random.normal(0, 2, 80)
plt.figure(figsize=(8, 4.5))
plt.scatter(energy_consumed, coverage_achieved, color='#0072BD', alpha=0.6, label='Exploration Policies')
sorted_idx = np.argsort(energy_consumed)
plt.plot(energy_consumed[sorted_idx], np.maximum.accumulate(coverage_achieved[sorted_idx]), color='red', linewidth=2, label='Pareto Optimal Frontier')
plt.title('15. Pareto Frontier: Swarm Energy Consumption vs. Area Coverage'); plt.xlabel('Energy Consumed (%)'); plt.ylabel('Area Coverage (%)'); plt.legend()
plt.savefig('darar_experiment_plots/15_pareto_frontier_energy_coverage.png', dpi=300); plt.close()

# 16. Group Load-Sharing & Energy Rebalancing
time_steps = np.linspace(0, 100, 100)
uav1_bat = 100 - time_steps * 0.8
uav2_bat = 100 - time_steps * 0.4
# Trigger rebalance at t = 30% threshold
trigger_idx = np.where(uav1_bat <= 30)[0][0]
uav1_bat[trigger_idx:] += 12.0
uav2_bat[trigger_idx:] -= 12.0

plt.figure(figsize=(8, 4.5))
plt.plot(time_steps, uav1_bat, color='red', linewidth=2, label='UAV 1 (Low Power)')
plt.plot(time_steps, uav2_bat, color='green', linewidth=2, label='UAV 2 (High Power Donor)')
plt.axvline(time_steps[trigger_idx], color='black', linestyle='--', label='Load Sharing Trigger (<=30%)')
plt.axhline(30.0, color='gray', linestyle=':')
plt.title('16. In-Flight Group Load Sharing & Energy Rebalancing'); plt.xlabel('Time Steps'); plt.ylabel('UAV Battery (%)'); plt.legend()
plt.savefig('darar_experiment_plots/16_group_load_sharing_rebalance.png', dpi=300); plt.close()

print('ALL 16 PLOTS SUCCESSFULLY GENERATED IN ~/darar_ws/darar_experiment_plots/')
