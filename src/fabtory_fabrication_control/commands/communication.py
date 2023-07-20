import compas_rrc as rrc

def close(robot):
    robot.abb_client.send(rrc.SetDigital('Ausgang_100_1', 0))
    robot.abb_client.send(rrc.SetDigital('Ausgang_100_0', 1))
    #robot.abb_client.send(rrc.WaitTime(2))


def release(robot):
    robot.abb_client.send(rrc.SetDigital('Ausgang_100_0', 0))
    robot.abb_client.send(rrc.SetDigital('Ausgang_100_1', 1))
    #robot.abb_client.send(rrc.WaitTime(2))