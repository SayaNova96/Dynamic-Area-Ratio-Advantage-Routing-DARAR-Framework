[Screencast from 2026-07-20 20-14-50.webm](https://github.com/user-attachments/assets/c27e834d-3d7d-4eaf-92ad-23dd0e66b570)
<img width="1435" height="963" alt="2026-07-20T21:20:44 511993953" src="https://github.com/user-attachments/assets/d3b8679b-725c-41d0-8052-1d5cc10a401e" />



### **Note on DARAR**

**DARAR** (**D**ynamic **A**rea-**R**atio **A**dvantage **R**outing) is a decentralized Deep Reinforcement Learning (DRL) framework designed for multi-UAV (Unmanned Aerial Vehicle) swarm coordination in search and rescue (SAR) operations across non-stationary disaster environments.

Created by **Sayantan Chakraborty** (PhD Research Scholar at IIIT Guwahati), the algorithm addresses key multi-robot challenges: scale volatility, dynamic hazards (e.g., wind, smoke), edge-compute constraints, and individual battery drain.

---

### **Key Technical Features**

* **Localized 10D State Vector:** To run on low-power onboard microcontrollers, each UAV tracks a compact 10-dimensional feature tensor containing its normalized 3D position, velocity vector, a relative threat repulsion field ($\mathbf{V}_{\text{dynamic}}$), and local map entropy ($H$).
* **Informative Path Planning (IPP):** Embeds an environment map uncertainty decay parameter ($\lambda$), ensuring unmonitored sectors naturally regain uncertainty. This forces the swarm into continuous patrol loops to harvest Dynamic Information Gain ($DIG$) rewards.
* **Scale-Invariant Reward Architecture:** Utilizes an Area-Ratio Adjuster ($\Omega = (\text{Volume})^{-1/3}$) to equalize reward step magnitudes, allowing policy weights to operate seamlessly across small or large search arenas.
* **Bounded Gradient Step Proxy:** Replaces computationally heavy TRPO/PPO trust-region Hessian updates with an algebraic parameter clip ($\pm\delta = 0.01$). This safeguards the neural network against policy collapse caused by sudden collision penalties without overloading edge hardware.
* **Cooperative Energy Balancing:** Incorporates a peer-to-peer load-sharing logic within sub-groups to transfer operational charge mid-air to low-battery drones, ensuring sustained fleet flight time.

---

### **Performance**

In CUDA-accelerated $1000^3$ spatial simulations with 50 UAVs, DARAR achieved a **97.6% rescue efficiency rate** (locating 293 out of 300 targets) while reducing per-step runtime complexity to $O(1)$ constant-time constraints per agent.
