import unittest
import cityflow
from collections import defaultdict
import numpy as np
from RL_brain import DeepQNetwork
from tqdm import tqdm

class TestAPI(unittest.TestCase):

    config_file = "./examples/config.json"
    period = 3600

    
    def test_data_api(self):
        """Single save and single load with single threading engine"""
        eng = cityflow.Engine(config_file=self.config_file, thread_num=1)
        RL = DeepQNetwork(8, 2,
                          learning_rate = 0.01,
                          reward_decay = 0.9,
                          e_greedy = 0.9,
                          replace_target_iter = 200,
                          memory_size = 200)
        

        with open("rl_vehicle_info_data_api.txt", "w") as vehicle_file, open("rl_intersection_info_data_api.txt", "w") as intersection_file:
            next_intersection_observation = defaultdict(list)
            for step in tqdm(range(self.period)):
                running_count = len(eng.get_vehicles())
                total_count = len(eng.get_vehicles(include_waiting=True))
                self.assertTrue(running_count <= total_count)
                self.assertEqual(running_count, eng.get_vehicle_count())
                lane_vehicle_count = eng.get_lane_vehicle_count()
                lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()
                lane_vehicles = eng.get_lane_vehicles()
                vehicle_speed = eng.get_vehicle_speed()
                vehicle_distance = eng.get_vehicle_distance()
                current_time = eng.get_current_time()

                # 存储车辆信息到文件
                vehicle_file.write(f"当前时间: {current_time}\n")
                for vehicle_id, speed in vehicle_speed.items():
                    distance = vehicle_distance.get(vehicle_id)
                    vehicle_file.write(f"车辆 ID: {vehicle_id}, 速度: {speed}, 行驶距离: {distance}\n")

                # 存储路口信息到文件
                intersection_file.write(f"当前时间: {current_time}\n")
                for lane, count in lane_vehicle_count.items():
                    waiting_count = lane_waiting_vehicle_count.get(lane)
                    vehicles_on_lane = lane_vehicles.get(lane)
                    intersection_file.write(f"车道: {lane}, 车辆总数: {count}, 等待车辆数: {waiting_count}, 车道上的车辆: {vehicles_on_lane}\n")

                # observation
                if next_intersection_observation and next_intersection_observation != {}:
                    intersection_observation = next_intersection_observation.copy()
                
                else:
                    vehicle_observations = defaultdict(list)

                    for lane,vehicle_count in lane_vehicle_count.items():
                        vehicle_observations[lane].append(vehicle_count)
                    for lane,vehicle_waiting_count in lane_waiting_vehicle_count.items():
                        vehicle_observations[lane].append(vehicle_waiting_count)

                    intersection_observation = defaultdict(list)

                    for lane,observation in vehicle_observations.items():
                        road_index = lane[4:10]
                        if road_index[-1] == '0':
                            intersection_id = f"interseciton_{int(road_index[1])+1}" + road_index[2:4]
                        elif road_index[-1] == '1':
                            intersection_id = "interseciton" + road_index[:3] + f"{int(road_index[3])+1}"
                        elif road_index[-1] == '2':
                            intersection_id = f"interseciton_{int(road_index[1])-1}" + road_index[2:4] 
                        elif road_index[-1] == '3':
                            intersection_id = "interseciton" + road_index[:3] + f"{int(road_index[3])-1}"

                        intersection_observation[intersection_id].append(observation)
                    
                
                # reinforcement learning
                for intersection_id,observation in intersection_observation.items():
                    input_observation = np.sum(observation, axis = 0)
                    action = RL.choose_action(input_observation)
                    eng.set_tl_phase(intersection_id, action)
                    
                eng.next_step() #next observation
                next_lane_vehicle_count = eng.get_lane_vehicle_count()
                next_lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()
                next_vehicle_observations = defaultdict(list)

                for lane,vehicle_count in next_lane_vehicle_count.items():
                    next_vehicle_observations[lane].append(vehicle_count)
                for lane,vehicle_waiting_count in next_lane_waiting_vehicle_count.items():
                    next_vehicle_observations[lane].append(vehicle_waiting_count)
                
                next_intersection_observation = defaultdict(list)

                for lane,observation in next_vehicle_observations.items():
                    road_index = lane[4:10]
                    if road_index[-1] == '0':
                        intersection_id = f"interseciton_{int(road_index[1])+1}" + road_index[2:4]
                    elif road_index[-1] == '1':
                        intersection_id = "interseciton" + road_index[:3] + f"{int(road_index[3])+1}"
                    elif road_index[-1] == '2':
                        intersection_id = f"interseciton_{int(road_index[1])-1}" + road_index[2:4] 
                    elif road_index[-1] == '3':
                        intersection_id = "interseciton" + road_index[:3] + f"{int(road_index[3])-1}"

                    next_intersection_observation[intersection_id].append(observation)
                
                # reward function
                for intersection_id, next_observation_list in next_intersection_observation.items():
                    cnt = 0
                    total = 0
                    for next_ob in next_observation_list:
                        vehicle_count = next_ob[0]
                        vehicle_waiting_count = next_ob[1]
                        if vehicle_count == 0:
                            continue
                        if vehicle_waiting_count / vehicle_count < 0.3:
                            cnt += 1
                        total += 1
                    if total > 0:
                        if cnt / total > 0.7:
                            reward = 1
                        else:
                            reward = 0
                    else:
                        reward = 0.5
                #store memory
                    for index,ob in enumerate(intersection_observation[intersection_id]):
                        ob = np.array(ob)
                        next_ob = np.array(next_observation_list[index])
                        RL.store_transition(ob, action, reward, next_ob)
                        if step > 200 and step % 5 == 0:
                            RL.learn()
                        
        print("simulation over")
                        
        del eng

    def test_set_replay(self):
        """change replay path on the fly"""
        eng = cityflow.Engine(config_file=self.config_file, thread_num=1)

        with open("rl_vehicle_info_set_replay.txt", "w") as vehicle_file, open("rl_intersection_info_set_replay.txt", "w") as intersection_file:
            for _ in range(100):
                eng.next_step()

            eng.set_replay_file("replay2.txt")

            for _ in range(100):
                eng.next_step()
                vehicle_speed = eng.get_vehicle_speed()
                vehicle_distance = eng.get_vehicle_distance()
                current_time = eng.get_current_time()

                # 存储车辆信息到文件
                vehicle_file.write(f"当前时间: {current_time}\n")
                for vehicle_id, speed in vehicle_speed.items():
                    distance = vehicle_distance.get(vehicle_id)
                    vehicle_file.write(f"车辆 ID: {vehicle_id}, 速度: {speed}, 行驶距离: {distance}\n")

                # 存储路口信息到文件
                intersection_file.write(f"当前时间: {current_time}\n")
                lane_vehicle_count = eng.get_lane_vehicle_count()
                lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()
                lane_vehicles = eng.get_lane_vehicles()
                for lane, count in lane_vehicle_count.items():
                    waiting_count = lane_waiting_vehicle_count.get(lane)
                    vehicles_on_lane = lane_vehicles.get(lane)
                    intersection_file.write(f"车道: {lane}, 车辆总数: {count}, 等待车辆数: {waiting_count}, 车道上的车辆: {vehicles_on_lane}\n")

        del eng


if __name__ == '__main__':
    unittest.main(verbosity=2)
    