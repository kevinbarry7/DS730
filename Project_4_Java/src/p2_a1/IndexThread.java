import java.util.*;
import java.io.*;
public class IndexThread extends Thread {
	// declare private variables
	private File inputFile;
	private String outputFolder;
	private Integer num_chars;
	private Scanner input;
	private TreeMap<String, TreeSet<Integer>> word_indices;
	private int totalCharCount;
	private int index;
	private String filename;
	private String suffix;
	private File dir;
	private File file_path;
	private PrintWriter output;

	public IndexThread(File inputFile, String outputFolder, Integer num_chars) throws Exception {
		this.num_chars = num_chars;
		this.inputFile = inputFile;
		this.outputFolder = outputFolder;
	}

	public void run() {
		try {
			// Create Scanner object using FileReader
			Scanner input = new Scanner(new FileReader(inputFile));
		} catch (Exception e) {
			System.out.println("Exception occurred");
		}
		
		// Create treemap to keep word + index pairs
		TreeMap<String, TreeSet<Integer>> word_indices = new TreeMap<>();

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
			PrintWriter output = new PrintWriter(new FileWriter(file_path));
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

				// Logic for comma delimited output
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
}