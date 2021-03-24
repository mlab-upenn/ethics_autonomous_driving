from commonroad.scenario.scenario import Tag

interstate = 0
interstate_success = 0

urban = 0
urban_success = 0

highway = 0
highway_success = 0

comfort = 0
comfort_success = 0

critical = 0
critical_success = 0

evasive = 0
evasive_success = 0

cut_in = 0
cut_in_success = 0

illegal_cutin = 0
illegal_cutin_success = 0

intersection = 0
intersection_success = 0

lane_change = 0
lane_change_success = 0

lane_following = 0
lane_following_success = 0

merging_lanes = 0
merging_lanes_success = 0

multi_lane = 0
multi_lane_success = 0

oncoming_traffic = 0
oncoming_traffic_success = 0

no_oncoming_traffic = 0
no_oncoming_traffic_success = 0

parallel_lanes = 0
parallel_lanes_success = 0

race_track = 0
race_track_success = 0

roundabout = 0
roundabout_success = 0

rural = 0
rural_success = 0

simulated = 0
simulated_success = 0

single_lane = 0
single_lane_success = 0

slip_road = 0
slip_road_success = 0

speed_limit = 0
speed_limit_success = 0

traffic_jam = 0
traffic_jam_success = 0

turn_left = 0
turn_left_success = 0

turn_right = 0
turn_right_success = 0

two_lane = 0
two_lane_success = 0

emergency_braking = 0
emergency_braking_success = 0

def sort_scenario(scenario_id, scenario_loader, is_success):
    scenario, planning_problem_set = scenario_loader.load_scenario(scenario_id)
    for tag in scenario.tags:
       
        if tag == Tag.INTERSTATE:
            global interstate
            interstate += 1
            if is_success:
                global interstate_success
                interstate_success += 1
        
        if tag == Tag.URBAN:
            global urban 
            urban += 1
            if is_success:
                global urban_success 
                urban_succes +=1
        
        if tag == Tag.HIGHWAY:
            global highway 
            highway += 1
            if is_success:
                global highway_success
                highway_success += 1
                
        if tag == Tag.COMFORT:
            global comfort
            comfort += 1
            if is_success:
                global comfort_success 
                comfort_success += 1
                
        if tag == Tag.CRITICAL:
            global critical
            critical += 1
            if is_success:
                global critical_success
                critical_success += 1
                
        if tag == Tag.EVASIVE:
            global evasive
            evasive += 1
            if is_success:
                global evasive_success
                evasive_success += 1
                
        if tag == Tag.CUT_IN:
            global cut_in
            cut_in += 1
            if is_success:
                global cut_in_success
                cut_in_success += 1
                
        if tag == Tag.ILLEGAL_CUTIN:
            global illegal_cutin
            illegal_cutin += 1
            if is_success:
                global illegal_cutin_success
                illegal_cutin_success += 1
                
        if tag == Tag.INTERSECTION:
            global intersection
            intersection += 1
            if is_success:
                global intersection_success
                intersection_success += 1
                
        if tag == Tag.LANE_CHANGE: 
            global lane_change
            lane_change += 1
            if is_success:
                global lane_change_success
                lane_change_success += 1
                
        if tag == Tag.LANE_FOLLOWING:
            global lane_following
            lane_following += 1
            if is_success:
                global lane_following_success
                lane_following_success += 1
                
        if tag == Tag.MERGING_LANES:
            global merging_lanes
            merging_lanes += 1
            if is_success:
                global merging_lanes_success
                merging_lanes_success += 1
                
        if tag == Tag.MULTI_LANE:
            global multi_lane
            multi_lane += 1
            if is_success:
                global multi_lane_success
                multi_lane_success += 1
                
        if tag == Tag.ONCOMING_TRAFFIC:
            global oncoming_traffic
            oncoming_traffic += 1
            if is_success:
                global oncoming_traffic_success
                oncoming_traffic_success += 1
                
        if tag == Tag.NO_ONCOMING_TRAFFIC:
            global no_oncoming_traffic
            no_oncoming_traffic += 1
            if is_success:
                global no_oncoming_traffic_success
                no_oncoming_traffic_success += 1
                
        if tag == Tag.PARALLEL_LANES:
            global parallel_lanes
            parallel_lanes += 1
            if is_success:
                global parallel_lanes_success
                parallel_lanes_success += 1
                
        if tag == Tag.RACE_TRACK:
            global race_track
            race_track += 1
            if is_success:
                global race_track_success
                race_track_success += 1
                
        if tag == Tag.ROUNDABOUT:
            global roundabout
            roundabout += 1
            if is_success:
                global roundabout_success
                roundabout_success += 1
                
        if tag == Tag.RURAL:
            global rural
            rural += 1
            if is_success:
                global rural_success
                rural_success += 1
                
        if tag == Tag.SIMULATED:
            global simulated
            simulated += 1
            if is_success:
                global simulated_success
                simulated_success += 1
                
        if tag == Tag.SINGLE_LANE:
            global single_lane
            single_lane += 1
            if is_success:
                global single_lane_success
                single_lane_success += 1
                
        if tag == Tag.SLIP_ROAD:
            global slip_road
            slip_road += 1
            if is_success:
                global slip_road_success
                slip_road_success += 1
                
        if tag == Tag.SPEED_LIMIT:
            global speed_limit
            speed_limit += 1
            if is_success:
                global speed_limit_success
                speed_limit_success += 1
                
        if tag == Tag.TRAFFIC_JAM:
            global traffic_jam
            traffic_jam += 1
            if is_success:
                global traffic_jam_success
                traffic_jam_success += 1
                
        if tag == Tag.TURN_LEFT:
            global turn_left
            turn_left += 1
            if is_success:
                global turn_left_success
                turn_left_success += 1
                
        if tag == Tag.TURN_RIGHT:
            global turn_right
            turn_right += 1
            if is_success:
                global turn_right_success
                turn_right_success += 1
                
        if tag == Tag.TWO_LANE:
            global two_lane
            two_lane += 1
            if is_success:
                global two_lane_success
                two_lane_success += 1
                
        if tag == Tag.EMERGENCY_BRAKING:
            global emergency_braking
            emergency_braking += 1
            if is_success:
                global emergency_braking_success
                emergency_braking_success += 1
                
