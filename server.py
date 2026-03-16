import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

#----------them test
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):

    def Add(self, request, context):
        return calculator_pb2.NumberReply(result=request.a + request.b)

    def Subtract(self, request, context):
        return calculator_pb2.NumberReply(result=request.a - request.b)

    def Multiply(self, request, context):
        return calculator_pb2.NumberReply(result=request.a * request.b)

    def Divide(self, request, context):
        return calculator_pb2.NumberReply(result=request.a / request.b)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Server running on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()

import math

def Square(self, request, context):
    return calculator_pb2.Result(result=request.a ** 2)

def Sqrt(self, request, context):
    return calculator_pb2.Result(result=math.sqrt(request.a))

def Sin(self, request, context):
    return calculator_pb2.Result(result=math.sin(request.a))

def Cos(self, request, context):
    return calculator_pb2.Result(result=math.cos(request.a))

def Tan(self, request, context):
    return calculator_pb2.Result(result=math.tan(request.a))
