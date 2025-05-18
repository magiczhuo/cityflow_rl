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
 * lightphase在不同time下的available roadlinkindices（信号灯相位）

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
