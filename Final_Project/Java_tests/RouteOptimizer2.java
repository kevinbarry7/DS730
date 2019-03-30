import java.util.*;
import java.io.*;
public class RouteOptimizer2 extends Thread {
	// private ListIterator<List<Integer>> iterator;
	private List<List<Integer>> perm_subset;
	private TreeMap<Integer, ArrayList<Integer>> buildings_map;
	private TreeMap<Integer, Integer> route_times;
	private int start;
	
	public RouteOptimizer2(List<List<Integer>> perm_subset, TreeMap<Integer, ArrayList<Integer>> buildings_map, int start) throws Exception {
		// this.iterator = perm_subset.listIterator();
		this.buildings_map = buildings_map;
		this.route_times = new TreeMap<>();
		this.start = start;
		this.perm_subset = perm_subset;
	}

	public void run() {
		int i = start;
		for (List<Integer> route : perm_subset) {
			int total_time = 0;
			// System.out.printf("route: %s - i: %d %n", route, i);

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

	@SuppressWarnings("unchecked")
	public static synchronized void print_optimal_route(TreeMap<Integer, Integer> all_routes, List<List<Integer>> permutations, TreeMap<Integer, String> buildings_id_map) throws Exception {
		Integer min_time = all_routes.values().stream().min(Integer::compare).get();

		// loop through route_times to get route that was the fastest time
		for (Map.Entry<Integer, Integer> entry : all_routes.entrySet()) {
			if (entry.getValue().equals(min_time)) {
				// get key of min time
				Integer min_index = entry.getKey();
				
				// loop through route indices and get actual route of fastest time
				List<Integer> route_indices = permutations.get(min_index);

				// Create string to display result
				String optimal_route = Integer.toString(min_time) + " ";
				for (int i = 0; i < route_indices.size()-1; i++) {
					String next_building = buildings_id_map.get(route_indices.get(i));
					optimal_route = optimal_route + " " + next_building;
				}
				System.out.println(optimal_route);
			}
		}
	}

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
		File file = new File("input5.txt");

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

		List<List<Integer>> permutations = get_permutations(input_list);

		for (int i = 0; i < permutations.size(); i++) {
			List<Integer> perm = permutations.get(i);
			perm.add(0,0);
			perm.add(0);
			permutations.set(i, perm);
		}

		int num_permutations = permutations.size();
		int num_threads = 1;

		if(num_permutations >= 100) {
			num_threads = 20;
		}
		
		RouteOptimizer2[] agents = new RouteOptimizer2[num_threads];
		
		int count = 1;
		int start = 0;
		int perm_per_thread = num_permutations / num_threads;
		int thread_id = 0;
		int len_test = 0;

		for (int i = 0; i < num_permutations; i++) {
			// System.out.printf("Count %d - i %d %n", count, i);
			if(count == perm_per_thread) {
				if((i + 1) == num_permutations) i += 1;
				List<List<Integer>> perm_subset = permutations.subList(start, i);
				// int perm_len = perm_subset.size();
				// len_test += perm_len;
				agents[thread_id] = new RouteOptimizer2(perm_subset, buildings_map, start);
				agents[thread_id].start();
				// System.out.println(len_test);
				start = i;
				count = 0;
				thread_id += 1;
			}
			count += 1;
		}

		TreeMap<Integer, Integer> all_routes = new TreeMap<>();

		for(RouteOptimizer2 agent : agents) {
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

		print_optimal_route(all_routes, permutations, buildings_id_map);		

		long endTime = System.currentTimeMillis();
		long elapsedTime = endTime - startTime;
		System.out.println(elapsedTime);
	}	
}