# Renato Piermarini Autos · Setup Técnico para Heroku

Este repo replica la arquitectura del documento **“Renato Piermarini Autos — Setup Técnico”** y la adapta para despliegue en **Heroku**, manteniendo la misma idea funcional:

- `POST /message` con `phone`, `message`, `execution_id`
- respuesta inmediata `200 OK`
- procesamiento en background con `ThreadPoolExecutor`
- clasificación por pattern matching, sin LLM
- crews especializados por dominio
- `resume_execution(execution_id, respuesta)` hacia Kapso
- historial conversacional en `storage/conversations.json`
- follow-up automático de checklist en `storage/checklists.json`

## Qué quedó replicado

### Arquitectura del mensaje
- WhatsApp inbound → Kapso flow → `POST /message`
- FastAPI responde enseguida
- el thread pool corre `run_agencia()` en background
- `AgenciaFlow` clasifica el mensaje por keywords
- enruta al crew correspondiente
- el resultado vuelve por `resume_execution`

### Router de mensajes
Se respetó el router por pattern matching con estas rutas:

- `transferencia`
- `bienvenida`
- `tareas`
- `stock`
- `research`
- `email`
- `documentos`
- `finanzas`
- `completa` como fallback a stock

### Crews incluidos
Se dejaron runners separados para:
- `StockCrew`
- `TransferenciaCrew`
- `TareasCrew`
- `EmailCrew`
- `DocumentosCrew`
- `FinanzasCrew`
- `ResearchCrew`

Sus metas y restricciones siguen el documento original, aunque varias tools quedaron como **stubs conectables** para que las adaptes a la forma exacta de tu Kapso DB API.

### Variables de entorno
Se incluyeron las variables equivalentes del documento:
- `ANTHROPIC_API_KEY`
- `KAPSO_API_KEY`
- `KAPSO_DB_URL`
- `WEBHOOK_SECRET`
- `KAPSO_PHONE_NUMBER_ID`
- `PHONE_RENA`
- `PHONE_FRAN`
- `PHONE_NEGOCIO`
- `TEAM_EMAIL_RENA`
- `TEAM_EMAIL_FRAN`
- `SERPER_API_KEY`
- `GMAIL_TOKEN_PATH`

### Historial conversacional
Se implementó:
- ventana de 20 mensajes
- reset por 30 minutos de inactividad
- storage en `storage/conversations.json`
- últimos 4 mensajes, comprimidos a 600 chars

## Qué está adaptado para Heroku

El documento original menciona Railway y 4 threads. Acá se mantiene la misma idea de threads, pero el despliegue está preparado para Heroku con:
- `Procfile`
- `runtime.txt`
- `app.json`
- `requirements.txt`

## Qué NO quedó “exactamente igual”

Hay 3 puntos donde tuve que dejar una base conectable, no una implementación cerrada:

1. **Kapso DB API real**  
   El PDF describe tools y endpoints lógicos, pero no trae el contrato REST exacto ni payloads de Kapso DB. Por eso `app/integrations/kapso_client.py` viene con rutas razonables y stubs que vas a tener que ajustar.

2. **CrewAI con tools reales**  
   Dejé los runners y el wiring listos. Cuando haya `ANTHROPIC_API_KEY`, pueden usar CrewAI; si no, caen en fallback determinístico. No conecté tools reales de CrewAI porque el documento no trae el código fuente de las tools.

3. **Gmail / Serper / cron jobs**  
   Están preparados como placeholders, no como integración completa.

## Deploy local

### 1. Crear entorno
```bash
python -m venv .venv
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Completar variables
Como mínimo:
```env
WEBHOOK_SECRET=...
KAPSO_API_KEY=...
KAPSO_DB_URL=https://tu-api-kapso.com
KAPSO_PHONE_NUMBER_ID=...
PHONE_RENA=5492216699450
```

### 3. Ejecutar
```bash
uvicorn app.main:app --reload
```

### 4. Probar
```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{
    "phone":"5492216699450",
    "message":"hola",
    "execution_id":"exec_123"
  }'
```

## Deploy en Heroku

### 1. Crear app
```bash
heroku create renato-autos-whatsapp
```

### 2. Config vars
```bash
heroku config:set WEBHOOK_SECRET=tu_secret
heroku config:set KAPSO_API_KEY=tu_kapso_api_key
heroku config:set KAPSO_DB_URL=https://tu-api-kapso.com
heroku config:set KAPSO_PHONE_NUMBER_ID=tu_phone_number_id
heroku config:set PHONE_RENA=5492216699450
heroku config:set PHONE_FRAN=5492213589822
heroku config:set PHONE_NEGOCIO=5491161590852
heroku config:set TEAM_EMAIL_RENA=renatopiermarinih@gmail.com
heroku config:set APP_ENV=production
heroku config:set APP_DEBUG=false
```

Opcionales:
```bash
heroku config:set ANTHROPIC_API_KEY=tu_anthropic_key
heroku config:set SERPER_API_KEY=tu_serper_key
heroku config:set GMAIL_TOKEN_PATH=/app/secrets/gmail-token.json
```

### 3. Deploy
```bash
git init
git add .
git commit -m "Initial Heroku deploy"
heroku git:remote -a renato-autos-whatsapp
git push heroku main
```

### 4. Escalar dyno
```bash
heroku ps:scale web=1
```

### 5. Logs
```bash
heroku logs --tail
```

## Cómo conectar Kapso de verdad

Ajustá `app/integrations/kapso_client.py` a tu API real.

Métodos a revisar:
- `get_vehiculos_en_stock`
- `get_vehiculos_by_estado`
- `create_tarea`
- `create_checklist`
- `create_transferencia`
- `get_clientes`
- `send_resume_execution`

## Nota importante

El documento original habla de modelos `Claude Opus 4.7`, `Claude Sonnet 4.6` y `Claude Haiku 4.5`. En el ecosistema público actual de Anthropic/CrewAI, esos nombres exactos pueden no coincidir 1:1 con los IDs expuestos por SDK. Por eso dejé nombres compatibles y una capa fácil de ajustar. La arquitectura y roles sí siguen el documento técnico.
