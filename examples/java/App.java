import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        try(Scanner sc = new Scanner(System.in)){
            int x = sc.nextInt();
            System.out.println(2*x);
        }
    }
}
