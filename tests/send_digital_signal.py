import compas_rrc as rrc

if __name__ == '__main__':

    # Create Ros Client
    ros = rrc.RosClient()
    ros.run()

    # Create ABB Client
    abb = rrc.AbbClient(ros, '/rob1')
    print('Connected.')

    # Send a digital signal
    abb.send(rrc.SetDigital('Ausgang_100_0',0))

    # Wait for a bit
    abb.send(rrc.WaitTime(2))

    # End of Code
    abb.send(rrc.PrintText('Finished communicating'))

    # Close client
    ros.close()
    ros.terminate()
