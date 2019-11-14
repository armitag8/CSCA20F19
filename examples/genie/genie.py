import doctest

FILENAME = "Homo_sapiens.GRCh38.cds.all.fa"

def sample(filename):
    '''(str) -> NoneType
    
    Read and print the first two lines of a given file
    
    '''
    file = open(filename, "r")
    header = print(file.readline().strip()) # header
    print(file.readline()) # associated sequence, could span multiple lines
    #for i in range(20):
        #print(file.readline())
    file.close()
    
def gene_symbols(filename):
    '''(str) -> NoneType
    
    Prints a list of all the genes, by their gene_symbol in this file
    
    '''
    file = open(filename, "r")
    gene_symbol_list = []
    for line in file:
        if ">" in line: 
            header = line.split(" ")
            gene_symbol_header = header[6] # ex: "gene_symbol:BRCA1"
            gene_symbol = gene_symbol_header.split(":")[1] # ex: "BRCA1"
            # check if they symbol is already in the list
            if gene_symbol_list.count(gene_symbol) == 0:
                gene_symbol_list.append(gene_symbol)
    file.close()
    print(gene_symbol_list)

def get_sequence_by_chromosome(chromosome, filename):
    '''(str) -> str
    
    Print the sequence associated with a given chromosome location
    
    >>> get_sequence_by_chromosome("GRCh38:7:142786213:142786224:1",FILENAME)
    'GGGACAGGGGGC'
    
    >>> get_sequence_by_chromosome("GRCh38:7:142482548:142483019:1",FILENAME)
    'ATGGGCCCTGGGCTCCTCTGCTGGGTGCTGCTTTGTCTCCTGGGAGCAGGCCCAGTGGACGCTGGAGTCACCCA\
AAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACTCTGAGATGCTCTCCTATCTCTGGGCACAAGAGTGTG\
TCCTGGTACCAACAGGTCCTGGGTCAGGGGCCCCAGTTTATCTTTCAGTATTATGAGAAAGAAGAGAGAGGAAGAGGAA\
ACTTCCCTGATCGATTCTCAGCTCGCCAGTTCCCTAACTATAGCTCTGAGCTGAATGTGAACGCCTTGTTGCTGGGGGA\
CTCGGCCCTGTATCTCTGTGCCAGCAGCTTGG'
    
    '''
    file = open(filename, "r")
    sequence = ""
    for line in file:
        # header lines are identified by ">" at the start
        if ">" in line: 
            #make sure we're looking specifically at the chromosome location
            if ("chromosome:"+chromosome) in line: 
                line = file.readline().strip()
                # keep reading the sequence until you reach a header
                while not ">" in line: 
                    sequence += line
                    line = file.readline().strip()    
                break # because we found sequence
    if sequence == "":
        sequence = "the sequence was not found"
    return sequence

def get_presequence(dna):
    '''(str) -> str
    Convert a given DNA sequence to a list of possible mRNA sequence by 
    substituting all T (thymidine) values with U (uracil)
    
    >>> get_presequence('TGACTATGGTGCTAACTAC')
    'UGACUAUGGUGCUAACUAC'
    >>> get_presequence('GGGACAGGGGGC')
    'GGGACAGGGGGC'
    
    '''
    precursor = ''
    for nucleotide in dna: 
        if nucleotide == 'T':
            precursor += 'U'
        else:
            precursor += nucleotide
    return precursor

def codon_to_amino(codon):
    '''(str) -> str
    Given a codon (3 nucleotides), returns the programmed amino acid
    '''
    

################################################################################
################################################################################
# There's so much more you can do!
# find the location(s) for a given gene
# use the FASTA encoding guide to translate the sequence to a DNA sequence
# translate the DNA sequence into an amino acid sequence
#     3 nucleotides is a codon --> 1 amino acid
# compare the sequence of a human gene to the sequence for the same 
#    gene in a different vertebrate (from a different file in Ensembl)


# prints the first line (shows the format of the comments) and a sequence
sample(FILENAME)

