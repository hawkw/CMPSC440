/**
 * UseSizeOf.java
 * by Hawk Weisman
 * for CMPSC440 Lab 6
 * at Allegheny College
 *
 * Determines the size of various Java data types.
 */

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
	private static final String HEAD_FMT = "%-12s%8s%8s\n";
	private static boolean texMode = false;

	/**
	 * Converts numbers of bits to numbers of bytes.
	 * @param bits an integer representing a number of bits
	 * @return the number of bytes represented by that measurements.
	 */
	private static int bytes (int bits) {
		return bits / Byte.SIZE;
	}

	/**
	 * Converts numbers of bytes to numbers of bits.
	 * @param bytes an integer representing a number of bytes
	 * @return the number of bits represented by that measurements.
	 */
	private static int bits (int bytes) {
		return bytes * Byte.SIZE;
	}

	/**
	 * Prints a line describing the size of the given class.
	 * @param 	target	the class to describe
	 */
	private static void makeLine (Class target) {
		String name;
		int bytes;

		if (target.getPackage() != null) {
			// strip package names from objects (so that they fit in the table)
			name = target.getName().replaceAll(target.getPackage().getName() + ".", "");
		} else {
			name = target.getName();
		}

		try {
			// get the size in bytes of the target object by running
			// ObjectProfiler.profile on a new anonymous instance of the class
			bytes = ObjectProfiler.profile(target.newInstance()).size();

			if (texMode) {
				System.out.printf("%-12s & %d & %8d \\\\ \n", name, bytes, bits(bytes));
			} else {
				System.out.printf("%-12s%8d%8d\n", name, bytes, bits(bytes));
			}

		} catch (InstantiationException ie) {

			if (texMode) {
				System.out.printf("%-12s & %16s \\\\ \n", name, "InstantiationException");
			} else {
				System.out.printf("%-12s%16s\n", name, "InstantiationException");
			}

		} catch (IllegalAccessException iae) {

			if (texMode) {
				System.out.printf("%-12s & %16s \\\\ \n", name, "IllegalAccessException");
			} else {
				System.out.printf("%-12s%16s\n", name, "IllegalAccessException");
			}

		}
	}

	public static void main(String[] argv) {

		// check to see if we're making the TeX-friendly table and set the flag
		texMode = (argv[0].equals("-t") || argv[0].equals("--tex"));

		// print the table header
		System.out.printf(HEAD_FMT, "data type", "bytes", "bits");
		System.out.printf(HEAD_FMT, "---- ----", "-----", "----");

			// if the TeX mode flag is set...
			if (texMode) {
				// ...print the Tex-friendly table for the Java primitives.
				System.out.printf("%-12s & %d & %8d \\\\ \n", "byte", bytes(Byte.SIZE), Byte.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "short",bytes(Short.SIZE), Short.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "int", bytes(Integer.SIZE), Integer.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "long", bytes(Long.SIZE), Long.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "float", bytes(Float.SIZE), Float.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "double", bytes(Double.SIZE),  Double.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "char", bytes(Character.SIZE), Character.SIZE);
				System.out.printf("%-12s & %d & %8d \\\\ \n", "boolean", ObjectProfiler.profile(new Boolean("true")).size() - ObjectProfiler.profile(new Object()).size(), bits(ObjectProfiler.profile(new Boolean("true")).size() - ObjectProfiler.profile(new Object()).size()));
			// ...otherwise...
			} else {
				// ...print out the standard table for the Java primitives
				System.out.printf("%-12s%8d%8d\n", "byte", bytes(Byte.SIZE), Byte.SIZE);
				System.out.printf("%-12s%8d%8d\n", "short", bytes(Short.SIZE), Short.SIZE);
				System.out.printf("%-12s%8d%8d\n", "int", bytes(Integer.SIZE), Integer.SIZE);
				System.out.printf("%-12s%8d%8d\n", "long", bytes(Long.SIZE), Long.SIZE);
				System.out.printf("%-12s%8d%8d\n", "float", bytes(Float.SIZE), Float.SIZE);
				System.out.printf("%-12s%8d%8d\n", "double", bytes(Double.SIZE),  Double.SIZE);
				System.out.printf("%-12s%8d%8d\n", "char", bytes(Character.SIZE), Character.SIZE);
				System.out.printf("%-12s%8d%8d\n", "boolean", ObjectProfiler.profile(new Boolean("true")).size() - ObjectProfiler.profile(new Object()).size(), bits(ObjectProfiler.profile(new Boolean("true")).size() - ObjectProfiler.profile(new Object()).size()));
			}

		// print lines describing some other classes.
		makeLine(Object.class);
		makeLine(Int2D.class);
		makeLine(Int3D.class);
		makeLine(Double2D.class);
		makeLine(Double3D.class);
	}
}