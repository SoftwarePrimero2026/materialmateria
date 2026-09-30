# Buscaminas — Reglas del juego

## Objetivo

Destapar todas las casillas que **no** contienen una mina, sin pisar ninguna mina.

## Tablero

- Cuadrícula de casillas (tamaños típicos: 9×9, 16×16, 30×16).
- Cada tablero tiene un **número fijo de minas** ocultas distribuidas al azar.
- Las minas se colocan al generar el tablero (usualmente en el primer clic del jugador).

## Controles

| Acción | Efecto |
|---|---|
| **Clic izquierdo** (o toque) | Destapa la casilla |
| **Clic derecho** (o Shift+clic / largo en móvil) | Coloca o quita una **banderita** (marcador) |
| **Medio clic / clic en número** (SoloPC, "chording") | Si un número ya tiene tantas banderitas como indica, destapa las casillas vecinas restantes |

## Cómo funciona al destapar

| Lo que muestra la casilla | Significado |
|---|---|
| **0** (vacío, a veces se revela en verde/azul) | No hay minas en los 8 vecinos; se destapan recursivamente las casillas adyacentes |
| **1–8** (número) | Cantidad exacta de minas en las 8 casillas vecinas (N, S, E, O + 4 diagonales) |
| **Mina** (💣) | La casilla contiene una mina → **pierdés** |

## Banderitas (marcadores)

- No destapan la casilla; solo la marcan como "acá creo que hay mina".
- Sirven para contar: cuando la cantidad de banderitas vecinas de un número coincide con el número, podés usar el medio clic para destapar seguro las casillas restantes.
- Poner demasiadas banderitas no hace perder, pero dificulta la cuenta si no son correctas.

## Victoria

Destapás **todas** las casillas que no son mina. El juego termina en victoria aunque queden banderitas sin confirmar.

## Derrota

Pisás una mina (clic izquierdo sobre una mina). El juego acaba:
- Se revela la mina que pisaste.
- Usualmente se muestran todas las demás minas del tablero.

## Estrategia básica

1. **Primeros clics:** en la mayoría de implementaciones el tablero se genera en el primer clic, que es libre de mina. Un clique en el centro o esquina es común de inicio.
2. **Esquinas y bordes:** tienen menos vecinos (3 en esquina, 5 en borde), lo que los hace más seguros para empezar a leer los números.
3. **Contar minas:** los números son información directa — si un 1 ya tiene una banderita vecina, el resto de sus vecinos son seguros.
4. **Patrones conocidos:**
   - `1-1` contra un borde: la mina está en la posición compartida de los dos 1s.
   - `1-2` contra un borde: la mina está en la casilla más lejana del 2.
   - `2-1` contra un borde: la mina está en la casilla más cercana al 2.
5. **Atribución (chording):** una vez que tenés la cantidad correcta de banderitas en cada número, usá el medio clic para destapar seguro. Es la base del juego avanzado.

## Variantes comunes

| Variante | Nivel | Filas × Columnas | Minas |
|---|---|---|---|
| Fácil | Beginner | 9 × 9 | 10 |
| Medio | Intermediate | 16 × 16 | 40 |
| Difícil | Expert | 30 × 16 | 99 |

> Algunas implementaciones permiten tableros personalizados (dimensiones y cantidad de minas arbitrarias).

## Resumen rápido

- Destapar sin pisar minas = ganar.
- Los números cuentan minas vecinas → son la única pista.
- Las banderitas organizan la información; no cambian el estado del juego.
- El primer clic es seguro; después todo depende de leer los números.
