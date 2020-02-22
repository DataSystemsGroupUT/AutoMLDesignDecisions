package ee.ut.bigdata;

import ee.ut.bigdata.impl.AutoWekaBenchmark;
import ee.ut.bigdata.impl.MLPlanBenchmark;

import java.util.HashMap;
import java.util.Map;

public class Main {

	private static Map<String, Class<? extends Benchmark>> models = new HashMap<>();
	static {
		models.put("autoweka", AutoWekaBenchmark.class);
		models.put("mlplan", MLPlanBenchmark.class);
	}

	public static void main(String[] args) throws Exception {
		if (args.length < 4)
			throw new IllegalArgumentException(
					"Not enough arguments. Usage: <model> <dataset> [<test>] <output> <timeLimit>");
		String model = args[0];
		String dataset = args[1];
		String output = args[args.length - 2];
		int timeLimit = Integer.parseInt(args[args.length - 1]);
		String test = args.length == 5? args[2]: null;

		Benchmark benchmark = models.get(model).newInstance();
		if (test == null)
			benchmark.benchmark(dataset, output, timeLimit, 0.75f);
		else {
			benchmark.benchmark(dataset, test, output, timeLimit);
		}
	}

}
