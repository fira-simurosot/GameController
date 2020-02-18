# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: REF2CLI/service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from REF2CLI import messages_pb2 as REF2CLI_dot_messages__pb2
import common_pb2 as common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='REF2CLI/service.proto',
  package='fira_message.ref_to_cli',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x15REF2CLI/service.proto\x12\x17\x66ira_message.ref_to_cli\x1a\x16REF2CLI/messages.proto\x1a\x0c\x63ommon.proto2\xb4\x03\n\x07Referee\x12R\n\x08Register\x12!.fira_message.ref_to_cli.TeamInfo\x1a!.fira_message.ref_to_cli.TeamName\"\x00\x12W\n\x0bRunStrategy\x12$.fira_message.ref_to_cli.Environment\x1a .fira_message.ref_to_cli.Command\"\x00\x12\x45\n\x07SetBall\x12$.fira_message.ref_to_cli.Environment\x1a\x12.fira_message.Ball\"\x00\x12Z\n\x0fSetFormerRobots\x12$.fira_message.ref_to_cli.Environment\x1a\x1f.fira_message.ref_to_cli.Robots\"\x00\x12Y\n\x0eSetLaterRobots\x12$.fira_message.ref_to_cli.Environment\x1a\x1f.fira_message.ref_to_cli.Robots\"\x00\x62\x06proto3'
  ,
  dependencies=[REF2CLI_dot_messages__pb2.DESCRIPTOR,common__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_REFEREE = _descriptor.ServiceDescriptor(
  name='Referee',
  full_name='fira_message.ref_to_cli.Referee',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=89,
  serialized_end=525,
  methods=[
  _descriptor.MethodDescriptor(
    name='Register',
    full_name='fira_message.ref_to_cli.Referee.Register',
    index=0,
    containing_service=None,
    input_type=REF2CLI_dot_messages__pb2._TEAMINFO,
    output_type=REF2CLI_dot_messages__pb2._TEAMNAME,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RunStrategy',
    full_name='fira_message.ref_to_cli.Referee.RunStrategy',
    index=1,
    containing_service=None,
    input_type=REF2CLI_dot_messages__pb2._ENVIRONMENT,
    output_type=REF2CLI_dot_messages__pb2._COMMAND,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetBall',
    full_name='fira_message.ref_to_cli.Referee.SetBall',
    index=2,
    containing_service=None,
    input_type=REF2CLI_dot_messages__pb2._ENVIRONMENT,
    output_type=common__pb2._BALL,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetFormerRobots',
    full_name='fira_message.ref_to_cli.Referee.SetFormerRobots',
    index=3,
    containing_service=None,
    input_type=REF2CLI_dot_messages__pb2._ENVIRONMENT,
    output_type=REF2CLI_dot_messages__pb2._ROBOTS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetLaterRobots',
    full_name='fira_message.ref_to_cli.Referee.SetLaterRobots',
    index=4,
    containing_service=None,
    input_type=REF2CLI_dot_messages__pb2._ENVIRONMENT,
    output_type=REF2CLI_dot_messages__pb2._ROBOTS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_REFEREE)

DESCRIPTOR.services_by_name['Referee'] = _REFEREE

# @@protoc_insertion_point(module_scope)
