# 🏗️ ARQUITECTURA DEL PROJECTE TECHSHOP

Documentació tècnica de l'arquitectura implementada.

---

## 📐 Patró Model-Vista-Controlador (MVC)

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│                      USER / BROWSER                           │
│                                                               │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ HTTP Request (GET/POST)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       VISTA (View)                            │
│                   templates/ + static/                        │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   HTML      │  │     CSS     │  │ JavaScript  │          │
│  │  (Jinja2)   │  │   Styles    │  │   Client    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
│  • base.html, products.html, cart.html, checkout.html        │
│  • style.css (modern, responsive)                            │
│  • main.js (AJAX, validations)                               │
│                                                               │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ Renderitza / Rebut esdeveniments
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  CONTROLADOR (Controller)                     │
│                      routes/ (Flask)                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Product    │  │     Cart     │  │    Order     │       │
│  │   Routes     │  │   Routes     │  │   Routes     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
│  • @app.route() decorators                                   │
│  • Request handling (GET, POST)                              │
│  • Response formatting (HTML, JSON)                          │
│  • Session management                                        │
│                                                               │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ Crida serveis
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                LÒGICA DE NEGOCI (Business Logic)              │
│                      services/                                │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Cart      │  │    Order     │  │    User      │       │
│  │   Service    │  │   Service    │  │   Service    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
│  • Validacions de negoci (màx 5 unitats)                     │
│  • Càlculs (totals, subtotals)                               │
│  • Orquestració de repositoris                               │
│  • Gestió de transaccions                                    │
│                                                               │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ Crida repositoris
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     MODEL (Models)                            │
│                        models/                                │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   User   │  │ Product  │  │  Order   │  │OrderItem │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                               │
│  • Classes Python (POPO)                                     │
│  • Atributs de dades                                         │
│  • Validacions bàsiques                                      │
│  • Mètodes to_dict()                                         │
│                                                               │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ CRUD operations
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                CAPA DE DADES (Data Access)                    │
│                     repositories/                             │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    User      │  │   Product    │  │    Order     │       │
│  │ Repository   │  │ Repository   │  │ Repository   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
│  • find_by_id(), get_all(), create(), update()               │
│  • Consultes SQL parametritzades                             │
│  • Mapatge DB ↔ Objects                                      │
│                                                               │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ SQL Queries
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   BASE DE DADES (SQLite)                      │
│                       techshop.db                             │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   user   │  │ product  │  │  order   │  │order_item│    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 🎯 Tres Capes de l'Arquitectura

### 1️⃣ CAPA DE PRESENTACIÓ

**Responsabilitats**:
- Renderitzar interfície d'usuari
- Capturar input de l'usuari
- Mostrar dades de forma visual
- Validacions client-side (UX)

**Components**:
```
templates/
├── base.html              # Layout base (herència)
├── index.html             # Pàgina principal
├── products.html          # Llista de productes
├── cart.html              # Carretó de compres
├── checkout.html          # Formulari de comanda
├── order_confirmation.html # Confirmació
└── error.html             # Pàgina d'error

static/
├── css/
│   └── style.css          # Estils moderns, responsive
└── js/
    └── main.js            # Interactivitat, AJAX
```

**NO conté**:
- ❌ Consultes SQL
- ❌ Lògica de negoci
- ❌ Accés directe a repositoris

---

### 2️⃣ CAPA DE LÒGICA DE NEGOCI

**Responsabilitats**:
- Validar regles de negoci
- Orquestrar operacions
- Calcular valors derivats
- Gestionar transaccions

**Components**:

#### Services (Serveis)
```
services/
├── cart_service.py        # Gestió del carretó
├── order_service.py       # Creació de comandes
└── user_service.py        # Autenticació, registre
```

**Exemples de Regles**:
- Màxim 5 unitats per producte
- Validar stock abans d'afegir
- Calcular totals amb Decimal
- Hash de contrasenyes
- Validar formats (email, username)

#### Routes (Controladors)
```
routes/
├── product_routes.py      # /products/*
├── cart_routes.py         # /cart/*
└── order_routes.py        # /orders/*
```

**Funcions**:
- Rebre peticions HTTP
- Validar input
- Cridar serveis
- Retornar respostes (HTML/JSON)

**NO conté**:
- ❌ SQL directe
- ❌ HTML embegut
- ❌ Lògica de presentació

---

### 3️⃣ CAPA DE DADES

**Responsabilitats**:
- Accés a base de dades
- CRUD operations
- Mapatge ORM manual
- Gestió de transaccions

**Components**:

#### Database Manager
```python
database.py
├── Database class
│   ├── get_connection()      # Context manager
│   ├── init_db()             # Crear schema
│   └── reset_db()            # Reset (dev only)
```

