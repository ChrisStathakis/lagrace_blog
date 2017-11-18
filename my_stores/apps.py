from django.apps import AppConfig


class MyStoresConfig(AppConfig):
    name = 'my_stores'
    def ready(self):
        import my_stores.signals
        import blog.signals
