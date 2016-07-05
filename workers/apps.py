from django.apps import AppConfig

class WorkersConfig(AppConfig):
    '''
    '''
    name='workers'
    verbose_name='Jobs Manager'
    def ready(self):
        '''
        '''
        import workers.signals
