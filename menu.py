from sqlite3 import connect
from tokenize import String
import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import codecs
import base64
import os
from time import sleep
from lnd import NodeConnection
import draws

wallet = {
    "name": 'Trueno',
    "pubkey": '', 
    "cert": '', 
    "admin_macaroon": '', 
    "channel": ''
}
coffee_shop = {
    "name": 'Cafetería',
    "pubkey": '', 
    "cert": '', 
    "admin_macaroon": '', 
    "channel": ''
}
providor = {
    "name": 'Panadería',
    "pubkey": '', 
    "cert": '', 
    "admin_macaroon": '', 
    "channel": ''
}

def main():
    print("""
    Hola bienvenido/a, te contaremos la historia de Lisa con Lightning Network. 
    Esta historia contiene un tesoro que ganaras si la terminas. Lisa es dueña de 
    una cafeteria  en la Univeridad del Valle de Guatemala. Ella quiere poder 
    transaccionar Bitcoin a través de su nodo de Lightning Network recién instalado. 
    
    Lisa conoce de una billetera de LN llamada Trueno, y quiere recibir pagos a 
    travez de ellos ya que es la billetera más usada por los estudiantes de la UVG.
    Por otro lado a Lisa le intereza tener sus pagos automatizados con el sistema de 
    pagos de su proveedor de pan. 
    
    DESAFIO:
    Si logras que un cliente de Trueno pague a la panadería de Lisa y luego que 
    Lisa le pague el pan a la panadería ganarás una llave a el tesoro.
    """)
    print('\n===========================================================\n')
    display_node_info(NodeConnection(coffee_shop))
    display_node_info(NodeConnection(wallet))
    display_node_info(NodeConnection(providor))
    print('\n===========================================================\n')
    node_config_menu()

def node_config_menu():
    challenge()
    # display the node configuration menu
    print("\nElige a qué nodo conectarte.")
    print("1. billetera Trueno")
    print("2. cafetería de Lisa")
    print("3. panadería")
    print("4. Salir")

    choice = input("Ingresa el numero de tu eleccion: ")

    if choice == "1":
        node_connection = NodeConnection(wallet)
        node_action_menu(node_connection)
    elif choice == "2":
        node_connection = NodeConnection(coffee_shop)
        node_action_menu(node_connection)
    elif choice == "3":
        node_connection = NodeConnection(providor)
        node_action_menu(node_connection)
    elif choice == "4":
        return
    else:
        print("Invalid choice. Please try again.")
        node_config_menu()

def node_action_menu(node_connection):
    node, err = node_connection.node_info()
    if err:
        print("\n", "\033[91m" + err + "\033[0m")
        return
    print('\n===========================================================\n')
    display_node_info(node_connection)
    print('===========================================================\n')

    #=======================================
    print("\nEscoje qué acción hacer:")
    print("1. Abrir un canal")
    print("2. Revisar canales pendientes")
    print("3. Cerrar canal")
    print("4. Crear Factura")
    print("5. Pagar Factura")
    print("6. Ver Transacciones")
    print("7. Decifrar PR")
    print("8. Regresar")

    choice = input("Ingresa tu respuesta: ")

    if choice == '1':
        print("\nrequest_open_channel=======================================>\n")
        pubkey = input("Ingresa la llave pública del nodo receptor: ")
        funding_amount = input("Ingresa la cantidad que depositarás en tu balance del canal: ")
        push_satoshis = input("Ingresa la cantidad que depositarás a la contraparte del canal: ")
        response, err = node_connection.request_open_channel(pubkey, funding_amount, push_satoshis)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
            node_action_menu(node_connection)
        node, err = node_connection.node_info()
        drawer("request_open_channel", node["pubkey"], pubkey)
        print(f"""    Monto: {funding_amount}         ==> BALANCE <==       Monto: {push_satoshis}""")
        input("""\033[93m
        Recuerda que al crear un canal, estás realizando una transacción de bitcoin que
        necesita de 4 confirmaciones para que el canal funcione correctamente. Cada 
        confirmación representa 1 bloque minado.
        
        Para minar bloques en Polar debes ir a la red de nodos y hacer click en Quick Mine.\033[0m
        """)
        node_action_menu(node_connection)

    elif choice == '2':
        response, err = node_connection.check_pending_channels()
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
            node_action_menu(node_connection)
        print(response)
        node_action_menu(node_connection)

    elif choice == '3':
        channel_pnt = input("Ingresa el channel_point del canal que deseas cerrar: ")
        response, err = node_connection.close_channel(channel_pnt)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
            node_action_menu(node_connection)
        print("Peticion de cierre de canal exitosa!")
        print("Por las reglas internas de Polar se necesita minar 6 bloques para validar esta petición")
        node_action_menu(node_connection)

    elif choice == '4':
        invoice_amt = input("Ingresa el monto del cobro que deseas hacer: ")
        response, err = node_connection.create_invoice(invoice_amt)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
            node_action_menu(node_connection)
        print(draws.factura_string)
        print(response.payment_request)
        node_action_menu(node_connection)

    elif choice == '5':
        payment_request = input("Ingresa el payment_request a pagar: ")
        decoded_pr, err = node_connection.decode_pr(payment_request)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
            node_action_menu(node_connection)
        print(f"\nInformacion relevante al decifrar factura:\n")
        print(f"Monto: {decoded_pr.num_satoshis}")
        print(f"Hash del pago: \n{decoded_pr.payment_hash}")
        print(f"Fecha: {decoded_pr.timestamp}")
        print(f"Llave publica destino: \n{decoded_pr.destination}\n")

        confirmation = input("Escribe si o no para continuar con el pago: ")
        if confirmation == "si":
            response, err = node_connection.pay_invoice(payment_request)
            if err:
                print("\n", "\033[91m" + err + "\033[0m")
                node_action_menu(node_connection)
            drawer("pay_invoice", node["pubkey"], decoded_pr.destination)
            print("\n\t\033[93mPago enviado, confirma que esté en tus transacciones como pagada.\033[0m\n")
            node_action_menu(node_connection)
        node_action_menu(node_connection)

    elif choice == '6':
        get_transactions(node_connection)
        node_action_menu(node_connection)

    elif choice == '7':
        pr = input("Ingresa una peticion de pago: ")
        response, err = node_connection.decode_pr(pr)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
            node_action_menu(node_connection)
        print(response)
        node_action_menu(node_connection)

    elif choice == '8':
        node_config_menu()
    else:
        print("\n<===Invalid choice===>\n")
        node_action_menu(node_connection)

