package ee.ut.bigdata.impl;

import de.upb.crc901.mlplan.core.MLPlan;
import de.upb.crc901.mlplan.core.MLPlanBuilder;
import ee.ut.bigdata.BenchmarkResult;
import ee.ut.bigdata.WekaBenchmark;
import jaicore.basic.TimeOut;
import weka.classifiers.Classifier;
import weka.core.Instances;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class MLPlanBenchmark extends WekaBenchmark<Classifier> {

	@Override
	protected void benchmark(Instances train, Instances test, String output, int timeLimit) {
		try {
			MLPlanBuilder builder = new MLPlanBuilder().withAutoWEKAConfiguration()
					.withRandomCompletionBasedBestFirstSearch();
			TimeOut evalTimeout = new TimeOut(Math.round(timeLimit * 60 * 0.1), TimeUnit.SECONDS);
			builder.withTimeoutForNodeEvaluation(evalTimeout);
			builder.withTimeoutForSingleSolutionEvaluation(evalTimeout);
			MLPlan mlplan = new MLPlan(builder, train);
			mlplan.setPortionOfDataForPhase2(0f);
			mlplan.setTimeout(timeLimit, TimeUnit.MINUTES);
			mlplan.setNumCPUs(2);

			BenchmarkResult result = doBenchmark(mlplan, train, test, timeLimit);
			output(result, output);

			System.exit(0);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected BenchmarkResult doBenchmark(MLPlan mlplan, Instances train, Instances test, int timeLimit) {
		BenchmarkResult result = new BenchmarkResult();
		Thread trainingThread = trainingThread(mlplan, result);
		runWithTimeout(trainingThread, timeLimit, result);

		if (result.getError() == null) {
			try {
				evaluate(mlplan.getSelectedClassifier(), train, test, result);
			} catch (Exception e) {
				result.setError(e.getMessage());
			}
		}
		return result;
	}

	protected Thread trainingThread(MLPlan mlPlan, BenchmarkResult result) {
		return new Thread(() -> {
			try {
				System.out.println("Training...");
				mlPlan.call();
				System.out.println("Completed");
			} catch (InterruptedException e) {
				System.out.println("Interrupted");
			} catch (Exception e) {
				result.setError(e.getMessage());
				e.printStackTrace();
			}
		});
	}

	@Override
	protected Classifier initClassifier(int timeLimit) {
		return null; // Not used
	}
}
