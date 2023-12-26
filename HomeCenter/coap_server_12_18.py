import datetime
import logging
import asyncio
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap

class server_put(resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "
                b"with numbers to be large enough to trigger blockwise "
                b"transfer.\n")

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_put(self, request):
        payload = request.payload.decode('utf-8')
        print('PUT payload: %s' % payload)

        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"server_receive_put")

class server_get(resource.Resource):

    async def render_get(self, request):
        return aiocoap.Message(payload=b"server_receive_get")

logging.getLogger().addHandler(logging.NullHandler())

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['put'], server_put())
    root.add_resource(['get'], server_get())
    await aiocoap.Context.create_server_context(root, bind=('192.168.168.43', 5683))
    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())