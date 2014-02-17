public class Consumer extends Thread {
    
    private CubbyHole cubbyhole;
    private int number;
    private int maxTimes;

    public Consumer(CubbyHole c, int number) 
    {
    
	cubbyhole = c;
        this.number = number;

    }

    public void run() 
    {
        int value = 0;
    
	while( true )
	    {	
		
		value = cubbyhole.get(number);
		
	    }

    }

}

