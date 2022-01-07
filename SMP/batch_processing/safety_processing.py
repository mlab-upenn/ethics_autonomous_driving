from commonroad.common.file_reader import CommonRoadFileReader
import os
from commonroad.common.file_reader import CommonRoadFileReader
import numpy as np
from commonroad.prediction.prediction import TrajectoryPrediction
from commonroad.geometry.shape import Rectangle
from commonroad.geometry.shape import Circle
from commonroad.scenario.obstacle import StaticObstacle, ObstacleType, DynamicObstacle
from commonroad.scenario.trajectory import State, Trajectory
from commonroad_dc.collision.collision_detection.pycrcc_collision_dispatch import create_collision_checker, \
    create_collision_object
from commonroad_dc.boundary import boundary
import commonroad_dc.pycrcc as pycrcc
from commonroad_dc.collision.trajectory_queries import trajectory_queries
import cvxpy as cp
import pandas as pd
import triangle
from math import sqrt

def distance(x_0, x_1, y_0, y_1):
    return sqrt((x_1-x_0)**2 + (y_1-y_0)**2)

def create_ego_tvo_from_i(scenario, i):
    safe_dist_list = []
    
    ego = scenario.obstacle_by_id(-1)
    car_length = ego.obstacle_shape.length
    car_width = ego.obstacle_shape.width
    state_list = ego.prediction.trajectory.state_list
    tvo=pycrcc.TimeVariantCollisionObject(i)

    for j in range(i, len(state_list)-1):
        
        current_pos = state_list[j].position
        next_pos = state_list[j+1].position
        orientation = state_list[j].orientation
        
        x = current_pos[0]
        y = current_pos[1]
        x_1 = next_pos[0]
        y_1 = next_pos[1]
        
        v = distance(x, x_1, y, y_1)
        
        safe_dist = 3*v
        if i == 0:
            safe_dist_list.append(safe_dist)
        
        if (v > 0):
            length = (car_length/2) + safe_dist/2
            offset_magnitude = ((length*2) - car_length)/2
            offset_x = ((x_1-x)/v)*offset_magnitude
            offset_y = ((y_1-y)/v)*offset_magnitude


            #note that the collision obstacle created needs a half length input
            tvo.append_obstacle(pycrcc.RectOBB(length,car_width/2,orientation,x+offset_x,y+offset_y))
        else: 
            tvo.append_obstacle(pycrcc.RectOBB(car_length/2,car_width/2,orientation,x,y))
    return tvo, safe_dist_list
def create_triangle_mesh(vertices):
    # triangulate the polygon
    number_of_vertices = len(vertices)
    segments = list(zip(range(0, number_of_vertices-1), range(1, number_of_vertices)))
    segments.append((0, number_of_vertices-1))
    triangles = triangle.triangulate({'vertices': vertices, 'segments': segments}, opts='pqS2.4')
    # convert all triangles to pycrcc.Triangle
    mesh = list()
    for t in triangles['triangles']:
        v0 = triangles['vertices'][t[0]]
        v1 = triangles['vertices'][t[1]]
        v2 = triangles['vertices'][t[2]]
        mesh.append(pycrcc.Triangle(v0[0], v0[1],
                                    v1[0], v1[1],
                                    v2[0], v2[1]))
    return mesh

#Problem: cannot assume that a dynamic obstacle is a rectangle shape
#Must use abstract class methods to ensure code is generalizable
def create_tvo(obs, i, obs_obj_dict):
    length = obs.obstacle_shape.length
    width = obs.obstacle_shape.width
    state_list = obs.prediction.occupancy_set
    tvo = pycrcc.TimeVariantCollisionObject(i)
    
    for j in range(i, len(state_list)):
        pos = state_list[j].shape.center
        orientation = state_list[j].shape.orientation
        
        x = pos[0]
        y = pos[1]
        
        vertices = state_list[j].shape.vertices
        mesh = create_triangle_mesh(vertices)
        tvo.append_obstacle(pycrcc.Polygon(vertices,list(),mesh))
    obs_obj_dict[tvo] = obs
    return tvo
    


def get_shortest_distance(obs_1, obs_2, i):
    
    X = np.transpose(obs_1.occupancy_at_time(i).shape.vertices[:-1])
    Y = np.transpose(obs_2.occupancy_at_time(i).shape.vertices[:-1])

    # maximum thickness separating slab
    a, b = cp.Variable(2), cp.Variable()
    prob = cp.Problem(cp.Minimize(cp.norm2(a)), [a.T@X - b >= 1, a.T@Y - b <= -1])
    prob.solve()
    if a.value is None:
        return 0
    width_max = 2 / np.linalg.norm(a.value)
    return width_max

