package johnsHopkins;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

public class HW {

	final static Pattern pattern = Pattern.compile("DP=(\\d+)");
	public static int getDepth(String info) {
		Matcher m = pattern.matcher(info);
		if (m.find())
			return Integer.parseInt(m.group(1));
		return 0;
	}
	public static boolean isSNV(String ref, String alt) {
		String[] altList = alt.split(",");
		boolean all = true;
		for (String alts : altList) {
			all = (alts.length() == 1) && all;
		}
		return (ref.length() == 1 && all);
	}
	
	public static void printStats(String filename) {
		try {
			BufferedReader reader = new BufferedReader(new FileReader(filename));
			String header = null; 
			do {
				header = reader.readLine();
			} while (header.startsWith("##"));
			String[] headerList = header.split("\t");
			Iterable<CSVRecord> records = CSVFormat.DEFAULT.withDelimiter('\t').withHeader(headerList).parse(reader);
//			ArrayList<String> alts = new ArrayList<String>();
			int numSNV = 0, numIndels = 0, meanDepthSNV = 0;
			for (CSVRecord record : records) {
				if (isSNV(record.get("REF"), record.get("ALT"))) {
					numSNV++;
					meanDepthSNV += getDepth(record.get("INFO"));
				} else{
					numIndels++;
				}
//				alts.add(record.get("ALT"));
			}
			System.out.println("Number of indels: "+numIndels);
			System.out.println("Number of SNVs: "+numSNV);
			System.out.println("SNV mean depth: "+meanDepthSNV);
			reader.close();
		}catch(IOException ex) {
			System.err.println("IOException:");
			ex.printStackTrace();
		}
	}
	
	public static void main(String args[]) {
		
		String file1 = "NA12891.QC_RAW_OnBait_truncated.vcf";
//		String file2 = "NA12891.QC_RAW_OnBait_truncated.vcf";
		printStats(file1);
		

	}
}
