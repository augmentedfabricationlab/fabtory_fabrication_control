import compas_rrc as rrc

if __name__ == '__main__':

    # Create Ros Client
    ros = rrc.RosClient()
    ros.run()

    # Create ABB Client
    abb = rrc.AbbClient(ros, '/rob1')
    print('Connected.')

    # Print text on FlexPenant
    abb.send(rrc.PrintText('Welcome TUM to COMPAS_RRC ;)'))

    # Define robot joint positions
    robot_pos_joints_park = [-90.0, -30.0, 70.0, 0.0, 50.0, 0.0]
    robot_pos_joints_start = [-135.0, 30.0, 20.0, 0.0, 30.0, 0.0]

    # Define track joint positions 
    track_pos_joint_park = [0.0]
    track_pos_joint_start = [3342.0]

    # Set speed [mm/s]
    speed = 1000
    
    # Move to start position 
    done = abb.send_and_wait(rrc.MoveToJoints(robot_pos_joints_start, track_pos_joint_start, speed, rrc.Zone.FINE))

    # Move to park position
    done = abb.send_and_wait(rrc.MoveToJoints(robot_pos_joints_park, track_pos_joint_park, speed, rrc.Zone.FINE))

    # Print feedback 
    print('Feedback = ', done)

    # End of Code
    print('Finished')

    # Close client
    ros.close()
    ros.terminate()
