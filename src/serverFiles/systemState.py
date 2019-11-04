from grpcFiles import systemstate_pb2
from grpcFiles import systemstate_pb2_grpc

from db.system_state.stateDb import StateDB


class SystemStateServer(systemstate_pb2_grpc.SystemStateServicer):
    def saveState(self, request, context):
        # TODO salvar estado no banco
        print("REQUEST IS TO SAVE STATE")
