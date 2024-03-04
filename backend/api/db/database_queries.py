
import logging
from flask_restful import abort


class DbQueries:
    def __init__(self, session):
        self.session = session

    def get_instance(self, model, **kwargs):
        try:
            instance = self.session.query(model).filter_by(**kwargs).one_or_none()
        except Exception as e:
            logging.log(logging.ERROR, e)
            abort(500, message='DB', status=500)
        finally:
            self.session.close()

        return instance

    def create_instance(self, model, **kwargs):
        instance = model(**kwargs)

        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
            return None
        finally:
            self.session.close()

        return instance

    def update_instance(self, instance, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)

            self.session.flush()
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
            return None
        finally:
            self.session.close()

        return instance

    def update_instance_by_dn(self, model, dn, data: dict):
        try:
            self.session.query(model). \
                filter(model.dn == dn). \
                update(data)
            self.session.commit()
            return 'OK'
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
            return None
        finally:
            self.session.close()

    def delete_instance(self, instance):
        try:
            self.session.delete(instance)
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
        finally:
            self.session.close()

    def delete_instance_by_params(self, model, **kwargs):
        try:
            self.session.query(model).filter_by(**kwargs).delete()
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
        finally:
            self.session.close()

    def bulk_delete(self, model, filter_del):
        try:
            self.session.query(model).filter(filter_del).delete(synchronize_session=False)
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, str(e))
            self.session.rollback()
        finally:
            self.session.close()
