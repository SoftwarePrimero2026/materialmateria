"""Genera los assets del dado con Blender.

Produce dos cosas:

1. `dado.glb` — el dado 3D completo (cubo biselado + pipas como geometria real)
   con un marcador por cara, listo para importar en Godot y hacerlo rodar con
   fisica. Los marcadores son empties llamados `cara_1` .. `cara_6` ubicados en
   el centro de cada cara: Godot los usa para saber que cara quedo hacia arriba
   despues de la tirada (ver src/dado3d.gd). El mapeo se verifica en runtime,
   asi que no depende de la convencion de ejes.

2. `cara_1.png` .. `cara_6.png` — las 6 caras renderizadas, para vista previa o
   para usar como textura.

Las pipas se ubican en las posiciones estandar (caras opuestas suman 7):

    +X -> 1     -X -> 6
    +Y -> 2     -Y -> 5
    +Z -> 3     -Z -> 4

La iluminacion esta definida RELATIVA a la camara y rota con ella, de modo que
las 6 caras se renderizan con exactamente la misma luz. Si las luces quedaran
fijas, cada cara saldria con una iluminacion distinta y el set no serviria como
textura coherente.

Uso:
    blender -b --python generar_dados_blender.py -- [opciones]

    --salida DIR    Carpeta de destino (por defecto ../diezmil_godot/assets/dados)
    --res N         Resolucion de las caras en pixeles (por defecto 512)
    --muestras N    Muestras de Cycles (por defecto 48)
    --solo-glb      Exporta solo el modelo, sin renderizar las caras
    --solo-caras    Renderiza solo las caras, sin exportar el modelo
"""

import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

# --- Mapa de caras: normal local -> valor de la cara ----------------------
# Las caras opuestas suman 7 (dado estandar).
CARAS = [
    ((1, 0, 0), 1),
    ((-1, 0, 0), 6),
    ((0, 1, 0), 2),
    ((0, -1, 0), 5),
    ((0, 0, 1), 3),
    ((0, 0, -1), 4),
]

# --- Disposicion de las pipas en una cara --------------------------------
# Coordenadas (u, v) dentro de la cara, en el rango [-0.5, 0.5].
SEP = 0.26  # separacion de las pipas respecto del centro
PIPAS = {
    1: [(0, 0)],
    2: [(-SEP, -SEP), (SEP, SEP)],
    3: [(-SEP, -SEP), (0, 0), (SEP, SEP)],
    4: [(-SEP, -SEP), (-SEP, SEP), (SEP, -SEP), (SEP, SEP)],
    5: [(-SEP, -SEP), (-SEP, SEP), (0, 0), (SEP, -SEP), (SEP, SEP)],
    6: [(-SEP, -SEP), (-SEP, 0), (-SEP, SEP),
        (SEP, -SEP), (SEP, 0), (SEP, SEP)],
}

TAMANO = 1.0        # lado del dado
BISEL = 0.055       # ancho del bisel de los bordes
RADIO_PIPA = 0.085  # radio de cada pipa
ALTO_PIPA = 0.018   # cuanto sobresale la pipa de la cara

# Luces definidas relativo a la camara: (posicion, energia, tamano).
LUCES = [
    ((1.6, 1.9, 2.2), 260.0, 2.4),    # key: arriba y a un costado
    ((-2.0, 1.1, 1.2), 110.0, 2.8),   # fill: del otro costado, mas suave
    ((0.0, -1.4, 2.0), 130.0, 2.2),   # rim: por detras, despega del fondo
]


