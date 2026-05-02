import asyncio
import re

MOBILE_PATTERNS = [b'iPhone', b'iPad']

def is_mobile(header_bytes):
    ua = re.search(b'User-Agent: ([^\r\n]+)', header_bytes, re.IGNORECASE)
    if ua:
        return any(p in ua.group(1) for p in MOBILE_PATTERNS)
    return False

async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass

async def handle(client_r, client_w):
    header = b''
    try:
        while b'\r\n\r\n' not in header:
            chunk = await asyncio.wait_for(client_r.read(4096), timeout=10)
            if not chunk:
                client_w.close()
                return
            header += chunk
    except Exception:
        client_w.close()
        return

    port = 7683 if is_mobile(header) else 7682

    for attempt in range(5):
        try:
            srv_r, srv_w = await asyncio.open_connection('127.0.0.1', port)
            break
        except Exception:
            if attempt == 4:
                client_w.close()
                return
            await asyncio.sleep(0.5)

    srv_w.write(header)
    await srv_w.drain()
    await asyncio.gather(pipe(client_r, srv_w), pipe(srv_r, client_w))

async def main():
    srv = await asyncio.start_server(handle, '0.0.0.0', 7681)
    async with srv:
        await srv.serve_forever()

asyncio.run(main())
