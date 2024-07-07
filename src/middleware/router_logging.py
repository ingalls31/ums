import json
from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from uuid import uuid4
from typing import AsyncIterator, Callable
from starlette.types import Message
import time

def format_nested_dict_to_multiline(data, indent=0):
    """
    This function takes a nested dictionary or list and formats it into a list of strings.
    Each string represents a line of the formatted output.

    Parameters:
    data (dict or list): The nested dictionary or list to be formatted.
    indent (int): The number of indentation levels to add to each line. Default is 0.

    Returns:
    list: A list of strings, each representing a line of the formatted output.
    """

    # Initialize an empty list to store the formatted lines
    lines = []

    # Define the string to be used for each indentation level
    indent_str = '    ' * indent 

    # Check if the data is a dictionary
    if isinstance(data, dict):
        # Iterate over each key-value pair in the dictionary
        for key, value in data.items():
            # Check if the value is another dictionary or list
            if isinstance(value, (dict, list)):
                # Add the key to the formatted line
                lines.append(f"{indent_str}{key}:")
                # Recursively format the value and append its lines to the formatted lines
                lines.extend(format_nested_dict_to_multiline(value, indent + 1))
            else:
                # Add the key-value pair to the formatted line
                lines.append(f"{indent_str}{key}: {value}")
    # Check if the data is a list
    elif isinstance(data, list):
        # Iterate over each item in the list
        for index, item in enumerate(data):
            # Add the index to the formatted line
            lines.append(f"{indent_str}[{index}]")
            # Recursively format the item and append its lines to the formatted lines
            lines.extend(format_nested_dict_to_multiline(item, indent + 1))
    # If the data is neither a dictionary nor a list, add it as a line
    else:
        lines.append(f"{indent_str}{data}")

    # Return the formatted lines
    return lines

def format_log_to_multiline(log_dict):
    return '\n'.join(format_nested_dict_to_multiline(log_dict))

class AsyncIteratorWrapper:
    """The following is a utility class that transforms a
        regular iterable to an asynchronous one.

    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value

class RouterLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI,
            *,
            logger: logging.Logger
    ) -> None:
        self._logger = logger
        super().__init__(app)
   
    async def dispatch(self,
                       request: Request,
                       call_next: Callable
                       ) -> Response:
    
        request_id: str = str(uuid4())
        logging_dict = {
            "X-API-REQUEST-ID": request_id  # X-API-REQUEST-ID maps each request-response to a unique ID
        }

        await self.set_body(request)
        response, response_dict = await self._log_response(call_next,
                                                           request,
                                                           request_id
                                                           )
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict
        

        self._logger.info(format_log_to_multiline(logging_dict))

        return response

    async def set_body(self, request: Request):
        """Avails the response body to be logged within a middleware as,
            it is generally not a standard practice.

               Arguments:
               - request: Request
               Returns:
               - receive_: Receive
        """
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive
    
    async def _log_request(
            self,
            request: Request
    ) -> str:
        """Logs request part
            Arguments:
           - request: Request

        """

        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host
        }

        try:
            body = await request.json()
            request_logging["body"] = body
        except:
            body = None

        return request_logging
    
    async def _log_response(self,
                            call_next: Callable,
                            request: Request,
                            request_id: str
                            ) -> Response:
        """Logs response part

               Arguments:
               - call_next: Callable (To execute the actual path function and get response back)
               - request: Request
               - request_id: str (uuid)
               Returns:
               - response: Response
               - response_logging: str
        """

        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request, request_id)
        finish_time = time.perf_counter()

        overall_status = "successful" if response.status_code < 400 else "failed"
        execution_time = finish_time - start_time

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s"
        }

        resp_body = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

        try:
            resp_body = json.loads(resp_body[0].decode())
        except:
            resp_body = str(resp_body)

        response_logging["body"] = resp_body

        return response, response_logging

    async def _execute_request(self,
                               call_next: Callable,
                               request: Request,
                               request_id: str
                               ) -> Response:
        """Executes the actual path function using call_next.
               It also injects "X-API-Request-ID" header to the response.

               Arguments:
               - call_next: Callable (To execute the actual path function
                            and get response back)
               - request: Request
               - request_id: str (uuid)
               Returns:
               - response: Response
        """
        try:
            response: Response = await call_next(request)

            # Kickback X-Request-ID
            response.headers["X-API-Request-ID"] = request_id
            return response

        except Exception as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "reason": e
                }
            )