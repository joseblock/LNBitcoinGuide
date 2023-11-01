#===========================> OBJECTS <===========================#

cafeteria_string = """
    ______________   
   /   Cafeteria  \\   
  /________________\\  
    |            |    
    |      o~    |      
    |_____/L\____|   
    |VVVVV||VVVVV|     
"""

panaderia_string = """
              SS
    _________|--|_
   |   Panaderia  | 
   |______________|
    |      o     |   
    |_____/L\____|
    |VVVVV||VVVVV|
"""

billetera_string = """
     ____________ _                          
    |  Billetera |||     
    |   Trueno   |||     
    | |--------| |||     
    | |        | ||| ⚡ 
    | |        | |||   
    | |________| |||     
    |____________///     
"""

factura_string = """
     ____________                           
    |  Factura   |   
    |  ^^^^^^^   |     
    | ---------- |     
    | ---------- | 
    | ---------- |    
    | Total----% |     
    |____________/     

"""

ln_string = """
 __
\\  \\     
 / /    
\\ \\    
 \/    

"""

#===========================> ACTIONS <===========================#

#===========================> PAY <===========================#

billetera_pay_cafeteria = """
     ____________ _                          
    |  Billetera |||                            ______________ 
    |   Trueno   |||                           /   Cafeteria  \\ 
    | |--------| |||                          /________________\\ 
    | |        | ||| ⚡  Pago con Lightning     |            | 
    | |        | |||   $------------------>     |      o~    |   
    | |________| |||                            |_____/L\____| 
    |____________///                            |VVVVV||VVVVV| 

"""
billetera_pay_panaderia = """
     ____________ _                          
    |  Billetera |||                                      SS
    |   Trueno   |||                           _________|--|_
    | |--------| |||                          |   Panaderia  | 
    | |        | ||| ⚡  Pago con Lightning   |______________|
    | |        | |||   $------------------>    |      o     |   
    | |________| |||                           |_____/L\____|
    |____________///                           |VVVVV||VVVVV| 

"""

cafeteria_pay_panaderia = """
    ______________                                     SS
   /   Cafeteria  \\                         _________|--|_
  /________________\\                       |   Panaderia  | 
    |            |                          |______________|
    |      o~    |   Pago con Lightning      |      o     |   
    |_____/L\____|   $------------------>    |_____/L\____|
    |VVVVV||VVVVV|                           |VVVVV||VVVVV| 

"""
cafeteria_pay_billetera = """

    ______________                          ____________ _   
   /   Cafeteria  \\                       |  Billetera |||  
  /________________\\                      |   Trueno   |||  
    |            |                         | |--------| |||  
    |      o~    |   Pago con Lightning    | |        | ||| ⚡
    |_____/L\____|   $------------------>  | |        | |||  
    |VVVVV||VVVVV|                         | |________| |||  
                                           |____________///  
"""

panaderia_pay_billetera = """

              SS                           ____________ _   
    _________|--|_                        |  Billetera |||  
   |   Panaderia  |                       |   Trueno   |||  
   |______________|                       | |--------| |||  
    |      o     |  Pago con Lightning    | |        | ||| ⚡
    |_____/L\____|  $------------------>  | |        | |||  
    |VVVVV||VVVVV|                        | |________| |||  
                                          |____________///  
"""
panaderia_pay_cafeteria = """

              SS                            ______________   
    _________|--|_                         /   Cafeteria  \\   
   |   Panaderia  |                       /________________\\  
   |______________|                         |            |    
    |      o     |   Pago con Lightning     |      o~    |      
    |_____/L\____|   $------------------>   |_____/L\____|   
    |VVVVV||VVVVV|                          |VVVVV||VVVVV|     
                                          
"""

#===========================> OPEN CHANNEL <===========================#

billetera_open_cafeteria = """
     ____________ _                          
    |  Billetera |||                            ______________ 
    |   Trueno   |||                           /   Cafeteria  \\ 
    | |--------| |||                          /________________\\ 
    | |        | ||| ⚡  apertura de canal      |            | 
    | |        | |||   ===================>     |      o~    |   
    | |________| |||                            |_____/L\____| 
    |____________///                            |VVVVV||VVVVV| 
"""
billetera_open_panaderia = """
     ____________ _                          
    |  Billetera |||                                     SS
    |   Trueno   |||                           _________|--|_
    | |--------| |||                          |   Panaderia  | 
    | |        | ||| ⚡  apertura de canal    |______________|
    | |        | |||   ===================>    |      o     |   
    | |________| |||                           |_____/L\____|
    |____________///                           |VVVVV||VVVVV| 
"""

cafeteria_open_panaderia = """
    ______________                                     SS
   /   Cafeteria  \\                          _________|--|_
  /________________\\                        |   Panaderia  | 
    |            |                          |______________|
    |      o~    |    apertura de canal      |      o     |   
    |_____/L\____|   ===================>    |_____/L\____|
    |VVVVV||VVVVV|                           |VVVVV||VVVVV| 
"""
cafeteria_open_billetera = """
                                            ____________ _   
    ______________                         |  Billetera |||  
   /   Cafeteria  \\                        |   Trueno   |||  
  /________________\\                       | |--------| |||  
    |            |                         | |        | ||| ⚡
    |      o~    |    apertura de canal    | |        | |||  
    |_____/L\____|   ===================>  | |________| |||  
    |VVVVV||VVVVV|                         |____________///  
"""

panaderia_open_billetera = """
                                           ____________ _   
              SS                          |  Billetera |||  
    _________|--|_                        |   Trueno   |||  
   |   Panaderia  |                       | |--------| |||  
   |______________|                       | |        | ||| ⚡
    |      o     |   apertura de canal    | |        | |||  
    |_____/L\____|  ===================>  | |________| |||  
    |VVVVV||VVVVV|                        |____________///  
"""
panaderia_open_cafeteria = """

              SS                            ______________   
    _________|--|_                         /   Cafeteria  \\   
   |   Panaderia  |                       /________________\\  
   |______________|                         |            |    
    |      o     |    apertura de canal     |      o~    |      
    |_____/L\____|   ===================>   |_____/L\____|   
    |VVVVV||VVVVV|                          |VVVVV||VVVVV|                                    
"""

#===========================> ACTION DICTIONARY <===========================#

transaction_drawings = {
    "billetera_pay_cafeteria" : billetera_pay_cafeteria,
    "billetera_pay_panaderia" : billetera_pay_panaderia,
    "cafeteria_pay_panaderia" : cafeteria_pay_panaderia,
    "cafeteria_pay_billetera" : cafeteria_pay_billetera,
    "panaderia_pay_billetera" : panaderia_pay_billetera,
    "panaderia_pay_cafeteria" : panaderia_pay_cafeteria,
    "billetera_open_cafeteria" : billetera_open_cafeteria,
    "billetera_open_panaderia" : billetera_open_panaderia,
    "cafeteria_open_panaderia" : cafeteria_open_panaderia,
    "cafeteria_open_billetera" : cafeteria_open_billetera,
    "panaderia_open_billetera" : panaderia_open_billetera,
    "panaderia_open_cafeteria" : panaderia_open_cafeteria,
}

#===========================> NODES DICTIONARY <===========================#

nodes_info = {
    "Trueno" : billetera_string,
    "Cafetería" : cafeteria_string,
    "Panadería" : panaderia_string
}
