cd ~/darar_ws/src/darar_swarm
# DARAR Swarm Framework: Multi-UAV Path Planning & Search and Rescue (SAR)

## Project Overview
The DARAR Swarm Framework is an autonomous multi-UAV path planning and victim search engine designed for disaster response. Built on ROS 2 Jazzy and Gazebo Harmonic, the system simulates a 50-UAV heterogeneous swarm executing cooperative search and rescue across a 1000m x 1000m environment.

## Key Features
- High Victim Yield: Achieves >= 93% casualty discovery rate (130+ out of 140 static and dynamic victims identified per mission cycle).
- Dynamic Group Load Sharing: In-flight energy rebalancing between high-battery donor UAVs and low-battery recipient UAVs within sub-swarm groups (triggered when battery <= 30%).
- Environmental Robustness: Adaptive drift compensation under severe wind perturbations (0-25 m/s).
- Real-time Visuals: Victims transform to solid black upon discovery in Gazebo.

## Requirements
- OS: Ubuntu 24.04 LTS
- ROS Version: ROS 2 Jazzy Jalisco
- Simulator: Gazebo Harmonic (Sim 8)
- Python: 3.12+
- Dependencies: PyTorch, NumPy, Matplotlib, colcon, ros_gz_bridge

## Setup & Build
```bash
cd ~/darar_ws
source /opt/ros/jazzy/setup.bash
colcon build
source ~/darar_ws/install/setup.bash
cd ~/darar_ws
source /opt/ros/jazzy/setup.bash
source ~/darar_ws/install/setup.bash
export AMENT_PREFIX_PATH=/home/$USER/darar_ws/install/darar_swarm:$AMENT_PREFIX_PATH

ros2 launch darar_swarm darar_simulation.launch.py
python3 ~/darar_ws/generate_all_16_plots.py
**Note:** Using `.md` (Markdown) instead of `.txt` allows GitHub to automatically render formatted headers, code blocks, and bullet points on your main project page. If you explicitly want plain text, name it `README.txt`.

---

#### Step 3: Check Git Status
Verify that Git sees the new README file:

```bash
git status
git add README.md
git commit -m "Add project README documentation"
git push origin main
cd ~/darar_ws/src/darar_swarm
git pull origin main
