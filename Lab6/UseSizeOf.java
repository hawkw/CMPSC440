import com.vladium.utils.IObjectProfileNode;
import com.vladium.utils.ObjectProfileFilters;
import com.vladium.utils.ObjectProfileVisitors;
import com.vladium.utils.ObjectProfiler;

//---------------------------------------------------------
// These classes play the role of the int_2d, int_3d, 
// double_2d, and double_3d structs from usesizeof.c

/**
 * Represents a point in 2D space with integer precision coordinates.
 */
class Int2D {
	private int x, y;

	public Int2D() {
		this.x = 0;
		this.y = 0;
	}

	public Int2D (int x, int y) {
		this.x = x;
		this.y = y;
	}
}

/**
 * Represents a point in 3D space with integer precision coordinates.
 */
class Int3D {
	private int x, y, z;

	public Int3D() {
		this.x = 0;
		this.y = 0;
		this.z = 0;
	}

	public Int3D (int x, int y, int z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}
}

/**
 * Represents a point in 2D space with double precision coordinates.
 */
class Double2D {
	private double x, y;

	public Double2D() {
		this.x = 0.0;
		this.y = 0.0;
	}

	public Double2D (double x, double y) {
		this.x = x;
		this.y = y;
	}
}

/**
 * Represents a point in 3D space with double precision coordinates.
 */
class Double3D {
	private double x, y ,z;

	public Double3D() {
		this.x = 0.0;
		this.y = 0.0;
		this.z = 0.0;
	}

	public Double3D (double x, double y, double z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}
}
//---------------------------------------------------------

public class UseSizeOf {
	private static final int BYTE_SIZE 	= 8;
	private static final String HEAD_FMT = "%-12s%8s%8s\n";
	private static boolean texMode = false;

	private static int bits (int bytes) {
		return bytes * BYTE_SIZE;
	}

	private static void makeLine (Class<?> target) {
		String name = target.getName().substring(0, target.getClass().getName().indexOf("$"));
		int bytes 	= ObjectProfiler.profile(new target()).size();

		if (texMode) {
			System.out.printf("%-12s & %d & %8d \\\\ \n", name, bytes, bits(bytes));
		} else {
			System.out.printf("%-12s%8d%8d\n", name, bytes, bits(bytes));
		}
	}

	public static void main(String[] argv) {

		// check to see if we're making the TeX-friendly table and set the flag
		texMode = (argv[0].equals("-t") || argv[0].equals("--tex"));

		System.out.printf(HEAD_FMT, "data type", "bytes", "bits");
		System.out.printf(HEAD_FMT, "---- ----", "-----", "----");

		makeLine(byte.class);
		makeLine(short.class);
		makeLine(int.class);
		makeLine(long.class);
		makeLine(float.class);
		makeLine(char.class);
		makeLine(boolean.class);

		makeLine(Int2D.class);
		makeLine(Int3D.class);

	}
}