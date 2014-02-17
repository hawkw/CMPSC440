public class Producer extends Thread 
{

    private CubbyHole cubbyhole;
    private int number;
    private int maxTimes;

    public Producer(CubbyHole c, int number, int maxTimes) 
    {
    
	cubbyhole = c;
        this.number = number;
	this.maxTimes = maxTimes;
	
    }

    public void run() 
    {
        
	for (int i = 0; i < maxTimes; i++) 
	    {
		cubbyhole.put(number, i);
		
		try 
		    {
		    
			sleep((int)(Math.random() * 100));
		    } 
		
		catch (InterruptedException e) 
		    { e.printStackTrace(); }
	    }

	System.out.println("Producer done.");
	System.out.println("Terminating model.");

    }
}
