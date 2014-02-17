import com.beust.jcommander.Parameter;
import java.util.List;
import java.util.ArrayList;

public class Parameters {

	@Parameter
	public List<String> parameters = new ArrayList<String>();

	@Parameter(names = {"--verbose", "--debug", "-v", "-d"}, description = "Level of verbosity")
	public boolean verbose = false;

	@Parameter(names = {"--consumers", "-c"}, description = "Number of consumers")
	public int totalConsumerNumber = 4;

	@Parameter(names = {"--items", "-i"}, description = "Number of data items")
	public int totalDataItemsNumber = 10000;
 
}
