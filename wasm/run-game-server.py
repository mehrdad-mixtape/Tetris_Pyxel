import http.server, socketserver, sys, argparse

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # self.path = '/run-game.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def main() -> None:
    Handler = MyHttpRequestHandler
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', help="bind address to server (default is 127.0.0.1)", required=False)
    parser.add_argument('-p', '--port', help="bind port to address of server (default is 8000)", type=int, required=False)
    args = parser.parse_args()

    ADDR = "127.0.0.1"
    PORT = 8000

    if args.addr:
        ADDR = args.addr
    if args.port:
        PORT = args.port

    with socketserver.TCPServer((ADDR, PORT), Handler) as httpd:
        print(f"""
            PyxelTetris Server Running on {ADDR}:{PORT}
            1. Open Your Browser And Go to URL: http://{ADDR}:{PORT}
            2. Click On 'game.html'
            3. Wait For Minutes (depends on your internet-quality)
            Do You Wanna Help? Run This:
                run-game-server --help
            Press Ctrl+C to Exit ..."""
        )
        httpd.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nGoodbye!")
