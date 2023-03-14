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

Here is a [bag file](https://drive.google.com/file/d/1cLoHWzQg_FMSKjitQA6Xdf4vHOku7xHR/view?usp=share_link) that contains a variety of topics. Please check to see if the bag file contains the topics you need.