def print_stats():
    print(f"Interstate solutions found: {interstate_success}/{interstate}")
    print(f"Urban solutions found: {urban_success}/{urban}")
    print(f"Highway solutions found: {highway_success}/{highway}")
    print(f"Comfort solutions found: {comfort_success}/{comfort}")
    print(f"Critical solutions found: {critical_success}/{critical}")
    print(f"Evasive solutions found: {evasive_success}/{evasive}")
    print(f"Cut in solutions found: {cut_in_success}/{cut_in}")
    print(f"Illegal cut in solutions found: {illegal_cutin_success}/{illegal_cutin}")
    print(f"Intersection solutions found: {intersection_success}/{intersection}")
    print(f"Lane change solutions found: {lane_change_success}/{lane_change}")
    print(f"Lane following solutions found: {lane_following_success}/{lane_following}")
    print(f"Merging lanes solutions found: {merging_lanes_success}/{merging_lanes}")
    print(f"Multi lane solutions found: {multi_lane_success}/{multi_lane}")
    print(f"Oncoming traffic solutions found: {oncoming_traffic_success}/{oncoming_traffic}")
    print(f"Parallel lanes solutions found: {parallel_lanes_success}/{parallel_lanes}")
    print(f"Race track solutions found: {race_track_success}/{race_track}")
    print(f"Roundabout solutions found: {roundabout_success}/{roundabout}")
    print(f"Rural solutions found: {rural_success}/{rural}")
    print(f"Simulated solutions found: {simulated_success}/{simulated}")
    print(f"Single lane solutions found: {single_lane_success}/{single_lane}")
    print(f"Slip road solutions found: {slip_road_success}/{slip_road}")
    print(f"Speed limit solutions found: {speed_limit_success}/{speed_limit}")
    print(f"Traffic jam solutions found: {traffic_jam_success}/{traffic_jam}")
    print(f"Turn left solutions found: {turn_left_success}/{traffic_jam}")
    print(f"Turn right solutions found: {turn_right_success}/{turn_right}")
    print(f"Two lane solutions found: {two_lane_success}/{two_lane}")
    print(f"Emergency braking solutions found: {emergency_braking_success}/{emergency_braking}")
