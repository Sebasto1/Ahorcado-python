import pygame
import random
import sys
import pygame_menu
import palabras

#Cambiar letra de menu

#Se inicializa la libreria pygame
pygame.init()

#Se define el tamaño y el nombre de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ahorcado")

FPS = 30
clock = pygame.time.Clock()


#Se defines colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Se define las fuentes del titulo y el menu
font_title = pygame.font.Font(None, 60)
font_menu = pygame.font.Font(None, 36)



#Se recibe las palabras desde palabras.py
palabras = palabras.palabras_juego

#Funcion para seleccionar palabra
def seleccionar_palabra():
    return random.choice(palabras)

#Funcion que se encarga de mostrar las palabras
def mostrar_palabra(palabra, letras_correctas):
    resultado = ""
    for letra in palabra:
        if letra.isalpha() and letra.lower() in letras_correctas:
            resultado += letra + " "
        else:
            resultado += "_ "
    texto = font_menu.render(resultado, True, BLACK)
    screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 + 100))

#Funcion para dibujar la figura
def mostrar_figura_humana(intentos):
    if intentos >= 1:
        pygame.draw.circle(screen, BLACK, (150, 150), 30, 2)
    if intentos >= 2:
        pygame.draw.line(screen, BLACK, (150, 180), (150, 300), 2)
    if intentos >= 3:
        pygame.draw.line(screen, BLACK, (150, 200), (120, 250), 2)
    if intentos >= 4:
        pygame.draw.line(screen, BLACK, (150, 200), (180, 250), 2)
    if intentos >= 5:
        pygame.draw.line(screen, BLACK, (150, 300), (120, 350), 2)
    if intentos >= 6:
        pygame.draw.line(screen, BLACK, (150, 300), (180, 350), 2)

#Funcion para mostrar los carteles animados del inicio y el final
def mostrar_cartel_animado(mensaje, color, duracion):
    texto_cartel = font_menu.render(mensaje, True, color)
    for i in range(1, 100):
        screen.fill(WHITE)
        screen.blit(texto_cartel, (WIDTH // 2 - texto_cartel.get_width() // 2, i))
        pygame.display.flip()
        pygame.time.delay(5)
    pygame.time.delay(duracion)

#Funcion que recibe el nombre del jugador del menu principal
def recibir_nombre_jugador(value, **kwargs):
    global nombre_jugador
    nombre_jugador = value
    if len(nombre_jugador) == 0 or nombre_jugador == '':
        nombre_jugador = "SinNombre"
    return nombre_jugador

#Loop principal del juego
def juego():
    palabra = seleccionar_palabra()
    letras_correctas = set()
    intentos = 0

    mostrar_cartel_animado(f"¡Comencemos, {nombre_jugador}!", BLACK, 2000)
    mostrar_cartel_animado(f" Para jugar usar el teclado, tenés 6 intentos", BLACK, 1500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                letra = event.unicode
                if letra.isalpha() and letra.lower() not in letras_correctas:
                    letras_correctas.add(letra.lower())
                    if letra.lower() not in palabra:
                        intentos += 1

        screen.fill(WHITE)

        mostrar_figura_humana(intentos)
        mostrar_palabra(palabra, letras_correctas)
        

        texto_intentos = font_menu.render("Intentos restantes: {}".format(6 - intentos), True, BLACK)
        calculos_puntos = 6 - intentos
        screen.blit(texto_intentos, (WIDTH // 2 - texto_intentos.get_width() // 2, 20))

        if all(letra.isalpha() and letra.lower() in letras_correctas for letra in palabra):
            puntaje(calculos_puntos)
            insertar_puntajes(nombre_jugador,puntuacion)
            mostrar_cartel_animado(f"¡Felicidades!, {nombre_jugador} ¡Has ganado!", BLACK, 2000)
            break
        elif intentos >= 6:
            mostrar_cartel_animado(f"¡Perdiste {nombre_jugador}, la palabra era '{palabra}'!", BLACK, 2000)
            puntaje(0)
            insertar_puntajes(nombre_jugador,puntuacion)
            break

        pygame.display.flip()
        
def puntaje(puntaje):
    global puntuacion
    puntuacion = puntaje
    return puntuacion
    
        
def insertar_puntajes(nombre_jugador, puntaje):
    escribir_archivo = open("highscore.txt", "a")
    escribir_archivo.write(f" \n {nombre_jugador} ------------ Puntaje = {puntaje}\n")
    escribir_archivo.close()
    
    
def mostrar_puntajes():
    leer_archivo = open("highscore.txt")
    texto = leer_archivo.read()
    texto_dibujo = font_menu.render(texto, True, BLACK, None)
    lineas = texto.splitlines()
    leer_archivo.close()

    puntaje_rect = texto_dibujo.get_rect()
    puntaje_rect.center = (WIDTH / 2, 10)
    puntaje_rect.centery = 50
    puntaje_rect.left = 150
    
    cartel = font_menu.render("Los puntajes son:", True, BLACK, None)
    cartel_rect = cartel.get_rect()
    cartel_rect.center = (WIDTH / 2, 10)
    cartel_rect.centery = 20
    
    
    if len(texto) is 0:
        mostrar_cartel_animado("No hay puntajes guardados",BLACK, 2000)
        menu.mainloop(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        screen.blit(cartel,cartel_rect)
        
        
        for i in lineas:
            pygame.time.delay(200)
            texto_dibujo1 = font_menu.render(i,True,BLACK,None)
            puntaje_rect.centery = puntaje_rect.centery + 10
            screen.blit(texto_dibujo1, puntaje_rect)
            pygame.display.flip()
            pygame.time.delay(5)
            
        pygame.time.delay(1000)
        menu.mainloop(screen)
            
    
#Armado del menu principal
menu = pygame_menu.Menu('AHORCADO', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_DEFAULT)

nombre_jugador = 'SinNombre'
puntuacion = 0


menu.add.text_input('Nombre jugador: ',default='Nombre', onchange=recibir_nombre_jugador)
menu.add.button('Jugar', juego)
menu.add.button('Puntajes', mostrar_puntajes)
menu.add.button('Salir', pygame_menu.events.EXIT)

menu.mainloop(screen)
