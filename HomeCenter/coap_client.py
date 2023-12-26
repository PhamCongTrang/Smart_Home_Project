import asyncio
from aiocoap import Context, Message, Code

async def coap_client():
    # Modify the URI to match the server's IP address and port
    uri = "coap://192.168.66.243:5683/hello"

    # Create a CoAP request message
    request = Message(code=Code.GET, uri=uri)

    try:
        # Create a CoAP context and send the request
        async with Context() as context:
            response = await context.request(request).response

            # Print the response payload
            print(f"Response Code: {response.code}")
            print(f"Response Payload: {response.payload.decode('utf-8')}")

    except Exception as e:
        print(f"Failed to fetch resource: {e}")

if __name__ == "__main__":
    # Run the CoAP client
    try:
        asyncio.run(coap_client())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
