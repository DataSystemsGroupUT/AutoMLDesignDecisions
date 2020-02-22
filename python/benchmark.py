import json
import time
from abc import ABC, abstractmethod
from typing import Dict, List
import subprocess

import pandas as pd
from autosklearn.classification import AutoSklearnClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tpot import TPOTClassifier

from utils import Thread


class ModelBenchmark(ABC):

    @abstractmethod
    def benchmark(self, dataset_file: str, output_file: str,
                  time_limit: int = None,
                  dataset_test_file: str = None, split: float = 0.75,
                  config: List[str] = None):
        '''
        Benchmarks the model on train/test datasets and saves results to a file
        '''
        pass

    def _timeout(self, func, args, time_limit, result):
        time_start, time_end = time.time(), None
        try:
            train_thread = Thread(target=func, args=args)
            train_thread.start()
            train_thread.join(timeout=time_limit * 60 * 1.1)
            time_end = time.time()

            if train_thread.is_alive():
                train_thread.terminate()
                result['error'] = 'Timeout'
        except Exception as e:
            result['error'] = str(e)
        finally:
            if time_end is None:
                time_end = time.time()
            result['time'] = time_end - time_start

    def _output(self, output_file, result: Dict):
        with open(output_file, 'w') as out:
            out.write(json.dumps(result))


class SklearnBenchmark(ModelBenchmark, ABC):

    def benchmark(self, dataset_file: str, output_file: str,
                  time_limit: int = None,
                  dataset_test_file: str = None, split: float = 0.75,
                  config: List[str] = None):
        X_train, y_train, X_test, y_test = self._load_data(dataset_file, dataset_test_file, split)
        model = self._init_model(time_limit)

        result = {}
        self._timeout(self._fit_model, (model, X_train, y_train), time_limit, result)
        try:
            result.update(self._evaluate(model, X_test, y_test))
            result['model'] = str(self._best_model(model))
        except Exception as e:
            result['error'] = str(e)

        self._output(output_file, result)

    def _fit_model(self, model, X, y):
        model.fit(X, y)

    @abstractmethod
    def _init_model(self, time_limit: int = None):
        pass

    @abstractmethod
    def _best_model(self, model):
        pass

    def _load_data(self, dataset_file, dataset_test_file=None, split=0.75):
        if dataset_test_file is None:
            data = pd.read_csv(dataset_file, na_values='?')
            train, test = train_test_split(data, train_size=split)
        else:
            train, test = [pd.read_csv(file, na_values='?') for file in [dataset_file, dataset_test_file]]
            data = pd.concat([train, test])

        self.categorical_ = data.select_dtypes(['object']).columns
        lab_encs = {col: LabelEncoder().fit(data[col].astype('str')) for col in self.categorical_}

        for col in self.categorical_:
            train[col] = lab_encs[col].transform(train[col].astype('str'))
            test[col] = lab_encs[col].transform(test[col].astype('str'))

        y_col = data.columns[-1]
        return train.drop(y_col, axis=1), train[y_col], test.drop(y_col, axis=1), test[y_col]

    def _evaluate(self, model, X, y):
        predictions = model.predict(X)
        return {
            'accuracy': accuracy_score(y, predictions),
            'precision': precision_score(y, predictions, average='binary'),
            'recall': recall_score(y, predictions, average='binary'),
            'f1score': f1_score(y, predictions, average='binary')
        }


class AutoSklearnBenchmark(SklearnBenchmark):

    def _init_model(self, time_limit: int = None):
        return AutoSklearnClassifier(time_left_for_this_task=(time if time is None else 60 * time_limit),
                                     ml_memory_limit=6144, ensemble_memory_limit=2048)

    def _fit_model(self, model, X, y):
        model.fit(X, y, feat_type=['Categorical' if col in self.categorical_ else 'Numerical' for col in X])

    def _best_model(self, model):
        return model.get_models_with_weights()


class AutoSklearnVanillaBenchmark(AutoSklearnBenchmark):

    def _init_model(self, time_limit: int = None):
        return AutoSklearnClassifier(time_left_for_this_task=(time if time is None else 60 * time_limit),
                                     ml_memory_limit=6144, ensemble_memory_limit=2048,
                                     ensemble_size=1, initial_configurations_via_metalearning=0)


class AutoSklearnMetaBenchmark(AutoSklearnBenchmark):

    def _init_model(self, time_limit: int = None):
        return AutoSklearnClassifier(time_left_for_this_task=(time if time is None else 60 * time_limit),
                                     ml_memory_limit=6144, ensemble_memory_limit=2048,
                                     ensemble_size=1)


class AutoSklearnEnsBenchmark(AutoSklearnBenchmark):

    def _init_model(self, time_limit: int = None):
        return AutoSklearnClassifier(time_left_for_this_task=(time if time is None else 60 * time_limit),
                                     ml_memory_limit=6144, ensemble_memory_limit=2048,
                                     initial_configurations_via_metalearning=0)


class TPOTBenchmark(SklearnBenchmark):
    def _init_model(self, time_limit: int = None):
        return TPOTClassifier(max_time_mins=time_limit, verbosity=3,
                              periodic_checkpoint_folder='tpot_pipelines', scoring='f1',
                              config_dict={'sklearn.svm.SVC': {}})

    def _best_model(self, model):
        return model.fitted_pipeline_


class RecipeBenchmark(ModelBenchmark):

    def benchmark(self, dataset_file: str, output_file: str, time_limit: int = None,
                  dataset_test_file: str = None, split: float = 0.75,
                  config: List[str] = None):
        result = {}

        self._timeout(self._fit_model, (dataset_file, dataset_test_file, time_limit, config), time_limit, result)
        try:
            # result.update
            print('Evaluate here')

        except Exception as e:
            result['error'] = str(e)

        self._output(output_file, result)

    def _fit_model(self, train, test, time_limit, config: List[str]):
        python2_bin, recipe_dir = config
        cmd = ' '.join(['cd', recipe_dir, '&&',
                        python2_bin, '-u', 'exec.py',
                        '-dTr', train, '-dTe', test, '-ft', str(time_limit * 60), '-v', '3'])
        print(cmd)
        subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)

