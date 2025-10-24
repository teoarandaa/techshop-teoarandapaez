# 🧪 INSTRUCCIONS DE PROVA - TechShop

Guia ràpida per provar totes les funcionalitats de l'aplicació TechShop.

---

## 🚀 Inici Ràpid

### 1. Instal·lació

```bash
# Navegar al directori del projecte
cd techshop-teoarandapaez

# Crear entorn virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# o venv\Scripts\activate en Windows

# Instal·lar dependències
pip install -r requirements.txt

# Inicialitzar base de dades
python init_db.py
```

### 2. Executar l'Aplicació

```bash
python app.py
```

Obre el navegador a: **http://localhost:5000**

---

## 📋 Casos de Prova

### ✅ TEST 1: Navegació Bàsica

1. Accedeix a http://localhost:5000
2. **Verifica**: Pàgina d'inici amb hero i 4 features
3. Clica "Explorar Productes"
4. **Verifica**: 15 productes en grid responsiu
5. **Verifica**: Badge del carretó mostra "0"

**Expected**: Navegació fluida, disseny modern

---

### ✅ TEST 2: Afegir Productes al Carretó

#### 2.1 Afegir 1 Unitat
1. A la pàgina de productes, selecciona "iPhone 15 Pro"
2. Quantitat: 1
3. Clica "Afegir al Carretó"
4. **Verifica**: Missatge de confirmació
5. **Verifica**: Badge carretó = "1"

#### 2.2 Afegir Múltiples Unitats
1. Selecciona "Samsung Galaxy S24"
2. Quantitat: 3
3. Clica "Afegir al Carretó"
4. **Verifica**: Badge carretó = "4" (1 + 3)

#### 2.3 Límit Màxim (5 unitats)
1. Selecciona "MacBook Air M2"
2. Quantitat: 5
3. Afegeix al carretó ✅
4. Intenta afegir 1 més del mateix producte
5. **Verifica**: Error "No pots afegir més de 5 unitats"

#### 2.4 Validació de Quantitat
1. Intenta canviar quantitat a 0 o negatiu
2. **Verifica**: HTML5 impedeix valors < 1
3. Intenta canviar a 6
4. **Verifica**: HTML5 impedeix valors > 5

---

### ✅ TEST 3: Gestió del Carretó

1. Clica la icona del carretó (badge)
2. **Verifica**: Llista de productes afegits
3. **Verifica**: Subtotals correctes per cada producte
4. **Verifica**: Total general correcte

#### 3.1 Actualitzar Quantitat
1. Canvia quantitat d'un producte
2. Clica "Actualitzar"
3. **Verifica**: Subtotal i total s'actualitzen

#### 3.2 Eliminar Producte
1. Clica "Eliminar" en un producte
2. Confirma l'eliminació
3. **Verifica**: Producte desapareix
4. **Verifica**: Total recalculat

#### 3.3 Buidar Carretó
1. Clica "Buidar Carretó"
2. Confirma
3. **Verifica**: Carretó buit
4. **Verifica**: Badge = "0"

---

### ✅ TEST 4: Checkout - Validacions Frontend

Afegeix productes al carretó i clica "Finalitzar Compra"

#### 4.1 Camps Buits
1. Intenta enviar formulari buit
2. **Verifica**: Errors HTML5 "Aquest camp és obligatori"

#### 4.2 Username Invàlid
**Test**: Username curt
- Input: "abc"
- **Verifica**: Error "mínim 4 caràcters"

**Test**: Username llarg
- Input: 21 caràcters
- **Verifica**: Error "màxim 20 caràcters"

**Test**: Username amb espais
- Input: "user name"
- **Verifica**: Error "només alfanumèrics"

#### 4.3 Password Invàlid
- Input: "1234567" (7 caràcters)
- **Verifica**: Error "mínim 8 caràcters"

#### 4.4 Email Invàlid
- Input: "notanemail"
- **Verifica**: Error "format invàlid"

#### 4.5 Adreça Curta
- Input: "Curt" (< 10 caràcters)
- **Verifica**: Error "mínim 10 caràcters"

---

### ✅ TEST 5: Checkout - Creació de Comanda

#### 5.1 Usuari Nou
Omple el formulari amb dades vàlides:
```
Username: testuser2025
Password: password123
Email: test@example.com
Adreça: Carrer Example 123, Barcelona, 08001
```

1. Clica "Confirmar Comanda"
2. **Verifica**: Redirecció a pàgina de confirmació
3. **Verifica**: Número de comanda generat
4. **Verifica**: Llista de productes correcta
5. **Verifica**: Total correcte
6. **Verifica**: Data i hora mostrades

#### 5.2 Usuari Existent
1. Torna a afegir productes
2. Al checkout, usa el mateix username i password
3. **Verifica**: Login automàtic (no crea usuari duplicat)
4. **Verifica**: Comanda es crea correctament

---

### ✅ TEST 6: Actualització d'Inventari

1. Abans de comprar, nota el stock del producte
   - Exemple: iPhone 15 Pro - Stock: 15
2. Afegeix 3 unitats al carretó
3. Completa la compra
4. Torna a la llista de productes
5. **Verifica**: Stock = 12 (15 - 3)

