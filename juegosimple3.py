import pygame
import random

# Inicializa pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO_OSCURO = (255, 0, 0)

# Tamaños
radio_bola = 20
ancho_paleta = 100
alto_paleta = 20

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego estilo Circus")

# Reloj para controlar el framerate
reloj = pygame.time.Clock()

# Fuente de texto para el marcador
fuente = pygame.font.SysFont("Arial", 30)

# Estado del juego
juego_terminado = False  # Variable para controlar si el juego terminó o no

# Función para reiniciar el juego
def reiniciar_juego():
    global bola_x, bola_y, bola_velocidad, paleta_x, paleta_y, paleta_velocidad, errores, puntuacion, juego_terminado
    bola_x = random.randint(50, ANCHO - 50)
    bola_y = 0
    bola_velocidad = 5
    paleta_x = ANCHO // 2 - ancho_paleta // 2
    paleta_y = ALTO - alto_paleta - 10  # Aquí se inicializa paleta_y
    paleta_velocidad = 7  # Aquí se inicializa paleta_velocidad
    errores = 0
    puntuacion = 0
    juego_terminado = False  # Resetea el estado del juego

# Función para dibujar todo
def dibujar():
    pantalla.fill(BLANCO)

    # Dibuja la bola
    pygame.draw.circle(pantalla, ROJO, (bola_x, bola_y), radio_bola)

    # Dibuja la paleta
    pygame.draw.rect(pantalla, AZUL, (paleta_x, paleta_y, ancho_paleta, alto_paleta))

    # Muestra la puntuación
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, VERDE)
    pantalla.blit(texto_puntuacion, (10, 10))

    # Muestra el número de errores
    texto_errores = fuente.render(f"Errores: {errores}/3", True, ROJO_OSCURO)
    pantalla.blit(texto_errores, (10, 40))

    # Si el jugador ha perdido
    if errores >= 3:
        texto_gameover = fuente.render("¡Juego terminado!", True, ROJO_OSCURO)
        pantalla.blit(texto_gameover, (ANCHO // 2 - 100, ALTO // 2 - 50))
        texto_reiniciar = fuente.render("Presiona 'R' para reiniciar o 'Q' para salir.", True, ROJO_OSCURO)
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - 150, ALTO // 2))

    pygame.display.update()

# Bucle principal del juego
def bucle_principal():
    global bola_x, bola_y, bola_velocidad, paleta_x, paleta_y, paleta_velocidad, errores, puntuacion, juego_terminado
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        if not juego_terminado:
            # Mueve la bola hacia abajo solo si el juego no ha terminado
            bola_y += bola_velocidad
            if bola_y > ALTO:
                if errores < 3:
                    errores += 1  # Se incrementa el número de errores
                    bola_y = 0
                    bola_x = random.randint(50, ANCHO - 50)  # Reinicia la bola
                else:
                    # El juego termina cuando el número de errores alcanza el máximo
                    juego_terminado = True

            # Mueve la paleta con las teclas
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and paleta_x > 0:
                paleta_x -= paleta_velocidad
            if teclas[pygame.K_RIGHT] and paleta_x < ANCHO - ancho_paleta:
                paleta_x += paleta_velocidad

            # Colisión con la paleta
            if (bola_y + radio_bola > paleta_y and
                bola_y + radio_bola < paleta_y + alto_paleta and
                bola_x > paleta_x and bola_x < paleta_x + ancho_paleta):
                bola_y = 0
                bola_x = random.randint(50, ANCHO - 50)  # Reinicia la bola
                puntuacion += 1  # Aumenta la puntuación cuando la bola es atrapada

        # Dibuja todos los objetos y la puntuación
        dibujar()

        # Si el jugador ha perdido, espera la entrada del jugador
        if juego_terminado:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_r]:  # Reiniciar el juego si se presiona 'R'
                reiniciar_juego()
            if teclas[pygame.K_q]:  # Salir del juego si se presiona 'Q'
                corriendo = False

        # Limita a 60 FPS
        reloj.tick(60)

    pygame.quit()

# Inicialización del juego
reiniciar_juego()  # Inicializa el juego antes de empezar
bucle_principal()  # Inicia el bucle principal del juego 