import java.util.*; 
import java.io.*; 

public class TestStateless{
	public static void main(String args[]){
		ArrayList<String> deleteMe = new ArrayList<>();
		try{
			if(args.length!=5){
				System.out.println("Usage: java TestStateless mapperFile reducerFile inputFile outputFile deleteTempFiles");
				System.exit(0);
			}
			//split up the input
			BufferedReader file = new BufferedReader(new FileReader(args[2]));
			int fileNumber = 0;
			String line = file.readLine();
			while(line!=null){
				PrintWriter fout = new PrintWriter(new FileWriter("mapperOut"+fileNumber+".tmp"));
				fout.println(line);
				fout.close();
				deleteMe.add("mapperOut"+fileNumber+".tmp");
				fileNumber++;
				line = file.readLine();
			}
			file.close();
			String delimeter = "\t";
			ArrayList<String> everything = new ArrayList<>();
			//run the mapper on each line of the input
			for(int i=0; i<fileNumber; i++){
				ProcessBuilder builder = new ProcessBuilder();
				builder.command("python", args[0]);
				Process p = builder.start();
				OutputStream pos = p.getOutputStream();
				InputStream ios = p.getInputStream();
				InputStream fis = new FileInputStream("mapperOut"+i+".tmp");
				byte[] buffer = new byte[1024];
				int read = 0;
				while((read = fis.read(buffer)) != -1) {
					pos.write(buffer, 0, read);
				}
				pos.close();
				fis.close();
				p.waitFor();
				BufferedReader buff = new BufferedReader(new InputStreamReader(ios));
				line = buff.readLine();
				while(line!=null){
					everything.add(line);
					line = buff.readLine();
				}
			}
			Collections.sort(everything);

			ArrayList<String> tempEverything = new ArrayList<String>();
			String curKey = "";
			int beginning = 0;
			for(int end=0; end<everything.size(); end++){
				String now = everything.get(end).substring(0, everything.get(end).indexOf(delimeter));
				if(curKey.equals("")){
					//beginning of list, get first key
					curKey = now;
				} else if(!curKey.equals(now)){
					//got a new key, shuffle from beginning to end-1 so the values aren't sorted
					List<String> tempSort = everything.subList(beginning, end);
					Collections.shuffle(tempSort);
					tempEverything.addAll(tempSort);
					//store new key and restart the numbering
					curKey = now;
					beginning = end;
				}
			}
			//add the last key to the mix
			List<String> tempSort = everything.subList(beginning, everything.size());
			Collections.shuffle(tempSort);
			tempEverything.addAll(tempSort);
			everything = tempEverything;
			//all keys are sorted but the values are not
			fileNumber = 0;
			String curString = "";
			curKey = "";
			for(String s : everything){
				String key = s.substring(0, s.indexOf(delimeter));
				String value = s.substring(s.indexOf(delimeter)+1, s.length());
				if(curKey.equals("")){
					//it's the start
					curKey = key;
					curString = s;
				} else{
					if(curKey.equals(key)){
						curString += "\n"+s;
					}else{
						//got a new key, output old stuff
						PrintWriter fout = new PrintWriter(new FileWriter("reducerIn"+fileNumber+".tmp"));
						fout.print(curString);
						fout.close();
						deleteMe.add("reducerIn"+fileNumber+".tmp");
						curKey = key;
						curString = s;
						fileNumber++;
					}
				}
			}
			//output the last key
			PrintWriter fout = new PrintWriter(new FileWriter("reducerIn"+fileNumber+".tmp"));
			fout.print(curString);
			deleteMe.add("reducerIn"+fileNumber+".tmp");
			fileNumber++;
			fout.close();
			//run reducer on them
			PrintWriter finalOutput = new PrintWriter(new FileWriter(args[3]));
			for(int i=0; i<fileNumber; i++){
				ProcessBuilder builder = new ProcessBuilder();
				builder.command("python", args[1]);
				Process p = builder.start();
				OutputStream pos = p.getOutputStream();
				InputStream ios = p.getInputStream();
				InputStream fis = new FileInputStream("reducerIn"+i+".tmp");
			 	byte[] buffer = new byte[1024];
				int read = 0;
				while((read = fis.read(buffer)) != -1) {
					pos.write(buffer, 0, read);
				}
				pos.close();
				fis.close();
				p.waitFor();
				BufferedReader buff = new BufferedReader(new InputStreamReader(ios));
				line = buff.readLine();
				while(line!=null){
					finalOutput.println(line);
					line = buff.readLine();
				}
			}
			finalOutput.close();
			System.out.println("Mapping and Reducing completed successfully. Your output is stored in "+args[3]+". This message does not mean your answer is correct though. All this message is saying is that your mapper and reducer executed without failing. It does not mean the mapper and reducer are correct.");
		} catch(Exception e){
			//something went wrong
			System.out.println(e);
		} finally{
			if(args[4].equalsIgnoreCase("N")){
				for(String gone : deleteMe){
					File f = new File(gone);
					f.delete();
				}
			}
		}
	}
}