def long_dist(scenario):
    
    long_dist_violations = []
    actual_dist_list = []
    obs_obj_dict = {}
    
    ego = scenario.obstacle_by_id(-1)

    co, safe_dist_list = create_ego_tvo_from_i(scenario, 0)

    dynamic_obstacles = []
    for obs in scenario.dynamic_obstacles:
        if obs.obstacle_id != -1:
            tvo = create_tvo(obs, 0, obs_obj_dict)
            dynamic_obstacles.append(tvo)


    actual_dist_list = []
       
    for i in range(0, len(safe_dist_list)):
        actual_dist_list.append(safe_dist_list[i])
        co_ego = co.obstacle_at_time(i)
        for obj in dynamic_obstacles:
            co_obs = obj.obstacle_at_time(i)
            if co_ego.collide(co_obs):
                
                obs = obs_obj_dict.get(obj)
            
                actual_dist = get_shortest_distance(ego, obs, i)
                actual_dist_list[i] = actual_dist
                
    for i in range(0, len(safe_dist_list)):
        long_dist_violations.append(safe_dist_list[i] - actual_dist_list[i])
    
    return long_dist_violations

def lane_tracking(scenario):
    
    ego = scenario.obstacle_by_id(-1)
    state_list = ego.prediction.trajectory.state_list
    
    desired_state_list = []
    error_list = []
    for i in range(0, len(state_list)-1):
        desired_state_list.append(state_list[i].position)
        error_list.append(1000000.0)
    for i in range(0, len(state_list)-1):
        candidate_lanelets = []
        for lanelet in scenario.lanelet_network.lanelets:
            pos = state_list[i].position
            if (lanelet.convert_to_polygon().contains_point(pos)):
                candidate_lanelets.append(lanelet)
        for lanelet in candidate_lanelets:
            
            lanelet_start = lanelet.interpolate_position(0)[0]
            curr_pos = state_list[i].position
            init_dist = distance(lanelet_start[0], curr_pos[0], lanelet_start[1], curr_pos[1])
            
            next_pos = state_list[i+1].position
            next_dist = distance(next_pos[0], curr_pos[0], next_pos[1], curr_pos[1])
            
            if(init_dist + next_dist <= lanelet.distance[-1]):
                desired_pos = lanelet.interpolate_position(init_dist + next_dist)[0]
                error = distance(desired_pos[0], next_pos[0], desired_pos[1], next_pos[1])
            
                if (error < error_list[i]):
                    desired_state_list[i] = desired_pos
                    error_list[i] = error
            else: 
                #edge case where we have reached the end of a lanelet and cannot calculate interpolated position
                desired_pos = lanelet.interpolate_position(lanelet.distance[-1])[0]
                error = distance(desired_pos[0], next_pos[0], desired_pos[1], next_pos[1])
            
                if (error < error_list[i]):
                    desired_state_list[i] = desired_pos
                    error_list[i] = error
    return error_list

def relative_speed(scenario):    
    avg_v = []
    differential_v = []
    
    ego = scenario.obstacle_by_id(-1)
    state_list = ego.prediction.trajectory.state_list
    
    count = len(scenario.dynamic_obstacles)
    
    for i in range(0, len(state_list)):
        total_v = 0
        for obs in scenario.dynamic_obstacles:
            if obs.obstacle_id != -1:
                if len(obs.prediction.trajectory.state_list) < i:
                    obs_v = obs.prediction.trajectory.state_list[i].velocity
                    total_v += obs_v
        avg_v.append(total_v/count)
        ego_v = state_list[i].velocity
        diff_v = ego_v - (total_v/count)
        differential_v.append(diff_v)
    return differential_v

def get_stats(scenario, safety_csv_list):
    long_dist_list = long_dist(scenario)
    lane_tracking_list = lane_tracking(scenario)
    relative_speed_list = relative_speed(scenario)
    
    long_dist_row = [scenario.scenario_id] + ['long_dist'] + long_dist_list
    lane_tracking_row = [scenario.scenario_id] + ['lane_tracking'] + lane_tracking_list
    relative_speed_row = [scenario.scenario_id] + ['relative_speed'] + relative_speed_list

    safety_csv_list.append(long_dist_row)
    safety_csv_list.append(lane_tracking_row)
    safety_csv_list.append(relative_speed_row)
    
    