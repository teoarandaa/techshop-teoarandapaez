# TechShop - E-commerce Flask Application

Aplicació web de comerç electrònic per a la gestió d'un carretó de compres, desenvolupada amb Flask seguint el patró **Model-Vista-Controlador (MVC)** i l'arquitectura en **tres capes** (presentació, lògica de negoci i dades).

## 📋 Descripció del Projecte

TechShop és una botiga en línia fictícia que ven productes electrònics. Aquesta aplicació implementa:

- ✅ Arquitectura MVC amb separació clara de responsabilitats
- ✅ Gestió de productes amb control d'inventari
- ✅ Carretó de compres amb sessions
- ✅ Sistema de comandes amb gestió d'usuaris
- ✅ Validacions tant al servidor com al client
- ✅ Base de dades SQLite amb quatre taules relacionades
- ✅ Interfície moderna i responsiva

## 🏗️ Arquitectura

### Model-Vista-Controlador (MVC)

```
├── models/              # MODEL - Entitats de dades
│   ├── user.py
│   ├── product.py
│   ├── order.py
│   └── order_item.py
│
├── services/            # CONTROLADOR - Lògica de negoci
│   ├── cart_service.py
│   ├── order_service.py
│   └── user_service.py
│
├── routes/              # CONTROLADOR - Rutes HTTP
│   ├── product_routes.py
│   ├── cart_routes.py
│   └── order_routes.py
│
└── templates/           # VISTA - Presentació
    ├── base.html
    ├── products.html
    ├── cart.html
    └── checkout.html
```

### Tres Capes

1. **Capa de Presentació** (`templates/`, `static/`)
   - Plantilles HTML amb Jinja2
   - CSS modern i responsiu
   - JavaScript per interactivitat

2. **Capa de Lògica de Negoci** (`services/`)
   - `CartService`: Gestió del carretó (màxim 5 unitats per producte)
   - `OrderService`: Creació de comandes i actualització d'inventari
   - `UserService`: Registre, autenticació i validacions

3. **Capa de Dades** (`repositories/`, `database.py`)
   - Repositoris per cada entitat
   - Abstracció d'accés a SQLite
   - Context manager per transaccions

## 📊 Diagrama Entitat-Relació

```
User (1) -----> (*) Order
                  |
                  |
Order (1) -----> (*) OrderItem
                       |
                       |
OrderItem (*) -----> (1) Product
```

### Taules de la Base de Dades

**User**
- `id`: INTEGER PRIMARY KEY
- `username`: VARCHAR(20) UNIQUE
- `password_hash`: VARCHAR(60)
- `email`: VARCHAR(100) UNIQUE
- `created_at`: DATETIME

**Product**
- `id`: INTEGER PRIMARY KEY
- `name`: VARCHAR(100)
- `price`: DECIMAL(10,2)
- `stock`: INTEGER

**Order**
- `id`: INTEGER PRIMARY KEY
- `total`: DECIMAL(10,2)
- `created_at`: DATETIME
- `user_id`: INTEGER (FK → User)

**OrderItem**
- `id`: INTEGER PRIMARY KEY
- `order_id`: INTEGER (FK → Order)
- `product_id`: INTEGER (FK → Product)
- `quantity`: INTEGER

## 🚀 Instal·lació i Execució

### Requisits Previs

- Python 3.8 o superior
- pip (gestor de paquets de Python)

### Passos d'Instal·lació

1. **Clonar o descarregar el repositori**

```bash
cd techshop-teoarandapaez
```

2. **Crear un entorn virtual (recomanat)**

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

3. **Instal·lar dependències**

```bash
pip install -r requirements.txt
```

4. **Inicialitzar la base de dades**

```bash
python init_db.py
```

Això crearà la base de dades SQLite amb 15 productes de mostra.

5. **Executar l'aplicació**

```bash
python app.py
```

L'aplicació estarà disponible a: `http://localhost:5000`

### Reiniciar la Base de Dades

Per esborrar totes les dades i reiniciar:

```bash
python init_db.py --reset
```

## 🔧 Estructura del Projecte

