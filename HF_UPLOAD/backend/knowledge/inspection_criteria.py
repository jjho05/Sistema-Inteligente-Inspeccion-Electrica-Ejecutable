"""
Inspection criteria for different installation types.
Defines what to check for each type of electrical installation.
"""

INSPECTION_CRITERIA = {
    "tablero_distribucion": {
        "checklist": [
            "Identificación clara de todos los circuitos",
            "Espacio de trabajo frontal mínimo de 1 metro",
            "Conexión a tierra visible y en buen estado",
            "Interruptores termomagnéticos adecuados",
            "Ausencia de conductores sueltos o expuestos",
            "Tapa del tablero en buen estado",
            "Señalización de voltaje",
            "Ausencia de humedad o corrosión"
        ],
        "medidas_requeridas": {
            "espacio_frontal": "1.0 m mínimo",
            "altura_instalacion": "1.2 - 2.0 m",
            "ancho_acceso": "0.75 m mínimo"
        },
        "materiales_permitidos": [
            "Cobre",
            "Aluminio (con especificaciones)"
        ],
        "condiciones_rechazo": [
            "Ausencia de identificación de circuitos",
            "Conexiones expuestas sin protección",
            "Falta de conexión a tierra",
            "Espacio de trabajo insuficiente"
        ]
    },
    "puesta_tierra": {
        "checklist": [
            "Electrodo de tierra instalado correctamente",
            "Conductor de tierra continuo sin empalmes",
            "Conexiones firmes y protegidas contra corrosión",
            "Identificación del conductor (verde o verde/amarillo)",
            "Resistencia de tierra dentro de límites (< 25 Ω)",
            "Accesibilidad para inspección"
        ],
        "medidas_requeridas": {
            "resistencia_maxima": "25 Ω",
            "profundidad_electrodo": "2.4 m mínimo",
            "calibre_conductor": "Según tabla 250-122"
        },
        "materiales_permitidos": [
            "Cobre",
            "Acero galvanizado",
            "Acero inoxidable"
        ],
        "condiciones_rechazo": [
            "Resistencia superior a 25 Ω",
            "Conexiones sueltas o corroídas",
            "Conductor sin identificación",
            "Empalmes en conductor de tierra"
        ]
    },
    "alumbrado": {
        "checklist": [
            "Luminarias adecuadas para el ambiente",
            "Altura de instalación correcta",
            "Protección contra contacto directo",
            "Conexiones seguras",
            "Nivel de iluminación adecuado",
            "Interruptores accesibles"
        ],
        "medidas_requeridas": {
            "altura_minima_interior": "2.5 m",
            "altura_minima_exterior": "3.0 m",
            "nivel_iluminacion_oficina": "300-500 lux"
        },
        "materiales_permitidos": [
            "Luminarias certificadas",
            "Conductores tipo THW o THHN"
        ],
        "condiciones_rechazo": [
            "Luminarias sin protección en ambientes húmedos",
            "Altura insuficiente",
            "Conexiones expuestas",
            "Falta de protección termomagnética"
        ]
    },
    "conexiones_empalmes": {
        "checklist": [
            "Aislamiento adecuado en todas las conexiones",
            "Método de conexión apropiado (conectores certificados)",
            "Accesibilidad para inspección y mantenimiento",
            "Identificación de conductores",
            "Protección mecánica donde sea necesario",
            "Ausencia de tensión mecánica en conductores"
        ],
        "medidas_requeridas": {
            "torque_conexiones": "Según fabricante",
            "espacio_caja": "Volumen adecuado según número de conductores"
        },
        "materiales_permitidos": [
            "Conectores certificados (tipo Wirenut, compresión)",
            "Cinta aislante de grado eléctrico",
            "Cajas de conexión certificadas"
        ],
        "condiciones_rechazo": [
            "Empalmes sin aislamiento",
            "Conexiones con cinta aislante únicamente",
            "Cajas de conexión sin tapa",
            "Conductores sin identificación"
        ]
    },
    "acometida": {
        "checklist": [
            "Protección principal adecuada",
            "Distancias de seguridad cumplidas",
            "Identificación clara",
            "Medidor instalado correctamente",
            "Interruptor principal accesible",
            "Puesta a tierra de la acometida"
        ],
        "medidas_requeridas": {
            "altura_acometida": "3.0 m mínimo",
            "distancia_ventanas": "0.9 m mínimo",
            "distancia_puertas": "0.9 m mínimo"
        },
        "materiales_permitidos": [
            "Conductores tipo intemperie",
            "Tubo conduit metálico o PVC pesado"
        ],
        "condiciones_rechazo": [
            "Distancias de seguridad insuficientes",
            "Ausencia de protección principal",
            "Medidor sin sello",
            "Falta de puesta a tierra"
        ]
    },
    "industrial": {
        "checklist": [
            "Protecciones adecuadas para maquinaria",
            "Señalización de seguridad visible",
            "Programa de mantenimiento documentado",
            "Puesta a tierra de equipos",
            "Espacios de trabajo adecuados",
            "Protección contra contacto directo"
        ],
        "medidas_requeridas": {
            "espacio_trabajo": "Según voltaje (Tabla 110.26)",
            "altura_equipos": "Según especificaciones"
        },
        "materiales_permitidos": [
            "Equipos certificados para uso industrial",
            "Conductores adecuados para carga"
        ],
        "condiciones_rechazo": [
            "Ausencia de señalización",
            "Falta de mantenimiento documentado",
            "Protecciones inadecuadas",
            "Espacios de trabajo insuficientes"
        ]
    }
}

def get_criteria(installation_type):
    """Get inspection criteria for a specific installation type."""
    return INSPECTION_CRITERIA.get(installation_type, {})

def get_checklist(installation_type):
    """Get checklist for a specific installation type."""
    criteria = get_criteria(installation_type)
    return criteria.get("checklist", [])

def get_rejection_conditions(installation_type):
    """Get rejection conditions for a specific installation type."""
    criteria = get_criteria(installation_type)
    return criteria.get("condiciones_rechazo", [])
