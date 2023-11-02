import os
import codecs
import grpc
import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc

class NodeConnection:
    def __init__(self, node):
        try:
            self.node = node
            self.cert = open(os.path.expanduser(node["cert"]), 'rb').read()
            macaroon_bytes = open(os.path.expanduser(node["admin_macaroon"]), 'rb').read()
            self.macaroon = codecs.encode(macaroon_bytes, 'hex')
            os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
            metadata = [('macaroon', self.macaroon)]
            auth_credentials = grpc.metadata_call_credentials(lambda context, callback: callback(metadata, None))
            ssl_credentials = grpc.ssl_channel_credentials(self.cert)
            channel_credentials = grpc.composite_channel_credentials(ssl_credentials, auth_credentials)
            channel = grpc.secure_channel(self.node["channel"], channel_credentials)
            self.stub = lnrpc.LightningStub(channel)
        except FileNotFoundError as e:
            print(f"File not found error at {self.node['name']}: {e}")
        except grpc.RpcError as e:
            print(f"GRPC error at {self.node['name']}: {e}")
        except Exception as e:
            print(f"An error occurred connecting to {self.node['name']}: {e}")

    def get_info(self):
        try:
            response = self.stub.GetInfo(ln.GetInfoRequest())
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error: Revisa la informacion del nodo al que intentaste acceder por favor.\n Mas informacion del error:\n{e.details()}"

    def request_open_channel(self, pubkey, funding_amount, push_amount):
        try:
            request = ln.OpenChannelRequest(
                node_pubkey=codecs.decode(str(pubkey), 'hex'),
                local_funding_amount=int(funding_amount),
                push_sat=int(push_amount),
                private=False,
            )
            response = self.stub.OpenChannelSync(request)
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error grpc en credenciales {self.node['name']}: {e.details()}"
            elif "synced" in e.details():
                return "", f"Error grpc al abrir canal parece que es un problema de sincronización, mina un bloque."
            return "", f"Error grpc al abrir canal: {e.details()}"
        except Exception as e:
            return "", f"Error al abrir canal: {e}"

    def check_pending_channels(self):
        try:
            response = self.stub.PendingChannels(ln.PendingChannelsRequest())
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error al revisar canales pendientes.{e.details()}"

    def close_channel(self, channel_point, force_close=True):
        try:
            params = channel_point.split(':')
            channel_point = ln.ChannelPoint(
                funding_txid_str=params[0],
                output_index=int(params[1])
            )
            request = ln.CloseChannelRequest(
                channel_point=channel_point,
                force=True,
            )
            response = self.stub.CloseChannel(request)
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error al cerrar canal: {e.details()}"

    def create_invoice(self, invoice_amt):
        try:
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
            response = self.stub.AddInvoice(request)
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error al crear la factura: {e.details()}"

    def pay_invoice(self, payment_request):
        try:
            lowercased_request = payment_request.lower()
            request = ln.SendRequest(
                payment_request=lowercased_request,
                allow_self_payment=False,
            )
            response = self.stub.SendPaymentSync(request)
            payment_list = self.stub.ListPayments(request)
            if len(payment_list) > 0:
                for payment in payment_list.payments:
                    if payment.payment_request == lowercased_request:
                        return response, ""
            else:
                return "", "Error al pagar la factura, revisa que tus canales no estén pendientes."
                
            
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            elif "synced" in e.details():
                return "", f"Error grpc al abrir canal parece que es un problema de sincronización, mina un bloque."
            return "", f"Error grpc al pagar la factura: {e.details()}"
        except Exception as e:
            if "ListPaymentsResponse" in str(e):
                return "", f"Error al pagar la factura, revisa que tus canales no estén pendientes."
            return "", f"Error al pagar la factura: {e}"

    def get_invoices(self):
        try:
            request = ln.ListInvoiceRequest(
                num_max_invoices=15,
            )
            response = self.stub.ListInvoices(request)
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error al buscar las facturas creadas: {e.details()}"
              
    def get_payments(self):
        try:
            request = ln.ListPaymentsRequest(
                max_payments=15,
            )
            response = self.stub.ListPayments(request)
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error al buscar pagos realizados: {e.details()}"

    def decode_pr(self, payment_request):
        try:
            request = ln.PayReqString(
                pay_req=str(payment_request),
            )
            response = self.stub.DecodePayReq(request)
            return response, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error al decifrar peticion de pago: {e.details()}"

    def node_info(self):
        try:
            return self.node, ""
        except grpc.RpcError as e:
            if e.details() == "permission denied":
                return "", f"Error en credenciales {self.node['name']}: {e.details()}"
            return "", f"Error de grpc al pedir informacion del nodo: {e.details()}"
        except Exception as e:
            return "", "Error al pedir informacion del nodo."