```
techshop-teoarandapaez/
│
├── models/                 # Models de dades
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   ├── order.py
│   └── order_item.py
│
├── repositories/           # Capa d'accés a dades
│   ├── __init__.py
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── order_repository.py
│   └── order_item_repository.py
│
├── services/              # Lògica de negoci
│   ├── __init__.py
│   ├── cart_service.py
│   ├── order_service.py
│   └── user_service.py
│
├── routes/                # Controladors/Rutes
│   ├── __init__.py
│   ├── product_routes.py
│   ├── cart_routes.py
│   └── order_routes.py
│
├── templates/             # Plantilles HTML
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   └── error.html
│
├── static/                # Arxius estàtics
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── database.py            # Configuració de BD
├── app.py                 # Punt d'entrada
├── init_db.py            # Script d'inicialització
├── requirements.txt       # Dependències
├── .gitignore
└── README.md
```

## 📝 Funcionalitats Principals

### 1. Llistat de Productes

- Visualització de tots els productes disponibles
- Informació de preu i stock
- Formulari per afegir al carretó (1-5 unitats)

### 2. Carretó de Compres

- Visualització dels productes afegits
- Actualització de quantitats
- Eliminació de productes
- Càlcul automàtic de totals
- Validació de stock en temps real

**Regles de Negoci:**
- Màxim 5 unitats per producte al carretó
- No es poden afegir més unitats que les disponibles en stock

### 3. Checkout i Comanda

- Formulari amb validacions:
  - **Username**: 4-20 caràcters (alfanumèrics i guions baixos)
  - **Password**: Mínim 8 caràcters
  - **Email**: Format vàlid
  - **Adreça**: 10-200 caràcters

- Creació automàtica d'usuari si no existeix
- Processament de comanda amb actualització d'inventari
- Pàgina de confirmació amb detalls de la comanda

### 4. Validacions

**Client-side (HTML5 + JavaScript):**
- Atributs `required`, `minlength`, `maxlength`, `pattern`
- Validació de tipus (`type="email"`, `type="number"`)
- Rangs per quantitats (`min="1"`, `max="5"`)

**Server-side (Python):**
- Validació de dades d'entrada
- Comprovació de stock disponible
- Verificació de límits de quantitat
- Validació de formats (email, username, password)

## 🛡️ Seguretat

- **Contrasenyes**: Emmagatzemades amb hash bcrypt (no text pla)
- **Sessions**: Gestió segura amb Flask sessions
- **Validacions**: Doble validació (client + servidor)
- **SQL Injection**: Prevenció amb consultes parametritzades
- **Errors**: Missatges genèrics sense exposar informació interna

## 🎨 Característiques de Disseny

- **Responsive**: Adaptat a mòbils, tablets i escriptoris
- **Modern**: Disseny net amb CSS modern
- **UX**: Navegació intuïtiva i feedback visual
- **Accessibilitat**: Formularis amb labels i validacions clares

## 🧪 Proves

### Provar l'Aplicació Manualment

1. **Navegar pels productes**
   - Visita `http://localhost:5000/products`

2. **Afegir productes al carretó**
   - Prova afegir diferents quantitats (1-5)
   - Intenta afegir més de 5 unitats del mateix producte

3. **Gestionar el carretó**
   - Actualitza quantitats
   - Elimina productes
   - Buida el carretó

4. **Finalitzar compra**
   - Omple el formulari de checkout
   - Prova amb credencials noves (crea usuari)
   - Comprova la confirmació de comanda

5. **Validacions**
   - Intenta enviar formularis buits
   - Prova amb username curt (<4 caràcters)
   - Prova amb password curt (<8 caràcters)
   - Prova amb email invàlid

## 📚 Tecnologies Utilitzades

- **Backend**: Python 3.x, Flask 3.0
- **Base de Dades**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Seguretat**: bcrypt
- **Patrons**: MVC, Repository Pattern, Service Layer

## 🤖 Ús d'Intel·ligència Artificial

Aquest projecte ha estat desenvolupat amb el suport d'eines d'IA per:

- Generar esbossos de codi seguint l'arquitectura MVC
- Revisar i optimitzar la separació de capes
- Validar el compliment de requisits funcionals
- Suggerir millores en seguretat i validacions

**Regles establertes per a la IA:**
1. No barrejar codi HTML amb consultes SQL
2. Tots els accessos a BD a través de repositoris
3. Màxim 5 unitats per producte al carretó
4. Validar sempre les dades del client abans de processar
5. No exposar informació sensible en missatges d'error

Veure document de memòria per més detalls sobre l'ús d'IA.

## 👨‍💻 Autor

**Teo Aranda Paez**
- La Salle - IA & Big Data
- Pràctica: Arquitectura MVC i Tres Capes amb Flask

## 📄 Llicència

Aquest projecte és material educatiu per a la pràctica de l'assignatura.

---

**Data**: Octubre 2025  
**Versió**: 1.0

