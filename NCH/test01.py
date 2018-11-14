#!/usr/bin/python3
import pandas as pd


# assume each chromosome has 1M positions
NUM_POSITIONS = 1000000.0
# files to be analyzed
FILES = ["sample1_depths.txt", "sample2_depths.txt", "sample3_depths.txt"]


# get # of unique elements of sample2
def problem1(pos):
    unique_sample2 = set(pos[1]) - set(pos[0] + pos[2])
    return len(unique_sample2)


# get # of common elements across samples
def problem2(pos):
    common_sample = set(pos[0]) & set(pos[1]) & set(pos[2])
    return len(common_sample)


# get avg depth of each chromosome
def problem3(dataframes):
    # concatenate all samples
    all_df = pd.concat(dataframes)

    # get group by chr and avg
    avg1 = all_df[all_df["Chromosome"] == "chr1"].Depth.sum() / NUM_POSITIONS
    avg2 = all_df[all_df["Chromosome"] == "chr2"].Depth.sum() / NUM_POSITIONS
    avg3 = all_df[all_df["Chromosome"] == "chr3"].Depth.sum() / NUM_POSITIONS

    return (avg1, avg2, avg3)


# get position with largest avg depth
def problem4(dataframes):
    #set chr and pos as indices so that we can merge commmon values
    df1 = dataframes[0].set_index(['Chromosome', 'Position'])
    df2 = dataframes[1].set_index(['Chromosome', 'Position'])
    df3 = dataframes[2].set_index(['Chromosome', 'Position'])

    # merge indices, adding together common values. 0 if none found
    all_df = df1.add(df2, fill_value=0).add(df3, fill_value=0)

    # no need to divide because position with largest total = position with largest average
    return all_df.loc[all_df["Depth"].idxmax()].name



def main():
    # import inputs as pandas dataframes
    dataframes = []
    for file in FILES:
        dataframes.append(pd.read_csv(file, sep="\t"))

    #isolate dataframe columns (chromosome, position) into list of tuples
    pos = []
    for df in dataframes:
        pos.append(list(zip(df.Chromosome, df.Position)))


    print("Sample 2 has {} positions unique to it.".format(problem1(pos)))
    print("The samples have {} positions in common.".format(problem2(pos)))
    print("Chromosome 1 avg depth: {}\n" \
            "Chromosome 2 avg depth: {}\n" \
            "Chromosome 3 avg depth: {}".format(*problem3(dataframes)))
    print("Chromosome {} at position {} has the largest avg depth.".format(*problem4(dataframes)))


main()