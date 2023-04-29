from sqlite3 import connect
from tokenize import String
import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import codecs
import base64
import os
from time import sleep

billetera = {
  "pubkey": '020fe45e80bf106640697d8ae6c7c548f4daebd2281c8e126c81b9f1a95eeb1f98', 
  "cert": '~/.polar/networks/4/volumes/lnd/alice/tls.cert', 
  "admin_macaroon": '~/.polar/networks/4/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon', 
  "channel": '127.0.0.1:10001'
}
cafeteria = {
  "pubkey": '03e3b403708d32926650d0669d5aacea96e09415739cc6c512b41ff7938d77f4e7', 
  "cert": '~/.polar/networks/4/volumes/lnd/bob/tls.cert', 
  "admin_macaroon": '~/.polar/networks/4/volumes/lnd/bob/data/chain/bitcoin/regtest/admin.macaroon', 
  "channel": '127.0.0.1:10002'
}
proveedor = {
  "pubkey": '0341f4b5fa8c1775da3f66d1dde760895d1af15053ec45338ab8e2edaeed02f364', 
  "cert": '~/.polar/networks/4/volumes/lnd/carol/tls.cert', 
  "admin_macaroon": '~/.polar/networks/4/volumes/lnd/carol/data/chain/bitcoin/regtest/admin.macaroon', 
  "channel": '127.0.0.1:10003'
}

def main():
  # Primer menú, carga los datos del nodo deseado al programa.
  print("""
    Hola bienvenido/a, te contaremos la historia de Lisa con Lightning Network. 
    Esta historia contiene un tesoro que ganaras si la terminas. Lisa es dueña de 
    una cafeteria  en la Univeridad del Valle de Guatemala. Ella quiere poder 
    transaccionar Bitcoin a través de su nodo de Lightning Network recién instalado. 
    
    Lisa conoce de una billetera de LN llamada Trueno, y quiere recibir pagos a 
    travez de ellos ya que es la billetera más usada por los estudiantes de la UVG.
    Por otro lado a Lisa le intereza tener sus pagos automatizados con el sistema de 
    pagos de su proveedor de pan PanItalo. 
    
    DESAFIO:
    Si logras que un cliente de Trueno pague a la panadería de Lisa y luego que 
    Lisa le pague el pan a PanItalo ganarás una llave a el tesoro.
  """)

  print("Elige a qué nodo conectarte.")
  print("1. billetera Trueno")
  print("2. cafeteria de Lisa")
  print("3. proveedor PanItalo.")
  choice = input("Enter your choice: ")
  if choice == '1':
    node = billetera
  elif choice == '2':
    node = cafeteria
  elif choice == '3':
    node = proveedor                                         
  #-----------------------------------------------------------
  # Esta variable de entorno es usada por gRPC para especificar que el servidor 
  # debe usar un conjunto de algoritmos de seguridad alto en protocolos SSL/TLS 
  # con uso de certificados ECDSA para la autenticación.
  os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
  #----------------------------------------------------------------------------

  # Es un certificado TLS autofirmado que debe ser usado por los clientes que desean
  #  conectarse a un servidor LND.
  cert = open(os.path.expanduser(node["cert"]), 'rb').read()
  #---------------------------------------------------------------------------------

  #Aquí se lee el macaroon de cada nodo que esta localmente guardado en el dispositivo que
  #corre el nodo, un macaroon es un token criptográficamente verificable.
  macaroon_bytes = open(os.path.expanduser(node["admin_macaroon"]), 'rb').read()
  macaroon = codecs.encode(macaroon_bytes, 'hex')
  #########################################################################################
  
  #Funcións que agregan el macaroon como metadata y el cert como las credenciales para el canál 
  # SSL(Secure Sockets Layer) a cada petición que haga este programa al servidor del nodo.
  metadata = [('macaroon', macaroon)]
  auth_credentials = grpc.metadata_call_credentials(lambda context, callback: callback(metadata, None))
  ssl_credentials = grpc.ssl_channel_credentials(cert)
  channel_credentials = grpc.composite_channel_credentials(ssl_credentials, auth_credentials)
  channel = grpc.secure_channel(node["channel"], channel_credentials)
  #---------------------------------------------------------------------------------------------

  # Se crea un objeto que nos servirá como canal seguro de 
  # comunicación y accesso para poder hacer peticiones al 
  # servidor del nodo.
  stub = lnrpc.LightningStub(channel)
  #-------------------------------------------------------

  # Se hace una petición al nodo para poder obtener su informacion general.
  try:
    response = stub.GetInfo(ln.GetInfoRequest())
    print('\n=================================================>\n')
    print("Has accedido al nodo: ", response.alias)
    print("Su llave pública: ", response.identity_pubkey)
    print("Version: ", response.version)
    print('\n=================================================>\n')
    #------------------------------------------------------------------------

    # Segundo menú, realiza las peticiones deseadas al nodo.
    while True:
      print("\nEscoje qué acción hacer:")
      print("1. Abrir un canal")
      print("2. Revisar por canales pendientes")
      print("3. Cerrar canal")
      print("4. Crear Factura")
      print("5. Pagar Factura")
      print("6. Transacciones")
      print("7. Decifrar PR")
      print("8. Exit")

      choice = input("Ingresa tu respuesta: ")

      if choice == '1':
        request_open_channel(stub)
      elif choice == '2':
        check_pending_channels(stub)
      elif choice == '3':
        close_channel(stub)
      elif choice == '4':
        create_invoice(stub)
      elif choice == '5':
        pay_invoice(stub)
      elif choice == '6':
        get_transactions(stub)
      elif choice == '7':
        pr = input("Ingresa una petigcion de pago: ")
        decoded = decode_pr(stub, pr)
        print(decoded)
      elif choice == '8':
        break
      else:
        print("\n<===Invalid choice===>\n")
    #--------------------------------------------------------
  except grpc.RpcError as e:
    print("Error: Revisa la informacion del nodo al que intentaste acceder por favor.\n Mas informacion del error:\n", e.details())

