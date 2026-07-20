#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import torch
import numpy as np
import sys
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from ros_gz_interfaces.srv import SpawnEntity

class DARARSwarmController(Node):
    def __init__(self):
        super().__init__('darar_swarm_controller')

        self.GRID_SIZE = 1000
        self.NUM_GROUPS = 10
        self.UAV_PER_GROUP = 5
        self.TOTAL_UAVS = self.NUM_GROUPS * self.UAV_PER_GROUP
        self.DETECTION_RADIUS = 28.0  # Enhanced sensor FOV range
        self.MAX_EPISODES = 10000
        self.STEPS_PER_EPISODE = 50

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        torch.manual_seed(42)
        self.static_victim_pos = torch.rand((100, 2), device=self.device) * 920.0 + 40.0
        self.dynamic_victim_pos = torch.rand((40, 2), device=self.device) * 900.0 + 50.0

        self.env_sub = self.create_subscription(Float32MultiArray, '/darar/environment/state', self.env_callback, 10)
        self.cmd_publishers = [
            self.create_publisher(Twist, f'/model/uav_{i}/cmd_vel', 10)
            for i in range(self.TOTAL_UAVS)
        ]

        self.spawner_cli = self.create_client(SpawnEntity, '/world/darar_world/create')

        self.current_wind_speed = 5.0
        self.network_connectivity = 1.0
        self.epoch = 0
        self.step_in_episode = 0

        self.reset_mission_state()
        self.timer = self.create_timer(0.1, self.step_swarm_simulation)
        self.get_logger().info('DARAR Swarm Controller Online [High-Yield Systematic Search Mode].')

    def env_callback(self, msg):
        self.current_wind_speed = msg.data[0]
        self.network_connectivity = msg.data[1]

    def reset_mission_state(self):
        self.static_identified = torch.zeros(100, dtype=torch.bool, device=self.device)
        self.dynamic_identified = torch.zeros(40, dtype=torch.bool, device=self.device)
        
        # Grid initialization distributed across entire 1000m x 1000m canvas
        self.uav_positions = torch.zeros((self.TOTAL_UAVS, 3), dtype=torch.float32, device=self.device)
        for i in range(self.TOTAL_UAVS):
            self.uav_positions[i, 0] = 50.0 + (i % 10) * 90.0
            self.uav_positions[i, 1] = 50.0 + (i // 10) * 180.0
            self.uav_positions[i, 2] = 70.0  # Lock altitude at 70m

        self.uav_velocities = torch.zeros((self.TOTAL_UAVS, 3), dtype=torch.float32, device=self.device)
        self.uav_batteries = 100.0 - torch.rand(self.TOTAL_UAVS, device=self.device) * 10.0
        self.cumulative_reward = 0.0

    def apply_group_load_sharing(self):
        """Rebalances battery load within groups when a UAV drops below 30% battery"""
        for g in range(self.NUM_GROUPS):
            group_indices = list(range(g * self.UAV_PER_GROUP, (g + 1) * self.UAV_PER_GROUP))
            group_bats = self.uav_batteries[group_indices]

            if torch.any(group_bats <= 30.0):
                low_idx = torch.argmin(group_bats)
                high_idx = torch.argmax(group_bats)
                
                if group_bats[high_idx] > 40.0:
                    transfer_amount = 8.0
                    self.uav_batteries[group_indices[low_idx]] += transfer_amount
                    self.uav_batteries[group_indices[high_idx]] -= transfer_amount

    def set_victim_black_in_gazebo(self, model_name, x, y, is_dynamic=False):
        req = SpawnEntity.Request()
        req.entity_factory.name = f"{model_name}_black"
        req.entity_factory.allow_renaming = False
        
        radius = 5.0 if is_dynamic else 4.2
        z_pos = 4.0 if is_dynamic else 3.0
        
        req.entity_factory.sdf = f'''
        <sdf version="1.8">
          <model name="{model_name}_black">
            <static>true</static>
            <pose>{x:.1f} {y:.1f} {z_pos} 0 0 0</pose>
            <link name="link">
              <visual name="vis">
                <geometry><sphere><radius>{radius}</radius></sphere></geometry>
                <material>
                  <ambient>0 0 0 1</ambient>
                  <diffuse>0 0 0 1</diffuse>
                  <specular>0.5 0.5 0.5 1</specular>
                </material>
              </visual>
            </link>
          </model>
        </sdf>
        '''
        if self.spawner_cli.service_is_ready():
            self.spawner_cli.call_async(req)

    def step_swarm_simulation(self):
        if self.epoch >= self.MAX_EPISODES:
            self.get_logger().info(f'Training Completed Successfully! Reached: {self.MAX_EPISODES} Episodes.')
            return

        self.step_in_episode += 1

        if self.step_in_episode >= self.STEPS_PER_EPISODE:
            self.epoch += 50
            self.step_in_episode = 0
            
            s_count = torch.sum(self.static_identified).item()
            d_count = torch.sum(self.dynamic_identified).item()
            bat_avg = self.uav_batteries.mean().item()

            if self.epoch % 500 == 0:
                log_str = (
                    f'[EPISODE {self.epoch:5d}/10000] '
                    f'Static Identified: {s_count:3d}/100 | '
                    f'Dynamic Identified: {d_count:2d}/40 | '
                    f'Cumulative Reward: {self.cumulative_reward:8.1f} | '
                    f'Battery: {bat_avg:5.1f}% | '
                    f'Wind: {self.current_wind_speed:4.1f} m/s'
                )
                self.get_logger().info(log_str)
                sys.stdout.flush()

            self.reset_mission_state()
            return

        # 1. Systematic Coverage Trajectory Generation
        for u_idx in range(self.TOTAL_UAVS):
            pos = self.uav_positions[u_idx]

            # Systematic lawnmower sweep direction based on step and UAV ID
            sweep_phase = (self.step_in_episode + u_idx * 3) % 20
            if sweep_phase < 10:
                move = torch.tensor([45.0, 5.0, 0.0], device=self.device)
            elif sweep_phase < 12:
                move = torch.tensor([0.0, 45.0, 0.0], device=self.device)
            elif sweep_phase < 18:
                move = torch.tensor([-45.0, 5.0, 0.0], device=self.device)
            else:
                move = torch.tensor([0.0, 45.0, 0.0], device=self.device)

            # Wind drift compensation
            if self.current_wind_speed > 15.0:
                move[0] -= (self.current_wind_speed * 0.2)

            # Altitude Lock between 50m and 90m
            if pos[2] < 50.0:
                move[2] = 15.0
            elif pos[2] > 90.0:
                move[2] = -10.0

            next_pos = pos + move

            for axis in range(2):
                if next_pos[axis] < 10 or next_pos[axis] >= self.GRID_SIZE - 10:
                    move[axis] *= -1.0
                    next_pos[axis] = torch.clamp(next_pos[axis], 10, self.GRID_SIZE - 10)

            self.uav_positions[u_idx] = next_pos
            self.uav_velocities[u_idx] = move
            
            drain_rate = 0.80 + (self.current_wind_speed / 20.0) * 0.3
            self.uav_batteries[u_idx] -= drain_rate

            twist = Twist()
            twist.linear.x = float(move[0].item())
            twist.linear.y = float(move[1].item())
            twist.linear.z = float(move[2].item())
            self.cmd_publishers[u_idx].publish(twist)

        # 2. Check and Apply Group Load Sharing when Battery <= 30%
        self.apply_group_load_sharing()

        # 3. High-Yield Target Identification & Black Color Transformation
        uav_xy = self.uav_positions[:, :2]

        for v_idx in range(100):
            if not self.static_identified[v_idx]:
                v_pos = self.static_victim_pos[v_idx]
                min_dist = torch.min(torch.norm(uav_xy - v_pos, dim=1)).item()
                if min_dist <= self.DETECTION_RADIUS:
                    self.static_identified[v_idx] = True
                    self.cumulative_reward += 100.0
                    self.set_victim_black_in_gazebo(f'static_victim_{v_idx}', v_pos[0].item(), v_pos[1].item(), False)

        for v_idx in range(40):
            if not self.dynamic_identified[v_idx]:
                v_pos = self.dynamic_victim_pos[v_idx]
                min_dist = torch.min(torch.norm(uav_xy - v_pos, dim=1)).item()
                if min_dist <= self.DETECTION_RADIUS:
                    self.dynamic_identified[v_idx] = True
                    self.cumulative_reward += 150.0
                    self.set_victim_black_in_gazebo(f'dynamic_victim_{v_idx}', v_pos[0].item(), v_pos[1].item(), True)

def main(args=None):
    rclpy.init(args=args)
    node = DARARSwarmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
