import argparse
import datetime
import json
import memory_profiler
import os
import shutil
import subprocess
import threading
import psutil
import time as t

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

models = ['tpot']
time = 30 # in minutes
n_runs = 3
split_seed = 1

python_bin = '/home/Eldeeb/anaconda3/bin/python3.7'
java_bin = 'java'

resource_log_dir = '/home/Eldeeb/logs'

java_benchmark_jar = 'java/automl-benchmarking-0.0.1-SNAPSHOT-jar-with-dependencies.jar'
autoweka_jar = '/home/Eldeeb/autoweka-2.6/autoweka.jar'
ml_plan_dir = '/home/Eldeeb/ailibs-0.9.0'
mlplan_jar = f'{ml_plan_dir}/AILibs-0.0.1-SNAPSHOT-all.jar'
jars = '"' + ':'.join([os.path.abspath(java_benchmark_jar), autoweka_jar, mlplan_jar]) + '"'

python2_bin = '/home/Eldeeb/anaconda3/envs/py27/bin/python'
recipe_dir = '/home/Eldeeb/Recipe'


def split(dataset_file: str, output_dir: str, p: float = 0.75):
    name = os.path.splitext(os.path.basename(dataset_file))[0]
    df = pd.read_csv(dataset_file)
    train, test = train_test_split(df, train_size=p, random_state=split_seed)
    train.to_csv(os.path.join(output_dir, f'{name}_train.csv'), index=False)
    test.to_csv(os.path.join(output_dir, f'{name}_test.csv'), index=False)



def benchmark(model: str, train_file: str, test_file: str, output_file: str):
    cmd = None
    if model in ['autosklearn', 'autosklearn-v', 'autosklearn-m', 'autosklearn-e', 'tpot']:
        cmd = ' '.join([python_bin, '-u', 'python/main.py', train_file, output_file,
                        '-t', str(time), '-m', model, '-te', test_file])
    elif model == 'recipe':
        cmd = ' '.join([python_bin, '-u', 'python/main.py', train_file, output_file,
                        '-t', str(time), '-m', model, '-te', test_file,
                        '-c', python2_bin, recipe_dir])
    elif model == 'autoweka':
        cmd = ' '.join(['java', '-Xmx6g', '-cp', jars, 'ee.ut.bigdata.Main',
                        model, train_file, test_file, output_file, str(time)])
    elif model == 'mlplan':
        cmd = ' '.join(['cd', ml_plan_dir, '&&', 'java', '-Xmx6g', '-cp', jars, 'ee.ut.bigdata.Main',
                        model, os.path.abspath(train_file), os.path.abspath(test_file),
                        os.path.abspath(output_file), str(time)])
    if cmd:
        try:
            proc = subprocess.Popen("exec " + cmd, shell=True, stderr=subprocess.STDOUT)
            logger(proc.pid)
            proc.wait(timeout=time*60*1.5)
        except TimeoutExpired:
            print("Timeout Expired")
            #exit()
        finally:
            proc.terminate()


def collect(output_dir: str, collect_dir: str):
    data = {}
    for benchmark in os.listdir(output_dir):
        benchmark_dir = os.path.join(output_dir, benchmark)
        if os.path.isdir(benchmark_dir):
            for dataset in os.listdir(benchmark_dir):
                dataset_dir = os.path.join(benchmark_dir, dataset)
                if os.path.isdir(dataset_dir):
                    dataset_name = os.path.splitext(dataset)[0]
                    for run in os.listdir(dataset_dir):
                        run_file = os.path.join(dataset_dir, run)
                        if os.path.getsize(run_file) > 0:
                            with open(run_file) as f:
                                run_result = json.load(f)
                                data.setdefault(benchmark, {}).setdefault(dataset_name, []).append(run_result)

    if not os.path.isdir(collect_dir):
        os.makedirs(collect_dir)

    for benchmark, datasets in data.items():
        benchmark_data = {}
        for dataset, runs in datasets.items():
            dataset_data = {}
            run_values = {}
            for i, run in enumerate(runs):
                for k, v in run.items():
                    dataset_data['{}_{}'.format(k, i + 1)] = v

                    if k not in ['time', 'error', 'model']:
                        run_values.setdefault(k, []).append(v)
            for k, vs in run_values.items():
                dataset_data[k + '_mean'] = np.mean(vs)
                dataset_data[k + '_std'] = np.std(vs)
            benchmark_data[dataset] = dataset_data
        df = pd.DataFrame.from_dict(benchmark_data, orient='index')
        df.to_csv(os.path.join(collect_dir, benchmark + '.csv'))


def makedirs(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))


def cpu_logger(pid, filename):
    print("CPU logger start\n")
    makedirs(filename)

    process = psutil.Process(pid)
    with open(filename, "a+") as f:
        f.write(str(datetime.datetime.now()) + '\n')
        for index in range(1, 360000):
            message = f'{index}, memory_percent: {process.memory_percent()}, ' \
                f'cpu_percent: {psutil.cpu_percent(percpu=False)}'
            f.write(message + "\n")
            t.sleep(1)


def mem_logger(pid, filename):
    print("Memory logger start\n")
    makedirs(filename)

    with open(filename, "a") as f:
        f.write(str(datetime.datetime.now()) + '\n')
        memory_profiler.memory_usage(pid, interval=1, timeout=360000, retval=False, stream=f)


def logger(pid):
    try:
        threading.Thread(target=cpu_logger, args=(pid, os.path.join(resource_log_dir, 'cpu.log')), daemon=True).start()
        threading.Thread(target=mem_logger, args=(pid, os.path.join(resource_log_dir, 'mem.log')), daemon=True).start()
    except:
        print("Error while running the logger service")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Datasets directory')
    parser.add_argument('output_dir', help='Benchmark results directory')
    args = parser.parse_args()
    input_dir, output_dir = args.input_dir, args.output_dir

    tmp_splits = '/home/Eldeeb/AutoMLBenchmarking/splits'
    tmp_output = '/home/Eldeeb/AutoMLBenchmarking/output'

    datasets = [file for file in os.listdir(input_dir) if file.endswith('.csv')]
    runs = list(range(1, n_runs + 1))

    if not datasets:
        print('No datasets supplied')
    else:
        if not os.path.isdir(tmp_splits):
            os.makedirs(tmp_splits)
            for dataset in datasets:
                split(os.path.join(input_dir, dataset), tmp_splits, 0.75)

        params = [(model, dataset, run) for model in models for dataset in datasets for run in runs]
        completed = True
        for model, dataset, run in params:
            dataset_name = os.path.splitext(dataset)[0]
            full_output_dir = os.path.join(tmp_output, model, dataset_name)
            output_file = os.path.join(full_output_dir, '{}.json'.format(run))
            if not os.path.isfile(output_file):
                train_file = os.path.join(tmp_splits, f'{dataset_name}_train.csv')
                test_file = os.path.join(tmp_splits, f'{dataset_name}_test.csv')

                if not os.path.isdir(full_output_dir):
                    os.makedirs(full_output_dir)
                open(output_file, 'w').close()

                print('{} <{}> <{}> run {} start'.format(datetime.datetime.now(), model, dataset, run))
                benchmark(model, train_file, test_file, output_file)
                print('{} <{}> <{}> run {} end'.format(datetime.datetime.now(), model, dataset, run))

                completed = False
                break

        if completed:
            collect(tmp_output, output_dir)
            print('{} completed!'.format(datetime.datetime.now()))
            shutil.rmtree(tmp_splits)
            shutil.rmtree(tmp_output)

        else:
            print('{} rebooting...'.format(datetime.datetime.now()))
            os.system('reboot')
