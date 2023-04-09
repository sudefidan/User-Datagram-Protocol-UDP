import asyncio
import websockets
import base64
import struct
import time

async def main():
    uri = "ws://localhost:5612"
    async with websockets.connect(uri) as websocket:
        # After joining server will send client unique id.
        await recv_and_decode_packet(websocket)
        #TASK3
        while True:
            await send_packet(websocket, 0, 542, b'1111') 
            await recv_and_decode_packet(websocket) 
            time.sleep(1)

async def send_packet(websocket, source_port, dest_port, payload):
    # Convert port numbers to bytes
    source_bytes = source_port.to_bytes(2, 'little')
    dest_bytes = dest_port.to_bytes(2, 'little')
    
    # Calculate packet length and convert to bytes
    packet_length = len(payload) + 8
    len_bytes = packet_length.to_bytes(2, 'little')
    
    # Calculate checksum and convert to bytes
    checksum = checksum_validation(source_port, dest_port, payload)
    checksum_bytes = checksum.to_bytes(2, 'little')
    
    # Combine all parts into packet
    packet = source_bytes + dest_bytes + len_bytes + checksum_bytes + payload
    
    # Send packet over websocket
    await websocket.send(base64.b64encode(packet))

#TASK1
async def recv_and_decode_packet(websocket):
    # Recieve the udp packet as a base64-encoded string
    packet64 = await websocket.recv()
    
    # Decode packet64
    packet = base64.b64decode(packet64) 

    # Get source port
    source_port = int.from_bytes(packet[0:2], 'little')

    # Get destination port 
    dest_port = int.from_bytes(packet[2:4], 'little') 

    # Get data lentgh
    data_length = int.from_bytes(packet[4:6], 'little') 

    # Get checksum
    checksum = int.from_bytes(packet[6:8], 'little') 

    # Get payload
    payload = packet[8:(data_length+8)] 
    
    # Checksum validation
    is_checksum = checksum_validation(source_port, dest_port, payload)
    if is_checksum:
        print("\n--------CORRECT CHECKSUM HAS BEEN CALCULATED !!!--------")
        print("\nBase64: " + str(packet64) + "\nServer Sent: " + str(packet) +  "\nSource Port: " + str(source_port)+ "\nDest Port: " + str(dest_port) + "\nData Length: " + str(data_length) + "\nChecksum: " + str(checksum)+ "\nPayload: " + str(payload.decode("utf-8")) + "\n")
    else: 
        print("ERROR: CHECKSUM IS NOT CORRECT !!!")

#TASK2
def checksum_validation(source_port: int, destination_port: int, payload: bytes)-> bool:
    checksum=0

    # Packet length = payload + 8
    length = len(payload) + 8

    # Temporary checksum
    temp = destination_port.to_bytes(2, 'little') + source_port.to_bytes(2, 'little') + length.to_bytes(2, byteorder="little") + payload
    packet_length = len(temp)

    if packet_length % 2 != 0:
        temp += struct.pack("!B", 0)
  
    for i in range(0, packet_length, 2):
        temp_sum = (temp[i] << 8) + (temp[i+1])
        checksum += temp_sum

    # Performs 1s complement
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    
    return checksum


if __name__ == "__main__": 
    asyncio.run(main())
    