# ros2_node_evaluation

## Overview

This framework evaluates any node in an application like Autoware. Single node or multiple nodes (around 2~3 is suitable) can be evaluated. This framework runs on a GUI. The framework provides three main functions.

- Arbitrary node activation
  - A file is generated that describes the commands to activate each node and a file that describes the parameters of each node. These two files enable parameter-aware node activation. In addition, remap can be taken into account by using a yaml file that contains remap information for each node.

- bag file processing
  - The framework processes the bag file according to which node it is activated. The bag file is processed so that it contains only the input topics of the node to be evaluated.

- Node evaluation with CARET
  - The proposed framework uses CARET to evaluate the performance of any node. The callback of the evaluated node is evaluated. The evaluation metrics are latency, period, and frequency. If there is a path in the architecture file, the message flow, chain latency, and response time of the sequence of nodes defined in the path are visualized.

Each function is independent, so users can use only the functions they want to use.
  

## Requirements

ROS 2 Humble

Ubuntu 22.04 LTS

[Autoware](https://autowarefoundation.github.io/autoware-documentation/main/)

[CARET](https://tier4.github.io/CARET_doc/latest/)

[ViRAD](https://github.com/NAIST-SE/ViRAD) : External tool to obtain remap information for each node

## How to use framework

Clone the repository
```
git clone https://github.com/azu-lab/ros2_node_evaluation.git
```

After extracting the cloned repository, run the following command
```
$ source /opt/ros/humble/setup.bash
$ source ~/autoware/install/setup.bash
$ source ~/ros2_caret_ws/install/setup.bash
```

CARET-related settings
```
$ export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)
$ export CARET_IGNORE_NODES="/rviz*"
$ export CARET_IGNORE_TOPICS="/clock:/parameter_events"
```

Launch the GUI of the framework
```
$ cd ros2_node_evaluation
$ python3 main.py
```

※Requires a bagfile that contains the input topics of the nodes to be evaluated in advance.<br>
※The config.yaml file should contain information about the nodes to be evaluated.

1.First, run ```python3 rosbag_test_generator.py``` on hardware A.<br>
2.Enter the path to the bagfile (relative to rosbag_test_generator.py) in the ROSBAG input field, and click the "Generate bagfile" button.<br>
3.Set the tolerance (tolerance is a relative error).<br>
4.Select a node to evaluate (in this case, we are using the pure_pursuit node for evaluation).<br>
5.Click the "Genarate source1.py" button.<br>
6.Click on the "Run of source1.py" button, and you will see the output results in the result folder.<br>
7.Perform steps 1~6 again on hardware B and store the output result in the result folder of hardware A.<br>
8.Click on the "Run of diff.py" button to output the results of hardware A and hardware B to the graph.<br>
* Sample.
<img src="https://github.com/CPFL/ros2b2b/blob/main/src/result/diff_pure_vehicle_vehicle_command_front_wheel_angle_rad_page-0001.jpg" alt="figure" title="figure">
9.From the output graphs, users can evaluate the porting of self-driving software.<br>