---

### ✅ TEST 7: Validacions Backend

Aquestes proves requereixen manipular peticions (Postman/curl o DevTools):

#### 7.1 Quantitat Invàlida (Bypass HTML5)
```bash
curl -X POST http://localhost:5000/cart/add \
  -d "product_id=1&quantity=10"
```
**Verifica**: Error 400 "Màxim 5 unitats"

#### 7.2 Producte Inexistent
```bash
curl -X POST http://localhost:5000/cart/add \
  -d "product_id=999&quantity=1"
```
**Verifica**: Error "Producte no trobat"

#### 7.3 Stock Insuficient
1. Compra fins deixar stock = 1
2. Intenta afegir 2 unitats
**Verifica**: Error "Stock insuficient"

---

### ✅ TEST 8: Seguretat

#### 8.1 Contrasenyes Hasheades
1. Registra un usuari
2. Obre `techshop.db` amb un editor SQLite
3. Consulta: `SELECT * FROM user;`
4. **Verifica**: `password_hash` és un hash bcrypt (comença amb `$2b$`)
5. **Verifica**: NO és la contrasenya en text pla

#### 8.2 SQL Injection
Intenta username: `' OR '1'='1`
**Verifica**: No causa errors, es tracta com a text normal

#### 8.3 Sessions
1. Afegeix productes al carretó
2. Tanca el navegador
3. Reobre i torna a la pàgina
4. **Verifica**: Carretó es manté (sessió persistent)

---

### ✅ TEST 9: Responsivitat

#### 9.1 Mòbil (< 768px)
1. Obre DevTools (F12)
2. Activa vista mòbil (iPhone SE)
3. **Verifica**: Grid de productes = 1 columna
4. **Verifica**: Navegació llegible
5. **Verifica**: Formularis usables

#### 9.2 Tablet (768px - 968px)
1. Vista iPad
2. **Verifica**: Grid adaptatiu
3. **Verifica**: Checkout en 1 columna

#### 9.3 Desktop (> 968px)
1. Vista normal
2. **Verifica**: Grid 3-4 columnes
3. **Verifica**: Checkout en 2 columnes

---

## 🎯 Checklist Completa

### Funcionalitats
- [ ] Llistat de productes
- [ ] Afegir al carretó (1-5 unitats)
- [ ] Actualitzar quantitat
- [ ] Eliminar del carretó
- [ ] Buidar carretó
- [ ] Càlcul de totals
- [ ] Formulari checkout
- [ ] Registre d'usuari
- [ ] Login d'usuari
- [ ] Creació de comanda
- [ ] Actualització d'inventari
- [ ] Confirmació de comanda

### Validacions Frontend
- [ ] HTML5 required
- [ ] HTML5 minlength/maxlength
- [ ] HTML5 pattern (username)
- [ ] HTML5 type="email"
- [ ] HTML5 min/max (quantitat)
- [ ] JavaScript custom validation

### Validacions Backend
- [ ] Quantitat 1-5
- [ ] Stock disponible
- [ ] Username format
- [ ] Email format
- [ ] Password mínim
- [ ] Unicitat username/email

### Seguretat
- [ ] Password hasheado (bcrypt)
- [ ] Consultes parametritzades
- [ ] Sessions segures
- [ ] Errors genèrics (no exposen info)

### UI/UX
- [ ] Disseny modern
- [ ] Responsiu (mòbil, tablet, desktop)
- [ ] Feedback visual (notificacions)
- [ ] Navegació intuïtiva
- [ ] Missatges d'error clars

### Arquitectura
- [ ] Separació Models-Vista-Controlador
- [ ] Tres capes (Presentació-Negoci-Dades)
- [ ] Repositoris per accés a BD
- [ ] Serveis per lògica de negoci
- [ ] Cap SQL en templates
- [ ] Cap HTML en serveis

---

## 🐛 Errors Comuns i Solucions

### Error: "No module named 'flask'"
**Solució**: `pip install -r requirements.txt`

### Error: "Database is locked"
**Solució**: Tanca altres connexions a la BD

### Error: Port 5000 ja en ús
**Solució**: 
```bash
# Canvia el port a app.py
app.run(debug=True, port=5001)
```

### La BD no es crea
**Solució**: 
```bash
python init_db.py --reset
```

---

## 📊 Resultats Esperats

Després de completar totes les proves:

✅ **Funcional**: Totes les funcionalitats operen correctament  
✅ **Validació**: Doble validació funciona (client + servidor)  
✅ **Seguretat**: No hi ha vulnerabilitats evidents  
✅ **UI/UX**: Interfície moderna i usable  
✅ **Arquitectura**: Separació clara de responsabilitats  

---

## 📝 Notes per l'Avaluador

- **Base de dades**: `techshop.db` (SQLite, es crea automàticament)
- **Dades de prova**: 15 productes amb stock variable
- **Sessions**: Gestionades per Flask (cookies encriptades)
- **Logs**: A la consola on s'executa `python app.py`

**Temps estimat de proves**: 20-30 minuts

---

**Última actualització**: Octubre 2025 
**Contacte**: Teo Aranda Paez

