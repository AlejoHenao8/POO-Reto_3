# POO-Reto_3

## Sistema de Facturación de Restaurante
Este proyecto consiste en un sistema básico de gestión de pedidos y facturación para un restaurante desarrollado en Python bajo el paradigma de Programación Orientada a Objetos (POO). El código permite organizar los elementos del menú en diferentes categorías como **bebidas, entradas y platos fuertes**, aplicando automáticamente reglas de precio específicas (impuestos por alcohol, recargos por porciones compartidas o costos por guarniciones) para generar una cuenta detallada y formateada para cada mesa de forma eficiente.
### Características principales
- **Gestión por categorías:** Uso de herencia para diferenciar comportamientos entre tipos de alimentos.
- **Cálculo dinámico:** Ajuste de precios basado en atributos del producto.
- **Generación de facturas:** El formato legible en consola para el resumen total de la mesa fue con ayuda de la IA.

### Diagrama UML de Clases
```mermaid
classDiagram
   direction BT
    class MenuItem {
        - name: str
        - price: float
        + total_price() float
        + description() str
    }

    class Beverage {
        - is_alcoholic: bool
        - mls: int
        + total_price() float
        + description() str
    }

    class Appetizer {
        - is_vegan: bool
        - portion: str
        + total_price() float
        + description() str
    }

    class MainCourse {
        - protein: str
        - has_garnish: bool
        + total_price() float
        + description() str
    }

    class Order {
        - table_number: int
        - items: list
        + add_item(item MenuItem)
        + total() float
        + show_bill()
        + _count_MainCourse() int
        + _count_Beverage() int
    }

    MenuItem <|-- Beverage
    MenuItem <|-- Appetizer
    MenuItem <|-- MainCourse
    Order o-- MenuItem : 0..*
```
