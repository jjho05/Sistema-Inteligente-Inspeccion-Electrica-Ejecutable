"""
Installation types and their associated metadata.
Defines the different types of electrical installations that can be inspected.
"""

INSTALLATION_TYPES = {
    "tablero_distribucion": {
        "nombre": "Tablero de Distribución",
        "descripcion": "Tablero eléctrico de distribución residencial, comercial o industrial",
        "normas": [
            "NOM-001-SEDE-2012 Artículo 408",
            "NOM-001-SEDE-2012 Artículo 110"
        ],
        "elementos_clave": [
            "interruptores",
            "identificación de circuitos",
            "conexión a tierra",
            "espacios de trabajo",
            "protecciones"
        ],
        "prompt_template": "tablero_template",
        "icon": "📊"
    },
    "puesta_tierra": {
        "nombre": "Sistema de Puesta a Tierra",
        "descripcion": "Sistema de protección mediante puesta a tierra",
        "normas": [
            "NMX-J-549-ANCE-2005",
            "NOM-001-SEDE-2012 Artículo 250"
        ],
        "elementos_clave": [
            "electrodo de tierra",
            "conductor de tierra",
            "conexiones",
            "continuidad",
            "resistencia"
        ],
        "prompt_template": "tierra_template",
        "icon": "⚡"
    },
    "alumbrado": {
        "nombre": "Instalación de Alumbrado",
        "descripcion": "Sistema de iluminación interior o exterior",
        "normas": [
            "NOM-001-SEDE-2012 Artículo 410",
            "NOM-025-STPS-2008"
        ],
        "elementos_clave": [
            "luminarias",
            "altura de instalación",
            "protecciones",
            "conexiones",
            "nivel de iluminación"
        ],
        "prompt_template": "alumbrado_template",
        "icon": "💡"
    },
    "conexiones_empalmes": {
        "nombre": "Conexiones y Empalmes",
        "descripcion": "Conexiones eléctricas y empalmes de conductores",
        "normas": [
            "NOM-001-SEDE-2012 Artículo 110.14",
            "NOM-001-SEDE-2012 Artículo 300"
        ],
        "elementos_clave": [
            "aislamiento",
            "método de conexión",
            "accesibilidad",
            "identificación",
            "protección mecánica"
        ],
        "prompt_template": "conexiones_template",
        "icon": "🔌"
    },
    "acometida": {
        "nombre": "Acometida Eléctrica",
        "descripcion": "Punto de conexión de la red de suministro",
        "normas": [
            "NOM-001-SEDE-2012 Artículo 230"
        ],
        "elementos_clave": [
            "protecciones",
            "distancias de seguridad",
            "identificación",
            "medidor",
            "interruptor principal"
        ],
        "prompt_template": "acometida_template",
        "icon": "🏗️"
    },
    "industrial": {
        "nombre": "Instalación Industrial",
        "descripcion": "Instalación eléctrica en entorno industrial",
        "normas": [
            "NOM-001-SEDE-2012 Artículo 430",
            "NOM-029-STPS-2011"
        ],
        "elementos_clave": [
            "maquinaria",
            "protecciones",
            "señalización",
            "mantenimiento",
            "seguridad"
        ],
        "prompt_template": "industrial_template",
        "icon": "🏭"
    },
    'desconocido': {
        'nombre': 'Desconocido / Otro',
        'descripcion': 'Tipo de instalación desconocida o no especificada. El sistema analizará la imagen y determinará el tipo automáticamente.',
        'normas': [
            'NOM-001-SEDE-2012 (General)',
            'NOM-029-STPS-2011 (Seguridad)'
        ],
        'elementos_clave': [
            'componentes eléctricos',
            'conductores',
            'protecciones',
            'conexiones'
        ],
        'prompt_template': 'general_template',
        'icon': '❓'
    }
}

def get_installation_type(type_id):
    """Get installation type by ID."""
    return INSTALLATION_TYPES.get(type_id)

def get_all_types():
    """Get all installation types."""
    return INSTALLATION_TYPES

def get_type_names():
    """Get list of installation type names for UI."""
    return {
        type_id: {
            "nombre": data["nombre"],
            "descripcion": data["descripcion"],
            "icon": data["icon"]
        }
        for type_id, data in INSTALLATION_TYPES.items()
    }
