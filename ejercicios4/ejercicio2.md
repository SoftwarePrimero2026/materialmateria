# Ejercicio 2 — Sistema de turnos de una peluquería

## La situación

Tengo una peluquería y atiendo **con turnos**. Quiero un programa que me ayude a manejar
la agenda del día: ver qué horarios están libres, reservar un turno para un cliente,
cancelarlo si avisa que no viene, y al final del día ver un resumen.

## Lo que necesito que haga el programa

La peluquería atiende en **horarios fijos** definidos en el código, por ejemplo:
`09:00, 10:00, 11:00, 12:00, 16:00, 17:00, 18:00`. Cada horario puede estar **libre** o
**reservado por un cliente**.

El programa debe mostrar un **menú** que se repita hasta que yo elija salir:

1. **Ver agenda**: muestra todos los horarios indicando si están libres o, si están
   ocupados, el nombre del cliente que reservó.
2. **Reservar un turno**: muestra los horarios **libres**, me deja elegir uno y pide el
   nombre del cliente. Si el horario ya está ocupado, debe avisar.
3. **Cancelar un turno**: me pide el horario y, si estaba reservado, lo libera. Si ya
   estaba libre, avisa que no había nada que cancelar.
4. **Buscar el turno de un cliente**: me pide un nombre y me dice en qué horario tiene el
   turno (o que no tiene ninguno).
5. **Ver resumen del día**: muestra cuántos turnos hay **reservados**, cuántos quedan
   **libres** y el **porcentaje de ocupación** de la agenda.
6. **Salir**.

## Detalles importantes

- Cada horario está asociado a un cliente (o a "libre"). Pensá bien qué estructura te
  permite relacionar cada horario con quién lo reservó.
- No se puede reservar un horario que **no existe** en la agenda ni uno que ya está
  **ocupado**: el programa debe avisar.
- Un mismo cliente no debería poder tener **dos turnos** el mismo día (al reservar,
  verificá que el nombre no esté ya en la agenda).
- Si elijo una opción inválida del menú, el programa debe avisar y volver a mostrarlo.
- El porcentaje de ocupación se calcula como `turnos reservados / total de horarios × 100`.

## Pista de qué conceptos entran en juego

Una estructura para relacionar cada horario con su estado/cliente (pensá en
diccionarios), un ciclo para el menú, decisiones para validar reservas y cancelaciones,
recorridos para buscar y contar, funciones para organizar cada acción y cálculos de
porcentajes. El manejo de errores te sirve para las opciones y los datos mal ingresados.
