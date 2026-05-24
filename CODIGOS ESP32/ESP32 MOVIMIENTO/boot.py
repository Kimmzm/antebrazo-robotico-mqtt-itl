from emg import EMGServoController
from signlanguage import SignLanguage 
import api
import time

if __name__ == '__main__':
    
    while True:
        
        iniciar = api.enter('http://192.168.109.89:5000/getCam/123')
        print(iniciar)
    
        if iniciar != "Diferentes":
            
            ssid_ = "RedJonny"
            wp2_pass = "1234567890"
    
            api.conexionWIfi(ssid_, wp2_pass)
            
            inicializar = EMGServoController([4, 19, 12, 13, 14], 34)
            while iniciar == "Iguales":
                iniciar = api.enter('http://192.168.109.89:5000/getCam/123')
                
                palabra_api =  api.send_word('http://192.168.109.89:5000/ABC/123')
                print(palabra_api)
        
                if palabra_api:
                    #----- Leguaje se señas -----
                    sign_language = SignLanguage([4, 19, 12, 13, 14])
                    sign_language.read_word(str(palabra_api))
                    sign_language.detener_servos()
        
                else:
                    #----- Lectura de sensor emg -----
                    print("hola")
                    
                    inicializar.ejecutar()
                time.sleep(.5)
        else:
            print('Nop')
            pass