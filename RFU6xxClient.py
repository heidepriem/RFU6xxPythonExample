'''
Created on 29.11.2021

@author: Sebastian Heidepriem (SICK AG)
'''
from asyncua.client.client import Client
from asyncua.common.node import Node
from asyncua.ua.uatypes import ExtensionObject, ByteString, Int32
from asyncua.common.node import ua
import struct
import string

class RFU6xxClient(object):
    
    client : Client = None
    nsAutoID : int = 0
    nsOpcDI : int = 0
    nsRfu : int = 0
    
    rfu6xxNode : Node = None

    
    async def init(self):
        self.nsAutoID = await self.client.get_namespace_index('http://opcfoundation.org/UA/AutoID/') #3
        self.nsOpcDI = await self.client.get_namespace_index('http://opcfoundation.org/UA/DI/') #2
        self.nsRfu = await self.client.get_namespace_index('http://www.sick.com/RFU6xx/') #4
        objects = self.client.nodes.objects
        deviceSet = await objects.get_child(f"{self.nsOpcDI}:DeviceSet")
        self.rfu6xxNode = await deviceSet.get_child(f"{self.nsRfu}:RFU6xx")
         
    def __init__(self, client: Client):
        self.client = client 
        
        
    async def StartScan(self,duration : float, cycle: int, dataAvailable : bool):
        db = struct.pack("IdI?",0,duration,cycle,dataAvailable)
        eo = ExtensionObject(TypeId=ua.NodeId.from_string(f"ns={self.nsAutoID};i=3010"), Body=db)
        return await self.rfu6xxNode.call_method(f"{self.nsAutoID}:ScanStart", eo)
         
    async def StopScan(self):
        return await self.rfu6xxNode.call_method(f"{self.nsAutoID}:ScanStop")

    async def WriteTag(self, id : string, bank : int, offset : int, value: bytes):
        ba = bytearray()
        l = 0;
        for i in range(0,len(id),2) :
            l += 1
            sub = id[i:i+2]
            ba += bytearray.fromhex(sub)

        db = struct.pack("II",2,l) + ba
        eo = ExtensionObject(TypeId=ua.NodeId.from_string(f"ns={self.nsAutoID};i=5030"),Body=db)
        return await self.rfu6xxNode.call_method(f"{self.nsAutoID}:WriteTag",eo,"RAW:STRING",Int32(bank),Int32(offset),ByteString(value),ByteString())

    async def ReadTag(self, id : string, bank : int, offset : int, length : int):
        ba = bytearray()
        l = 0;
        for i in range(0,len(id),2) :
            l += 1
            sub = id[i:i+2]
            ba += bytearray.fromhex(sub)

        db = struct.pack("II",2,l) + ba
        eo = ExtensionObject(TypeId=ua.NodeId.from_string(f"ns={self.nsAutoID};i=5030"),Body=db)
        return await self.rfu6xxNode.call_method(f"{self.nsAutoID}:ReadTag",eo,"RAW:STRING",Int32(bank),Int32(offset),Int32(length),ByteString())
        
    async def readLastScanData(self):   
        node = await self.rfu6xxNode.get_child(f"{self.nsAutoID}:LastScanData")
        return await node.read_value() 