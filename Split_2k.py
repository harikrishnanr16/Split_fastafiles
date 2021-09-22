import pandas as pd
import os
from glob import glob

from Bio import SeqIO

os.makedirs("Sep_files", exist_ok=True)


def joinstuff(x):
    x["Seq"] = "".join(x["Seq"])
    return x["Seq"]


for filename in glob("*.fasta"):
    # print(k)
    fasta_sequences = SeqIO.parse(open(filename), 'fasta')
    os.makedirs("Sep_files/"+filename+"/", exist_ok=True)

    l = {}

    for file in fasta_sequences:
        l[file.id] = list(file.seq)
        # print(file.id,file.seq)

    df = pd.DataFrame(l.items())
    df.columns = ["Id", "Seq"]
    print(df)
    df["joined"] = df.apply(joinstuff, axis=1)
    df = df[["Id", "joined"]]

    print(df)

    rows = 2000
    df_list = []

    while len(df) > rows:
        df_list.append(df[:rows])
        df = df[rows:]
    else:
        df_list.append(df)

    for _, frame in enumerate(df_list):

        s_dict = {}

        for i, rows in frame.iterrows():

            s_dict[frame["Id"][i]] = frame["joined"][i]

        output = open("Sep_files/"+filename+"/"+filename+str(_)+".txt", "w")
        for i in s_dict:
            print(i)
            output.write(">" + i + "\n" + s_dict[i] + "\n")
        output.close()