def display_node_info(node_connection):
    response, err = node_connection.get_info()
    if err:
        print("\n", "\033[91m" + err + "\033[0m")
        return
    node, err = node_connection.node_info()
    if err:
        print("\n", "\033[91m" + err + "\033[0m")
        return
    print("Estas en el nodo: ", node["name"])
    print("Su llave pública: ", response.identity_pubkey)
    print("Version: ", response.version)
    print(draws.nodes_info[node["name"]])

def get_transactions(node_connection):
    response, err = node_connection.get_invoices()
    if err:
        print("\n", "\033[91m" + err + "\033[0m")
        node_action_menu(node_connection)
    for invoice in response.invoices:
        decoded, err = node_connection.decode_pr(invoice.payment_request)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
        print("\n=================================================>\n")
        print(f"Confirmacion de pago: {'Si se pagó' if invoice.settled else 'No se pagó'}")
        print(f"Monto: {invoice.value}")
        print(f"Mensaje: {invoice.memo}")
        print(f"Llave publica destinataria: {decoded.destination}\n")
        print(f"Peticion de Pago: {invoice.payment_request}")

    response, err = node_connection.get_payments()
    if err:
        print("\n", "\033[91m" + err + "\033[0m")
        node_action_menu(node_connection)
    print("\n=================================================>\n")
    print("==>PAGOS\n")
    for payment in response.payments:
        decoded, err = node_connection.decode_pr(payment.payment_request)
        if err:
            print("\n", "\033[91m" + err + "\033[0m")
        print(f"Confirmacion de pago: {'Si se pagó' if payment.status == 2 else 'No se pagó'}")
        print(f"Monto: {payment.value_sat}")
        print(f"Llave publica destinataria: {decoded.destination}\n")
        print(f"Peticion de Pago: {payment.payment_request}")
        print("=================================================>\n")

def drawer(operation, node_pk, destinated_pk):
    if operation == "request_open_channel":
        action_manager("open", node_pk, destinated_pk)
    elif operation == "pay_invoice":
        action_manager("pay", node_pk, destinated_pk)
    return
        
def action_manager(action, node_pk, destinated_pk):
    if node_pk == wallet["pubkey"]:
        if destinated_pk == coffee_shop["pubkey"]:
            print(draws.transaction_drawings["billetera_" + action + "_cafeteria"])
        elif destinated_pk == providor["pubkey"]:
            print(draws.transaction_drawings["billetera_" + action + "_panaderia"])
        return

    elif node_pk == coffee_shop["pubkey"]:
        if destinated_pk == wallet["pubkey"]:
            print(draws.transaction_drawings["cafeteria_" + action + "_billetera"])
        elif destinated_pk == providor["pubkey"]:
            print(draws.transaction_drawings["cafeteria_" + action + "_panaderia"])
        return

    elif node_pk == providor["pubkey"]:
        if destinated_pk == wallet["pubkey"]:
            print(draws.transaction_drawings["panaderia_" + action + "_billetera"])
        elif destinated_pk == coffee_shop["pubkey"]:
            print(draws.transaction_drawings["panaderia_" + action + "_cafeteria"])
        return
    return

def challenge():
    ch1 = c1()
    ch2 = c2()
    if ch1 and ch2:
        clue = wallet["name"]+coffee_shop["name"]+providor["name"]
        key = base64.b64encode(clue.encode('utf-8'))
        print(f"""\033[92m
        FELICIDADES, HAZ COMPLETADO EL DESAFIO!
        Llave del tesoro:
        {key.decode('utf-8')}\033[0m
        """)
        raise SystemExit(0)
    return


def c1():
    node_connection = NodeConnection(wallet)
    response, err = node_connection.get_payments()
    if err:
        print("\n", err)
        node_config_menu()
    for payment in response.payments:
        decoded, err = node_connection.decode_pr(payment.payment_request)
        if decoded.destination == coffee_shop["pubkey"]:
            return True
    return False
            
def c2():
    node_connection = NodeConnection(coffee_shop)
    response, err = node_connection.get_payments()
    if err:
        print("\n", err)
        node_config_menu()
    for payment in response.payments:
        decoded, err = node_connection.decode_pr(payment.payment_request)
        if decoded.destination == providor["pubkey"]:
            return True
    return False

main()