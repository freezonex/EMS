from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkshopViewSet, EquipmentViewSet,EnergyConsumptionViewSet,EnergySourceViewSet,MaintenanceRecordViewSet,AlarmRecordViewSet,EnergyPlanViewSet

router = DefaultRouter()
router.register(r'workshops', WorkshopViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'energyconsumption', EnergyConsumptionViewSet)
router.register(r'energysource', EnergySourceViewSet)
router.register(r'maintenancerecord', MaintenanceRecordViewSet)
router.register(r'alarmrecord', AlarmRecordViewSet)
router.register(r'energyplan', EnergyPlanViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