#### Repositories (Patró Repository)
```
repositories/
├── user_repository.py         # CRUD User
├── product_repository.py      # CRUD Product
├── order_repository.py        # CRUD Order
└── order_item_repository.py   # CRUD OrderItem
```

**Operacions típiques**:
```python
# Create
def create(entity: Model) -> int

# Read
def find_by_id(id: int) -> Optional[Model]
def get_all() -> List[Model]

# Update
def update(entity: Model) -> bool

# Delete
def delete(id: int) -> bool
```

**NO conté**:
- ❌ Lògica de negoci
- ❌ Validacions complexes
- ❌ Càlculs de totals

---

## 🔄 Flux de Dades: Exemple "Afegir al Carretó"

```
1. USER clica "Afegir al Carretó" (form submit)
   │
   ▼
2. BROWSER envia POST /cart/add
   │   product_id: 1
   │   quantity: 3
   ▼
3. ROUTES (cart_routes.py)
   │   @cart_bp.route('/add', methods=['POST'])
   │   def add_to_cart():
   │       product_id = request.form.get('product_id')
   │       quantity = request.form.get('quantity')
   │       cart = get_cart()
   ▼
4. SERVICE (cart_service.py)
   │   CartService.add_to_cart(cart, product_id, quantity)
   │   
   │   VALIDACIONS:
   │   ✓ quantity > 0?
   │   ✓ total <= 5?
   │   ✓ validate_stock()?
   │       │
   │       ▼
   │   5. REPOSITORY (product_repository.py)
   │       ProductRepository.find_by_id(product_id)
   │           │
   │           ▼
   │       6. DATABASE
   │           SELECT * FROM product WHERE id = ?
   │           │
   │           ◄───────── Row data
   │       │
   │       ◄───────── Product object
   │   │
   │   ◄─── Validation result
   │   
   │   SI OK: cart[product_id] += quantity
   │   
   │   ◄─── {'success': True, 'message': '...'}
   ▼
7. ROUTES
   │   session['cart'] = cart
   │   return jsonify(result)
   ▼
8. BROWSER rep JSON
   │   {'success': true, 'message': 'Producte afegit', 'cart_count': 4}
   ▼
9. JAVASCRIPT (main.js)
   │   Actualitza badge: cart-badge.textContent = 4
   │   Mostra notificació: showNotification('Producte afegit', 'success')
   ▼
10. USER veu confirmació visual
```

---

## 🗂️ Estructura de Carpetes Completa

```
techshop-teoarandapaez/
│
├── 📄 app.py                    # Entry point, Flask app factory
├── 📄 database.py               # Database manager
├── 📄 init_db.py               # DB initialization script
├── 📄 requirements.txt          # Dependencies
├── 📄 .gitignore               # Git ignore rules
│
├── 📄 README.md                 # User documentation
├── 📄 MEMORIA_PRACTICA.md       # Full project memory
├── 📄 INSTRUCCIONS_PROVA.md    # Test instructions
├── 📄 ARQUITECTURA.md           # This file
│
├── 📁 models/                   # MODEL - Data entities
│   ├── __init__.py
│   ├── user.py                 # User entity
│   ├── product.py              # Product entity
│   ├── order.py                # Order entity
│   └── order_item.py           # OrderItem entity
│
├── 📁 repositories/             # DATA ACCESS - Repository pattern
│   ├── __init__.py
│   ├── user_repository.py      # User CRUD
│   ├── product_repository.py   # Product CRUD
│   ├── order_repository.py     # Order CRUD
│   └── order_item_repository.py # OrderItem CRUD
│
├── 📁 services/                 # BUSINESS LOGIC - Service layer
│   ├── __init__.py
│   ├── cart_service.py         # Cart operations + validations
│   ├── order_service.py        # Order creation logic
│   └── user_service.py         # Auth, registration, password
│
├── 📁 routes/                   # CONTROLLER - HTTP handlers
│   ├── __init__.py
│   ├── product_routes.py       # Product endpoints
│   ├── cart_routes.py          # Cart endpoints
│   └── order_routes.py         # Order endpoints
│
├── 📁 templates/                # VIEW - HTML templates
│   ├── base.html               # Base layout
│   ├── index.html              # Home
│   ├── products.html           # Product listing
│   ├── cart.html               # Shopping cart
│   ├── checkout.html           # Checkout form
│   ├── order_confirmation.html # Success page
│   └── error.html              # Error page
│
├── 📁 static/                   # VIEW - Static files
│   ├── css/
│   │   └── style.css           # Styles (modern, responsive)
│   └── js/
│       └── main.js             # Client-side JavaScript
│
└── 📁 (runtime files)
    └── techshop.db             # SQLite database (created on init)
```

