import logging

logger = logging.getLogger(__name__)

def isHome(x):
    if x == 'Home' or x == 'sessions' or x == 'auth' or x == 'admin':
        return True
    else:
        return False
    
class AppRouter:
    def db_for_read(self, model, **hints):
        if isHome(model._meta.app_label):
            return 'default'
        else:
            return model._meta.app_label

    def db_for_write(self, model, **hints):
        if isHome(model._meta.app_label):
            return 'default'
        return model._meta.app_label

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default', 'Lancamento_obra', 'TI', 'Reservas', 'sessions', 'auth')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            logger.debug(f'Allowing relation between {obj1._state.db} and {obj2._state.db}')
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if isHome(app_label):
            return db == 'default'
        return db == app_label
