# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11transaction.proto\"\xb0\x01\n\x12TransactionRequest\x12\x1d\n\x15sender_account_number\x18\x01 \x01(\t\x12\x1b\n\x13sender_account_type\x18\x02 \x01(\t\x12\x1f\n\x17receiver_account_number\x18\x03 \x01(\t\x12\x1d\n\x15receiver_account_type\x18\x04 \x01(\t\x12\x0e\n\x06\x61mount\x18\x05 \x01(\x01\x12\x0e\n\x06reason\x18\x06 \x01(\t\"7\n\x13TransactionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"3\n\x19GetALLTransactionsRequest\x12\x16\n\x0e\x61\x63\x63ount_number\x18\x01 \x01(\t\"g\n\x0bTransaction\x12\x16\n\x0e\x61\x63\x63ount_number\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x01\x12\x0e\n\x06reason\x18\x03 \x01(\t\x12\x12\n\ntime_stamp\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x01(\t\"@\n\x1aGetALLTransactionsResponse\x12\"\n\x0ctransactions\x18\x01 \x03(\x0b\x32\x0c.Transaction\"\\\n\x0cZelleRequest\x12\x14\n\x0csender_email\x18\x01 \x01(\t\x12\x16\n\x0ereceiver_email\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x01\x12\x0e\n\x06reason\x18\x04 \x01(\t2\xcd\x01\n\x12TransactionService\x12\x36\n\tSendMoney\x12\x13.TransactionRequest\x1a\x14.TransactionResponse\x12Q\n\x16getTransactionsHistory\x12\x1a.GetALLTransactionsRequest\x1a\x1b.GetALLTransactionsResponse\x12,\n\x05Zelle\x12\r.ZelleRequest\x1a\x14.TransactionResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRANSACTIONREQUEST._serialized_start=22
  _TRANSACTIONREQUEST._serialized_end=198
  _TRANSACTIONRESPONSE._serialized_start=200
  _TRANSACTIONRESPONSE._serialized_end=255
  _GETALLTRANSACTIONSREQUEST._serialized_start=257
  _GETALLTRANSACTIONSREQUEST._serialized_end=308
  _TRANSACTION._serialized_start=310
  _TRANSACTION._serialized_end=413
  _GETALLTRANSACTIONSRESPONSE._serialized_start=415
  _GETALLTRANSACTIONSRESPONSE._serialized_end=479
  _ZELLEREQUEST._serialized_start=481
  _ZELLEREQUEST._serialized_end=573
  _TRANSACTIONSERVICE._serialized_start=576
  _TRANSACTIONSERVICE._serialized_end=781
# @@protoc_insertion_point(module_scope)
