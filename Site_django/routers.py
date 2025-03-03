import logging

logger = logging.getLogger(__name__)

def isHome(x):
    if x in ('Home', 'sessions', 'auth', 'admin', 'contenttypes'):
        return True
    return False

class AppRouter:
    def db_for_read(self, model, **hints):
        if not hasattr(model, '_meta') or not hasattr(model._meta, 'app_label'):
            return 'default'  # Fallback para o banco de dados padrão
        if isHome(model._meta.app_label):
            return 'default'
        return model._meta.app_label

    def db_for_write(self, model, **hints):
        if not hasattr(model, '_meta') or not hasattr(model._meta, 'app_label'):
            return 'default'  # Fallback para o banco de dados padrão
        if isHome(model._meta.app_label):
            return 'default'
        return model._meta.app_label

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default', 'lancamento_obra', 'ti', 'reservas', 'sessions', 'auth')
        if hasattr(obj1, '_state') and hasattr(obj2, '_state'):
            if obj1._state.db in db_list and obj2._state.db in db_list:
                logger.debug(f'Allowing relation between {obj1._state.db} and {obj2._state.db}')
                return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label is None:
            return False  # Não permite migrações sem app_label
        if isHome(app_label):
            return db == 'default'
        return db == app_label