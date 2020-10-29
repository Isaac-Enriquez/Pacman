#A00827133 Andrea Fernanda Molina Blandon
#A00829207 Isaac Alejandro Enriquez Trejo
from random import choice
from turtle import *
from freegames import floor, vector

#Estas lineas inicializan el juego, poniendo el puntaje en 0
#y las posiciones iniciales del jugador y los fantasmas.
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
#Esta matriz es el tablero, los 0 son los espacios negros y los
#1 representan los espacios azules por donde se puede caminar
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]

#Esta función dibuja los cuadrados del camino (azules)
def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

#Esta función detecta si es posible moverse al siguiente punto,
#y si as así retorna True, en caso contrario retorna False.
def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

#Esta función dibuja el mapa y pinta el fondo de negro,
#mientras que el camino lo pinta de azul.
def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            #Esta condición pone las bolitas blancas que come Pacman
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

#Esta función mueve a Pacman y a los fantamas
def move():
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])

    clear()

    #La condición hacer que Pacman se mueva
    #solamente si no choca contra una pared
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    #Esta condición aumenta el puntaje cuando se
    #come una bolita y hace que desaparezca
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')
 
    #Esta condición inicia y mueve a los fantasmas
    for point, course in ghosts:
        
        if valid(point + course): 
            point.move(course)
        else:
            options = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
            ]
            
            
            #Este contador es para que no se queden
            #sin moverse si Pacman se queda quieto
            counter = 0
            for i in range(3):
                #Este bloque de condiciones detecta si Pacman está más a un
                #lado y guían gentilmente a los fantasmas hacia el jugador
                #sin que sean unas máquinas asesinas como en Terminator.
                #Igual son capaces de atraparlo si se queda quieto mucho tiempo
                #o si el jugador es descuidado con sus movimientos
                if pacman.x > ghosts[i][0].x and counter < 2:
                    plan = options[0] #Elige moverse más a la derecha
                    course.x = plan.x
                    course.y = plan.y
                    counter +=1
                elif pacman.y > ghosts[i][0].y and counter < 2:
                    plan = options[2] #Elige moverse más arriba
                    course.x = plan.x
                    course.y = plan.y
                    counter +=1
                elif pacman.x < ghosts[i][0].x and counter < 2:
                    plan = options[1] #Elige moverse más a la izquierda
                    course.x = plan.x
                    course.y = plan.y
                    counter +=1
                elif pacman.y < ghosts[i][0].y and counter < 2:
                    plan = options[3] #Elige moverse más abajo
                    course.x = plan.x
                    course.y = plan.y
                    counter +=1
                
                #Si los fantasmas gastas 2 oportunidades de movimiento para acercarse
                #se hace que se muevan aletoriamente en la siguiente elección
                else:
                    plan = choice(options)
                    course.x = plan.x
                    course.y = plan.y
                    counter = 0


        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return
        
    ontimer(move, 50)

#Esta función cambia la dirección de Pacman
#según la tecla direccional que se presione
def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

#Se crea el recuadro inicial y se esconde la tortuga
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
#Estas lineas crean y actualizan el puntaje
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
#Estas lineas hacen que Pacman cambien su
#dirección según la tecla que es presionada
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()