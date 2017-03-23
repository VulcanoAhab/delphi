from django.conf.urls import url, include
from rest_framework import routers
from workers import views as workers_views
from grabbers import views as grabbers_views
from drivers import views as drivers_views



router = routers.DefaultRouter()

router.register(r'jobs',
                workers_views.JobsViewSet)

router.register(r'tasks_configs',
                workers_views.TaskConfigsViewSet,
                'task_config')


router.register(r'sequences',
                grabbers_views.SequenceViewSet,
                'sequence')

router.register(r'mappers',
                 grabbers_views.MapperViewSet,
                 'mapper')

router.register(r'drivers',
                drivers_views.DriverViewSet,
                'driver')

#urlpatterns = router.urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
