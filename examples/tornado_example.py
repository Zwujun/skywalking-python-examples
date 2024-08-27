import os

from tornado import httpserver
from tornado import web, ioloop


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return web.Application([
        (r"/", MainHandler),
    ])


def skywalking_agent():
    """setup skywalking agent"""
    if not os.getenv("SW_ENABLE"):
        return
    from skywalking import agent, config
    config.init(
        agent_collector_backend_services=os.getenv("SW_AGENT_COLLECTOR_BACKEND_SERVICES"),
        agent_name=os.getenv("SW_AGENT_NAME"),
        agent_instance_name=os.getenv("SW_AGENT_INSTANCE_NAME"),
        agent_trace_ignore_path=os.getenv("SW_AGENT_TRACE_IGNORE_PATH")
    )
    agent.start()
    print("skywalking_agent setup complete")


application = make_app()

server = httpserver.HTTPServer(application)
server.bind(8888, '0.0.0.0')
server.start(2)

# 在子进程中启动
skywalking_agent()

ioloop.IOLoop.instance().start()
