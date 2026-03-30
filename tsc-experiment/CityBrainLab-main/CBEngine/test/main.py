import os, sys
import time
import cbengine
from utils import Dataloader


roadnet_file = './mini_paris/roadnet.txt'
flow_file = './mini_paris/flow.txt'
cfg_file = './cfgs/config.cfg'
dataloader = Dataloader(roadnet_file, flow_file, cfg_file)

def main():
    running_step = 100 # 500                      # simulation time
    phase_time = 30                         # traffic signal phase duration time
    engine = cbengine.Engine(cfg_file, 12)
    LOG_ADDR = './log'

    print('Simulation starts ...')
    start_time = time.time()
    for step in range(running_step):
        engine.log_info(os.path.join(LOG_ADDR, 'time{}.json'.format(int(engine.get_current_time()))))
        for intersection in dataloader.intersections.keys():
            engine.set_ttl_phase(intersection, (int(engine.get_current_time()) // phase_time) % 4 + 1)
        engine.next_step()
        print(" time step: {}, number of vehicles: {}".format(step, engine.get_vehicle_count()))
        # print(engine.get_vehicle_info(1))
    end_time = time.time()
    print('Simulation finishes. Runtime: ', end_time - start_time)
    print(engine.get_lane_vehicles())
    print(engine.get_car_following_params())
    
    

if __name__ == '__main__':
    main()