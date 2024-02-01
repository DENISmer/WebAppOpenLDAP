import logging


class DbQueries:
    def __init__(self, session):
        self.session = session

    def get_instance(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).one_or_none()
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

        return instance

    def delete_instance(self, instance):
        self.session.delete(instance)