def limpiar_escena():
    """Borra todo lo que haya en la escena."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for bloque in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras,
                   bpy.data.lights, bpy.data.objects):
        for item in list(bloque):
            if item.users == 0:
                bloque.remove(item)


def crear_material(nombre, color, rugosidad=0.35, metalico=0.0):
    """Crea un material Principled simple."""
    mat = bpy.data.materials.new(nombre)
    if not mat.use_nodes:
        mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = rugosidad
        bsdf.inputs["Metallic"].default_value = metalico
    return mat


def ejes_de_cara(n):
    """Devuelve dos ejes tangentes (u, v) para una normal de cara."""
    if abs(n.x) > 0.5:
        return Vector((0, 1, 0)), Vector((0, 0, 1))
    if abs(n.y) > 0.5:
        return Vector((1, 0, 0)), Vector((0, 0, 1))
    return Vector((1, 0, 0)), Vector((0, 1, 0))


def suavizar(obj, angulo_grados=40.0):
    """Aplica sombreado suave respetando los angulos marcados.

    Sin esto el bisel se ve facetado y el dado parece low-poly. En Blender
    4.1+ se usa el operador `shade_auto_smooth`, que agrega un modificador
    "Smooth by Angle"; se aplica de inmediato para que las normales queden
    horneadas en la malla y el exportador glTF las lleve al .glb.
    """
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.shade_smooth()
    if hasattr(obj.data, "use_auto_smooth"):
        obj.data.use_auto_smooth = True
        if hasattr(obj.data, "auto_smooth_angle"):
            obj.data.auto_smooth_angle = math.radians(angulo_grados)
    else:
        try:
            bpy.ops.object.shade_auto_smooth(angle=math.radians(angulo_grados))
            # Hornear el modificador "Smooth by Angle": si queda pendiente,
            # las normales suaves no llegan al .glb exportado.
            for mod in list(obj.modifiers):
                if "Smooth" in mod.name or "Angle" in mod.name:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception as e:
            print(f"  (aviso: no se pudo aplicar auto-smooth: {e})")


def crear_dado(mat_cuerpo, mat_pipa):
    """Crea el dado y devuelve la lista de objetos a exportar."""
    a_exportar = []

    # --- Cuerpo: cubo con bordes redondeados ---
    bpy.ops.mesh.primitive_cube_add(size=TAMANO)
    cuerpo = bpy.context.active_object
    cuerpo.name = "Dado_Cuerpo"
    cuerpo.data.materials.append(mat_cuerpo)

    mod = cuerpo.modifiers.new(name="Bisel", type="BEVEL")
    mod.width = BISEL
    mod.segments = 6
    mod.limit_method = "ANGLE"
    bpy.ops.object.modifier_apply(modifier=mod.name)

    # El bisel debe verse redondeado, no facetado.
    suavizar(cuerpo, 45.0)

    a_exportar.append(cuerpo)

    mitad = TAMANO / 2.0
    for normal, valor in CARAS:
        n = Vector(normal)
        eje_u, eje_v = ejes_de_cara(n)

        # --- Empty marcador en el centro de la cara ---
        # Godot busca cual tiene la mayor componente Y global: ese es el valor
        # que quedo arriba. Verificarlo en runtime evita depender del mapeo de
        # ejes de la exportacion.
        bpy.ops.object.empty_add(type="PLAIN_AXES",
                                 location=n * (mitad + 0.001))
        marcador = bpy.context.active_object
        marcador.name = f"cara_{valor}"
        marcador.empty_display_size = 0.12
        a_exportar.append(marcador)

        # --- Pipas de la cara ---
        for (u, v) in PIPAS[valor]:
            centro = n * mitad + eje_u * u + eje_v * v
            centro = centro + n * (ALTO_PIPA / 2.0)

            bpy.ops.mesh.primitive_cylinder_add(
                radius=RADIO_PIPA,
                depth=ALTO_PIPA,
                vertices=32,
                location=centro,
            )
            pipa = bpy.context.active_object
            pipa.name = f"Pipa_{valor}_{u:.2f}_{v:.2f}"
            pipa.data.materials.append(mat_pipa)

            if abs(n.y) > 0.5:
                pipa.rotation_euler = (math.radians(90), 0, 0)
            elif abs(n.x) > 0.5:
                pipa.rotation_euler = (0, math.radians(90), 0)

            # Las pipas son cilindros: se suavizan para que se vean redondas.
            suavizar(pipa, 40.0)
            a_exportar.append(pipa)

    return a_exportar


def crear_camara_ortogonal():
    """Camara ortogonal que encuadra exactamente el dado."""
    cam_data = bpy.data.cameras.new("Camara")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = TAMANO * 1.02
    cam = bpy.data.objects.new("Camara", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


def crear_luces():
    """Crea las luces de area. Devuelve la lista de objetos."""
    objetos = []
    for i, (_pos, energia, tamano) in enumerate(LUCES):
        bpy.ops.object.light_add(type="AREA", location=(0, 0, 0))
        luz = bpy.context.active_object
        luz.name = f"Luz_{i}"
        luz.data.energy = energia
        luz.data.size = tamano
        objetos.append(luz)
    return objetos


def apuntar_al_origen(obj, pos):
    """Ubica `obj` en `pos` mirando al origen."""
    obj.location = pos
    direccion = Vector((0, 0, 0)) - Vector(pos)
    obj.rotation_euler = direccion.to_track_quat("-Z", "Y").to_euler()


def orientar_para_cara(cam, luces, normal):
    """Orienta camara Y luces para mirar una cara, conservando la luz relativa."""
    n = Vector(normal)
    apuntar_al_origen(cam, n * 6.0)

    # Rotacion que lleva el eje +Z a la normal de la cara. Se aplica igual a
    # las posiciones relativas de las luces, asi la iluminacion no cambia.
    rot = Vector((0, 0, 1)).rotation_difference(n)
    for luz, (pos_rel, _e, _t) in zip(luces, LUCES):
        apuntar_al_origen(luz, rot @ Vector(pos_rel))


def configurar_render(res, muestras):
    """Configura Cycles para un render limpio."""
    escena = bpy.context.scene
    escena.render.engine = "CYCLES"
    escena.cycles.samples = muestras
    escena.cycles.use_denoising = True
    escena.render.resolution_x = res
    escena.render.resolution_y = res
    escena.render.resolution_percentage = 100
    escena.render.film_transparent = False
    escena.render.image_settings.file_format = "PNG"
    escena.render.image_settings.color_mode = "RGB"

    # Fondo oscuro a tono con la interfaz del juego.
    mundo = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    escena.world = mundo
    if not mundo.use_nodes:
        mundo.use_nodes = True
    fondo = mundo.node_tree.nodes.get("Background")
    if fondo:
        fondo.inputs[0].default_value = (0.05, 0.06, 0.09, 1.0)
        fondo.inputs[1].default_value = 0.4


def exportar_glb(objetos, destino):
    """Exporta el dado a glTF binario (.glb)."""
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objetos:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objetos[0]

    bpy.ops.export_scene.gltf(
        filepath=destino,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,          # convencion Y-up de glTF/Godot
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
    )
    return destino


def main():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []

    parser = argparse.ArgumentParser(description="Genera los assets del dado")
    parser.add_argument("--salida", default=None)
    parser.add_argument("--res", type=int, default=512)
    parser.add_argument("--muestras", type=int, default=48)
    parser.add_argument("--solo-glb", action="store_true")
    parser.add_argument("--solo-caras", action="store_true")
    args = parser.parse_args(argv)

    if args.salida is None:
        aqui = os.path.dirname(os.path.abspath(__file__))
        args.salida = os.path.normpath(
            os.path.join(aqui, "..", "diezmil_godot", "assets", "dados"))
    os.makedirs(args.salida, exist_ok=True)

    print("=== Generando los assets del dado con Blender ===")
    print(f"  Blender: {bpy.app.version_string}")
    print(f"  Salida:  {args.salida}")
    print()

    limpiar_escena()

    # Dado claro sobre mesa oscura, a tono con la interfaz del juego.
    mat_cuerpo = crear_material("Cuerpo_Dado", (0.92, 0.93, 0.96), 0.28)
    mat_pipa = crear_material("Pipa", (0.09, 0.10, 0.13), 0.30)

    a_exportar = crear_dado(mat_cuerpo, mat_pipa)

    # --- 1) Modelo 3D ---
    if not args.solo_caras:
        destino = os.path.join(args.salida, "dado.glb")
        exportar_glb(a_exportar, destino)
        kb = os.path.getsize(destino) // 1024
        print(f"  Modelo exportado: {kb} KB  {destino}")
        print(f"    Objetos: {len(a_exportar)} "
              f"(1 cuerpo + 6 marcadores + pipas)")

    # --- 2) Caras renderizadas ---
    if not args.solo_glb:
        cam = crear_camara_ortogonal()
        luces = crear_luces()
        configurar_render(args.res, args.muestras)

        print()
        print(f"  Renderizando las 6 caras a {args.res}x{args.res}...")
        for normal, valor in CARAS:
            orientar_para_cara(cam, luces, normal)
            destino = os.path.join(args.salida, f"cara_{valor}.png")
            bpy.context.scene.render.filepath = destino
            bpy.ops.render.render(write_still=True)
            print(f"    cara {valor} ({normal}) -> {os.path.basename(destino)}")

    print()
    print("  Listo.")


if __name__ == "__main__":
    main()
