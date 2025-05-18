* Roadnet.json 文件格式说明

 * 坐标表示约定

系统中的地理和方向元素采用以下坐标表示形式：

* **Intersection (交叉路口)**: `intersection_x_y`
  * `x`: 横坐标
  * `y`: 纵坐标

* **Road (道路)**: `road_x_y_i`
  * `x`: 道路起点的横坐标
  * `y`: 道路起点的纵坐标
  * `i`: 表示道路的前进方向，取值为 0-3：
    * `0`: 向右 (东)
    * `1`: 向上 (北)
    * `2`: 向左 (西)
    * `3`: 向下 (南)
    
    *注：方向约定从向右开始，逆时针方向变换*

* **Lane (车道)**: `lane_x_y_i_j`
  * `x, y, i`: 与其所属的 Road 定义一致
  * `j`: 表示当前道路中该车道的索引

* Roadnet.json 结构说明

`Roadnet.json` 文件定义了以下关键元素：
 * intersection（交叉路口）
 * intersection邻接的roads（道路）
 * roads的lanes（车道）
 * lightphase在不同time下的available roadlinkindices（信号灯相位）[{'time':5, 'availableroadlinks': []}, {}, {}]

* ⚠️ 重要说明

**Roadlinks**：
 * Roadlinks为一个列表，记录当前intersection中所有的起始road-终止road的link
 * 每一个roadlink使用字典储存
 * 每一个roadlinks列表中的roadlink字典，记录了当前road link的种类（turn left等），以及起始road-终止road的link
 * 每一个roadlink中包含了所有的lane links
 * Key为"Lanelinks"的子字典中记录的是可以变道的所有情况
 * Points为变道过程中为了可视化变道过程所设计的点

 **交通信号灯**：
 * 在当前的intersection sample中一共有12个roadlinks
 * key为"trafficlight"的字典中"roadlinkindices"为当前路口的各个road之间的汽车行驶方式的index
 * Key为"lightphases"的字典中为时长不同"time"下的"availableroadlink"的可行使的roadlink的index


* Reinforcement Learning 接口

 * 写好的DQN放置于主文件夹中
 * 文件tests/python/test_api2.py中通过调用DeepQNetwork初始化RL
 * 首先检查当前处于第一步还是一后之前step，通过for循环完成状态更新。
 * 代码 line 80开始，根据当前各项observation，选择action，并根据人为逆推出的intersection_id和选择的action，对traffic light进行控制，并进一步模拟next_step。
 * 人为设定intersection_id思路，根据quick start文档中对intersection_id，lane_id，road_id等格式的描述，对字符串进行处理，通过cityflow.c中定义的函数返回的lane_id，逆推出对应的intersection_id，即代码line 66-75 、 line 98-107 部分。
 * 代码 line 112 开始，定义当前的reward，即选择了action之后的observation根据当前road中所有的lane上等待的车辆与总车辆的数量的比例，简单的赋值reward为0，0.5，1。最后通过store_transition更新网络记忆。

* ⚠️ 重要说明

 * 当前每一次step都会存储不止一次memory，即每一个intersection都是一次next observation，而不是全局的所有的intersection为一个整体的状态。需要改进！！！

 * 根据源代码中的set_tl_phase函数以及初始化的intersection、trafficlight等类，原始代码中直接定义了intersection中traffic light的多种不同状态phase，phase为包含字典的列表，即上述roadnet.json当中的lightphases。这里的choose action仅根据当前intersection中的多种状态进行选择和切换，并非直接控制traffic light的红黄绿变化。
