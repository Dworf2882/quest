import os
import time

import launch_ros.actions as actions

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription, GroupAction
from launch_ros.actions import PushRosNamespace, SetRemap
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    gz_sim = GroupAction([IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': '-r robots.sdf'
        }.items(),
    ),
    ])

    ld.add_action(gz_sim)

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[ 
                    "/camera@sensor_msgs/msg/Image@gz.msgs.Image",
                    # "/world/robots/model/chebu/link/lidar/sensor/laser/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
                    # "/world/robots/model/chebu/link/lidar/sensor/laser/scan/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
                    "/world/robots/model/vehicle1/link/lidar/sensor/laser/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
                    "/world/robots/model/vehicle1/link/lidar/sensor/laser/scan/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
                    # "/world/robots/model/vehicle2/link/lidar/sensor/laser/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan",
                    # "/world/robots/model/vehicle2/link/lidar/sensor/laser/scan/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
                    "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
                    ],
         parameters=[{'qos_overrides./vehicle1.subscriber.reliability': 'reliable',}],
                         
        remappings=[
                    # ("/world/robots/model/chebu/link/lidar/sensor/laser/scan","/chebu/lidar"),
                    # ("/world/robots/model/chebu/link/lidar/sensor/laser/scan/points", "/chebu/lidar_points"),
                    ("/world/robots/model/vehicle1/link/lidar/sensor/laser/scan","/vehicle1/lidar"),
                    ("/world/robots/model/vehicle1/link/lidar/sensor/laser/scan/points", "/vehicle1/lidar_points"),
                    # ("/world/robots/model/vehicle2/link/lidar/sensor/laser/scan","/vehicle2/lidar"),
                    # ("/world/robots/model/vehicle2/link/lidar/sensor/laser/scan/points", "/vehicle2/lidar_points"),
                    ],
        output='screen'
        )
    
    ld.add_action(bridge)

    return ld