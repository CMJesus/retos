# -*- coding: utf-8 -*-

# GRUPOS DE LETRAS EN CASTELLANO
consonantes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'll', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z' ]
vocales_abiertas = ['a', 'e', 'o', 'á', 'ó'] 
vocales_cerradas = ['i', 'í', 'u', 'ú', 'ü', 'y']
semivocales = ['y']

# GRUPOS ESPECIALES
# Diptongos:
#    Vocal cerrada + vocal abierta
#    vocal abierta + vocal cerrada
#    vocal cerrada + vocal abierta 

# Triptongos:
#    Vocal cerrada + vocal abierta + vocal cerrada

pares_consonantes = ["bl", "cl", "fl", "gl", "kl", "pl", "tl", "br", "cr", "dr", "fr", "gr", "kr", "pr", "tr", "ch", "ll", "rr"]

# ALGORITMO:

# Devuelve True si pertenece a la lista de colcales abiertas o cerradas. En cc devuelve False
def esvocal(caracter):
    caracter_encontrado = False
    if caracter in vocales_abiertas:
        caracter_encontrado = True
    elif caracter in vocales_cerradas:
            caracter_encontrado = True
    else:
        if caracter in semivocales:
            caracter_encontrado = True        
    return caracter_encontrado

def esdiptongo(caracteres):
    diptongo_encontrado = False
    if len(caracteres) == 2:
        vocal1 = caracteres[0]
        vocal2 = caracteres[1]
        if (vocal1 in vocales_cerradas) and (vocal2 in vocales_cerradas):
            diptongo_encontrado = True
        elif (vocal1 in vocales_abiertas) and (vocal2 in vocales_cerradas):
            diptongo_encontrado = True
        else:
            if (vocal1 in vocales_abiertas) and (vocal2 in vocales_cerradas):
                diptongo_encontrado = True       
    return diptongo_encontrado

def estriptongo(caracteres):
    triptongo_encontrado = False
    if len(caracteres) == 3:
        vocal1 = caracteres[0]
        vocal2 = caracteres[1]
        vocal3 = caracteres[2]
        if (vocal1 in vocales_cerradas) and (vocal2 in vocales_abiertas) and (vocal3 in vocales_cerradas):
            triptongo_encontrado = True      
    return triptongo_encontrado    

def obtener_grupos_vocales(palabra):
    grupos_vocales = []
    indices_grupos_vocales = []
    grupo_vocales = ""
    indice_grupo = 0 # posicion con base 0 del primer elemento del grupo

    for caracter in palabra:
        if esvocal(caracter):
            grupo_vocales = grupo_vocales + caracter
        else:
            if grupo_vocales != "":
                indices_grupos_vocales.append(indice_grupo - len(grupo_vocales))
                grupos_vocales.append(grupo_vocales)
                grupo_vocales = ""

        indice_grupo = indice_grupo + 1

    if grupo_vocales != "":
        indices_grupos_vocales.append(indice_grupo - len(grupo_vocales))
        grupos_vocales.append(grupo_vocales)

    return grupos_vocales, indices_grupos_vocales

def actualizar_grupos_vocales_especiales(grupos_vocales, indices_grupos_vocales):
    grupos_vocales_nuevo = []
    indices_grupos_vocales_nuevo = []

    for i in range(len(grupos_vocales)):
        grupo_vocales = grupos_vocales[i]
        indice_grupo = indices_grupos_vocales[i]
        if len(grupo_vocales) == 2 and not esdiptongo(grupo_vocales):
            #Esto es solo un ejemplo partiendo por la vocal abierta, en realidad creo 
            grupos_vocales_nuevo.append(grupo_vocales[:1])
            indices_grupos_vocales_nuevo.append(indice_grupo)

            grupos_vocales_nuevo.append(grupo_vocales[1:])
            indices_grupos_vocales_nuevo.append(indice_grupo + 1)

        elif len(grupo_vocales) == 3 and not estriptongo(grupo_vocales):
            #Esto es solo un ejemplo partiendo por la vocal abierta, en realidad creo 
            grupos_vocales_nuevo.append(grupo_vocales[:2])
            indices_grupos_vocales_nuevo.append(indice_grupo)
    
            grupos_vocales_nuevo.append(grupo_vocales[2:])
            indices_grupos_vocales_nuevo.append(indice_grupo + 2)
            
        else:  
            grupos_vocales_nuevo.append(grupo_vocales)
            indices_grupos_vocales_nuevo.append(indice_grupo)
        
    return grupos_vocales_nuevo, indices_grupos_vocales_nuevo

def asignar_consonante_previa(grupos_vocales, indices_grupos_vocales, palabra):
    for i in range(len(grupos_vocales)):
        grupo_vocales = grupos_vocales[i]
        indice_grupo = indices_grupos_vocales[i]
        if indice_grupo > 1 and palabra[indice_grupo-2:indice_grupo-1] in pares_consonantes:
            grupos_vocales[i] = palabra[indice_grupo-2:indice_grupo-1] + grupo_vocales
            indices_grupos_vocales[i] = indice_grupo - 2
        else:
            if indice_grupo > 0 and palabra[indice_grupo - 1] in consonantes:
                grupos_vocales[i] = palabra[indice_grupo - 1] + grupo_vocales
                indices_grupos_vocales[i] = indice_grupo - 1
                
    return grupos_vocales, indices_grupos_vocales

def agregar_caracteres_sin_usar(grupos_vocales, indices_grupos_vocales, palabra):
    if len(grupos_vocales) > 0:
        for i in range(len(grupos_vocales) - 1):
            indice_fin_palabra_i = indices_grupos_vocales[i] + len(grupos_vocales[i])
            num_caracteres_sin_utilizar = indices_grupos_vocales[i + 1] - indice_fin_palabra_i 
            if num_caracteres_sin_utilizar > 0:
                caracteres_sin_utilizar = palabra[indice_fin_palabra_i: indices_grupos_vocales[i + 1]]
                grupos_vocales[i] = grupos_vocales[i] + caracteres_sin_utilizar
        
        grupos_vocales[len(grupos_vocales)-1] = palabra[indices_grupos_vocales[len(grupos_vocales)-1]:]
                            
    return grupos_vocales
        
def obtener_silabas(palabra):
    # cons tan te
    # ([o, a, e] , [1, 5, 8])
    grupos_vocales, indices_grupos_vocales = obtener_grupos_vocales(palabra)
    print (grupos_vocales, indices_grupos_vocales)
    grupos_vocales, indices_grupos_vocales = actualizar_grupos_vocales_especiales(grupos_vocales, indices_grupos_vocales)
    print (grupos_vocales, indices_grupos_vocales)
    # ([co, ta, te] , [0, 4, 7])
    grupos_vocales, indices_grupos_vocales = asignar_consonante_previa(grupos_vocales, indices_grupos_vocales, palabra)
    print (grupos_vocales, indices_grupos_vocales)
    # ([cons, tan, te]) 
    silabas = agregar_caracteres_sin_usar(grupos_vocales, indices_grupos_vocales, palabra)
    return silabas

print (obtener_silabas('buey'))
print (obtener_silabas('guión'))
print (obtener_silabas('guían'))
print (obtener_silabas('guía'))
print (obtener_silabas('constante'))
print (obtener_silabas('estancia'))