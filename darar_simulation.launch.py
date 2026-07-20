import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('darar_swarm')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    world_path = os.path.join(pkg_share, 'worlds', 'darar_world.sdf')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_path}'}.items()
    )

    bridge_args = ['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock']

    for i in range(50):
        bridge_args.append(f'/model/uav_{i}/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist')

    for v in range(40):
        bridge_args.append(f'/model/dynamic_victim_{v}/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist')

    parameter_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=bridge_args,
        output='screen'
    )

    env_node = Node(
        package='darar_swarm',
        executable='environment_manager',
        name='environment_manager',
        output='screen'
    )

    swarm_node = Node(
        package='darar_swarm',
        executable='uav_swarm_controller',
        name='uav_swarm_controller',
        output='screen'
    )

    return LaunchDescription([
        SetEnvironmentVariable('QT_QPA_PLATFORM', 'xcb'),
        SetEnvironmentVariable('PYTHONUNBUFFERED', '1'),
        gazebo,
        parameter_bridge,
        env_node,
        swarm_node
    ])
