import java.util.*;
import java.io.*;
public class RouteOptimizer extends Thread {
	// private ListIterator<List<Integer>> iterator;
	private List<List<Integer>> perm_subset;
	private TreeMap<Integer, ArrayList<Integer>> buildings_map;
	private TreeMap<Integer, Integer> route_times;
	private int start;
	
	public RouteOptimizer(List<List<Integer>> perm_subset, TreeMap<Integer, ArrayList<Integer>> buildings_map, int start) throws Exception {
		this.buildings_map = buildings_map;
		this.route_times = new TreeMap<>();
		this.start = start;
		this.perm_subset = perm_subset;
	}

	public void run() {
		// for each route in an array, compute the time of the route and assign the route an id. add this to route_times array.

		int i = start;
		for (List<Integer> route : perm_subset) {
			int total_time = 0;

			for (int j = 1; j < route.size(); j++) {
				int current_building_index = route.get(j-1);
				int next_building_index = route.get(j);
				ArrayList<Integer> building_times = buildings_map.get(current_building_index);
				int time_to_next_bld = building_times.get(next_building_index);
				total_time += time_to_next_bld;
			}

			route_times.put(i, total_time);
			i += 1;
		}
	}

	public TreeMap<Integer, Integer> get_route_times() {
		return route_times;
	}

	// function to generate permutations
	public static List<List<Integer>> get_permutations(List<Integer> original) {
		if (original.size() == 0) {
			List<List<Integer>> result = new ArrayList<List<Integer>>(); 
			result.add(new ArrayList<Integer>()); 
			return result; 
		}

		Integer firstElement = original.remove(0);
		List<List<Integer>> returnValue = new ArrayList<List<Integer>>();
		List<List<Integer>> permutations = get_permutations(original);

		for (List<Integer> smallerPermutated : permutations) {
			for (int index=0; index <= smallerPermutated.size(); index++) {
				List<Integer> temp = new ArrayList<Integer>(smallerPermutated);
				temp.add(index, firstElement);
				returnValue.add(temp);
			}
		}
		return returnValue;
	}

	public static void main(String[] args) throws Exception {
		// Start timer
		long startTime = System.currentTimeMillis();
		
		TreeMap<Integer, ArrayList<Integer>> buildings_map = new TreeMap<>();
		TreeMap<Integer, String> buildings_id_map = new TreeMap<>();
		List<Integer> input_list = new ArrayList<>();

		// Read in file
		File file = new File("input2.txt");

		// read in file
		try(BufferedReader br = new BufferedReader(new FileReader(file))) {
			{
				int building_id = 0;
				for(String line;  (line = br.readLine()) != null; building_id++ ) {
					// split file into list by colon
					ArrayList<String> line_list = new ArrayList<String>(Arrays.asList(line.split(" : ")));
					String building_name = line_list.get(0);

					// convert (string) travel times to list
					ArrayList<String> travel_times_str = new ArrayList<String>(Arrays.asList(line_list.get(1).replace("\n", "").split(" ")));
					ArrayList<Integer> travel_times = new ArrayList<Integer>();
					
					// convert travel times to int
					for(String time : travel_times_str) travel_times.add(Integer.valueOf(time));
					
					// write building key + travel times to TreeMap
					buildings_map.put(building_id, travel_times);
					buildings_id_map.put(building_id, building_name);
					if(building_id != 0) {
						input_list.add(building_id);
					}
				}
			}

		}

		// get permutations
		List<List<Integer>> permutations = get_permutations(input_list);

		// loop through permutations and add start/end building
		for (int i = 0; i < permutations.size(); i++) {
			List<Integer> perm = permutations.get(i);
			perm.add(0,0);
			perm.add(0);
			permutations.set(i, perm);
		}

		// section start: split the list of permutations into chunks, and assign each chunk to a thread for mapping route to time
		int num_permutations = permutations.size();
		int num_threads = 1;

		if(num_permutations >= 100) {
			num_threads = 20;
		}
		
		RouteOptimizer[] agents = new RouteOptimizer[num_threads];
		
		int count = 1;
		int start = 0;
		int perm_per_thread = num_permutations / num_threads;
		int thread_id = 0;
		int len_test = 0;

		for (int i = 0; i < num_permutations; i++) {
			if(count == perm_per_thread) {
				if((i + 1) == num_permutations) i += 1;
				List<List<Integer>> perm_subset = permutations.subList(start, i);
				agents[thread_id] = new RouteOptimizer(perm_subset, buildings_map, start);
				agents[thread_id].start();
				start = i;
				count = 0;
				thread_id += 1;
			}
			count += 1;
		}
		// section end

		TreeMap<Integer, Integer> all_routes = new TreeMap<>();

		// section start: get mapped list of route times for each thread
		for(RouteOptimizer agent : agents) {
			if(agent.isAlive()) {
				agent.join();
			}

			TreeMap<Integer, Integer> thread_routes = agent.get_route_times();

			for (Map.Entry<Integer, Integer> entry : thread_routes.entrySet()) {
				int i = entry.getKey();
				int time = entry.getValue();
				all_routes.put(i, time);
			}
		}

		// get minimum route time
		Integer min_time = all_routes.values().stream().min(Integer::compare).get();

		// get route for minimum route time
		for (Map.Entry<Integer, Integer> entry : all_routes.entrySet()) {
			if (entry.getValue().equals(min_time)) {
				FileWriter fileWriter = new FileWriter("output2.txt");
				PrintWriter output = new PrintWriter(fileWriter);

				Integer min_index = entry.getKey();				
				List<Integer> route_indices = permutations.get(min_index);
				String optimal_route = Integer.toString(min_time);
				
				// print results
				for (int i = 0; i < route_indices.size()-1; i++) {
					String next_building = buildings_id_map.get(route_indices.get(i));
					optimal_route = optimal_route + " " + next_building;
				}
				output.print(optimal_route);
				output.close();
				break;
				// System.out.println(optimal_route);
			}
		}		

		long endTime = System.currentTimeMillis();
		long elapsedTime = endTime - startTime;
		System.out.println(elapsedTime);
	}	
}