# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE = """\
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Home Automation</title>
	<style>
	    .background
                {
                    position: absolute;
                    top: 6px;
		    left: 12px;
		    color: white;
		}

	    .btnpos1
		{
		    position: absolute;
		    top: 8px;
		    left: 16px;
		    background-color: transparent;
		}
	    .btnpos2
		{
		    position: absolute;
		    top: 8px;
		    left: 80px;
		    background-color: transparent;
		}
            .btnpos3
		{
		    position: absolute;
		    top: 8px;
		    left: 144px;
		    background-color: transparent;
		}
            .btnpos4
		{
		    position: absolute;
		    top: 8px;
		    left: 208px;
		    background-color: transparent;
		}
            .btnpos5
		{
		    position: absolute;
		    top: 8px;
		    left: 272px;
		    background-color: transparent;
		}
            .btnpos6
		{
		    position: absolute;
		    top: 8px;
		    left: 336px;
		    background-color: transparent;
		}
		
	</style>

    </head>
    <body>
	<p id="btnpos1"></p>
	<p id="btnpos2"></p>
	<p id="btnpos3"></p>
	<p id="btnpos4"></p>
	<p id="btnpos5"></p>
	<p id="btnpos6"></p>
	<script>
            function myFunction() 
            {
                document.getElementById("btnpos1").innerHTML = "btnpos1";
                document.getElementById("btnpos2").innerHTML = "btnpos2";
                document.getElementById("btnpos3").innerHTML = "btnpos3";
                document.getElementById("btnpos4").innerHTML = "btnpos4";
                document.getElementById("btnpos5").innerHTML = "btnpos5";
                document.getElementById("btnpos6").innerHTML = "btnpos6";                
	    }
	</script>
	
        <div class="left background">
            <left><img src="stream.mjpg" width="640" height="360"></left>
            
            <td> <input type="button" class="btnpos1" value="Button1" onClick="myFunction()"> </td>
	    <td> <input type="button" class="btnpos2" value="Button2" onClick="myFunction()"> </td>
	    <td> <input type="button" class="btnpos3" value="Button3" onClick="myFunction()"> </td>
	    <td> <input type="button" class="btnpos4" value="Button4" onClick="myFunction()"> </td>
	    <td> <input type="button" class="btnpos5" value="Button5" onClick="myFunction()"> </td>
	    <td> <input type="button" class="btnpos6" value="Button6" onClick="myFunction()"> </td>
	</div>

    </body>
</html>
""";
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

######program start here################################################
    
with picamera.PiCamera(resolution='640x360', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
