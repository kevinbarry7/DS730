import java.util.*;
import java.io.*;
public class IndexRunner extends Thread {
	// declare private variables
	private File inputFile;
	private String outputFolder;
	private Integer num_chars;
	private Scanner input;
	private PrintWriter output;
	private TreeMap<String, TreeSet<Integer>> word_indices;

	public IndexRunner(File inputFile, String outputFolder, Integer num_chars) throws Exception {
		this.num_chars = num_chars;
		this.inputFile = inputFile;
		this.outputFolder = outputFolder;
		// Create treemap to keep word + index pairs
		this.word_indices = new TreeMap<>();
	}

	public void run() {
		try {
			// Create Scanner object using FileReader
			input = new Scanner(new FileReader(inputFile));
		} catch (Exception e) {
			System.out.println("Exception occurred");
		}

		// Define variables
		int totalCharCount = 0;
		int index = 1;

		// Loop through text file if scanner has another token
		while(input.hasNext() == true) {
			// Get next word, convert to lower case, and also get length
			String word = input.next().toLowerCase();
			int length = word.length();

			// Increment total character count by word length
			totalCharCount = totalCharCount + length;

			// if total character count is greater than num_chars
			if(totalCharCount > num_chars) {
				// increment index and reset character count to length
				index = index + 1;
				totalCharCount = length;
			}

			// check if word_indices already has word (key)
			if(word_indices.containsKey(word) == true) {
				// if so, then get the key value, add index, and update key
				TreeSet<Integer> existing_val = word_indices.get(word);
				existing_val.add(index);
				word_indices.replace(word, existing_val);
			
			} else {
				// if word (key) is new, create new key with index value
				TreeSet<Integer> current_word_indices = new TreeSet<>();
				current_word_indices.add(index);
				word_indices.put(word, current_word_indices);
			}
		}

		// Create filename string that is stripped of extension
		String filename = inputFile.getName().toString().replaceFirst("[.][^.]+$", "");

		// create suffix, create new file
		String suffix = "_output.txt";
		File dir = new File(outputFolder);
		File file_path = new File(dir, filename + suffix);
		try {
			output = new PrintWriter(new FileWriter(file_path));
		} catch (Exception e) {
			System.out.println("Exception occurred");
		}
		
		// Write word indices to new file
		for(Map.Entry<String, TreeSet<Integer>> word : word_indices.entrySet()) {
			// Write current word
			output.print(word.getKey() + " ");

			// Write indices for word
			for(Iterator<Integer> i = word.getValue().iterator(); i.hasNext();) {
				int word_index = i.next();

				if(i.hasNext() == true) {
					output.print(word_index + ", ");
				} else {
					output.print(word_index);
				}
			}
			// Write newline
			output.println("");
		}

		// Close file writer
		output.close();
	}

	public static void main(String[] args) throws Exception {
		// Start timer
		long startTime = System.currentTimeMillis();
		
		// Get input args
		String inputFolder = args[0];
		String outputFolder = args[1];
		int num_chars = Integer.parseInt(args[2]);
		
		// Get input file list from input folder
		File[] inputFiles = new File(inputFolder).listFiles();

		// count num files
		int numFiles = 0;
		for(File file : inputFiles) {
			if (file.isFile() && file.getName().endsWith(".txt")) {
				numFiles = numFiles + 1;
			}
		}		

		// Create IndexThread
		IndexRunner[] agent = new IndexRunner[numFiles];
		
		// Loop through inputfile list and execute wordIndex method
		int count = 0;
		for(File file : inputFiles) {
			if (file.isFile() && file.getName().endsWith(".txt")) {
				agent[count] = new IndexRunner(file, outputFolder, num_chars);
				agent[count].start();
				count = count + 1;
			}
		}
		// Stop timer, print elapsed time
		long endTime = System.currentTimeMillis();
		long elapsedTime = endTime - startTime;
		System.out.println(elapsedTime);
	}	
}