import os
from glob import glob
from setuptools import setup

package_name = 'darar_swarm'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='DARAR Dev Team',
    maintainer_email='user@todo.todo',
    license='Apache-2.0',
    description='DARAR Swarm ROS 2 Package',
    entry_points={
        'console_scripts': [
            'environment_manager = darar_swarm.environment_manager:main',
            'uav_swarm_controller = darar_swarm.uav_swarm_controller:main',
        ],
    },
)
