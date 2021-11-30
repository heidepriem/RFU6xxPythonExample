# RFU6xxPythonExample
An example of connecting an using RFU6xx with AIM AutoID spec. with Python asyncua (freeopcua)

The main() function is in RFU6xxOPCUAExample.py. It uses "asyncua" which is said to be the better OPC UA implementation.
Install: 
>> pip install asyncua
The class encapsulating the functions
StartScan()
StopScan()
ReadTag()
WriteTag()
readLastScanData()
is found in RFU6xxClient.py which shall be in the root folder where Python excepts sources.

The example
1. switches on scanning (and skips in case of bad state)
2. waits 1 second
3. reads the variable LastScanData to retrieve the ID of a tag in front of the anntenna
4. stops the scanning
5. writes a meaningless sequence to bank 3, offset 0
6. reads some bytes out of bank 3, offset 0

Only identifier type "String" is being used.
