package ee.ut.bigdata.impl;

import ee.ut.bigdata.WekaBenchmark;
import weka.classifiers.meta.AutoWEKAClassifier;

public class AutoWekaBenchmark extends WekaBenchmark<AutoWEKAClassifier> {

	@Override
	protected AutoWEKAClassifier initClassifier(int timeLimit) {
		AutoWEKAClassifier classifier = new AutoWEKAClassifier();
		classifier.setTimeLimit(timeLimit);
		classifier.setMemLimit(6144);
		return classifier;
	}

	@Override
	protected String getBestModel(AutoWEKAClassifier classifier) {
		String[] modelOutput = classifier.toString().split("\n");
		return modelOutput[0] + "\n" + modelOutput[1];
	}
}
