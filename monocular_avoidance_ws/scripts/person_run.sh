#!/bin/zsh


sphinx ~/Desktop/MixedRealityTesting/monocular_avoidance_ws/src/drone_controller/worlds/empty.world /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=first::stolen_interface=::pose="0 0 0.2 0 0 0"::with_front_cam=true /opt/parrot-sphinx/usr/share/sphinx/actors/pedestrian.actor::path=$HOME/Desktop/MixedRealityTesting/monocular_avoidance_ws/src/drone_controller/worlds/paths/test1_walk.path