import psycopg2
from config import config

class CARModels_Connect(object):

    """docstring for Postgres"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            params = config()
            # normally the db_credenials would be fetched from a config file or the enviroment
            # meaning shouldn't be hardcoded as follow

            try:
                print('connecting to PostgreSQL database...')
                connection = CARModels_Connect._instance.connection = psycopg2.connect(**params)
                cursor = CARModels_Connect._instance.cursor = connection.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()

            except Exception as error:
                print('Error: connection not established {}'.format(error))
                CARModels_Connect._instance = None

            else:
                print('connection established\n{}'.format(db_version[0]))

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def select_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result=self.cursor.fetchall()
            #print(type(result))
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    def __del__(self):
        self.connection.close()
        self.cursor.close()


if __name__ == '__main__':
    carConnector=CARModels_Connect()

    results=carConnector.select_query("SELECT id, model_name, developer, binary_model, labels, sensor_system, sensor_list, algorithm, hyperparameters,"
                  " frequency, window_type, window_size, window_stride, features, train_dataset, validation_method, "
                  "train_valid_accuracy, test_accuracy, test_dataset, model_repository, model_size_in_bytes, created_time "
                  "FROM public.trained_models limit 100;")
    for r in results:
        print(r)

