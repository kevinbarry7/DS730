import java.util.*;
import java.io.*;
public class Index{
	public static void wordIndex(File inputFile, String outputFolder, Integer num_chars) throws Exception {
		// File file = new File("/Users/ebolotin/Dropbox/TechDev/UWL/730/Project_4/moby.txt");
		// File file = new File(filename);
		Scanner input = new Scanner(new FileReader(inputFile));
		TreeMap<String, TreeSet<Integer>> word_indices = new TreeMap<>();

		int sum_length = 0;
		int index = 1;
		while(input.hasNext() == true) {
			String word = input.next();
			int length = word.length();
			sum_length = sum_length + length;

			if(sum_length >= num_chars) {
				index = index + 1;
				sum_length = 0;
			}

			if(word_indices.containsKey(word) == true) {
				TreeSet<Integer> existing_val = word_indices.get(word);
				existing_val.add(index);
				word_indices.replace(word, existing_val);
			} else {
				TreeSet<Integer> current_word_indices = new TreeSet<>();
				current_word_indices.add(index);
				word_indices.put(word, current_word_indices);
			}
		}

		// for(Map.Entry<String, TreeSet<Integer>> word : word_indices.entrySet()) {
		// 	System.out.println(word);
		// }

		String filename = inputFile.getName().toString().replaceFirst("[.][^.]+$", "");
		String suffix = "_output.txt";
		File dir = new File(outputFolder);
		File file_path = new File(dir, filename + suffix);
		PrintWriter output = new PrintWriter(new FileWriter(file_path));
		for(Map.Entry<String, TreeSet<Integer>> word : word_indices.entrySet()) {
			output.println(word);
		}

		output.close();
	}

	public static void main(String[] args) throws Exception {
		long startTime = System.currentTimeMillis();
		String inputFolder = args[0];
		String outputFolder = args[1];
		int num_chars = Integer.parseInt(args[2]);
		File[] inputFiles = new File(inputFolder).listFiles();
		for(File file : inputFiles) {
			if (file.isFile() && file.getName().endsWith(".txt")) {;
				wordIndex(file, outputFolder, num_chars);
			}
		}
		long endTime = System.currentTimeMillis();
		long elapsedTime = endTime - startTime;
		System.out.println(elapsedTime);
	}
}