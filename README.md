# Dealer Agents MVP

MVP multi-tenant para concesionarias, pensado para deploy rápido en Heroku.

Incluye:
- FastAPI
- PostgreSQL
- Redis
- Celery worker
- webhook de WhatsApp
- Vendedor AI
- Secretaria AI
- organizaciones
- vehículos
- leads
- conversaciones
- handoff a humano

## 1. Requisitos

- Python 3.11
- PostgreSQL
- Redis
- cuenta de Heroku
- WhatsApp Cloud API de Meta

## 2. Estructura principal

- `app/main.py`: API principal
- `app/worker.py`: worker Celery
- `app/api/routes/*`: endpoints
- `app/services/*`: lógica de negocio
- `app/models/*`: modelos SQLAlchemy
- `alembic/*`: migraciones
- `scripts_seed.py`: seed inicial opcional

## 3. Instalación local

### Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Variables de entorno

Copiá `.env.example` a `.env`:

```bash
cp .env.example .env
```

### Crear base local

Asegurate de tener PostgreSQL corriendo y crear una base llamada `dealer_agents`.

### Ejecutar migraciones

```bash
alembic upgrade head
```

### Seed opcional

```bash
python scripts_seed.py
```

### Levantar API

```bash
uvicorn app.main:app --reload
```

### Levantar worker

En otra terminal:

```bash
celery -A app.worker.celery_app worker --loglevel=info
```

## 4. Endpoints principales

### Health
- `GET /health`

### Organizaciones
- `POST /api/v1/organizations`
- `GET /api/v1/organizations`

### Vehículos
- `POST /api/v1/vehicles`
- `GET /api/v1/vehicles?organization_id=1`

### Leads
- `POST /api/v1/leads`
- `GET /api/v1/leads?organization_id=1`

### Conversaciones
- `GET /api/v1/conversations?organization_id=1`
- `GET /api/v1/conversations/{conversation_id}/messages`
- `POST /api/v1/conversations/{conversation_id}/handoff`

### WhatsApp
- `GET /api/v1/webhooks/whatsapp`
- `POST /api/v1/webhooks/whatsapp`

## 5. Ejemplos de requests

### Crear organización

```bash
curl -X POST http://127.0.0.1:8000/api/v1/organizations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Atlántico Automotores",
    "slug": "atlantico-automotores",
    "whatsapp_phone_number": "1234567890",
    "active": true
  }'
```

### Crear vehículo

```bash
curl -X POST http://127.0.0.1:8000/api/v1/vehicles \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": 1,
    "brand": "Toyota",
    "model": "Hilux",
    "version": "SRV 4x4 AT",
    "year": 2021,
    "mileage": 45000,
    "price": 39500000,
    "currency": "ARS",
    "status": "available"
  }'
```

### Ver vehículos

```bash
curl "http://127.0.0.1:8000/api/v1/vehicles?organization_id=1"
```

### Handoff a humano

```bash
curl -X POST http://127.0.0.1:8000/api/v1/conversations/1/handoff
```

## 6. Configuración de WhatsApp Cloud API

### Webhook verify URL
Usá:

```txt
https://TU-APP.herokuapp.com/api/v1/webhooks/whatsapp
```

### Verify token
Debe coincidir con:

```txt
WHATSAPP_VERIFY_TOKEN
```

### Phone Number ID
Meta te lo da en la configuración de WhatsApp Cloud API. Ese valor debe coincidir con:

```txt
WHATSAPP_PHONE_NUMBER_ID
```

### Access token
Se guarda en:

```txt
WHATSAPP_ACCESS_TOKEN
```

## 7. Deploy en Heroku

### Login

```bash
heroku login
```

### Crear app

```bash
heroku create dealer-agents-mvp
```

### Crear addons

```bash
heroku addons:create heroku-postgresql:essential-0
heroku addons:create heroku-redis:mini
```

### Config vars mínimas

```bash
heroku config:set APP_ENV=production
heroku config:set APP_DEBUG=false
heroku config:set SECRET_KEY=supersecret
heroku config:set WHATSAPP_VERIFY_TOKEN=your_verify_token
heroku config:set WHATSAPP_ACCESS_TOKEN=your_meta_access_token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
heroku config:set OPENAI_API_KEY=your_openai_key
heroku config:set DEFAULT_LLM_MODEL=gpt-4.1-mini
```

### Importante sobre DATABASE_URL
Heroku crea `DATABASE_URL` automáticamente.

Este proyecto usa SQLAlchemy con `psycopg`, y normalmente Heroku entrega un `DATABASE_URL` compatible con `postgres://` o `postgresql://`.
Si notás problemas de driver, podés normalizarlo agregando una pequeña función de adaptación luego, pero en muchos casos actuales funciona sin tocar nada.

### Deploy con Git

```bash
git init
git add .
git commit -m "Initial dealer agents MVP"
heroku git:remote -a dealer-agents-mvp
git push heroku main
```

Si tu rama principal es `master`:

```bash
git push heroku master
```

### Escalar procesos

```bash
heroku ps:scale web=1 worker=1
```

### Ver logs

```bash
heroku logs --tail
```

### Ejecutar seed en Heroku

```bash
heroku run python scripts_seed.py
```

## 8. Verificaciones post deploy

### Health check

```bash
curl https://TU-APP.herokuapp.com/health
```

Debe devolver:

```json
{"status":"ok"}
```

### Organizaciones

```bash
curl https://TU-APP.herokuapp.com/api/v1/organizations
```

## 9. Flujo del webhook

Cuando entra un mensaje de WhatsApp:

1. entra al webhook
2. detecta la organización por `phone_number_id`
3. busca o crea lead
4. busca o crea conversación
5. guarda mensaje
6. detecta agente (`seller` o `secretary`)
7. genera respuesta
8. envía respuesta por WhatsApp
9. guarda respuesta

## 10. Cómo probar sin WhatsApp real

Podés probar primero:
- creando organizaciones
- cargando vehículos
- consultando endpoints
- ejecutando el seed

Para probar el webhook de verdad necesitás que Meta apunte al endpoint público de Heroku.

## 11. Limitaciones actuales del MVP

- no hay autenticación JWT todavía
- no hay panel frontend
- no hay integración CRM externa
- el vendedor usa reglas simples y búsqueda directa en DB
- el worker está preparado pero no tiene follow-ups reales todavía
- el LLM está reservado para una siguiente iteración

## 12. Próximos pasos recomendados

1. Agregar auth admin por organización
2. Agregar prompts configurables por concesionaria
3. Agregar asignación de leads a vendedores humanos
4. Agregar agenda/test drive
5. Agregar follow-ups automáticos con Celery
6. Agregar wrapper LLM real
7. Agregar import masivo de stock por CSV

## 13. Sugerencia operativa

Para un primer piloto comercial:
- una sola concesionaria
- un solo número de WhatsApp
- 20 a 200 vehículos
- vendedor AI + secretaria AI
- un operador humano que reciba handoffs

Eso ya te permite validar el producto sin meter complejidad enterprise demasiado pronto.
