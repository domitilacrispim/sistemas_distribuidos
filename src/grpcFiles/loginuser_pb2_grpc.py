# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from grpcFiles import loginuser_pb2 as loginuser__pb2


class LoginUserStub(object):
  """Definição do serviço
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.login = channel.unary_unary(
        '/LoginUser/login',
        request_serializer=loginuser__pb2.UserLogin.SerializeToString,
        response_deserializer=loginuser__pb2.UserInfo.FromString,
        )


class LoginUserServicer(object):
  """Definição do serviço
  """

  def login(self, request, context):
    """Recebe a página do passarinho
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_LoginUserServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'login': grpc.unary_unary_rpc_method_handler(
          servicer.login,
          request_deserializer=loginuser__pb2.UserLogin.FromString,
          response_serializer=loginuser__pb2.UserInfo.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'LoginUser', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
