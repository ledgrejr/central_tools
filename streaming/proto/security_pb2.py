# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: security.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='security.proto',
  package='Security',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0esecurity.proto\x12\x08Security\"\x1a\n\nMacAddress\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x02(\x0c\"s\n\x14RapidsStreamingEvent\x12\x0f\n\x07\x63ust_id\x18\x01 \x02(\t\x12#\n\x05rogue\x18\x02 \x03(\x0b\x32\x14.Security.RogueEvent\x12%\n\x08idsEvent\x18\x03 \x03(\x0b\x32\x13.Security.WIDSEvent\"\xab\x02\n\nRogueEvent\x12&\n\x08rogue_id\x18\x01 \x02(\x0b\x32\x14.Security.MacAddress\x12\x16\n\x0e\x63lassification\x18\x02 \x02(\r\x12\x12\n\nfirst_seen\x18\x03 \x01(\t\x12\x11\n\tlast_seen\x18\x04 \x01(\t\x12\x12\n\nrogue_name\x18\x05 \x01(\t\x12\x0c\n\x04ssid\x18\x06 \x01(\t\x12\x0f\n\x07lan_mac\x18\x07 \x01(\t\x12\x18\n\x10\x66irst_det_device\x18\x08 \x01(\t\x12\x17\n\x0flast_det_device\x18\t \x01(\t\x12\x12\n\nencryption\x18\n \x01(\r\x12\x0c\n\x04port\x18\x0b \x01(\t\x12\x1a\n\x12\x63ontainment_status\x18\x0c \x01(\t\x12\x12\n\nmac_vendor\x18\r \x01(\t\"\xd2\x01\n\tWIDSEvent\x12\x11\n\tdevice_id\x18\x01 \x02(\t\x12\x14\n\x0c\x65vent_number\x18\x02 \x02(\r\x12\x12\n\nevent_type\x18\x03 \x01(\t\x12\x13\n\x0b\x61ttack_type\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65tected_ap\x18\x06 \x01(\t\x12&\n\x08mac_addr\x18\x07 \x01(\x0b\x32\x14.Security.MacAddress\x12\x12\n\nradio_band\x18\x08 \x01(\t\x12\r\n\x05level\x18\t \x01(\t*)\n\x06\x41\x63tion\x12\x07\n\x03\x41\x44\x44\x10\x01\x12\n\n\x06\x44\x45LETE\x10\x02\x12\n\n\x06UPDATE\x10\x03'
)

_ACTION = _descriptor.EnumDescriptor(
  name='Action',
  full_name='Security.Action',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ADD', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETE', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UPDATE', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=688,
  serialized_end=729,
)
_sym_db.RegisterEnumDescriptor(_ACTION)

Action = enum_type_wrapper.EnumTypeWrapper(_ACTION)
ADD = 1
DELETE = 2
UPDATE = 3



_MACADDRESS = _descriptor.Descriptor(
  name='MacAddress',
  full_name='Security.MacAddress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='addr', full_name='Security.MacAddress.addr', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=54,
)


_RAPIDSSTREAMINGEVENT = _descriptor.Descriptor(
  name='RapidsStreamingEvent',
  full_name='Security.RapidsStreamingEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cust_id', full_name='Security.RapidsStreamingEvent.cust_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rogue', full_name='Security.RapidsStreamingEvent.rogue', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='idsEvent', full_name='Security.RapidsStreamingEvent.idsEvent', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=171,
)


_ROGUEEVENT = _descriptor.Descriptor(
  name='RogueEvent',
  full_name='Security.RogueEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rogue_id', full_name='Security.RogueEvent.rogue_id', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='classification', full_name='Security.RogueEvent.classification', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='first_seen', full_name='Security.RogueEvent.first_seen', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_seen', full_name='Security.RogueEvent.last_seen', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rogue_name', full_name='Security.RogueEvent.rogue_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ssid', full_name='Security.RogueEvent.ssid', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lan_mac', full_name='Security.RogueEvent.lan_mac', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='first_det_device', full_name='Security.RogueEvent.first_det_device', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_det_device', full_name='Security.RogueEvent.last_det_device', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encryption', full_name='Security.RogueEvent.encryption', index=9,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='Security.RogueEvent.port', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='containment_status', full_name='Security.RogueEvent.containment_status', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mac_vendor', full_name='Security.RogueEvent.mac_vendor', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=174,
  serialized_end=473,
)


_WIDSEVENT = _descriptor.Descriptor(
  name='WIDSEvent',
  full_name='Security.WIDSEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='Security.WIDSEvent.device_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event_number', full_name='Security.WIDSEvent.event_number', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event_type', full_name='Security.WIDSEvent.event_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attack_type', full_name='Security.WIDSEvent.attack_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='Security.WIDSEvent.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detected_ap', full_name='Security.WIDSEvent.detected_ap', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mac_addr', full_name='Security.WIDSEvent.mac_addr', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radio_band', full_name='Security.WIDSEvent.radio_band', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='level', full_name='Security.WIDSEvent.level', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=476,
  serialized_end=686,
)

_RAPIDSSTREAMINGEVENT.fields_by_name['rogue'].message_type = _ROGUEEVENT
_RAPIDSSTREAMINGEVENT.fields_by_name['idsEvent'].message_type = _WIDSEVENT
_ROGUEEVENT.fields_by_name['rogue_id'].message_type = _MACADDRESS
_WIDSEVENT.fields_by_name['mac_addr'].message_type = _MACADDRESS
DESCRIPTOR.message_types_by_name['MacAddress'] = _MACADDRESS
DESCRIPTOR.message_types_by_name['RapidsStreamingEvent'] = _RAPIDSSTREAMINGEVENT
DESCRIPTOR.message_types_by_name['RogueEvent'] = _ROGUEEVENT
DESCRIPTOR.message_types_by_name['WIDSEvent'] = _WIDSEVENT
DESCRIPTOR.enum_types_by_name['Action'] = _ACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MacAddress = _reflection.GeneratedProtocolMessageType('MacAddress', (_message.Message,), {
  'DESCRIPTOR' : _MACADDRESS,
  '__module__' : 'security_pb2'
  # @@protoc_insertion_point(class_scope:Security.MacAddress)
  })
_sym_db.RegisterMessage(MacAddress)

RapidsStreamingEvent = _reflection.GeneratedProtocolMessageType('RapidsStreamingEvent', (_message.Message,), {
  'DESCRIPTOR' : _RAPIDSSTREAMINGEVENT,
  '__module__' : 'security_pb2'
  # @@protoc_insertion_point(class_scope:Security.RapidsStreamingEvent)
  })
_sym_db.RegisterMessage(RapidsStreamingEvent)

RogueEvent = _reflection.GeneratedProtocolMessageType('RogueEvent', (_message.Message,), {
  'DESCRIPTOR' : _ROGUEEVENT,
  '__module__' : 'security_pb2'
  # @@protoc_insertion_point(class_scope:Security.RogueEvent)
  })
_sym_db.RegisterMessage(RogueEvent)

WIDSEvent = _reflection.GeneratedProtocolMessageType('WIDSEvent', (_message.Message,), {
  'DESCRIPTOR' : _WIDSEVENT,
  '__module__' : 'security_pb2'
  # @@protoc_insertion_point(class_scope:Security.WIDSEvent)
  })
_sym_db.RegisterMessage(WIDSEvent)


# @@protoc_insertion_point(module_scope)
