import java.util.*;
import java.io.*;
public class GlobalRunner extends Thread {
	// declare private variables
	private File inputFile;
	private String outputFolder;
	private Integer num_chars;
	private Scanner input;
	private PrintWriter output;
	private TreeMap<String, TreeSet<Integer>> word_indices;
	private String filename;

	public GlobalRunner(File inputFile, String outputFolder, Integer num_chars) throws Exception {
		this.num_chars = num_chars;
		this.inputFile = inputFile;
		this.outputFolder = outputFolder;
		// Create treemap to keep word + index pairs
		this.word_indices = new TreeMap<>();
		// Create filename string that is stripped of extension
		// this.filename = inputFile.getName().toString().replaceFirst("[.][^.]+$", "");
		this.filename = inputFile.getName().toString();	
	}

	public void run() {
		try {
			// Create Scanner object using FileReader
			input = new Scanner(new FileReader(inputFile));
		} catch (Exception e) {
			System.out.println("Exception occurred");
		}

		int totalCharCount = 0;
		int index = 1;

		// Loop through text file if scanner has another token
		while(input.hasNext() == true) {
			// Get next word, convert to lower case, and also get length
			String word = input.next().toLowerCase();
			int length = word.length();

			// Increment total character count by word length
			totalCharCount = totalCharCount + length;

			if(totalCharCount > num_chars) {
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

	}

	// Method to return word_indices for file
	public TreeMap<String, TreeSet<Integer>> getWordIndices() {
		return word_indices;
	}

	// Method to return filename
	public String getFilename() {
		return filename;
	}

	public static void updateGlobalIndex(TreeMap<String, ArrayList<TreeSet>> globalIndices, TreeSet fileWordIndex, String word) throws Exception {
		// If word index for file contains next word
		if(fileWordIndex != null) {
			// Check if the global container (globalindices) for indices has the word
			if(globalIndices.containsKey(word) == true) {
				// Update global index with word
				ArrayList<TreeSet> existing_indices = globalIndices.get(word);
				existing_indices.add(fileWordIndex);
				globalIndices.replace(word, existing_indices);
			// else, add ArrayList with word (TreeSet) to global indices
			} else {
				ArrayList<TreeSet> newIndex = new ArrayList<>();
				newIndex.add(fileWordIndex);				
				globalIndices.put(word, newIndex);
			}

		} else {
			TreeSet space = new TreeSet<>();
			// update existing key in globalword indices with appended Arraylist
			if(globalIndices.containsKey(word) == true) {
				ArrayList<TreeSet> existing_indices = globalIndices.get(word);
				existing_indices.add(space);
				globalIndices.replace(word, existing_indices);
			// create new key in globalword indices with new Arraylist
			} else {				
				ArrayList<TreeSet> newIndex = new ArrayList<>();
				newIndex.add(space);				
				globalIndices.put(word, newIndex);
			}
		}
	}

	// Method to print global word index
	@SuppressWarnings("unchecked")
	public synchronized static void printIndex(String outputFolder, TreeMap indicesByFile) throws Exception {
		// Define output folder
		File dir = new File(outputFolder);
		File file_path = new File(dir, "output.txt");

		PrintWriter output = new PrintWriter(new FileWriter(file_path));

		// Create TreeSet to contain unique, ordered list of words
		TreeMap<String, ArrayList<TreeSet>> globalIndices = new TreeMap<>();
		TreeSet<String> allWords = new TreeSet<>();
		
		output.print("Word, ");

		// Loop through filenames (key) of indicesByFile TreeMap
		for(Iterator<Map.Entry<String, TreeMap<String, TreeSet>>> entry = indicesByFile.entrySet().iterator(); entry.hasNext();) {
			Map.Entry<String, TreeMap<String, TreeSet>> file = entry.next();
			// Logic for comma delimited output
			String filename = file.getKey();
			TreeMap<String, TreeSet> file_indices = file.getValue();
			if(entry.hasNext() == true) {
				output.print(filename + ", ");
			} else {
				output.println(filename);
			}

			// loop through indices
			for(Map.Entry<String, TreeSet> word_index : file_indices.entrySet()) {
				String word = word_index.getKey();
				allWords.add(word);
				
			}
		}

		// Create collection of file indices, which are TreeMaps
		Collection file_values = indicesByFile.values();

		// Loop through TreeSet of words
		for(String word : allWords) {
			// For every word, loop through each File Index (TreeMap - 3 total) without recursing
			for(Iterator<TreeMap<String, TreeSet>> i = file_values.iterator(); i.hasNext();) {
				// Get next TreeMap word index and check if it contains word
				TreeMap<String, TreeSet> file = i.next();
				TreeSet fileWordIndex = file.get(word);

				// Update global word index
				updateGlobalIndex(globalIndices, fileWordIndex, word);

			}
		}

		// Write word indices to new file
		for(Map.Entry<String, ArrayList<TreeSet>> word : globalIndices.entrySet()) {
			// Write current word
			output.print(word.getKey() + ", ");
			ArrayList<TreeSet> all_indices = word.getValue();

			// Loop through ArrayList for each word
			for(Iterator<TreeSet> i = all_indices.iterator(); i.hasNext();) {
				// Get next file index (TreeSet)
				TreeSet file_indices = i.next();
				
				// If file index (TreeSet) is not empty
				if(file_indices.isEmpty() == false) {
					// Loop through integers of file index (TreeSet)
					for(Iterator<Integer> j = file_indices.iterator(); j.hasNext();) {
						Integer index = j.next();
						// Logic for comma delimited output
						if(j.hasNext() == true) {
							output.print(index + ":");
						} else {
							output.print(index);
						}
					}
				// If file index (TreeSet) is empty, print space
				} else {
					output.print("");
				}
				// If ArrayList of TreeSets has another index (TreeSet)
				if(i.hasNext() == true) {
					output.print(", ");
				}
			}
			// Write newline
			output.println("");
		}

	// Close file writer
	output.close();
	}

	public static void main(String[] args) throws Exception {
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
		GlobalRunner[] agents = new GlobalRunner[numFiles];
		
		// Loop through inputfile list and execute wordIndex method
		int count = 0;
		for(File file : inputFiles) {
			if (file.isFile() && file.getName().endsWith(".txt")) {
				agents[count] = new GlobalRunner(file, outputFolder, num_chars);
				agents[count].start();
				count = count + 1;
			}
		}

		// create TreeMap of TreeMaps to contain word indices for all input files
		TreeMap<String, TreeMap> indicesByFile = new TreeMap<String, TreeMap>();

		// Loop through threads, sync them, and print global indices
		for(GlobalRunner agent : agents) {
			if(agent.isAlive()) {
				// wait for agent to finish, then join with current thread
				agent.join();
			}
			// get filename, indices
			String filename = agent.getFilename();
			TreeMap file_indices = agent.getWordIndices();
			indicesByFile.put(filename, file_indices);
		}
		
		// Print all files
		printIndex(outputFolder, indicesByFile);

		// Stop timer, print elapsed time
		long endTime = System.currentTimeMillis();
		long elapsedTime = endTime - startTime;
		System.out.println(elapsedTime);
	}	
}