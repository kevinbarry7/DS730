import java.util.*;
import java.io.*;
public class RouteOptimizer extends Thread {
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
		
		TreeMap<Integer, ArrayList<Integer>> buildngs_map = new TreeMap<>();
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
					buildngs_map.put(building_id, travel_times);
					buildings_id_map.put(building_id, building_name);
					if(building_id != 0) {
						input_list.add(building_id);
					}
				}
			}

		}

		List<List<Integer>> permutations = get_permutations(input_list);
		TreeMap<Integer, Integer> route_times = new TreeMap<>();

		for (int i = 0; i < permutations.size(); i++) {
			List<Integer> perm = permutations.get(i);
			perm.add(0,0);
			perm.add(0);
			permutations.set(i, perm);
		}

		ListIterator<List<Integer>> iterator = permutations.listIterator();
		while (iterator.hasNext()) {
			int total_time = 0;
			int i = iterator.nextIndex();
			List<Integer> route = iterator.next();

			for (int j = 1; j < route.size(); j++) {
				int current_building_index = route.get(j-1);
				int next_building_index = route.get(j);
				ArrayList<Integer> building_times = buildngs_map.get(current_building_index);
				int time_to_next_bld = building_times.get(next_building_index);
				total_time += time_to_next_bld;
			}

			route_times.put(i, total_time);
		}

		Integer min_time = route_times.values().stream().min(Integer::compare).get();

		for (Map.Entry<Integer, Integer> entry : route_times.entrySet()) {
			if (entry.getValue().equals(min_time)) {
				Integer min_index = entry.getKey();
				
				List<Integer> route_indices = permutations.get(min_index);
				String optimal_route = Integer.toString(min_time) + " ";
				for (int i = 0; i < route_indices.size()-1; i++) {
					String next_building = buildings_id_map.get(route_indices.get(i));
					optimal_route = optimal_route + " " + next_building;
				}
				System.out.println(optimal_route);
			}
		}

		// for(List<Integer> perm : permutations) System.out.println(perm);
		// System.out.println(route_times);

		long endTime = System.currentTimeMillis();
		long elapsedTime = endTime - startTime;
		System.out.println(elapsedTime);
	}	
}

// CODE GRAVEYARD

	// public ArrayList<ArrayList<Integer>> get_permutations(List<Integer> input_list) throws Exception {
	// 	ArrayList<Integer> sub_list = new ArrayList<>();
	// 	List<Integer> perm_list = new ArrayList<>();
	// 	int list_length = input_list.size();

	// 	if(list_length == 0) {
	// 		return sub_list;
	// 	}

	// 	if(list_length == 1) {
	// 		sub_list.add(input_list.get(0));
	// 		return sub_list;
	// 	}


	// 	ListIterator<Integer> iterator = input_list.listIterator();
	// 	while (iterator.hasNext()) {
	// 		int i = iterator.nextIndex();
	// 		int parent = iterator.next();
			
	// 		List<Integer> children = new ArrayList<>();
	// 		List<Integer> elements_before = input_list.subList(0, i);
	// 		List<Integer> elements_after = input_list.subList(i+1, list_length);
	// 		children.addAll(elements_before);
	// 		children.addAll(elements_after);		
			
	// 		for (List<Integer> c : get_permutations(children)) {
	// 			List<Integer> parents_list = new ArrayList<>();
	// 			parents_list.addAll(parent);
	// 			parents_list.addAll(c);
	// 			perm_list.add(parents_list);
	// 		}

	// 	}

	// 	return perm_list;

	// }


		// for(List<Integer> perm : permutations) System.out.println(perm);
		// System.out.println(permutations.size());
		// swap(input_list, 1, 1);


		// List<Integer> combined = new ArrayList<>();
		// List<Integer> before = input_list.subList(0, 0);
		// List<Integer> after = input_list.subList(2, 3);
		// combined.addAll(before);
		// combined.addAll(after);
		// testing.add(input_list.subList(0, 1));
		// testing.add(input_list.subList(0, 1));
		// System.out.println(before);
		// System.out.println(after);
		// System.out.println(combined);

		// for(Map.Entry<String, ArrayList<Integer>> key_value : buildngs_map.entrySet()) {
		// 	String building_name = key_value.getKey();
		// 	ArrayList<Integer> travel_times = key_value.getValue();
		// 	TreeMap<String, Integer> travel_times_verbose = new TreeMap<>(); 

		// 	ListIterator<Integer> iterator = travel_times.listIterator();
		// 	while (iterator.hasNext()) {
		// 		int i = iterator.nextIndex();
		// 		String name = buildings_list.get(i);
		// 		int time = iterator.next();
		// 		travel_times_verbose.put(name, time);
		// 	}

		// 	buildngs_map_verbose.put(building_name, travel_times_verbose);

		// }

		// System.out.println(buildngs_map);
		// System.out.println(buildings_id_map);

		// Stop timer, print elapsed time