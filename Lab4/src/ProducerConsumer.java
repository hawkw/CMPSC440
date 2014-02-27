import java.util.Random;
import com.beust.jcommander.*;
import java.util.List;
import java.util.ArrayList;

class Producer implements Runnable {
    BoundedBuffer b = null;
    int count;

    public Producer(BoundedBuffer b){
        this.b = b;
        new Thread(this).start();
    }

    public void run() {
        double item;
        Random r = new Random();
        while (ProducerConsumer.isDone(count) == false) {
            item = r.nextDouble();

            if (ProducerConsumer.isVerbose())
                System.out.printf("[Verbose] [%s %s] produced item %s\n", this.toString(), Thread.currentThread().getName(), item);

            b.deposit(item);
            Util.mySleep(200);
            count++;
        }
    }
}
class Consumer implements Runnable {
    BoundedBuffer b = null;

    public Consumer(BoundedBuffer b) {
        this.b = b;
        new Thread(this).start();
    }

    public void run() {
        double item;
        while (true) {
            item = b.fetch();

            if (ProducerConsumer.isVerbose())
                System.out.printf("[Verbose] [%s %s] fetched item %s\n", this.toString(), Thread.currentThread().getName(), item);

            Util.mySleep(50);
        }
    }
}
class Parameters {
    @Parameter
    public List<String> parameters = new ArrayList<String>();

    @Parameter(names = {"--verbose", "--debug", "-v", "-d"}, description = "Level of verbosity")
    public boolean verbose = false;

    @Parameter(names = {"-!", "--disable"}, description = "What functions to disable.")
    public List<String> disables = new ArrayList<String>();

    @Parameter(names = {"--consumers", "-c"}, description = "Number of consumers")
    public int consumers = 1;

    @Parameter(names = {"--items", "-i"}, description = "Number of data items")
    public int dataItems = 10000;
}

class ProducerConsumer {
    private static boolean verbosity;
    private static List<String> disables;
    private static int dataItems;

    public static boolean isVerbose() {
        return verbosity;
    }

    public static boolean isDisabled(String function) {
        return disables.contains(function);
    }

    public static boolean isDone(int count) {
        return (count == dataItems);
    }

    public static void main(String[] args) {
        Parameters parameters = new Parameters();
        new JCommander(parameters, args);

        verbosity = parameters.verbose;
        disables = parameters.disables;
        dataItems = parameters.dataItems;

        BoundedBuffer buffer = new BoundedBuffer();
        Producer producer = new Producer(buffer);
        Consumer consumer;

        for(int i = 0; i < parameters.consumers; i++){
            consumer = new Consumer(buffer);
        }
    }
}

