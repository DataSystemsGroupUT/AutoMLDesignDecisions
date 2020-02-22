package ee.ut.bigdata;

public interface Benchmark {

	/**
	 * Benchmarks the model on train/test datasets and saves results to a file
	 */
	void benchmark(String dataset, String output, int timeLimit, float split);

	void benchmark(String train, String test, String output, int timeLimit);

}
