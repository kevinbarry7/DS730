import java.util.*;
public class First{
	public static boolean isPrime(int value){
		Boolean prime_check = true;
		for(int i = 2; i < value; i++){
			if((value % i) == 0) {
				prime_check = false;
			}
		}
		return prime_check;
	}	

	public static void printPrime(int first, int second){
		int diff_test = Math.abs(first - second);
		if(diff_test > 1) {
			ArrayList<Integer> numbers = new ArrayList<>();
			ArrayList<Integer> primes = new ArrayList<>();
			numbers.add(first);
			numbers.add(second);
			Collections.sort(numbers);

			int min = numbers.get(0) + 1;
			int max = numbers.get(1);

			for(int i = min; i < max; i++){
				Boolean prime_check = isPrime(i);

				if(prime_check == true && i != 1) {
					primes.add(i);
				}
			}

			if(primes.size() != 0) {
				for(Integer val : primes) {
					// System.out.format("%d", val);
					System.out.print(val + " ");
				}					
			} else {
				System.out.println("No primes.");
			}
		
		} else {
			System.out.println("No primes.");
		}
	}
	public static void main(String args[]){
		Scanner input = new Scanner(System.in);
		List<Integer> numbers = new ArrayList<>();

		for(int count=0; count < 2; count++){
			System.out.print("Enter number: ");
			int value = input.nextInt();

			while(value < 0){
				System.out.print("Enter in a positive number: ");
				value = input.nextInt();
				if(value >= 0) {
					numbers.add(value);
				}
			}
			numbers.add(value);
		}
		printPrime(numbers.get(0), numbers.get(1));
	}
}