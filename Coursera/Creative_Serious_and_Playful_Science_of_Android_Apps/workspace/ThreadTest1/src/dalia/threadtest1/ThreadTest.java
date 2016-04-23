package dalia.threadtest1;

public class ThreadTest extends Thread {
	private int number;

	public void run()
	{
		//while(number < 25)
		//{
			//System.out.println("Number: " + number);
			increaseNumber();
		//}
	}
	
	private synchronized void increaseNumber()
	{
		while(number < 25)
		{
			System.out.println("Number: " + number);
			number++;
		}
	}
	
	public static void main(String args[])
	{
		ThreadTest thread1 = new ThreadTest();
		ThreadTest thread2 = new ThreadTest();


		thread1.start();
		thread2.start();
	}
}