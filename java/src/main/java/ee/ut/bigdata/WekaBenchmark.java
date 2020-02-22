package ee.ut.bigdata;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import weka.classifiers.Classifier;
import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.misc.InputMappedClassifier;
import weka.core.Instances;
import weka.core.converters.ConverterUtils;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.NumericToNominal;

import java.io.*;
import java.util.Random;

public abstract class WekaBenchmark<C extends Classifier> implements Benchmark {

	@Override
	public void benchmark(String dataset, String output, int timeLimit, float split) {
		Instances data = loadInstances(dataset);
		data = preprocess(data);
		data.randomize(new Random());
		int trainSize = Math.round(data.numInstances() * split);
		int testSize = data.numInstances() - trainSize;
		Instances train = new Instances(data, 0, trainSize);
		Instances test = new Instances(data, trainSize, testSize);

		benchmark(train, test, output, timeLimit);
	}

	@Override
	public void benchmark(String train, String test, String output, int timeLimit) {
		Instances trainData = preprocess(loadInstances(train));
		Instances testData = preprocess(loadInstances(test));

		benchmark(trainData, testData, output, timeLimit);
	}

	protected void benchmark(Instances train, Instances test, String output, int timeLimit) {
		C classifier = initClassifier(timeLimit);
		BenchmarkResult result = doBenchmark(classifier, train, test, timeLimit);
		output(result, output);
	}

	protected abstract C initClassifier(int timeLimit);

	protected Instances loadInstances(String location) {
		try {
			ConverterUtils.DataSource source = new ConverterUtils.DataSource(location);
			Instances data = source.getDataSet();
			if (data.classIndex() == -1)
				data.setClassIndex(data.numAttributes() - 1);
			return data;
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}

	protected Instances preprocess(Instances data) {
		try {
			NumericToNominal convert = new NumericToNominal();
			convert.setAttributeIndicesArray(new int[]{ data.classIndex() });
			convert.setInputFormat(data);
			data = Filter.useFilter(data, convert);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return data;
	}

	protected BenchmarkResult doBenchmark(C classifier, Instances train, Instances test, int timeLimit) {
		BenchmarkResult result = new BenchmarkResult();
		Thread trainingThread = trainingThread(classifier, train, result);
		runWithTimeout(trainingThread, timeLimit, result);

		if (result.getError() == null) {
			try {
				evaluate(classifier, train, test, result);
			} catch (Exception e) {
				result.setError(e.getMessage());
			}
		}
		return result;
	}

	protected void evaluate(C classifier, Instances train, Instances test, BenchmarkResult result) {
		try {
			InputMappedClassifier mappedClassifier = new InputMappedClassifier();
			mappedClassifier.setClassifier(classifier);
			mappedClassifier.setModelHeader(new Instances(train, 0));
			mappedClassifier.setSuppressMappingReport(true);

			Evaluation eval = new Evaluation(train);
			eval.evaluateModel(mappedClassifier, test);
			result.setAccuracy(eval.pctCorrect() / 100.0);
			result.setPrecision(eval.weightedPrecision());
			result.setRecall(eval.weightedRecall());
			result.setF1score(eval.weightedFMeasure());
			result.setModel(getBestModel(classifier));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	protected void output(BenchmarkResult result, String output) {
		Gson gson = new GsonBuilder()
				.serializeSpecialFloatingPointValues()
				.create();
		String json = gson.toJson(result);
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(new File(output)))) {
			writer.write(json);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected Thread trainingThread(C classifier, Instances train, BenchmarkResult result) {
		return new Thread(() -> {
			try {
				classifier.buildClassifier(train);
			} catch (InterruptedException e) {
				// Ignore
			} catch (Exception e) {
				result.setError(e.getMessage());
				e.printStackTrace();
			}
		});
	}

	protected void runWithTimeout(Thread thread, int timeLimit, BenchmarkResult result) {
		long timeStart = System.currentTimeMillis();
		long timeEnd = 0;
		try {
			thread.start();
			thread.join((long) (timeLimit * 60000 * 1.1));
			timeEnd = System.currentTimeMillis();
			if (thread.isAlive()) {
				thread.interrupt();
				result.setError("Timeout");
			}
		} catch (Exception e) {
			result.setError(e.toString());
			e.printStackTrace();
		} finally {
			if (timeEnd == 0) {
				timeEnd = System.currentTimeMillis();
			}
			result.setTime(Math.round((timeEnd - timeStart) / 1000.0));
		}
	}


	protected String getBestModel(C classifier) {
		return classifier.toString();
	}
}