---

## 🔐 Principis SOLID Aplicats

### Single Responsibility Principle (SRP)
Cada classe té una única responsabilitat:
- `ProductRepository`: NOMÉS accés a dades de productes
- `CartService`: NOMÉS lògica del carretó
- `product_routes`: NOMÉS gestió de peticions HTTP

### Open/Closed Principle (OCP)
Les classes són obertes a extensió però tancades a modificació:
- Afegir nou repositori NO requereix modificar existents
- Afegir nova validació NO afecta les existents

### Dependency Inversion Principle (DIP)
Les capes superiors depenen d'abstraccions:
- Services depenen de Repositories (interfície)
- Routes depenen de Services (interfície)
- NO hi ha dependències cícliques

---

## 🎨 Patrons de Disseny Implementats

### 1. Repository Pattern
**Problema**: Accés directe a BD barrejat amb lògica  
**Solució**: Capa d'abstracció (repositories) entre BD i negoci

### 2. Service Layer Pattern
**Problema**: Lògica de negoci dispersa entre controladors  
**Solució**: Centralitzar en serveis reutilitzables

### 3. Factory Pattern
**Problema**: Inicialització complexa de l'app  
**Solució**: `create_app()` factory function

### 4. Template Method Pattern
**Problema**: Duplicació en plantilles HTML  
**Solució**: Herència Jinja2 (`{% extends "base.html" %}`)

### 5. Context Manager Pattern
**Problema**: Gestió manual de connexions BD  
**Solució**: `with db.get_connection() as conn:`

---

## 📊 Diagrama de Classes Simplificat

```
┌──────────────┐
│     User     │
├──────────────┤
│ - id         │
│ - username   │───┐
│ - password   │   │ 1
│ - email      │   │
└──────────────┘   │
                   │
                   │ *
              ┌────▼──────┐
              │   Order   │
              ├───────────┤
              │ - id      │───┐
              │ - total   │   │ 1
              │ - date    │   │
              │ - user_id │   │
              └───────────┘   │
                              │
                              │ *
                         ┌────▼────────┐
                         │  OrderItem  │
                         ├─────────────┤
                         │ - id        │
                         │ - order_id  │
                         │ - product_id│──┐
                         │ - quantity  │  │ *
                         └─────────────┘  │
                                          │
                                          │ 1
                                     ┌────▼──────┐
                                     │  Product  │
                                     ├───────────┤
                                     │ - id      │
                                     │ - name    │
                                     │ - price   │
                                     │ - stock   │
                                     └───────────┘
```

---

## 🧪 Separació de Preocupacions (Concerns)

| Concern | Capa | Exemple |
|---------|------|---------|
| **Com es mostra?** | Presentació | HTML, CSS, JS |
| **Què es pot fer?** | Negoci | Màx 5 unitats |
| **On s'emmagatzema?** | Dades | SQLite, Repository |
| **Com es valida?** | Negoci + Presentació | Doble validació |
| **Com es calcula?** | Negoci | Totals, subtotals |
| **Com s'autentica?** | Negoci | bcrypt, UserService |

---

## ✅ Beneficis de l'Arquitectura

### 🔧 Mantenibilitat
- Canviar BD (SQLite → PostgreSQL): NOMÉS tocar `database.py` i repositoris
- Canviar UI: NOMÉS tocar templates i CSS
- Afegir validació: NOMÉS tocar Service

### 🧪 Testabilitat
- Testejar serveis amb repositoris mock
- Testejar routes amb serveis mock
- Tests unitaris independents

### 🔄 Reutilització
- Services reutilitzables per API REST
- Repositoris compartits entre serveis
- Templates reutilitzables amb herència

### 👥 Col·laboració
- Frontend team: templates + static
- Backend team: services + repositories
- DB team: database + models

### 📈 Escalabilitat
- Afegir nous endpoints: Nou route + service
- Afegir noves entitats: Nou model + repository
- Afegir funcionalitats: Ampliar services

---

## 🎓 Conclusió

Aquesta arquitectura segueix els **principis professionals** de desenvolupament web:

✅ **Separació de responsabilitats**: Cada capa té el seu paper  
✅ **Baix acoblament**: Canvis en una capa NO afecten altres  
✅ **Alta cohesió**: Codi relacionat està junt  
✅ **Testable**: Fàcil de provar amb mocks  
✅ **Mantenible**: Fàcil de modificar i estendre  
✅ **Professional**: Segueix estàndards de la indústria  

---

**Autor**: Teo Aranda Paez  
**Data**: Octubre 2024 5
**Referència**: Martin Fowler - Patterns of Enterprise Application Architecture

