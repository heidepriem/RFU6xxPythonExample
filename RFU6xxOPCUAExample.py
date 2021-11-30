'''
Created on 29.11.2021

@author: Sebastian Heidepriem (SICK AG)
'''
import asyncio
from asyncua import Client
import traceback
from RFU6xxClient import RFU6xxClient
from asyncio.tasks import sleep
from asyncua.ua.uaerrors._auto import BadInvalidState

async def main():
        # starts a asyncua client instance, automatically stops it once the code segment is passed  
    url = "opc.tcp://192.168.188.25:4840"  # local simulated server address
    async with Client(url) as client:   
        try:
            rfu = RFU6xxClient(client)
            await rfu.init()
            try:
                await rfu.StartScan(0.0, 0, False)
            except BadInvalidState as e:
                print("StartScan returned BadInvalidState: Was the scanning already active?")
            await sleep(1.0)
            IDname = await rfu.readLastScanData()
            await rfu.StopScan()
            writeResult = await rfu.WriteTag(IDname,3,0,b'affedeafbeadaffe')
            print(writeResult)
            readResult = await rfu.ReadTag(IDname, 3, 0, 16)
            print(readResult[0])
        except Exception as e:
            print(f"################## Aborted by {e}")
            print(traceback.format_exc())
            #await client.close_session()
        print("ended")

if __name__ == '__main__':
    asyncio.run(main())
    pass