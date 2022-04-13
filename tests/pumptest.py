
import asyncio
#import sys
# sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua
import time

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    url = 'opc.tcp://192.168.125.10:4840/freeopcua/server/'
    # url = 'opc.tcp://commsvr.com:51234/UA/CAS_UA_Server'
    async with Client(url=url) as client:

        

        node_1 = client.get_node('ns=4;s=|var|ECC2100 0.8S 1131.Application.GVL_OPC.Ready_for_operation')
        print(node_1)
        value = await node_1.read_value()

        await node_1.write_value(True) # set node value using implicit data type
        value = await node_1.read_value()
        print(value)

        node_2 = client.get_node('ns=4;s=|var|ECC2100 0.8S 1131.Application.GVL_OPC.aut_mixingpump_fc')
        print(node_2)
        value = await node_2.read_value()

        await node_2.write_value(True) # set node value using implicit data type
        value = await node_2.read_value()
        print(value)

        node_3 = client.get_node('ns=4;s=|var|ECC2100 0.8S 1131.Application.GVL_OPC.aut_waterpump')
        print(node_3)
        value = await node_3.read_value()

        await node_3.write_value(True) # set node value using implicit data type
        value = await node_3.read_value()
        print(value)

        node_4 = client.get_node('ns=4;s=|var|ECC2100 0.8S 1131.Application.GVL_OPC.Remote_start')
        print(node_4)
        value = await node_4.read_value()

        await node_4.write_value(True) # set node value using implicit data type
        value = await node_4.read_value()
        print(value)
       

        #print(value)

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        # Node objects have methods to read and write node attributes as well as browse or populate address space
        #_logger.info('Children of root are: %r', await client.nodes.root.get_children())

        # get a specific node knowing its node id
        #var = client.nodes.root.get_child(["0:Objects", f"{87}:MyObject", f"{87}:MyVariable"])
        #print("My variable", var, await var.read_value())
        # print(var)
        # await var.read_data_value() # get value of node as a DataValue object
        # await var.read_value() # get value of node as a python builtin
        # await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #await node.write_value(True) # set node value using implicit data type
        #value = await node.read_value()
        #print(value)

        #time.sleep(60)

        #await node.write_value(False) # set node value using implicit data type
        #value = await node.read_value()
        #print(value)

        #time.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())