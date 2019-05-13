import java.util.*;
import java.io.*;
public class IndexRunner{
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
				// System.out.println(numFiles);
			}
		}		

		// Create IndexThread
		IndexThread[] agent = new IndexThread[numFiles];
		
		// Loop through inputfile list and execute wordIndex method
		int count = 0;
		for(File file : inputFiles) {
			if (file.isFile() && file.getName().endsWith(".txt")) {
				agent[count] = new IndexThread(file, outputFolder, num_chars);
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