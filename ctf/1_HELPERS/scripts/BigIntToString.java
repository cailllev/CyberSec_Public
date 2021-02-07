// Usage: java BigIntToString.java <Big Int here>
// used to convert RSA results to strings

import java.math.BigInteger;

public class Decrypt {
  //Main method
  public static void main(String[] args) {
    BigInteger bigInt = new BigInteger(args[0]);
      byte[] bytes = bigInt.toByteArray();

      char[] chars = new char[bytes.length];
      for (int i = 0; i < bytes.length; i++) {
        chars[i] = (char) bytes[i];
      }

      System.out.println(chars);
  }
}
