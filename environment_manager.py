#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import torch
import numpy as np
from geometry_msgs.msg import PoseArray, Pose, Vector3
from std_msgs.msg import Float32MultiArray, Float32

class DARAREnvironmentManager(Node):
    def __init__(self):
        super().__init__('darar_environment_manager')
        
        # Configuration Parameters
        self.GRID_SIZE = 1000
        self.NUM_STATIC_VICTIMS = 100
        self.NUM_DYNAMIC_VICTIMS = 40
        self.TOTAL_VICTIMS = self.NUM_STATIC_VICTIMS + self.NUM_DYNAMIC_VICTIMS
        
        # Device Setup
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.get_logger().info(f"DARAR System Engine Initialized on: {self.device}")
        
        # Maps Setup
        self.water_map = torch.zeros((self.GRID_SIZE, self.GRID_SIZE), device=self.device)
        self.water_map[0:400, 0:500] = 1.0       # Shallow Flood Zone
        self.water_map[600:1000, 400:900] = 2.0   # Deep Flood Surge Delta

        self.terrain_map = torch.zeros((self.GRID_SIZE, self.GRID_SIZE), device=self.device)
        self.terrain_map[100:400, 600:900] = 1.0  # Urban High-rises
        self.terrain_map[500:800, 100:400] = 2.0  # Suburban
        self.terrain_map[0:300, 0:300] = 3.0      # Dense Canopy

        # Victims Setup
        self.static_victims = torch.randint(0, self.GRID_SIZE, (self.NUM_STATIC_VICTIMS, 3), dtype=torch.float32, device=self.device)
        self.dyn_victims = torch.randint(0, self.GRID_SIZE, (self.NUM_DYNAMIC_VICTIMS, 3), dtype=torch.float32, device=self.device)
        self.dyn_victim_vel = torch.randn((self.NUM_DYNAMIC_VICTIMS, 3), device=self.device) * 4.5
        self.victim_positions = torch.cat([self.static_victims, self.dyn_victims], dim=0)
        self.victim_found = torch.zeros(self.TOTAL_VICTIMS, dtype=torch.bool, device=self.device)

        # Environmental Disturbances
        self.current_wind_speed = 5.0
        self.network_connectivity = 1.0
        self.epoch_counter = 0

        # ROS 2 Publishers
        self.victim_pub = self.create_publisher(PoseArray, '/darar/victims/positions', 10)
        self.env_state_pub = self.create_publisher(Float32MultiArray, '/darar/environment/state', 10)

        # Timer Execution Loop (10 Hz)
        self.timer = self.create_timer(0.1, self.environment_update_loop)

    def environment_update_loop(self):
        self.epoch_counter += 1

        # Dynamic Wind Speeds Update
        if self.epoch_counter % 40 == 0:
            self.current_wind_speed = float(np.random.uniform(2.0, 25.0))

        # Dynamic Communication Fades
        if self.epoch_counter % 250 == 0:
            self.network_connectivity = 0.0 if np.random.rand() < 0.2 else 1.0

        # Dynamic Victim Displacement
        self.dyn_victims = (self.dyn_victims + self.dyn_victim_vel) % self.GRID_SIZE
        self.victim_positions[self.NUM_STATIC_VICTIMS:] = self.dyn_victims

        # Publish Victim Positions
        pose_array_msg = PoseArray()
        pose_array_msg.header.stamp = self.get_clock().now().to_msg()
        pose_array_msg.header.frame_id = "world"

        for i in range(self.TOTAL_VICTIMS):
            p = Pose()
            p.position.x = float(self.victim_positions[i, 0].item())
            p.position.y = float(self.victim_positions[i, 1].item())
            p.position.z = float(self.victim_positions[i, 2].item())
            pose_array_msg.poses.append(p)

        self.victim_pub.publish(pose_array_msg)

        # Broadcast Global Environmental Telemetry [wind_speed, net_connectivity]
        env_msg = Float32MultiArray()
        env_msg.data = [self.current_wind_speed, self.network_connectivity]
        self.env_state_pub.publish(env_msg)


def main(args=None):
    rclpy.init(args=args)
    node = DARAREnvironmentManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
