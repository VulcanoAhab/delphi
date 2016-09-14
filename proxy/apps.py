from django.apps import AppConfig


class ProxyConfig(AppConfig):
    name = 'proxy'
    verbose_name='proxy'

    def ready(self):
        '''
        '''
        import proxy.signals


