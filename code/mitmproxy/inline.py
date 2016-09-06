# -*- coding: utf-8 -*-

import logging
from logging import FileHandler
from mitmproxy.script import concurrent, ScriptContext
from pythonjsonlogger import jsonlogger


logging.basicConfig(filename="sniff.log")
logger = logging.getLogger(__name__)

json_log_handler = FileHandler(__file__+".log")
formatter = jsonlogger.JsonFormatter("%(asctime)s - %(message)s")
json_log_handler.setFormatter(formatter)
logger.addHandler(json_log_handler)
logger.setLevel(logging.INFO)


# @concurrent
# def response(context, flow):
#     context.log(flow.request)
#     flow_dup = context.duplicate_flow(flow)
#     flow_dup.request.host = "121.41.41.54"
#     flow_dup.request.port = 11112
#     # context.replay_request(flow_dup)
#     context.log("duplicated: {}".format(flow_dup.request))
#     context.replay_request(flow_dup)


class Counter(object):

    def __init__(self):
        self._index = 0

    def __call__(self, *args, **kwargs):
        self._index += 1
        return self._index


counter = Counter()


def generate_request_info(request):
    api = request.method + " " + request.url + " "
    if request.method.lower() == "get":
        query = None
        if request.query:
            query = {item[0]: item[1] for item in request.query}
        return {"api": api, "query": query}
    elif request.urlencoded_form:
        return {"api": api, "form": request.urlencoded_form}
    elif request.multipart_form:
        return {"api": api, "multipart form": request.multipart_form}
    else:
        return {"api": api, "payload": request.data.content}


@concurrent
def response(context, flow):
    content_type = flow.response.headers.get("Content-Type", "").lower()
    if "application/json" not in content_type:
        return
    index = counter()
    request_info = generate_request_info(flow.request)
    request_info["index"] = index
    logger.info("request info", extra=request_info)
    logger.info("response info", extra={"content": flow.response.content, "index": index})
