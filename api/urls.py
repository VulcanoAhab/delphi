from django.conf.urls import url, include
from rest_framework import routers
from workers import views as workers_views

router = routers.DefaultRouter()

router.register(r'jobs',
                workers_views.JobsViewSet)

router.register(r'sequences',
                workers_views.SequenceViewSet,
                'sequence')

router.register(r'tasks_configs',
                workers_views.TaskConfigsViewSet,
                'task_config')

router.register(r'drivers',
                workers_views.DriverViewSet,
                'driver')

#urlpatterns = router.urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
