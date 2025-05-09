import json
import random

json_data = '''{"static":{"nodes":[{"id":"intersection_0_1","point":[-300.0,0.0],"virtual":true,"outline":[-300.0,-12.0,-295.0,-12.0,-295.0,12.0,-300.0,12.0,-300.0,0.0]},{"id":"intersection_1_0","point":[0.0,-300.0],"virtual":true,"outline":[0.0,-300.0,12.0,-300.0,12.0,-295.0,-12.0,-295.0,-12.0,-300.0]},{"id":"intersection_1_1","point":[0.0,0.0],"virtual":false,"width":20.0,"outline":[0.0,-26.0,12.0,-26.0,26.0,-12.0,26.0,12.0,12.0,26.0,-12.0,26.0,-26.0,12.0,-26.0,-12.0,-12.0,-26.0]},{"id":"intersection_1_2","point":[0.0,300.0],"virtual":true,"outline":[0.0,295.0,12.0,300.0,-12.0,300.0,-12.0,295.0]},{"id":"intersection_2_1","point":[300.0,0.0],"virtual":true,"outline":[300.0,-12.0,300.0,12.0,295.0,12.0,295.0,-12.0]}],"edges":[{"id":"road_0_1_0","from":"intersection_0_1","to":"intersection_1_1","points":[[-300.0,0.0],[0.0,0.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_1_0_1","from":"intersection_1_0","to":"intersection_1_1","points":[[0.0,-300.0],[0.0,0.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_1_1_0","from":"intersection_1_1","to":"intersection_2_1","points":[[0.0,0.0],[300.0,0.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_1_1_1","from":"intersection_1_1","to":"intersection_1_2","points":[[0.0,0.0],[0.0,300.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_1_1_2","from":"intersection_1_1","to":"intersection_0_1","points":[[0.0,0.0],[-300.0,0.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_1_1_3","from":"intersection_1_1","to":"intersection_1_0","points":[[0.0,0.0],[0.0,-300.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_1_2_3","from":"intersection_1_2","to":"intersection_1_1","points":[[0.0,300.0],[0.0,0.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]},{"id":"road_2_1_2","from":"intersection_2_1","to":"intersection_1_1","points":[[300.0,0.0],[0.0,0.0]],"nLane":3,"laneWidths":[4.0,4.0,4.0]}]}}'''

data = json.loads(json_data)

num_intersections = len(data["static"]["nodes"])

title = "Vehicle Numbers at Intersections"

time_steps = 10
simulated_data = []
for _ in range(time_steps):
    step_data = [random.randint(0,50) for _ in range(num_intersections)]
    simulated_data.append(step_data)

with open('chart.txt','w') as f:
    f.write(title + '\n')
    for step_data in simulated_data:
        line = " ".join(map(str,step_data)) + '\n'
        f.write(line)

print("Log file has been generated: chart.txt")

