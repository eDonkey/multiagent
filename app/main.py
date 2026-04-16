from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.organizations import router as organizations_router
from app.api.routes.vehicles import router as vehicles_router
from app.api.routes.leads import router as leads_router
from app.api.routes.conversations import router as conversations_router
from app.api.routes.whatsapp import router as whatsapp_router

app = FastAPI(title='Dealer Agents MVP')

app.include_router(health_router)
app.include_router(organizations_router)
app.include_router(vehicles_router)
app.include_router(leads_router)
app.include_router(conversations_router)
app.include_router(whatsapp_router)
