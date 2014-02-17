import java.io.*;
import com.beust.jcommander.*;

public class ProducerConsumerModel
{

    // NOTE: you must implement the command line processing for 
    // this class.  Currently, all variables are hard coded to 
    // some default values.

    // command line arguments : 
    // [ debug? ] [ number data items ] [ number of consumers ]

    public static void main(String[] args)
    {
        Parameters parameters = new Parameters();
        new JCommander(parameters, args);
        
        // create a CubbyHole that both the Producer and 
        // and the Consumer will use to store data items
        CubbyHole cubbyHole = new CubbyHole(parameters.verbose);

        // create the only producer as a single thread and
        // then get it started on producing numbers
        Producer producer = 
            new Producer(cubbyHole, 1, parameters.totalDataItemsNumber);
        producer.start();

        // this is the single Consumer variable that we will
        // use to start each of the Consumer threads
        Consumer consumerSource;

        // create all of the different consumer threads
        for(int i = 0; i < parameters.totalConsumerNumber; i++)
        {

            consumerSource = new Consumer(cubbyHole, i);
            consumerSource.start();

        }

        // wait for the producer to finish and then terminate
        // the process (note: this would not always work if the 
        // Consumer threads had "tasks" that took a long time 
        // to complete)

        try
        {

            producer.join();
            System.exit(1);

        }

        catch(Exception e)
        {

            e.printStackTrace();

        }

    }

}
