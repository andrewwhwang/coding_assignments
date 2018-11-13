#!/usr/bin/python3
import pandas as pd

def getHeaderLineNum(filename):
    with open(filename) as f:
        # iterate thru file, stops when prefix is not ##
        for i, line in enumerate(f):
            if not line.startswith("##"):
                # returns the line number
                return i

def getSNVs(df):
    #REF must be 1 char long AND every ALT must be 1 char long 
    condition = (df["REF"].str.len() == 1) & \
                (df.apply(lambda x: all(len(i) == 1 for i in x['ALT'].split(",")), axis=1))
    #apply the condition and return length of dataframe
    SNV = df[condition]
    return SNV

def getNumIndels(df):
    #It's an indel if length of REF > 1 OR any ALT is > 1 char long
    condition = (df["REF"].str.len() > 1) | \
                (df.apply(lambda x: any(len(i) > 1 for i in x['ALT'].split(",")), axis=1))
    #apply the condition and return length of dataframe
    indels = len(df[condition])
    return indels

def getMeanSVN(df):
    # uses regex on INFO column to get DP value
    # make sure to set type to int or else it'll avg the ASCII values!
    depths = df["INFO"].str.extract(r"DP=(\d+)").astype(int)
    # return the mean
    mean = float(depths.mean())
    return mean

def numByChrom(df):
    # compile list of unique chromosomes and loop thru them
    chromos = df['#CHROM'].unique().tolist()
    for chromo in chromos:
        # splits up df into sub-df, prints out length of sub-df
        chromDF = df[df["#CHROM"] == chromo]
        print("Chromosome {}: {}".format(chromo,len(chromDF)))

def concordance(SNV1, SNV2):
    #set (CHROM, POS) tuple as index
    SNV1 = SNV1.set_index(["#CHROM", "POS"])
    SNV2 = SNV2.set_index(["#CHROM", "POS"])

    # get rid of all columns except ALT for simplicity
    SNV1 = SNV1[["ALT"]]
    SNV2 = SNV2[["ALT"]]
    # renamed ALT --> ALT2 so we won't get confused when merging
    SNV2.columns = ["ALT2"]

    # merge by index
    merged = pd.concat([SNV1, SNV2], axis=1)

    # count if the ALTs match and calculate percentage
    condition = (merged["ALT"] == merged["ALT2"])
    common = len(merged[condition])
    total = len(merged)
    percent = 100.0 * common / total
    return percent

def main():
    # import and parse data
    vcf1 = "NA12891.QC_RAW_OnBait.vcf"
    vcf2 = "NA12878.QC_RAW_OnBait.vcf"
    df1 = pd.read_table(vcf1, dtype={"#CHROM": str}, skiprows=getHeaderLineNum(vcf1))
    df2 = pd.read_table(vcf2, dtype={"#CHROM": str}, skiprows=getHeaderLineNum(vcf2))
    # make df of SNVs only
    SNV1 = getSNVs(df1)
    SNV2 = getSNVs(df2)

    #######################################OUTPUT for 1st file########################################
    print("-------------{} stats-------------".format(vcf1))
    print("Number of SNVs: {}".format(len(SNV1)))
    print("Number of Indels: {}".format(getNumIndels(df1)))
    print("Mean Depth of SNVs: {}".format(getMeanSVN(SNV1)))
    numByChrom(SNV1)

    ########################################OUTPUT for 2nd file#######################################
    print("-------------{} stats-------------".format(vcf2))
    print("Number of SNVs: {}".format(len(SNV2)))
    print("Number of Indels: {}".format(getNumIndels(df2)))
    print("Mean Depth of SNVs: {}".format(getMeanSVN(SNV2)))
    numByChrom(SNV2)

    ##################################################################################################
    print("Concordance: {}".format(concordance(SNV1, SNV2)))

main()


########################################OUTPUT#######################################
# -------------NA12891.QC_RAW_OnBait.vcf stats-------------
# Number of SNVs: 87944
# Number of Indels: 14878
# Mean Depth of SNVs: 61.43909760756845
# Chromosome 1: 9037
# Chromosome 2: 6030
# Chromosome 3: 4784
# Chromosome 4: 3878
# Chromosome 5: 3828
# Chromosome 6: 5024
# Chromosome 7: 4271
# Chromosome 8: 3409
# Chromosome 9: 3549
# Chromosome 10: 3551
# Chromosome 11: 5039
# Chromosome 12: 4630
# Chromosome 13: 1716
# Chromosome 14: 2861
# Chromosome 15: 3024
# Chromosome 16: 3935
# Chromosome 17: 4884
# Chromosome 18: 1596
# Chromosome 19: 6061
# Chromosome 20: 2192
# Chromosome 21: 1287
# Chromosome 22: 2174
# Chromosome X: 1169
# Chromosome Y: 15
# -------------NA12878.QC_RAW_OnBait.vcf stats-------------
# Number of SNVs: 88057
# Number of Indels: 14585
# Mean Depth of SNVs: 59.266702249679184
# Chromosome 1: 9112
# Chromosome 2: 5816
# Chromosome 3: 4651
# Chromosome 4: 3783
# Chromosome 5: 3998
# Chromosome 6: 4885
# Chromosome 7: 4128
# Chromosome 8: 3275
# Chromosome 9: 3418
# Chromosome 10: 3608
# Chromosome 11: 5181
# Chromosome 12: 4549
# Chromosome 13: 1666
# Chromosome 14: 3001
# Chromosome 15: 3158
# Chromosome 16: 3596
# Chromosome 17: 5318
# Chromosome 18: 1680
# Chromosome 19: 6228
# Chromosome 20: 2242
# Chromosome 21: 1343
# Chromosome 22: 2228
# Chromosome X: 1182
# Chromosome Y: 11
# Concordance: 45.862492122980996