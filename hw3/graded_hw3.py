# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: rlouie
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
from load import load_seq
import random

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    dnalength = len(dna)
    growing_amino = ''

    if dnalength<3:
        print "ERROR: Too few DNA nucleotides"
    elif dnalength%3 != 0:
        print "Warning: DNA sequence must be a mulltiple of 3"
    else:
        while len(dna) > 0:
            for amino in codons:
                for codon in amino:
                    if codon == dna[:3]:
                        growing_amino += aa[codons.index(amino)]
                        dna = dna[3:]

    return growing_amino

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
        
    print coding_strand_to_AA("ATGCGA") == 'MR'
    print coding_strand_to_AA("ATGCCCGCTTT") =='MPA'
    print bool(coding_strand_to_AA("AT")) == False
    print bool(coding_strand_to_AA("ATGC")) == False

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    
    mapping = {
    'A': 'T',
    'T': 'A',
    'G': 'C',
    'C': 'G'
    } 

    return ''.join([mapping[dna[-i]] for i in range(1, len(dna) + 1)])

def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
        
    return get_reverse_complement('ATGC') == 'GCAT'

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    
    stop = codons[aa.index('|')]
    # print "stopcodons:", stop
    frame = dna[:3]
    newdna = ''

    while frame != stop[0] and frame != stop[1] and frame != stop[2] and frame:
        # print("current frame:", frame)
        newdna += frame
        # print("current dna", newdna)
        dna = dna[3:]
        frame = dna[:3]

    return newdna

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """   
    print "rest_of_ORF('ATGTGAA') == 'ATG':"
    print rest_of_ORF("ATGTGAA") == 'ATG'
    print "rest_of_ORF('ATGATGA') == 'ATGATGA'"
    print rest_of_ORF('ATGATGA') == 'ATGATGA'
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    all_ORF_oneframe = []
    while dna:
        while dna and dna[:3] != 'ATG': # adjust frame til we find a start sequence 
            dna = dna[3:]
        orf = rest_of_ORF(dna)  # find a orf
        all_ORF_oneframe.append(orf)
        dna = dna[len(orf):]     # reduce
        
    return all_ORF_oneframe

def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """

    print "Input: 'GTCATGCATGAATGTAGATAGATGTGCCC' "
    print "Expected Output: ['ATGCATGAATGTAGA', 'ATGTGCCC']"
    print "Output: ", find_all_ORFs_oneframe('GTCATGCATGAATGTAGATAGATGTGCCC')
    
def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    all_ORFs = []
    for i in range(3):
        all_ORFs += find_all_ORFs_oneframe(dna[i:])
    
    return [orf for orf in all_ORFs if orf] # removes empty string

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
        
    print "Input: ATGCATGAATGTAG"
    print "Expected Output: ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']"  
    print "Output: ", find_all_ORFs("ATGCATGAATGTAG")
         
def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
     
    return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    print "Input: ATGCGAATGTAGCATCAAA"
    print "Expected Output: ['ATGCGAATG', 'ATGCTACATTCGCAT']"
    print find_all_ORFs_both_strands('ATGCGAATGTAGCATCAAA')

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""

    ORFs = find_all_ORFs_both_strands(dna)
    return max(ORFs)

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """

    print "Input: ATGCGAATGTAGCATCAAA"
    print "Expected Output: 'ATGCTACATTCGCAT'"
    print "Output: ", longest_ORF('ATGCGAATGTAGCATCAAA')

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """

    # shuffle
    longestORF = ''
    for i in range(num_trials):
        dnalist = list(dna)
        random.shuffle(dnalist)
        ORF = longest_ORF(collapse(dnalist))
        if len(ORF) > len(longestORF):
            longestORF = ORF
    return longestORF

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    allORFs = find_all_ORFs(dna)
    allORFsCopy = list(allORFs)
    for ORF in allORFsCopy:
        if not len(ORF) > threshold:
            allORFs.remove(ORF)
    
    return [coding_strand_to_AA(ORF) for ORF in allORFs]
            
if __name__ == "__main__":
    
    dna = load_seq("./data/X73525.fa")
    # longestORFnoncoding = longest_ORF_noncoding(dna, 1500)
    # print "longest_ORF_noncoding(dna, 1500): \n", longestORFnoncoding
    # print "len(longestORFnoncoding): ", len(longestORFnoncoding)
    potential_aa = gene_finder(dna, 400)
    print "potential_aa: ", potential_aa
    f = open('salmonella_aa.txt', 'w')
    for aa in potential_aa:
        f.write(aa+'\n')
    f.close()