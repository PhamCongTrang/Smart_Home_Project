import asyncio
from aiocoap import Context, resource

async def hello(request):
    payload = b"Hello, CoAP!"
    return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=payload)

def main():
    # Create a resource for handling requests at the /hello path
    hello_resource = resource.Resource()
    hello_resource.render = hello

    # Create a CoAP context and set the root resource
    root = resource.Site()
    root.add_resource(("hello",), hello_resource)

    # Create and start the CoAP server
    asyncio.Task(Context.create_server_context(root, bind=('192:168:0:103', 5683)))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