def request_open_channel(stub):
  print("\nrequest_open_channel=======================================>\n")
  pubkey = input("Ingresa la llave pública del nodo receptor: ")
  funding_amount = input("Ingresa la cantidad que depositarás en tu balance del canal: ")
  push_satoshis = input("Ingresa la cantidad que depositarás a la contraparte del canal: ")
  request = ln.OpenChannelRequest(
    node_pubkey=codecs.decode(str(pubkey), 'hex'),
    local_funding_amount=int(funding_amount),
    push_sat=int(push_satoshis),
    private=False,
  )

  for response in stub.OpenChannel(request):
    print(response)
    print("Por las reglas internas de Polar se necesita minar 6 bloques para validar esta petición")
    pass

def check_pending_channels(stub):
    print("\ncheck_pending_channels=======================================>\n")
    request = ln.PendingChannelsRequest()
    response = stub.PendingChannels(request)
    print(response)
    pass

def close_channel(stub):
  channel_pnt = input("Ingresa el channel_point del canal que deseas cerrar: ")
  params = channel_pnt.split(':')
  channel_point = ln.ChannelPoint(
    funding_txid_str=params[0],
    output_index=params[1]
  )
  request = ln.CloseChannelRequest(
    channel_point=channel_point,
    force=True,
  )
  for response in stub.CloseChannel(request):
    print(response)
    print("Por las reglas internas de Polar se necesita minar 6 bloques para validar esta petición")
    pass

def create_invoice(stub):
  print("\ncreate_invoice=======================================>\n")
  invoice_amt = input("Ingresa el monto del cobro que deseas hacer: ")
  preimage = os.urandom(32)
  preimage_hex = preimage.hex()
  request = ln.Invoice(
    memo="my transaction",
    r_preimage=codecs.decode(preimage_hex, 'hex_codec'),
    value=int(invoice_amt),
    description_hash=codecs.decode(preimage_hex, 'hex_codec'),
    expiry=3600,
    cltv_expiry=144,
    private=False,
    is_keysend=False,
  )
  response = stub.AddInvoice(request)
  print('\nContenido:\n',response.payment_request,'\n=================================================>\n')
  #Decode invoice
  pass

def pay_invoice(stub):
  print("\npay_invoice=======================================>\n")
  payment_request = input("Ingresa el payment_request a pagar: ")
  payment_request = payment_request.lower()
  request = ln.SendRequest(
    payment_request=payment_request,
    allow_self_payment=False,
  )
  response = stub.SendPaymentSync(request)
  print(response.payment_route)
  pass

def get_invoices(stub):
  print("\n=================================================>\n")
  print("==>COBROS\n")
  request = ln.ListInvoiceRequest(
    num_max_invoices=15,
    # reversed=<bool>,
  )
  response = stub.ListInvoices(request)
  for invoice in response.invoices:
    decoded = decode_pr(stub, invoice.payment_request)
    print(f"Confirmacion de pago: {'Si se pagó' if invoice.settled else 'No se pagó'}\n=================================================>\n")
    print(f"Monto: {invoice.value}")
    print(f"Mensaje: {invoice.memo}")
    print(f"Llave publica destinataria: {decoded.destination}\n")
    print(f"Peticion de Pago: {invoice.payment_request}")
  pass

def get_payments(stub):
  print("\n=================================================>\n")
  print("==>PAGOS\n")
  request = ln.ListPaymentsRequest(
    max_payments=15,
  )
  response = stub.ListPayments(request)
  for payment in response.payments:
    decoded = decode_pr(stub, payment.payment_request)
    print(f"Confirmacion de pago: {'Si se pagó' if payment.status == 2 else 'No se pagó'}")
    print(f"Monto: {payment.value_sat}")
    print(f"Llave publica destinataria: {decoded.destination}\n")
    print(f"Peticion de Pago: {payment.payment_request}")
    print("=================================================>\n")

def get_transactions(stub):
  get_invoices(stub)
  get_payments(stub)

def decode_pr(stub, payment_request):
  request = ln.PayReqString(
    pay_req=str(payment_request),
  )
  response = stub.DecodePayReq(request)
  return response

def cq():
  pass

main()

#revisar transacciones de nodo de lisa para dar la clave final.

# TODO-LIST
# Create a story
# Change Node Names
# Create class for cleaner behavior
# Make all dependencies into a package
# Minning blocks
# - docker exec -it <container id> /bin/sh
# - su bitcoin
# - bitcoin-cli -regtest -generate 1
# Create a story

# payment_hash: "31159f363c97af76fc5b4ae3caa425d0d0e4047b8693548598b23302f1f79dea"
# num_satoshis: 30000
# timestamp: 1682695903
# expiry: 3600
# description_hash: "4202742c48430a02b36c4b842826a8a467c74057ceecb648290a9dba790b2d29"
# cltv_expiry: 144
# payment_addr: "\333\333{kA;\331\2622\345x$\256\211\007\'\036\003\003\216\377X\0374bx\307K\017\"\376\243"
# num_msat: 30000000
# features {
#   key: 9
#   value {
#     name: "tlv-onion"
#     is_known: true
#   }
# }
# features {
#   key: 14
#   value {
#     name: "payment-addr"
#     is_required: true
#     is_known: true
#   }
# }
# features {
#   key: 17
#   value {
#     name: "multi-path-payments"
#     is_known: true
#   }
# }