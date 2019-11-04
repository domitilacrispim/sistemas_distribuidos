# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: birdwiki.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='birdwiki.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0e\x62irdwiki.proto\"\x18\n\x08\x42irdName\x12\x0c\n\x04name\x18\x01 \x01(\t\"9\n\x08\x42irdInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x65\x64iting\x18\x02 \x01(\x08\x12\x0e\n\x06\x65\x64itor\x18\x03 \x01(\t\"&\n\x08\x42irdPage\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"\x1d\n\x0c\x43onfirmation\x12\r\n\x05saved\x18\x01 \x01(\x08\x32\xc4\x01\n\x08\x42irdWiki\x12%\n\tlistBirds\x12\t.BirdName\x1a\t.BirdInfo\"\x00\x30\x01\x12!\n\x07getBird\x12\t.BirdName\x1a\t.BirdInfo\"\x00\x12\"\n\x08readBird\x12\t.BirdName\x1a\t.BirdPage\"\x00\x12\"\n\x08\x65\x64itBird\x12\t.BirdName\x1a\t.BirdPage\"\x00\x12&\n\x08saveBird\x12\t.BirdPage\x1a\r.Confirmation\"\x00\x62\x06proto3')
)




_BIRDNAME = _descriptor.Descriptor(
  name='BirdName',
  full_name='BirdName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='BirdName.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=42,
)


_BIRDINFO = _descriptor.Descriptor(
  name='BirdInfo',
  full_name='BirdInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='BirdInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='editing', full_name='BirdInfo.editing', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='editor', full_name='BirdInfo.editor', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=101,
)


_BIRDPAGE = _descriptor.Descriptor(
  name='BirdPage',
  full_name='BirdPage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='BirdPage.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='BirdPage.text', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=141,
)


_CONFIRMATION = _descriptor.Descriptor(
  name='Confirmation',
  full_name='Confirmation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='saved', full_name='Confirmation.saved', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=172,
)

DESCRIPTOR.message_types_by_name['BirdName'] = _BIRDNAME
DESCRIPTOR.message_types_by_name['BirdInfo'] = _BIRDINFO
DESCRIPTOR.message_types_by_name['BirdPage'] = _BIRDPAGE
DESCRIPTOR.message_types_by_name['Confirmation'] = _CONFIRMATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BirdName = _reflection.GeneratedProtocolMessageType('BirdName', (_message.Message,), {
  'DESCRIPTOR' : _BIRDNAME,
  '__module__' : 'birdwiki_pb2'
  # @@protoc_insertion_point(class_scope:BirdName)
  })
_sym_db.RegisterMessage(BirdName)

BirdInfo = _reflection.GeneratedProtocolMessageType('BirdInfo', (_message.Message,), {
  'DESCRIPTOR' : _BIRDINFO,
  '__module__' : 'birdwiki_pb2'
  # @@protoc_insertion_point(class_scope:BirdInfo)
  })
_sym_db.RegisterMessage(BirdInfo)

BirdPage = _reflection.GeneratedProtocolMessageType('BirdPage', (_message.Message,), {
  'DESCRIPTOR' : _BIRDPAGE,
  '__module__' : 'birdwiki_pb2'
  # @@protoc_insertion_point(class_scope:BirdPage)
  })
_sym_db.RegisterMessage(BirdPage)

Confirmation = _reflection.GeneratedProtocolMessageType('Confirmation', (_message.Message,), {
  'DESCRIPTOR' : _CONFIRMATION,
  '__module__' : 'birdwiki_pb2'
  # @@protoc_insertion_point(class_scope:Confirmation)
  })
_sym_db.RegisterMessage(Confirmation)



_BIRDWIKI = _descriptor.ServiceDescriptor(
  name='BirdWiki',
  full_name='BirdWiki',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=175,
  serialized_end=371,
  methods=[
  _descriptor.MethodDescriptor(
    name='listBirds',
    full_name='BirdWiki.listBirds',
    index=0,
    containing_service=None,
    input_type=_BIRDNAME,
    output_type=_BIRDINFO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getBird',
    full_name='BirdWiki.getBird',
    index=1,
    containing_service=None,
    input_type=_BIRDNAME,
    output_type=_BIRDINFO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='readBird',
    full_name='BirdWiki.readBird',
    index=2,
    containing_service=None,
    input_type=_BIRDNAME,
    output_type=_BIRDPAGE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='editBird',
    full_name='BirdWiki.editBird',
    index=3,
    containing_service=None,
    input_type=_BIRDNAME,
    output_type=_BIRDPAGE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='saveBird',
    full_name='BirdWiki.saveBird',
    index=4,
    containing_service=None,
    input_type=_BIRDPAGE,
    output_type=_CONFIRMATION,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_BIRDWIKI)

DESCRIPTOR.services_by_name['BirdWiki'] = _BIRDWIKI

# @@protoc_insertion_point(module_scope)