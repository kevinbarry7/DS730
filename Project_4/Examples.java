import java.io.*;  //needed for File class below
import java.util.*;  //needed for Scanner class below

public class Examples
{
    public static void computeFactorial(int number){
        int factorial = 1;
        //calculates number * (number-1) * (number-2) * ... * 2 * 1
        while(number > 0){
            factorial = factorial * number;
            number--;
        }
        System.out.println("Factorial is: "+factorial);
    }
    
    public static void readInWords(String fileName){
        try{
            //open up the file
            Scanner input = new Scanner(new File(fileName));
            int count = 0;
            while(input.hasNext()){
                //read in 1 word at a time and increment our count
                input.next();
                count++;
            }
            System.out.println("Count is: "+count);
        }catch(Exception e){
            System.out.println("Something went really wrong...");
        }   
    }
    
    public static void average(String fileName){
        try{
            //open up the file
            Scanner input = new Scanner(new File(fileName));
            int count = 0;
            int total = 0;
            while(input.hasNextInt()){
                //read in 1 number at a time and add to total
                total += input.nextInt();
                count++;
            }
            //Java does integer division. Therefore, 5 / 3 is 1, not 1.66666666
            //To ensure we get an accurate average, the int is converted into a double.
            //Now it would become 5.0 / 3 which is 1.6666666...
            double totalAsDouble = total; 
            System.out.println("Average is: "+(totalAsDouble / count));
        }catch(Exception e){
            System.out.println("Something went really wrong...");
        }   
    }
    
    public static void main(String args[]){
        int x = 10;  //can read in from user or simply set here
        computeFactorial(x);
        
        String fileName = "input.txt";
        readInWords(fileName);
        
        fileName = "numberFile.txt";
        average(fileName);
    }
}
